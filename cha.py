import streamlit as st
import openai
import streamlit as st
from dotenv import load_dotenv
import pickle
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain.callbacks import get_openai_callback
import os
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.prompts import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
    MessagesPlaceholder
)
from streamlit_chat import message  # Importez la fonction message
import toml
import docx2txt
from langchain.memory.chat_message_histories import StreamlitChatMessageHistory
from langchain.callbacks.base import BaseCallbackHandler
import docx2txt
from dotenv import load_dotenv
if 'previous_question' not in st.session_state:
    st.session_state.previous_question = []

# Chargement de l'API Key depuis les variables d'environnement
load_dotenv(st.secrets["OPENAI_API_KEY"])

# Configuration de l'historique de la conversation
if 'previous_questions' not in st.session_state:
    st.session_state.previous_questions = []

st.markdown(
    """
    <style>

        .user-message {
            text-align: left;
            background-color: #E8F0FF;
            padding: 8px;
            border-radius: 15px 15px 15px 0;
            margin: 4px 0;
            margin-left: 10px;
            margin-right: -40px;
            color:black;
        }

        .assistant-message {
            text-align: left;
            background-color: #F0F0F0;
            padding: 8px;
            border-radius: 15px 15px 15px 0;
            margin: 4px 0;
            margin-left: -10px;
            margin-right: 10px;
            color:black;
        }

        .message-container {
            display: flex;
            align-items: center;
        }

        .message-avatar {
            font-size: 25px;
            margin-right: 20px;
            flex-shrink: 0; /* Empêcher l'avatar de rétrécir */
            display: inline-block;
            vertical-align: middle;
        }

        .message-content {
            flex-grow: 1; /* Permettre au message de prendre tout l'espace disponible */
            display: inline-block; /* Ajout de cette propriété */
}
        .message-container.user {
            justify-content: flex-end; /* Aligner à gauche pour l'utilisateur */
        }

        .message-container.assistant {
            justify-content: flex-start; /* Aligner à droite pour l'assistant */
        }
        input[type="text"] {
            background-color: #E0E0E0;
        }

        /* Style for placeholder text with bold font */
        input::placeholder {
            color: #555555; /* Gris foncé */
            font-weight: bold; /* Mettre en gras */
        }

        /* Ajouter de l'espace en blanc sous le champ de saisie */
        .input-space {
            height: 20px;
            background-color: white;
        }
    
    </style>
    """,
    unsafe_allow_html=True
)
# Sidebar contents
textcontainer = st.container()
with textcontainer:
    logo_path = "medi.png"
    logoo_path = "NOTEPRESENTATION.png"
    st.sidebar.image(logo_path,width=150)
   
    
st.sidebar.subheader("Suggestions:")
questions = [
        "Donnez-moi un résumé du rapport ",
        "Quels sont les projets d'investissement majeurs prévus pour 2025, et comment ces investissements contribueront-ils à la croissance économique du pays ?",        
        "Comment la répartition sectorielle des établissements publics a-t-elle évolué entre 2021 et 2023 ?",        
        "Quelle est la raison derrière l'amélioration des résultats nets bénéficiaires des établissements publics en 2023 par rapport aux années précédentes ?"
    ]    
load_dotenv(st.secrets["OPENAI_API_KEY"])
# Initialisation de l'historique de la conversation dans `st.session_state`
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = StreamlitChatMessageHistory()
def main():
    conversation_history = StreamlitChatMessageHistory()  # Créez l'instance pour l'historique

    st.header("Projet de Loi de Finances pour l’année budgétaire 2025: Rapport établissements et entreprises publics 💬")
    
    # Load the document
    docx = 'Rapport etablissement entreprise (3).docx'
    
    if docx is not None:
        # Lire le texte du document
        text = docx2txt.process(docx)

        # Afficher toujours la barre de saisie
        st.markdown('<div class="input-space"></div>', unsafe_allow_html=True)
        selected_questions = st.sidebar.radio("****Choisir :****", questions)
        # Afficher toujours la barre de saisie
        query_input = st.text_input("", key="text_input_query", placeholder="Posez votre question ici...", help="Posez votre question ici...")
        st.markdown('<div class="input-space"></div>', unsafe_allow_html=True)

        if query_input and query_input not in st.session_state.previous_question:
            query = query_input
            st.session_state.previous_question.append(query_input)
        elif selected_questions:
            query = selected_questions
        else:
            query = ""

        if query :
            st.session_state.conversation_history.add_user_message(query)  # Ajouter à l'historique
            if "Donnez-moi un résumé du rapport" in query:
                summary="""Le rapport sur les établissements et entreprises publics (EEP) pour le Projet de Loi de Finances 2025 présente un bilan détaillé des performances financières et opérationnelles des EEP au Maroc. Il couvre des indicateurs clés tels que le chiffre d'affaires, les charges d'exploitation, les investissements, et la dette de financement. Le secteur des EEP est dominé par des secteurs tels que l’énergie, les mines, l’eau et l’environnement, qui représentent une part importante du chiffre d'affaires et des investissements. En 2023, les EEP ont généré un chiffre d'affaires total de 332 milliards de dirhams, et leurs investissements ont augmenté de 6 % par rapport à l'année précédente. Le rapport met également en lumière les défis financiers, notamment des déficits dans certains secteurs et une diminution de la capacité d'autofinancement, nécessitant des transferts et subventions de l'État pour maintenir la viabilité des opérations."""
                st.session_state.conversation_history.add_ai_message(summary) 

        
            else:
                messages = [
                {
                    "role": "user",
                    "content": (
                        f"{query}. En tenant compte du texte suivant essayer de ne pas dire le texte ne contient pas les informations si ne trouve pas à partir de texte répondre d'aprés votre connaissance stp et ne dire pas stp le texte incomplet ou incompréhensible essayer de formulé une bon réponse sans critiquer le texte par exemple ne pas dire texte fragmenter ou quelque chose comme ça répondre directement stp parceque je vais l'afficher o lecteur: {text} "
                    )
                }
            ]

            # Appeler l'API OpenAI pour obtenir le résumé
                response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=messages
            )

            # Récupérer le contenu de la réponse

                summary = response['choices'][0]['message']['content']
            
                st.session_state.conversation_history.add_ai_message(summary)  # Ajouter à l'historique
            
            # Afficher la question et le résumé de l'assistant
            #conversation_history.add_user_message(query)
            #conversation_history.add_ai_message(summary)

            # Format et afficher les messages comme précédemment
            formatted_messages = []
            previous_role = None 
            if st.session_state.conversation_history.messages: # Variable pour stocker le rôle du message précédent
                    for msg in conversation_history.messages:
                        role = "user" if msg.type == "human" else "assistant"
                        avatar = "🧑" if role == "user" else "🤖"
                        css_class = "user-message" if role == "user" else "assistant-message"

                        if role == "user" and previous_role == "assistant":
                            message_div = f'<div class="{css_class}" style="margin-top: 25px;">{msg.content}</div>'
                        else:
                            message_div = f'<div class="{css_class}">{msg.content}</div>'

                        avatar_div = f'<div class="avatar">{avatar}</div>'
                
                        if role == "user":
                            formatted_message = f'<div class="message-container user"><div class="message-avatar">{avatar_div}</div><div class="message-content">{message_div}</div></div>'
                        else:
                            formatted_message = f'<div class="message-container assistant"><div class="message-content">{message_div}</div><div class="message-avatar">{avatar_div}</div></div>'
                
                        formatted_messages.append(formatted_message)
                        previous_role = role  # Mettre à jour le rôle du message précédent

                    messages_html = "\n".join(formatted_messages)
                    st.markdown(messages_html, unsafe_allow_html=True)

if __name__ == '__main__':
    main()
