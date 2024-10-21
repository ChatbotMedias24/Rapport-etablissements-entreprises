import streamlit as st
from dotenv import load_dotenv
import pickle
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
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
if 'previous_question' not in st.session_state:
    st.session_state.previous_question = []
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
        "Comment la répartition sectorielle des établissements publics a-t-elle évolué entre 2021 et 2023 ?"
        "Quelle est la raison derrière l'amélioration des résultats nets bénéficiaires des établissements publics en 2023 par rapport aux années précédentes ?"

    ]    
 
load_dotenv(st.secrets["OPENAI_API_KEY"])
conversation_history = StreamlitChatMessageHistory()

def main():
    conversation_history = StreamlitChatMessageHistory()  # Créez l'instance pour l'historique
    st.header("Projet de Loi de Finances pour l’année budgétaire 2025: Rapport sur les établissements et entreprises publics 💬")
    
    # Load the document
    docx = 'Rapport etablissement entreprise (3).docx'
    
    if docx is not None:
        text = docx2txt.process(docx)
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
        chunks = text_splitter.split_text(text=text)

        embeddings = OpenAIEmbeddings()
        VectorStore = FAISS.from_texts(chunks, embedding=embeddings)
        with open("aaa.pkl", "wb") as f:
            pickle.dump(VectorStore, f)

        st.markdown('<p style="margin-bottom: 0;"><h7><b>Posez vos questions ci-dessous:</b></h7></p>', unsafe_allow_html=True)

        query_input = st.text_input("")
        selected_questions = st.sidebar.radio("****Choisir :****", questions)
        
        # Initialize query
        query = ""
        
        if query_input and query_input not in st.session_state.previous_question:
            query = query_input
            st.session_state.previous_question.append(query_input)
        elif selected_questions:
            query = selected_questions
        
        if query:
            docs = VectorStore.similarity_search(query=query, k=3)

            llm = OpenAI(model="gpt-3.5-turbo-instruct")
            chain = load_qa_chain(llm=llm, chain_type="stuff")
            with get_openai_callback() as cb:
                response = chain.run(input_documents=docs, question=query)
                
                if "Donnez-moi un résumé du rapport" in query:
                    response = "Le rapport sur les établissements et entreprises publics (EEP) pour le Projet de Loi de Finances 2025 présente un bilan détaillé des performances financières et opérationnelles des EEP au Maroc. Il couvre des indicateurs clés tels que le chiffre d'affaires, les charges d'exploitation, les investissements, et la dette de financement. Le secteur des EEP est dominé par des secteurs tels que l’énergie, les mines, l’eau et l’environnement, qui représentent une part importante du chiffre d'affaires et des investissements. En 2023, les EEP ont généré un chiffre d'affaires total de 332 milliards de dirhams, et leurs investissements ont augmenté de 6 % par rapport à l'année précédente. Le rapport met également en lumière les défis financiers, notamment des déficits dans certains secteurs et une diminution de la capacité d'autofinancement, nécessitant des transferts et subventions de l'État pour maintenir la viabilité des opérations."
                conversation_history.add_user_message(query)
                conversation_history.add_ai_message(response)

            formatted_messages = []
            for msg in conversation_history.messages:
                role = "user" if msg.type == "human" else "assistant"
                avatar = "🧑" if role == "user" else "🤖"
                css_class = "user-message" if role == "user" else "assistant-message"
                
                message_div = f'<div class="{css_class}">{msg.content}</div>'
                avatar_div = f'<div class="avatar">{avatar}</div>'
                
                if role == "user":
                    formatted_message = f'<div class="message-container user"><div class="message-avatar">{avatar_div}</div><div class="message-content">{message_div}</div></div>'
                else:
                    formatted_message = f'<div class="message-container assistant"><div class="message-content">{message_div}</div><div class="message-avatar">{avatar_div}</div></div>'
                
                formatted_messages.append(formatted_message)

            messages_html = "\n".join(formatted_messages)
            st.markdown(messages_html, unsafe_allow_html=True)

if __name__ == '__main__':
    main()
