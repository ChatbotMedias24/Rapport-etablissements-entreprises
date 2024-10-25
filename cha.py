import streamlit as st
import openai
import streamlit as st
from dotenv import load_dotenv
import pickle
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.llms import OpenAI
from langchain.callbacks import get_openai_callback
import os
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
    "Quelle est la raison derrière l'amélioration des résultats nets bénéficiaires des établissements publics en 2023 par rapport aux années précédentes ?"
]
# Initialisation de l'historique de la conversation dans `st.session_state`
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = StreamlitChatMessageHistory()
def main():
    text=r"""
    
RESUME EXECUTIF

Les Etablissements et Entreprises Publics (EEP) ont toujours été au cœur des priorités des
pouvoirs publics eu égard à leur contribution déterminante dans la conduite et la mise en
œuvre des politiques de développement économique et social et à l’effort de l'investissement
public. En effet, ces entités interviennent dans tous les secteurs stratégiques, notamment
l'infrastructure, l'eau, l’énergie, l'agriculture, la pêche maritime, l’'éducation, l'enseignement,
la formation professionnelle, la recherche, la santé, la protection sociale, le tourisme, le
transport et la logistique outre la production d'une large gamme de services aux entreprises
et aux citoyens.

De même, les EEP interviennent massivement dans les programmes de développement des
territoires et de réduction des inégalités sociales et spatiales et jouent un rôle majeur dans la
mise en œuvre des chantiers stratégiques contribuant ainsi à la diversification des sources de
croissance, au renforcement de la résilience et de la compéétitivité de l’économie dans l'objectif
de consolidation du positionnement international du pays.

Les EEP assurent également un rôle majeur dans la dynamisation de la transformation
économique, numérique et sociale du pays et participent, activement, à la réalisation des
grands chantiers lancés par Sa Majesté le Roi Mohammed VI, que Dieu L’assiste, dont
notamment la généralisation de la protection sociale, la promotion de l'initiative privée et
l'accélération des programmes stratégiques dans les secteurs de l'eau, de l'énergie, de
l'agriculture et l'extension d'une infrastructure de qualité, outre leur contribution au nouveau
chantier de préparation de la Coupe du monde 2030.

Compte tenu des enjeux stratégiques liés à l’efficience économique et sociale de l'action des
EEP et dans l’objectif d’améliorer leurs performances, le chantier de la réforme profonde de
ce secteur a été érigé au rang de priorité nationale suite aux Hautes Orientations Royales,
notamment celles contenues dans le Discours Royal du 29 juillet 2020 appelant à réaliser avec
diligence une réforme profonde du secteur public pour corriger les dysfonctionnements
structurels des EEP, garantir une complémentarité et une cohérence optimales entre leurs
missions respectives et, /n fine, rehausser leur efficience économique et sociale.

Les contours de ce chantier de réforme ont été tracés à travers deux textes de référence
publiés en juillet 2021, à savoir :

- La loi-cadre n° 50-21 relative à la réforme des EEP ;

-  La loi n° 82-20 portant création de l'Agence Nationale de Gestion Stratégique des

Participations de l'Etat et de suivi des performances des établissements et entreprises
publics (ANGSPE).

Ce chantier de réforme tient également compte de la nécessité de s'aligner sur les dispositions
du projet d'amendement de la Loi Organique relative à la Loi de Finances qui prévoit
l'élargissement de son champ d’application aux établissements publics non marchands.

Les objectifs majeurs de cette réforme consistent en la rationalisation de la taille du
portefeuille public et la consolidation de ses performances par la réalisation d’un programme
d'opérations de restructuration visant à remédier aux chevauchements des missions ou des
activités imparties aux EEP, à dissoudre et à liquider les entités qui souffrent d’un déficit
financier chronique et à œuvrer à la valorisation des synergies et des complémentarités, à la
création de la valeur, à l'amélioration de la qualité de la gestion et de la gouvernance, à
l'ancrage des principes de transparence et de reddition des comptes. L'objectif ultime est de
garantir un service de qualité au moindre coût pour la collectivité en veillant à la réduction de
la pression sur le budget de l'Etat.

Ce chantier de réforme a connu une avancée importante suite à l'approbation par le Conseil
des Ministres tenu le 1° juin 2024 sous la présidence de Sa Majesté le Roi Mohammed VI, que
Dieu L’assiste, des Orientations Stratégiques de la Politique Actionnariale de l'Etat (PAE).

Ainsi, et suite à l'avis favorable émis, en date du 19/09/2024, par l'Instance de Concertation
sur le projet de la PAE, ce projet sera soumis à l’approbation du Conseil du Gouvernement, ce
qui permettra de lancer son déploiement. Cette politique marquera une étape importante dans
la restructuration et la modernisation du portefeuille de l’Etat, en fournissant un document de
référence unique pour guider l'action de l’Etat en tant qu'actionnaire.

En effet, l'adoption de la PAE permettra à l'ANGSPE d'engager les diligences, les études et les
évaluations en concertation avec les partenaires concernés en vue d'accélérer la mise en place
et l’exécution du programme de réforme des EEP relevant de son périmètre, qui portent des
enjeux économiques et sociaux importants.

S'agissant des EEP du périmètre piloté par le Ministère de l'Economie et des Finances, le plan
d'action engagé a permis d'identifier un programme d'opérations de restructuration
concernant une soixantaine d'EEP, dont une grande partie est en cours de mise en œuvre.
Parallèlement, les évaluations et les concertations se poursuivent dans d’autres secteurs en
vue de l'identification de nouvelles opérations de restructuration afin d'élaborer un
programme de réforme aligné sur les objectifs de rationalisation du portefeuille public et de
réduction de sa taille.

La Note d’Orientation du Chef du Gouvernement n° 10/2024 du O6 août 2024 relative à la
préparation du Projet de Loi de Finances pour l’année budgétaire 2025 énonce les priorités
majeures pour les années à venir qui s’articulent autour de la souveraineté hydrique,
alimentaire et énergétique et du renforcement de la soutenabilité des finances publiques avec
commoe objoctif de dégager les ospaces budgétaires nécessaires pour poursuivre la réalisation
des différents chantiers de développement, tout en préservant la dynamique de
l'investissement public, levier essentiel pour consolider les piliers de l'Etat social. Ainsi, les
orientations générales du Projet de Loi de Finances pour l'année budgétaire 2025 s'articulent
autour des priorités suivantes :

-  La poursuite du renforcement des piliers de l’Etat social ;

-  La consolidation de la dynamique d'investissement et de la création de l’emploi ;
-  La poursuite de la mise en œuvre des réformes structurelles ;

-  La préservation de la soutenabilité des finances publiques.

Dans ce cadre, la Circulaire n° 55/2024 du 02 octobre 2024 du Ministère de l'Economie et
des Finances relative aux prévisions budgétaires des EEP au titre de l’exercice 2025 invite
ces entités à œuvrer pour renforcer l’efficience de leurs actions et leurs performances et à
recentrer leurs plans d’action autour des priorités nationales et des chantiers stratégiques,
notamment :

- L'accélération de la réalisation du programme de généralisation de la couverture sociale ;

- L'actualisation de la stratégie de l'Eau et l’accélération de la réalisation des projets prévus
dans le cadre du Programme National pour l'Approvisionnement en Eau Potable et
l'Irrigation 2020-2027 (PNAEPI), conformément aux Hautes Instructions Royales ;

- L'accélération du chantier des Energies Renouvelables (EnR) et de la mise en œuvre de la
feuille de route relative à l'Offre Maroc pour le développement de la filière de l'hydrogène
vert ;

- La contribution à l’amélioration du climat des affaires et à l'encouragement de l'initiative
privée ;

- La réalisation, dans les délais prescrits et aux normes requises, du programme des travaux
de préparation de la Coupe du monde 2030.
En 2023, le chiffre d'affaires (CA) du secteur des EEP s'est établi à 332.070 MDH, marquant
par rapport à 2022, une quasi-stagnation qui résulte, essentiellement, de la baisse du CA du
Groupe OCP, qui est passé de 114.574 MDH en 2022 à 91.277 MDH en 2023.

Les prévisions pour l'exercice 2024 tablent sur un CA de 345.912 MDH pour l'ensemble du
secteur, en hausse de 4% par rapport à 2023.

S'agissant des Charges d'Exploitation Hors Dotations (CEHD), elles se sont établies à
279.128 MDH en 2023, en réduction de 7% par rapport à 2022 sous l'effet, essentiellement, de
la baisse enregistrée au niveau des CEHD du Groupe OCP.

Quant aux résultats nets du secteur des EEP, ils ont connu une amélioration importante, en
passant de 1.044 MDH enregistré en 2022 à 9.278 MDH en 2023. Les prévisions de clôture de
2024 confirment le retour de la tendance haussière des résultats du secteur des EEP. Ainsi, le
résultat net du secteur s’établirait à 14.071 MDH.

En 2023, les EEP ont investi un montant total de 81.285 MDH, en amélioration de 6% par
rapport à 2022 (+4.533 MDH). Une grande partie de cet investissement (74%) provient des
EEP relevant du périmètre de l'ANGSPE.

Pour l'année 2024, les prévisions de clôture indiquent un volume global des investissements
s'élevant à 115.215 MDH en hausse de 42% par rapport à 2023.

Pour les prévisions des exercices 2025, 2026 et 2027, les investissements des EEP seraient,
respectivement, de 137.700 MDH, de 141.614 MDH et de 122.298 MDH.

Les produits versés par les EEP à l’Etat (hors produits de cession d’actifs et de privatisation)
ont évolué de 13.146 MDH en 2022 à 13.987 MDH en 2023 (+6%), en soulignant qu’un montant
de 1.607 MDH a été réalisé en 2023 au titre des produits de cession d’actifs et de privatisation.

Pour l'année 2024, les prévisions de clôture sont estimées à 24.465 MDH (y compris un
montant de 5.980 MDH au titre des produits de cession d'actifs et de privatisation), soit
presque 100% des prévisions initiales (24.480 MDH).

À fin août 2024, les produits des EEP versés au Budget Général de l'Etat (BGE) se sont élevés
à 10.017 MDH, dont 8.317 MDH au titre des produits de dividendes et contributions diverses
et 1.700 MDH pour les opérations de cession d’actifs et de privatisation.

Les prévisions pour l’année 2025 tablent sur des recettes de l'ordre de 28.546 MDH dont
19.546 MDH pour les produits des dividendes et contributions diverses et 9.000 MDH pour
les produits de cossion d'actifs ct de privatisation.

Pour les subventions accordées par l'Etat aux EEP, le total de ces transferts a atteint, en
2023, un montant de 65.687 MDH dont 52% pour le fonctionnement, 33% pour
l'investissement et 15% au titre des dotations en capital. Les prévisions pour 2024, actualisées
à fin août, s’élèvent à 68.207 MDH et sont réalisées à hauteur de 53%.
Les EEP poursuivent la mise en œuvre de leurs plans d'action axés essentiellement sur les
chantiers lancés par Sa Majesté le Roi Mohammed VI, que Dieu L'assiste. Ces plans
s'articulent autour des objectifs de consolidation des bases de l'Etat social et de la
compétitivité de l'économie nationale, de la création de la valeur et de l'emploi, de la
promotion de l'initiative privée, du renforcement de la connectivité au moyen d'une
infrastructure aux meilleurs standards, de l’accélération des programmes axés sur les priorités
nationales dont notamment celles liées à la souveraineté du pays dans les secteurs de l'eau,
de l’énergie et de la santé.

Concernant le chantier Royal de la généralisation de la protection sociale, 31,5 millions de
personnes sont couvertes par l'AMO représentant 84% de la population marocaine, dont
24,2 millions de personnes assurées par la CNSS et 7,3 millions par les autres acteurs (CNOPS,
Mutuelle des Forces Armées Royales, etc.)

S'agissant du secteur de l’eau, et en vue de faire face aux effets multiples du stress hydrique
prolongé, Sa Majesté lc Roi Mohammed VI, que Dicu L'assiste, a appolé, lors du Discours
Royal à l'occasion de la Fête du Trône du 29 juillet 2024, à la mise à jour continue des leviers
de la politique nationale de l’eau et à la définition d’un objectif stratégique, quelles que soient
les circonstances : garantir l’eau potable à tous les citoyens et couvrir 80% au moins des
besoins d'irrigation sur tout le territoire national.

Ainsi, Sa Majesté a donné Ses Hautes Instructions en vue de la mise en œuvre optimale des
différentes composantes du PNAEPI 2020-2027, la protection du domaine public hydraulique,
l'opérationnalisation de la police de l'eau et la lutte contre le phénomène d'exploitation abusive
et de pompage anarchique de l'eau.

Dans ce cadrc, les organismes intervenant dans le secteur de l'eau (ABH, ONEE, ORMVA,
opérateurs de la distribution, etc.) sont appelés à collaborer étroitement avec les parties
prenantes en vue de l'actualisation et du déploiement de la stratégie de l'eau, et de mobiliser
les moyens nécessaires pour garantir une contribution efficace à la mise à jour des leviers de

la politique nationale de l'eau, et ce à travers notamment :

- Lacontribution à la réalisation dans les délais prescrits des projets inscrits dans le cadre
du PNAEPI, dont notamment le parachèvement du programme de construction des
barrages, la réalisation des grands projets de transfert d’eau entre bassins hydrauliques
et l’accélération de la réalisation des projets de dessalement de l’eau de mer et
d'épuration des eaux usées réutilisées ;

- Le renforcement de la police de l’eau pour en faire un levier efficace en matière de lutte
contre la surexploitation de la ressource, le pompage anarchique et l'anticipation des
rejets non contrôlés ;

- La contribution efficace à la réalisation des programmes d'économie et de
rationalisation de la consommation de l'eau ;

- La consolidation de la gouvernance du secteur de l'eau par la professionnalisation des
fonctions de planification, de gestion et de protection des ressources en eau.

En ce qui concerne le programme des travaux de préparation de la Coupe du monde 2030,
plusieurs EEP contribuent à la réalisation de ce chantier structurant notamment pour réaliser
et livrer, dans les délais prescrits et aux normes requises, les enceintes sportives et doter les
villes hôtes de cet événement d’infrastructures de transport et de communication répondant
aux normes internationales exigées.

Dans ce cadre, l'ONCF a lancé la réalisation d'un programme de développement ferroviaire
pour un coût estimé à 87 MMDH couvrant plusieurs composantes notamment l’extension de
la LGV de Kénitra vers Marrakech et le développement d’un Réseau Express Régional (RER)
au niveau des agglomérations de Casablanca, de Rabat et de Marrakech.

AUssi, les concertations ont été engagées en vue de mettre en place un contrat-programme à
conclure entre l’Etat et l'ONCF devant asseoir et définir les composantes de ce plan de
développement et de son montage de financement.

De son côté, ADM a engagé les concertations avec les parties prenantes en vue de définir et
d'arrêter le plan de financement du programme d'aménagement autoroutier de 1.000 KM à
réaliser conformément aux Hautes Orientations Royales suite au Message de Sa Majesté
le Roi Mohammed VI, que Dieu L'assiste, adressé, le O8 novembre 2023, aux participants à
la 4°me édition du Forum pour l'investissement en Afrique, annonçant l'extension du réseau
autoroutier à 3.000 km à l'horizon 2030.

L'ONDA a lancé la réalisation de son programme d'investissement évalué à 12,3 MMDH et qui
porte sur les travaux d’extension des capacités des aéroports de Mohammed V, de Rabat-Salé,
de Marrakech, d'Agadir, de Tétouan, de Tanger, de Fès et d’AI Hoceima.

Ce programme permettra également de soutenir la croissance du secteur touristique et [e plan
de développement de la RAM défini dans le cadre du contrat-programme conclu en juillet
2023 et visant notamment l’expansion de sa flotte de 50 à 200 avions et la densification de
son réseau des lignes internationales et domestiques.

De même, l'ANRT a lancé, conformément à la stratégie 2030 du secteur des
télécommunications, la réalisation du projet de couverture de la 5G dans l'objectif d'atteindre
une couverture de 25% de la population en 2026 et 70% à fin 2030 en assurant un niveau de
couverture de 100% pour les villes hôtes de la Coupe du monde 2030.

RAPPORT SUR LES ETABLISSEMENTS ET ENTREPRISES PUBI| s

Quant au secteur de l’énergie, MASEN et l'ONEE ont intensifié la cadence de réalisation du
programme de développement des Energies Renouvelables (EnR) en vue d’accélérer la
stratégie de transition énergétique et de contribuer à la réduction de la dépendance
énergétique de notre pays.

Ainsi, la capacité installée en EnR à fin 2023 est de 4.607 MW, soit plus de 41% du mix
électrique national. De même et compte tenu du programme en cours d'exécution, la part des
EnR dans le mix électrique atteindrait, en 2027, une part de 56% dépassant ainsi l'objectif
stratégique fixé pour 52% à l'horizon 2030.

De même, MASEN a lancé la mise en œuvre du plan d'action relatif à l'Offre Maroc pour le
développement de la filière de l’'hydrogène vert. Dans ce cadre, les investisseurs potentiels ont
déposé leurs offres, ce qui ouvre des perspectives prometteuses pour cette filière devant
contribuer, en profondeur, à l’accélération de la transition énergétique et à la décarbonisation
de la production nationale, outre les avantages en termes de croissance, de création d’emploi
et de renforcement de l’offre à l'export.

En outre, il a été procédé au lancement des études de conception et de structuration des
projets de Terminal du Gaz Naturel (GNL) de Nador West Med (NWM) et du Gazoduc de
connexion de NWM à Mohammedia via le Gazoduc Maghreb-Europe (GME), en soulignant que
l'ONHYM poursuit la réalisation des études et des concertations avec les partenaires concernés
cn vue de la concrétisation du projet stratégique du Gazoduc Nigéria-Maroc, qui a connu une
avancée décisive suite au lancement, à la fin du mois d'août 2024, des travaux de validation
de l'Accord Intergouvernemental (IGA) et de l'Accord Pays Hôte (HGA).

S'agissant du secteur agricole, les EEP de ce secteur poursuivent le déploiement de la
stratégie « Génération Green », par la réalisation de plusieurs projets en matière d’agrégation
agricole, de PPP autour des terres agricoles de l'Etat, d'appui à l'entrepreneuriat des jeunes
dans le secteur agricole. Ces organismes ont contribué également à la mise en œuvre de
plusieurs mesures pour le bon déroulement de la campagne agricole 2023-2024 dont
notamment l’approvisionnement en semences et en engrais, la gestion de l'eau d'irrigation et
l'assurance agricole.

Ainsi et en dépit d'une forte baisse des précipitations, le secteur agricole continue d'assurer
un approvisionnement régulier des marchés, en soulignant que ce secteur a montré une forte
résillence dans la mesure où les exportations, en 2023, des produits de l'agriculture et de
l'agro-alimentaire ont atteint 83.142 MDH contre 81.236 MDH en 2022, plaçant ainsi ce secteur
parmi les principaux secteurs pourvoyeurs de recettes en devises.

Pour ce qui concerne la formation professionnelle, l'offre de formation initiale de l'OFPPT
atteindra une capacité de 414.855 places pédagogiques pour l'année 2024-2025. Cette
amélioration est due à l’ouverture prévue de 20 nouveaux établissements dotés d'une capacité
de 5.000 places pédagogiques.

De même, le chantier Royal relatif à la réalisation des 12 Cités des Métiers et des
Compétences (CMC) connait unc avancée significative suite à la mise en service de six (6)
CMC dans les régions de Souss-Massa, de l’Oriental, de Laâyoune Sakia-E] Hamra, de Rabat-
Salé-Kénitra, de Tanger-Tétouan-AI Hoceima et de Béni Mellal-Khénifra avec une capacité de
21.865 sièges pédagogiques, soit 64% de la capacité cible de 34.000 stagiaires pour les
12 CMC, en soulignant que les six CMC restantes sont en cours de réalisation en vue de leur
ouverture en 2025.

A fin août 2024, les engagements au titre du programme des CMC s’élèvent à 4.900 MDH et
les paiements effectués ont atteint 3.200 MDH (65%).

Le secteur touristique a confirmé, en 2023, sa dynamique exceptionnelle et sa position
comme l’un des plus grands pourvoyeurs de devises pour notre pays avec un volume des
arrivées de 14,52 millions de touristes (+34% par rapport à 2022) et des recettes voyages en
devises de 105 MMDH contre 94 MMDH en 2022 (+12%).

Pour ce qui est des nuitées réalisées dans les Etablissements Hôteliers Touristiques Classés
(EHTC), leur flux a connu une hausse de 35% par rapport à 2022, soit Un taux de récupération
de 101,5% à fin 2023 par rapport au niveau antérieur à la crise sanitaire.

À fin août 2024, environ 11,8 millions de touristes ont franchi les postes frontières,
enregistrant une hausse de 16% par rapport à la même période de l’année précédente.

Les nuitées ont atteint 18,7 millions, en hausse de 7% par rapport à la même période de 2023.
Quant aux recettes touristiques, elles se sont élevées à 76,4 MMDH, en augmentation de 6,7%
par rapport à la même période de 2023.

Ainsi, l'ONMT poursuit le déploiement de son nouveau plan d'action, dénommé « light in
action » en vue d'accompagner la mise en œuvre de la nouvelle feuille de route stratégique du
tourisme 2023-2026 qui ambitionne, à l’horizon 2026, d’attirer 17,5 millions de touristes et de
hisser le Maroc parmi [es 10 destinations les plus appréciées dans le monde.

Pour le secteur des phosphates, les performances financières de l'OCP montrent une stabilité,
témoignant de la résililence du Groupe face aux fluctuations récurrentes du marché
international, Les fondamentaux du Groupe sont demeurés solides, lui permettant de maintenir
une position compétitive sur le marché mondial des engrais, en notant qu'’en 2022, le Groupe
a réalisé un chiffre d'affaires record sous l'effet d’une forte hausse des prix des produits
phosphatés.

Ainsi, le chiffre d'affaires du Groupe s’est établi à 91.277 MDH à fin 2023, enregistrant une
baisse de 20% par rapport à 2022 (114.574 MDH), Quant au résultat net, il a enregistré un recul
de 49% passant de 28.185 MDH en 2022 à 14.369 MDH en 2023.

S'agissant de l’appui à l’entreprise, l'exercice 2023 a été marqué par de solides performances
de la SNGFE, qui a mobilisé 54,14 MMDH de crédits à travers 86.790 opérations en faveur
aussi bien des entreprises que des particuliers, enregistrant une croissance de 14% par rapport
à 2022. Les engagements de la Société ont atteint 35,1 MMDH, contre 31 MMDH l'année
précédente. La SNGFE a principalement orienté son activité vers le soutien au financement
des entreprises notamment la TPME, représentant 93% de ses interventions avec des
engagements de 32,8 MMDH, ayant permis de mobiliser 50,2 MMDH de crédits et de financer
plus de 68.420 opérations en faveur des entreprises.

De son côté, le Fonds Mohammed VI pour l’Investissement (FM6I) intensifie es diligences
et les concertations pour la mise en œuvre de son plan d’action visant l’accélération des
investissements dans les secteurs productifs et prioritaires, en s'appuyant sur une approche
axée sur la mobilisation du financement privé.

Dans ce cadre, le Fonds a sélectionné 15 sociétés de gestion des fonds thématiques avec une
première enveloppe de 4,5 MMDH, mobilisant 13,5 MMDH supplémentaires pour atteindre une
taille globale de 18 MMDH avec un impact attendu de 50 MMDH sur cinq ans, dédiés à
plusieurs secteurs clés comme les PME, l'industrie, le tourisme et l'agriculture.

De même, et dans le cadre de la dynamique de diversification des instruments de financements
à l’appui de l’entreprise, le FM6I a lancé le fonds dénommé « Cap Access » doté d'une
enveloppe de 4 MMDH dédiés au soutien des entreprises marocaines en besoin de fonds
propres. Ce fonds, géré par la SNGFE, collabore avec les banques pour distribuer des produits
de dette subordonnée, facilitant ainsi l'accès au financement pour les entreprises avec des
projets d'investissement viables.

Le FM&I a lancé également un autre produit dénommé « Cap Hospitality » visant à accélérer
la mise à niveau des Etablissements Hôteliers Touristiques Classés (EHTC), avec pour objectif
la modernisation de 25.000 chambres d'hôtels en anticipation des événements sportifs
internationaux que le Maroc accueillera.
Concernant le chantier de la réforme des EEP, il a été procédé à la mise en place d’une feuille
de route reposant sur une approche visant une cohérence globale et une convergence de
l'ensemble des actions envisagées dans le cadre de ce chantier, en tenant compte des objectifs
du projet d’amendement de la Loi Organique relative à la Loi de Finances, Cette feuille de
route s'articule autour de deux principales composantes tenant principalement à la mise en
place des textes prévus dans le cadre du projet de réforme et à la mise en place et l'exécution
d'un programme d'opérations de restructuration.

La 1°° composante se rapportant à la mise en place des textes enregistre une avancée
significative dans la mesure où sur un total de 19 textes législatifs et réglementaires prévus par
le projet de réforme, 8 textes ont été adoptés et publiés au Bu//etin Officiel, 4 ont été mis dans
le circuit d'approbation et 7 projets de textes sont en cours d’élaboration et seront mis dans
le circuit d’adoption dès l’achèvement des études et des consultations y afférentes.

De même, l'ANGSPE a défini, pour son périmètre, un plan d’action qui s'articule autour des
chantiers prioritaires visant à renforcer la gouvernance, à accompagner les opérations de
transformation en sociétés anonymes (TSA), à conduire les restructurations sectorielles, à
mettre en œuvre la consolidation des comptes et à mettre en place un dispositif de pilotage
de la performance des EEP de son périmètre.

Dans ce cadre, l'ANGSPE poursuit la mise en œuvre de plusieurs opérations de restructuration
notamment dans le secteur audiovisuel en vue de la création d'une holding publique viable et
pérenne ainsi que l'engagement de l'étude visant la redéfinition du modèle stratégique de
l'ONEE au vu des changements institutionnels ayant touché l’écosystème de l'Office. De même,
l'Agence assure l'accompagnement de plusieurs EEP, dont notamment la SNTL et BAM, en vue
de la préparation de leurs projets de restructuration et de redéfinition de leurs modèles
stratégiques.
S’agissant du périmètre des EEP piloté par le Ministère de l’Economie et des Finances, les
opérations de restructuration les concernant se caractérisent par des complexités et des
difficultés tenant à plusieurs dimensions d’ordre stratégique, institutionnel, organisationnel et
social et nécessitent, par conséquent, des concertations élargies avec les ministères de tutelle,
les EEP concernés et les autres parties prenantes.

La réussite de ces opérations de restructuration nécessite de s'appuyer sur une vision
sectorielle déclinée dans le cadre d’une stratégie sectorielle actualisée et devant déterminer,
entre autres, les objectifs, les moyens et l’organisation institutionnelle et opérationnelle de
mise en œuvre de ladite stratégie.

Les cas du secteur de l’habitat et de l’urbanisme ainsi que celui de la santé sont illustratifs,
dans la mesure où ces deux Départements ont arrêté sur la base d'une vision sectorielle, le
schéma institutionnel cible devant porter la stratégie sectorielle. [Is ont procédé, à cet effet,
par voie législative, à la mise en place d'un plan de restructuration des EEP sous leur tutelle,
en cohérence avec la réorganisation préconisée pour leurs secteurs respectifs.

Dans ce cadre et dans une logique d’accélération, le Ministère de l'Economie et des Finances
(MEF) a engagé des concertations avec plusieurs ministères, certains EEP et d'autres parties
prenantes pour mettre en place un programme de restructuration des EEP dans le cadre d’une
approche centrée sur les enjeux stratégiques, financiers, économiques et opérationnels des
secteurs et des EEP concernés.

Cette approche repose sur des critères tenant notamment au renforcement de l’efficience
économique et sociale, à l’amélioration de la qualité de service, à la valorisation des synergies
et des complémentarités, à la suppression des chevauchements de missions des acteurs
publics, à la réduction de l'appel au budget de l’Etat et au retrait des marchés matures qui
peuvent être mieux gérés par le secteur privé.

Ladite approche s'appuie également sur les opérations des audits externes menées par le MEF
et qui ont été focalisées, au cours des dernières années, sur les audits stratégiques et les
réformes institutionnelles et organisationnelles, permettant ainsi l'identification de nouvelles
opérations de restructuration.

Les travaux réalisés, à date, ont permis d’identifier un programme global d'opérations de
restructuration, réparties en trois catégories :

-  Les opérations de restructuration en cours d’exécution ou ayant un niveau de maturité
avancé. Les opérations identifiées, à ce titre, concernent une soixantaine d’EEP ;

-  Les opérations en cours d’évaluation et de réflexion et qui n’ont pas encore atteint le
niveau de maturité requis et nécessitent, par conséquent, des analyses et des
concertations approfondies ;

- Un programme d'actions spécifiques visant l’amélioration de la gouvernance des EEP,
de leur contrôle financier ainsi que d’autres actions d’appui notamment en matière de
recouvrement des créances.

RAPPORT SUR LES ETABLISSEMENTS ET ENTREPRISES PUBLICS

En matière de réforme du dispositif de gouvernance et de contrôle financier de l’Etat sur
les EEP, un projet de loi est en cours de finalisation en concertation avec les partenaires
concernés pour recueillir leurs avis et propositions avant de le mettre dans le circuit
d'adoption.

Ce projet repose sur cinq grandes inflexions notamment la maîtrise du portefeuille public,
l'instauration des bonnes pratiques de gouvernance, la généralisation du contrôle financier, le
renforcement de la transparence, le pilotage par la performance et [a modulation du contrôle
sur la base de critères liés à la qualité de la gestion et de la gouvernance.

Concernant le projet du nouveau Codc des bonnes pratiques dc gouvernance des EEP,
son élaboration vise à s'adapter aux évolutions des référentiels nationaux et internationaux en
matière de gouvernance d'entreprise, Le projet de Code, soumis à consultation publique en
juillet 2023, à été mis dans le circuit d’adoption en vue de sa publication par voie de décret.

Un plan d'action sera engagé, dès publication du décret portant approbation de ce Code, en
vue de lancer une campagne de sensibilisation et de communication visant à disséminer les
nouvelles pratiques introduites par |le Code notamment en matière de responsabilisation des
organes de gouvernance, de leur composition, de leurs missions, d'introduction des
administrateurs indépendants, d’évaluation des performances, de respect des droits des
parties prenantes, de diffusion des valeurs et principes d'ordre Environnemental, Social et de
Gouvernance (ESG), de renforcement de la transparence et de publication des informations
financières et extra-financières,

En ce qui concerne la démarche de contractualisation des relations entre l'Etat et les EEP,
et conformément aux objectifs du chantier de réforme des EEP, la nouvelle génération des
projets de contrats-programmes reposera sur des plans stratégiques validés des EEP, des
schémas institutionnels clairs, des plans d'affaires performants et des modèles économiques
et financiers viables.

Dans ce cadre, un projet de décret est en cours d'adoption afin de fixer les cas dans lesquels
sont conclus les contrats-programmes, dans le but de garantir l'accompagnement requis aux
EEP pour assurer la réussite des programmes et des politiques confiés à ces organismes.

Un nouveau guide méthodologique de contractualisation est également en cours de mise en
place. Ce guide vise à clarifier le processus et la chaîne de contractualisation en proposant des
modèles de contrats-programmes, de contrats de performance et de contrats d'objectifs
internes. Il définira, en particulier, les obligations de services publics tout en encourageant une
contribution accrue des EEP à la transition verte et au développement durable.

En matière des délais de paiement, l'Observatoire des Délais de Paiement (ODP) créé en 2017,
joue un rôle clé pour accroître la transparence et la responsabilité dans les transactions
commerciales, Lors de sa sixième réunion tenue en juin 2024, l'ODP a mis en lumière les
résultats positifs du dispositif de sanctions pécuniaires instauré par la loi n° 69-21 modifiant la
loi n° 15-95 formant code de commerce et édictant des dispositions transitoires particulières
rolatives aux délais de paioment qui a été conçu pour réduire les délais de paiement dans le
secteur privé.



Le quatrième rapport publié par l'Observatoire, le 26 juillet 2024, intègre un premier bilan du
déploiement du dispositif de sanctions susvisé mettant en exergue des perspectives
prometteuses en matière de réduction des délais entre entreprises et de consolidation de
l'équilibre des relations entre acteurs privés.

Pour les EEP, le rapport précité confirme leurs performances en matière de réduction de leurs
délais de paiement qui ont atteint une moyenne de 35,5 jours à fin 2023 contre 55,9 jours en
2018.

S'agissant des Partenariats Public Privé, la loï n° 86-12 relative aux contrats de PPP a été
modifiée et complétée par la loi n° 46-18, publiée au Bu/etin Officie/ |e 19 mars 2020. L'entrée
en vigueur de cette loi est conditionnée par la publication de l'ensemble de ses textes
d'application dont sept (7) ont été publiés et deux (2) sont en cours de finalisation en vue de
les mettre dans le circuit d’adoption.

En perspective de l'entrée en vigueur de ce nouveau cadre juridique, les travaux ont été
engagés en vue de la préparation de la 1*° réunion de la Commission Nationale de PPP
(CNPPP), présidée par le Chef du Gouvernement, et dont les principales missions portent sur
la définition des orientations générales et de la stratégie nationale pour les PPP et sur
l‘élaboration du programme national des projets PPP.

Dans ce cadre, des réunions de concertation ont été tenues avec plusieurs ministères et les
EEP sous leur tutelle en vue de la collecte des projets à inscrire au programme national de PPP
et de recueillir leurs attentes et leurs propositions en matière d’orientations stratégiques du
PPP. De même, un projet de circulaire pour recenser les projets PPP a été soumis à la signature
du Chef du Gouvernement.

HH

Le présent rapport sur les EEP, élaboré conformément à l'article 48 de la Loi Organique
n° 130-13 relative à la Loi de Finances, intègre, pour la première fois, une partie qui s'inscrit
dans le cadre d'un plan d’action engagé pour la mise en place d’un dispositif de reporting
climat des activités des EEP visant à asseoir les bases de mesure, de suivi et d’évaluation des
performances des EEP en matière de développement durable et de leurs contributions aux
efforts et aux engagements du pays en matière de transition verte.

Ainsi, ce rapport est structuré en cinq parties déclinées comme suit :

-  La première partie porte sur la présentation des composantes du portefeuille public et
de son évolution ainsi que les performances économiques et financières des EEP avec un
focus sur les EEP du périmètre de l'ANGSPE et ce, en termes de réalisations de 2023, de
prévisions de clôture de 2024 et de projections 2025-2027 ;

-  La deuxième partie est consacrée à l'analyse des avancées et des contributions des EEP
dans la réalisation des stratégies sectorielles et dans la dynamique de développement
économique et social du pays ;

- _ La troisième partie présente un bilan de l'avancement du chantier de réforme des EEP ;
-  La quatrième partie est dédiée aux aspects relatifs aux actions de consolidation des
synergies entre les secteurs public et privé à travers notamment, la promotion du recours
aux PPP ainsi que la contribution des EEP à l'amélioration du climat des affaires, dont en
particulier la réduction des délais de paiement ;

- La cinquième partie porte sur la contribution des EEP à l’effort national de transition
verte et de développement durable.

Ce rapport comporte également des annexes retraçant, particulièrement, l'inventaire du
portefeuille public, les principaux indicateurs économiques et financiers des EEP, les fiches
signalétiques des principaux EEP ainsi que les opérations portant sur les privatisations et les
autorisations de création de filiales et de prises de participation.



1s Partie : COMPOSITION ET
PERFORMANCES DU PORTEFEUILLE
PUBLIC

Cette première partie du rapport présente la composition et l'évolution du portefeuille public
dans son ensemble. Elle analyse les performances économiques et financières obtenues par
les EEP sur la période 2021-2023, les prévisions de clôture de 2024, ainsi que les projections
pour la période 2025-2027. Cette partie traite également des transferts croisés entre l'Etat et
les EEP.

B PORTEFEUILLE PUBLIC
1.1. Composition du portefeuille public

Le portefeuille public se compose, à fin septembre 2024, de 271 EEP répartis comme suit :

- 228 Etablissements Publics (EP} ;
- 43 Sociétés Anonymes à Participation Directe du Trésor:(SA-PDT).

De plus, certains EEP détiennent des filiales et/ou des participations totalisant 525 entités,
dont 53% sont détenues majoritairement.

Le portefeuille public inclut également :

- 73 Sociétés Anonymes à Participation Directe des Collectivités Territoriales“
(SAPDCT) dont 21 sociétés sont soumises au contrôle financier et sont suivies au
niveau du portefeuille public ;

- 53 Autres Organismes Publics*, dont 30 entités sont soumises au contrôle financier
et sont suivies au niveau du portefeuille public.

1.2. Évolution du portefeuille public

Entre 2022 et septembre 2024, le portefeuille public a connu les principaux mouvements
suivants :
-  Créations d’établissements publics et d'autres organismes publics :

e  Agence de Développement du Haut Atlas (ADHA) : créée par le Dahir n° 1-23-
75 du 30 novembre 2023 portant promulgation de la loi n° 57-23 approuvant le
décret-loi n° 2-23-870 du 4 octobre 2023 ;

LI s'agit de porsonnes morales de droit public dotées de 19 personnalité juridique et de l'autonomie financière
Qualifiées en tant qu'établissement public par feur texte de création.

2/ s'agit de sociétés de droit privé dont le capital est détenu directement totalement ou partiellement par l'Etat,

# fl s'agit de sociétés de droit privé dont le capital est détenu au minimum à 34% par les Collectivités Territoriales.

4 1/ s'agit de personnes morales de droit public dotées de /a personnalité juridique et de l'autonomie financière.

yN



RAPPORT SUR LES ETABLISSEMENTS ET ENTREPRISES PUBI| s

e Agence Nationale d’Aide Sociale (ANAS) : créée par le Dahir n° 1-23-88 du
30 novembre 2023 portant promulgation de la loi n° 59-23 ;

e  Haute Autorité de la Santé (HAS) : qui est une personne morale de droit public,
créée par la loi n° 07-22 du 30 novembre 2023, promulguée par le Dahir n° 1-23-
84 du 30 novembre 2023.

-  Iransformations de statut :

e Institut Supérieur de la Magistrature (ISM) : transformé en personne morale de
droit public par le Dahir n° 1-23-60 du 10 août 2023 portant promulgation de la
loi n° 37-22.

-  Cession des participations et dissolutions :

e  Cession à l'OCP SA, via sa filiale MAGHRIB HOSPITALITY COMPANY (MHC), de
la totalité des participations détenues par l'Etat dans la Société
« LA MAMOUNIA », réalisée en juillet 2024 ;

e  Cession à l'OCP SA, de la totalité des participations détenues par l'Etat dans la
Société « d’Aménagement et de Développement de Mazagan » (SAEDM SA),
réalisée en décembre 2023 ;

e  Dissolution et liquidation de [a société « SABR Aménagement » en juin 2022 ;

e Dissolution et liquidation de la Ligue Nationale de Lutte contre les Maladies
Cardiovasculaires, suite à l'adoption et à la publication du Dahir n° 1-24-35 du
7 août 2024 portant promulgation de la loi n° 32-24,

-  Création de filiales et prises de participations :

e  Création de 7 nouvelles filiales et prises de participation, dont deux par OCP SA,
deux par BAM et trois chacune par la CDG, le CAM et l'ONCF.

Par ailleurs, dans le cadre de la dynamique de réforme des EEP et de la régionalisation avancée,
l'accélération des projets de création et de réorganisation de certains EEP se poursuit au
niveau territorial, avec notamment :

-  La création de 12 Sociétés Régionales Multiservices (SRM) conformément au Dabïr
n° 1-23-53 du 12 juillet 2023, portant promulgation de la loi n° 83-21 rolative à la création
des SRM. Les 12 SRM devront remplacer les Régies de Distribution et les Directions
Régionales de Distribution de l'ONEE. !! sera procédé, dans une première étape, au
déploiement de 4 SRM selon le calendrier ci-après :

e  Société Régionale Multiservices Casablanca Settat (SRM CS) dont le contrat de
gestion du service de distribution d’eau portable, d’électricité et d'assainissement
liquide entre en vigueur le 1°" octobre 2024 ;

e Société Régionale Multiservices Souss-Massa (SRM SM) dont le contrat de
gestion entre en vigueur le 15 octobre 2024 ;

e  Société Régionale Multiservices Marrakech Safi (SRM MS) dont le contrat de
gestion entre en vigueur le 1°" novembre 2024 ;

e  Société Régionale Multiservices l'Oriental (SRM O) dont le contrat de gestion du

service entre en vigueur le 15 novembre 2024.



l PROJET DE LOI DE FINANCES POUR L'ANNEE 2025 l

-  La création de 12 Groupements Sanitaires Territoriaux (GST) en remplacement de
tous les établissements de santé du secteur public relevant de son ressort territorial
notamment les Centres Hospitaliers Universitaires (CHU), à l'exclusion, toutefois, des
établissements de santé régis par des textes législatifs ou réglementaires particuliers,
des établissements de santé militaires et des bureaux communaux d’hygiène et ce,
conformément au Dahir n° 1-23-50 du 28 juin 2023 portant promulgation de la loi n° O8-
22 relative à la création des groupements sanitaires territoriaux.

COMPOSITION DU PORTEFEUILLE PUBLIC (2022-2024)

2024
2023

2022

Portefeuille*
Public

es participation Directe
e «_. duTrésor
44 46

Etablissements
Publics
Sociétés Anonymes à

Filiales ou
Participations
Publiques

1.3. Répartition sectorielle et régionale du portefeuille public

La répartition régionale des EEP témoigne de leur ancrage territorial profond, avec 62% des
entités du portefeuille public participant dans la mise en œuvre des programmes de
développement au niveau régional. Ce maillage territorial permet aux EEP de répondre
efficacement aux besoins locaux et d'accompagner les grands projets de développement

territorial.

Sur le plan sectoriel, la diversité des activités des EEP reflète leur capacité à intervenir dans
des secteurs stratégiques de l'économie nationale. Ils sont présents dans des domaines aussi
variés que les infrastructures, l'énergie, l'eau, l'agriculture, la pêche maritime, l’éducation, la
formation professionnelle, la santé, le tourisme, l'industrie, la logistique, et les services
financiers. Cette diversité sectorielle permet aux EEP de soutenir la croissance économique
tout en répongant aux priorités sociales du pays.



RAPPORT SUR LES ETABLISSEMENTS ET ENTREPRISES PUBLICS

La répartition du portefeuille par secteur est présentée dans le graphe ci-après :
REPARTITION DES EEP PAR SECTEUR (2024)

Energie, Mines, Eau et
Environnement

Agriculture et Pêche Maritim
15,1%

Habitat, Urbanisme et.…

9
Développement 12 2/° … Infrastructure et
Territorial Transport
16,2% 5,9%

… Tourisme et Artisanat
5,9%

Social, Santé Education ”

- Finances
et Formation 5,2%
24,4%
\Autres
15,1%

Bien que le portefeuille public soit majoritairement concentré dans les régions de Rabat-Salé-
Kénitra et Casablanca-Scttat, représontant 53% dos EEP, les actions de ces ontités ne se
limitent pas à ces deux régions. En effet, de nombreuses entités basées dans ces régions
disposent de compétences nationales, leur permettant d'opérer sur l'ensemble du territoire
marocain, assurant ainsi une couverture géographique étendue et une réponse cohérente et
adaptée aux besoins des différentes régions.

En parallèle, |les EEP intensifient leur expansion à l‘international, renforçant la position du
Maroc en tant que hub économique et financier vers l'Afrique. Cette stratégie
d'internationalisation est particulièrement visible dans des secteurs clés comme les mines, les
infrastructures, l'habitat, le tourisme, les télécommunications et l'énergie, où les EEP marocains
participent activement au développement des pays partenaires africains.



l PROJET DE LOI DE FINANCES POUR L'ANNEE 2025 l

La répartition régionale des EEP est illustrée ci-après :

REPARTITION TERRITORIALE DES EEP EN 2024

Tanger - Tétouan - AI Hoceima
Oriental

Fès - Meknès

Rabat -Salé - Kénitra

Beni Mellal - Khénifra
Casablanca - Settat
Marrakech -Safi

Drâa - Tafilalet

.  Souss - Massa

10. Guelmim - Oued Noun

11. Laâyoune - Sakia El Hamra
12. Dakhla - Oued Ed Dahab

SPENEUBUNE

@ Etblissements publics

@ sociétés Anonymes à Participation Directe du Trésor

Actuellement, 18% des filiales des EEP sont implantées à l'étranger, dont 20% en Afrique,
mettant en lumière les fortes opportunités offertes par ce continent en pleine croissance.

Il PERFORMANCES DU PORTEFEUILLE PUBLIC

La présente section porte sur une analyse des indicateurs économiques et financiers de
l'ensemble du portefeuille public en mettant, ensuite, un focus sur les indicateurs des EEP du
périmètre de l'ANGSPE. Cette section comprend également une lecture de la répartition
sectorielle et de la dimension territoriale des différents indicateurs de performance des EEP.

Mn


RAPPORT SUR LES ETABLISSEMENTS ET ENTREPRISES PUBLICS

I1.1. Indicateurs économiques et financiers

L’évolution des indicateurs financiers montrent un redressement significatif en termes de
réalisations de 2023 et de prévisions de clôture de 2024 en soulignant que les prévisions sur
la période 2025-2027 confirment cette tendance et ce, aussi bien pour l’ensemble du
portefeuille public que pour le périmètre de l'ANGSPE.

1) Réalisations 2023 et prévisions de clôture 2024

Le chiffre d’affaires (CA) du secteur des Chiftre d'affaires des EEP (en MDH)
EEP s’est établi, en 2023, à 332.070 MDH
enregistrant une —quasi-stagnation par saraDE 332:070 345.912

rapport à 2022. Cette situation s'explique
principalement par la baisse du chiffre 285.382
d'affaires du Groupe OCP, qui est passé de

114.574 MDH en 2022 à 91.277 MDH en

2023. En conséquence, la part du Groupe

OCP dans le CA total du secteur a diminué,

passant de 35% en 2022 à 27% en 2023.

Les prévisions de clôture pour l'exercice

2024 indiquent une reprise significative,

avec une augmentation estimée de 4% par s051 57052 1055 2024*
rapport à 2023, portant le chiffre d'affaires Petsihé d

du secteur à 345.9122 MDH. Cette
amélioration est principalement attribuable
à la performance attendue par le Groupe
OCP.

La répartition sectorielle montre une forte concentration, en 2023, du CA au niveau des
secteurs suivants : « Energie, Mines, Eau et Environnement », « nfrastructure et
Transport », « Social, Santé, Education et Formation » et « Finances ». En effet, ces quatre
secteurs détiennent une part de 93% pour l'ensemble du secteur.

Répartition sectorielle du chiffre d’affaires au titre de 2023

Autres :7%
|

Finances : 7%

Infrastructure et

Trorepan 1148 Energie, Mines, Eau et

Environnement : 44%

Social, Santé,
Education et
Formation : 28% _—



PROJET DE LOI DE FINANCES POUR L'ANNEE 2025 l

La valeur ajoutée (VA) du secteur des EEP a
atteint 97.698 MDH en 2023, marquant une
augmentation significative de 16% par rapport à
2022, imputée principalement à l'amélioration
importante constatée en 2023 dans la VA de
l'ONEE, du Groupe TMSA et du Groupe CDG.

En prévision de clôture de 2024, la VA du
secteur est estimée à 100.372 MDH, en hausse
de 3% par rapport à 2023.

Valeur ajoutée des EEP (en MDH)
100.372
97.164 s7658
l E l
2021 2022 2023 2024*
{°) Probabiités de clôture

Sur le plan sectoriel, trois secteurs ont principalement contribué à la VA de l'ensemble du

secteur au titre de l’année 2023. || s'agit des secteurs suivants

: « Energie, Mines, Eau et

Environnement », « Infrastructure et Transport », et « Finances » qui représentent ensemble

une part de 91% de la VA du secteur.

Les Charges d'exploitation Hors Dotations
(CEHD) du secteur des EEP ont atteint un montant
de 279.128 MDH en 2023, enregistrant une baisse
de 7% par rapport à 2022. Cette évolution est
imputée, en grande partie, à la contraction des
CEHD du Groupe OCP. Les probabilités de clôture
de l'année 2024 pour l'ensemble du secteur tablent
sur un total des CEHD de 297.130 MDH,
enregistrant une hausse de 6% par rapport à 2023.

La répartition sectorielle de 2023 montre que les secteurs « Energie, Mines,

Charges d’exploitation hors dotations de EEP
(en MDH)
298.683 297.130
279.128
| l l l
2021 2022 2023 2024*
(*) Probabilités de dôture
Eau et

Environnement », « Infrastructure et Transport », « Social, Santé, Education et Formation »
et « Finances », détiennent 91% des CEHD du secteur des EEP, comme illustré dans le

graphique ci-dessous :

A



RAPPORT SUR LES ETABLISSEMENTS ET ENTREPRISES PUBI|

Répartition Sectorielle des CEHD des EEP au titre 2023

Autres : 9%,
Energie, Mines, Eau et
\ Environnement : 41%

|
|
|
Les Charges de personnel (CP) qui constituent en moyenne, durant la période 2021-2023,
une proportion de 15% du total des charges d'exploitation (hors dotations) du secteur, ont
progressé de 5% par rapport à 2022, atteignant 43.208 MDH en 2023 contre 41.183 MDH en
2022.

Finances : 4%

Infrastructure et
Transport: 11%

Social, Santé, ——
Education et
Formation : 35%

Les probabilités de clôture des CP, au titre de 2024, montrent une tendance à la hausse avec
45.381 MDH, marquant ainsi une augmentation de 5% par rapport à 2023.

En termes de répartition sectorielle des CP au titre de l’exercice 2023, les secteurs « Energie,
Mines, Eau et Environnement », « Infrastructure et Transport» et « Social, Santé,
Education et Formation » représentent des parts respectives de 41%, 17% et 15% des CP de
l'ensemble du secteur.

Après une hausse en 2022, les résultats d’exploitation du secteur des EEP ont connu une
diminution notable de 32% au titre de 2023, enregistrant un total de 15.633 MDH.

Cette contraction s'explique par une diminution importante, en 2023, des résultats
d'exploitation bénéficiaires (-27%) avec un impact dépassant l’effet lié à l'amélioration des
résultats d'exploitation déficitaires (+23%).

Quant aux résultats nets du secteur des EEP, ils ont connu une amélioration importante, en
passant de 1.044 MDH enregistré en 2022 à 9.278 MDH en 2023.

Les prévisions de clôture de 2024 confirment le retour à la tendance haussière des résultats
du secteur des EEP, avec une amélioration des résultats d’exploitation de 85% (28.930 MDH)
et des résultats nets de 52% (14.071 MDH}.

VS



PROJET DE LOI DE FINANCES POUR L'ANNEE 2025 l

Résultats bénéficiaires et Résultats déficitaires des EEP (en MDH)
; 51.479
| 41772 41.131
u% ! 37323
25.506 26.366 26.722 ï
‘
‘
'
'
T T T ' T T T 1
24es -12.651 ! -10.584 -12,201
-17.088 ‘
A -21.690
' -28.336
-33.176
2021 | 2022 ‘ 2023 l 2024* 2021 l 2022 l 2023 l 2024*
Résultats Nets Résultats d'Exploitation
(°) Probabilités de clôture @ Résultats Bénéficiaires © Résultats Déficitaires

La répartition sectorielle montre une forte concentration du résultat net excédentaire global
dans les secteurs de « l’Energie, Mines, Eau et Environnement » à hauteur de 61% et de
« l’Infrastructure et Transport » à raison de 20%.

Répartition Sectorielle des Résultats Nets Excédentaires des EEP au titre de 2023

Autres : 7,9%

Finances : 10,3%

Infrastructure et
Transport : 20,4%

Energie, Mines, Eau et
Environnement : 61,4%



RAPPORT SUR LES ETABLISSEMENTS ET ENTREPRISES PUBLICS

Le total des actifs a connu, en 2023, une Toinl doxaciés deu TR en Mioi
appréciation de 5% par rapport à 2022, avec un
montant de 1.931.606 MDH,. Les prévisions de 1.987.758
clôture de 2024 (1.,987.758 MDH) présentent 1.931.606
une hausse de 3% par rapport à 2023.
Par ailleurs et en 2023, 52% des actifs du secteur Haspiss
des EEP sont détenus par cing entités, à savoir :
Groupe CDG, Groupe OCP, ONEE, Groupe CAM E
ct Groupe BAM. '
2021 2022 2023 2024*
(*) Probabilités de clôture
L’encours des dettes de financement du secteur Dettes de financement en MDH

336.035

des EEP s’est établi, à fin 2023, à 326.488 MDH, en
baisse légère de 1% ppar rapport à 2022.

228.206 s25088

Les prévisions de clôture de 2024 établies à

336.035 MDH montrent une hausse de 3% par

rapport aux réalisations de 2023.

Les baisses constatées, en 2023, des dettes de mere

financement ont été enregistrées par le Groupe

CAM, le Groupe RAM, MASEN et le Groupe ANP.

D'autre part, les principales hausses constatées au

niveau du secteur concernent le FEC, le Groupe
HAO, l'ONEE et le Groupe OCP. 2021 2022 2023 2024*

(*) Probabilités de dôture

L’analyse, par secteur, montre une concentration des dettes de financement au niveau des
secteurs suivants: « Energie, Mines, Eau et Environnement », « Finances» et
« Infrastructure et Transport ». Ces trois secteurs détiennent, en 2023, plus de 96% des
dettes de financement du secteur des EEP.

Répartition Sectorielle des dettes de financement des EEP au titre de 2023

Autres : 4%

Finances : 10%

Energie, Mines, Eau
et Environnement :
46%

rrr /

Transport : 40%



11) Prévisions 2025-2027

Les prévisions sur [a période 2025-2027 montrent une consolidation des indicateurs financiers
des EEP. Ces prévisions ont été établies sur la base d’hypothèses et de scénarios spécifiques
à chaque entité, tenant compte de leur secteur d'activité et des incertitudes externes, telles
que la volatilité des prix des matières premières et les perturbations dues aux tensions
internationales.

Le tableau, ci-après, présente les prévisions des principaux indicateurs sur la période 2025-
2027 pour l'ensemble du secteur des EEP :

MILLIONS DE DH 2025 2026 sor
Chiffre d'Affaires 375 029 402711 433 543 403 761
t 304 871 308 325 322 686 3n 961
Charges de Personnel 45 752 46 752 48 873 47126
Valeur Ajoutée 119006 137 144 150 713 135 620
Résultat d'Exploitation ( 49 591 67 787 78 585 65 321
Résultat Net (*) 20 397 39 366 46 416 35 393
Total des actifs 2 005 350 2040 689 2 057 894 2 034 644

() Hors CMR & CNSS

Les prévisions sur la période 2025-2027 des principaux indicateurs du secteur des EEP
annoncent des perspectives favorables :

- Une augmentation du chiffre d'affaires et de la valeur ajoutée par rapport à 2024,
enregistrant ainsi, une moyenne annuelle respective de 403.761 MDH et de
135.620 MDH :

- Un trend d’évolution progressif des charges d'exploitation (hors dotations) par rapport
à 2024, tablant ainsi sur Une moyenne annuelle d'un montant de 311.961 MDH sur la
période ;

-  Une tendance haussière des résultats d’exploitation et des résultats nets ;

- Une phase de renforcement des actifs.

H.2. Investissement

En 2024, les investissements actualisés des EEP s'élèvent à 132.067 MDH contre 152.013 MDH
prévus initialement (Loi de Finances pour l'année budgétaire 2024), soit une baisse de 13%.
Cette diminution s'explique par l'impact des décisions issues des discussions budgétaires et
des délibérations des organes de gouvernance des EEP qui tiennent compte des évolutions
de la conjoncture et du marché au cours du dernier trimestre de l'exercice écoulé et du premier

J


RAPPORT SUR LES ETABLISSEMENTS ET ENTREPRISES PUBLICS

trimestre de l’exercice en cours. Quant aux prévisions de clôture au titre de 2024, elles sont
établies à 115.215 MDH, soit un taux de 87% par rapport aux prévisions actualisées.

Concernant l’exercice 2025, les investissements des EEP connaitraient une légère hausse de
4% par rapport aux investissements actualisés de 2024, pour atteindre 137.700 MDH. En 2026
et 2027, il est prévu de réaliser un volume d'investissement à hauteur de 141.614 MDH et de
122.298 MDH respectivement.

) Investissements réalisés

En 2023, les EEP ont réalisé Un volume d'investissement total de 81.285 MDH, en amélioration
de 6% par rapport à 2022 (+4.533 MDH).

Evolution de l'investissement des EEP au titre de la période 2016-2024

115.215

66.063

81285
72.675 71174 76.752
61.286 59.033 SeLss
92.650
58.655 57.172 60.262
48.169 48.894 49.804 saget 45.915

2016 2017 2018 2019 2020 2021 2022 2023 2024*

(*) Probabilités de côture ESecteurdesEEP H Périmètre de l'Agence

Ce niveau de performances des EEP en matière d'investissement a été atteint grâce
notamment aux réalisations du Groupe OCP (27.400 MDH), de l’ONEE (6.823 MDH), des
AREF (6.059 MDH), du HAO (4.548 MDH), de la SRRA (3.747 MDH), du Groupe CDG
(3.417 MDH) et des Régies de Distribution (2.494 MDH).

Ces EEP représentent, à eux seuls, plus de 67% de l'ensemble des réalisations des EEP en
matière d’investissement au titre de 2023.



1) Projections 2025-2027

Pour l'exercice 2025, le programme Investissements 2025-2027 en MDH
d'investissement prévisionnel des EEP est évalué à
137.700 MDH dont un volume de 103.204 MDH est 337700 141.614

attribué aux EEP du périmètre de l'ANGSPE. pn
Ces investissements sont imputés, en grande partie
aux EEP suivants: Groupe OCP (45.000 MDH),
ONEE (13.788 MDH), AREF (7.516 MDH), HAO
(6.433 MDH), Régies de Distribution (5.896 MDH)
et Groupe CDG (4888MDH) Ces EEP 103.2

représentent à eux seuls presque 61% des 25607 82.210
projections d’investissement au titre de 2025.

Les prévisions de 2026, établies à 141.614 MDH ' T T
montrent une légère hausse par rapport à 2025 et 20 20s æ
qui sera suivie par une diminution en 2027 ESecteur des EEP _ Périmètre de l'Agence
(122.298 MDH). Ces investissements sont imputés
à 64% aux EEP du périmètre de l'ANGSPE.

fi{) Analyse par Région

L'analyse de la répartition régionale des prévisions actualisées des investissements des EEP
en 2024 (132.067 MDH) fait ressortir une concentration de 46,6% des investissements dans
les deux régions (Casablanca-Settat et Rabat-Salé-Kénitra). Trois autres régions émergentes
se réservent une part de 28,9% (Marrakech - Safi, Tanger - Tétouan - AIl Hoceima et l’Oriental).
Les régions de Beni Mellal - Khénifra, Laôyoune - Sakia El Hamra et Fès - Meknès s'accaparent,
respectivement, des parts de 5,4%, 4,6% et 4,2%. Le reste des régions se départagerait les
10,3% restant des investissements prévus.

Quant à l’exercice 2025, les deux régions « Fès - Meknès » et « Drâa - Tafilalet » devraient
enregistrer, par rapport à 2024, une progression de 1,5 point de leur part d'investissement
(soit, respectivement 5,8% et 6,2% en 2025), suivies de la région Casablanca - Settat avec une
amélioration de sa part de O,3 point (soit 32% en 2025 contre 31,7% en 2024).

En revanche, la région de l'Oriental marquera une régression de 1,6 point en se limitant à 4,7%
de sa part d'investissement en 2025 contre 6,4% en 2024. Les autres régions auront des
variations des parts d’investissements ne dépassant pas 1 point comme l'illustre le tableau ci-
après :



RAPPORT SUR LES ETABLISSEMENTS ET ENTREPRISES PUBLICS

hs pourc‘Ë1tage ‘ u , pour<Èeütage

Casablanca - Settat 41869 31,7 44 012 32,0
Rabat - Salé - Kénitra 19 665 14,9 18 995 13,8
Marrakech - Safi 19329 14,6 19648 14,3
Tanger - Tétouan - Al Hoceima 10 391 7,9 9 862 72
Oriental 8 395 6,4 6 503 4,7
Beni Mellal - Khénifra 7175 5,4 7254 5s
Laäyoune - Sakia El Hamra 6 063 4,6 6 459 4,7
Fès - Meknès 5273 4,2 7940 5,8
Souss - Massa 4 230 S 5126 sr
Drâa - Tafilalet 6 218 4,7 8495 62
Guelmim - Oued Noun 2141 16 2260 16
Dakhla - Oued Eddahab 1015 0,8 1146 0,8

Total Régions 132 067 100,0 ‘ 137 700 100,0

Il PERFORMANCES DES EEP DU PERIMETRE DE L’ANGSPE

La présente section porte sur une analyse des indicateurs économiques et financiers des EEP
du périmètre de l'ANGSPE accompagnée d’une lecture de leur répartition sectorielle.

IH.1. Réalisations 2023 et prévisions de clôture 2024

En 2023, le chiffre d'affaires (CA) des EEP du Chiffre d’affaires des EEP du périmètre de
périmètre de l'ANGSPE (223.607 MDH), qui l'Agence (en MDH)
représente 67% du CA total du secteur en 2023,

a diminué de 2% par rapport à 2022, bien qu'il ns 239.945

223.607

ait augmenté de 16% par rapport à 2021.

192.323

Concernant, les probabilités dc clôture de
l'exercice 2024, les EEP du périmètre de
l'ANGSPE prévoient un CA de 239.945 MDH en
augmentation de 7% par rapport à 2023 et 5%
par rapport à 2022. Cette amélioration est due,
essentiellement, aux performances attendues
par le Groupe OCP, le Groupe HAO et le Groupe 2021 2022 2023 2024*
ADM. (*) Probabilités de clôture



l PROJET DE LOI DE FINANCES POUR L'ANNEE 2025 |

Le chiffre d'affaires des EEP du
périmètre de l'ANGSPE est imputé à
hauteur de 92% à 3 secteurs ; « Energie,
Mines, Eau =et — Environnement »,
«Infrastructure et Transport» et
« Finances ».

Finances

Infrastructure eL
Transport : 21%

‘Autres : 8%

11%

Energie, Mines, Eau et
Environnement : 60%

La valeur ajoutée (VA) des EEP du périmètre
de l'ANGSPE a progressé de 17% pour s'établir à
93.859 MDH en 2023. Cette amélioration est
principalement due à la forte croissance de la
valeur ajoutée de l'ONEE, du Groupe TMSA et du
Groupe CDG.

Les prévisions de clôture de la VA
(97.295 MDH}) de l'année 2024 affichent une
croissance de 4% par rapport à 2023.

Valeur ajoutée des EEP du périmètre de
l'Agence (en MDH)
24.434 93.859 ns
80.132
2021 2022 2023 2024*
{*)Probabilités de dôture

Au niveau sectoriel, la VA des EEP du périmètre de l'ANGSPE, en 2023, est détenue,
essentiellement, par trois principaux secteurs : « Energie, Mines, Eau et Environnement »
pour 44%, « Infrastructure et Transport » pour 26% et « Finances » pour 21%.

Les Charges d'’Exploitation Hors Dotations
(CEHD) du périmètre de l'ANGSPE ont reculé
de 12% par rapport à 2022, enregistrant
164.727 MDH en hausse de 30% par rapport à
2021.

Les probabilités de clôture des CEHD des EEP
du périmètre de l'ANGSPE au titre de 2024 sont
estimées à 179.414 MDH soit une hausse de 9%
par rapport à 2023 due à la hausse prévue pour
le Groupe OCP.

A

Charges d’exploitation hors dotations des
EEP du périmètre de l'Agence (en MDH)

33728 179.414

164.727

126.893

2021 2022 2023

{)Probabilités de clôture



RAPPORT SUR LES ETABLISSEMENTS ET ENTREPRISES PUBLICS

En 2023, les CEHD des secteurs Répartition Sectorielle des CEHD au titre 2023
« Energie, Mines, Eau et

; Autres : 10%
Environnement », « Infrastructure |

et Transport », et « Finances »
représentent 90% de celles du
périmètre de l'ANGSPE.

Finances : 7%

Infrastructure et |
Transport : 19%-

“ Energie, Mines, Eau et
Environnement : 64%

Les charges de personnel (CP) des EEP du périmètre de l'ANGSPE, ont clôturé l’année 2023
avec un montant de 33.005 MDH contre 31.849 MDH en 2022 et 30.005 MDH en 202]1, soit
en moyenne, une augmentation de 5% sur la période 2021-2023.

En 2024, les CP des EEP du périmètre de l’Agence devraient enregistrer une hausse de 3% par
rapport à 2023 en passant de 33.005 MDH à 34.060 MDH.

En termes de répartition sectorielle des CP pour l’exercice 2023, les secteurs de « l’Energie,
Mines, Eau et Environnement », de « l'Infrastructure et Transport » et des « Finances »
représentent des parts respectives de 49%, 22% et 16% des CP du périmètre de l'ANGSPE.

En 2023, les résultats d'exploitation des EEP du périmètre de l'ANGSPE ont enregistré une
diminution de 33% par rapport à 2022 pour passer de 31.765 MDH en 2021 à 23.426 MDH en
2022, puis à environ 15.720 MDH en 2023. Cette évolution s'explique par la dégradation, en
2023, des résultats d'exploitation bénéficiaires (34.274 MDH) de 30% contre une amélioration
de 27% des résultats d’exploitation déficitaires (-18.554 MDH).

Par contre, les résultats nets des EEP du périmètre de l'ANGSPE ont connu une importante
amélioration, en passant d'un déficit de 744 MDH en 2022 à un bénéfice de 7.361 MDH en
2023. Cette hausse est expliquée par l’effet conjugué de l'amélioration des résultats nets
déficitaires (- 16.532 MDH) de 49% et la baisse des résultats nets excédentaires de 25% avec
un montant de 23.893 MDH.



PROJET DE LOI DE FINANCES POUR L'ANNEE 2025 |

Résultats bénéficiaires et Résultats déficitaires des EEP du périmètre de l'Agence (en
, MDH)
ï 48.995
E 89.512 38.408
31.735 ! 22
23.558 23.893 24.397 !
‘
'
T T T û T T T ,
5 : ]
-8.855 21.482 ! -7.747 -9.623
=16:532 Ï -18.554
T -25.569
-32.,479
2021 ] 2022 ‘ 2023 l 2024* 2021 l 2022 ‘ 2023 l 2024*
Résultats Nets Résultats d'Exploitation
(°) Probabilités de clôture @ Résultats Bénéficiaires © Résultats Déficitaires

En 2024, il est prévu un retour à une tendance haussière des résultats du secteur des EEP
relevant du périmètre de l'Agence. En effet, une amélioration de 83% des résultats
d'exploitation est attendue, atteignant 28.784 MDH. Parallèlement, les résultats nets devraient
progresser de 75% pour s'établir à 12.905 MDH.

En 2023, la répartition sectorielle montre
une forte concentration du résultat net
excédentaire global dans les secteurs de

« l'Energie, Mines, Eau et u \ autres:3%
Environnement » et de « l’Infrastructure

Répartition Sectorielle des

et Transport », avec une part de 86% du
résultat net du périmètre de l'ANGSPE.

Infrastructure
et Transport : —
21%

\ Energie, Mines,
Eauet
Environnement :
65%



RAPPORT SUR LES ETABLISSEMENTS ET ENTREPRISES PUBLICS

Le total des actifs des EEP relevant du Total des actifs des EEP du périmètre de
périmètre de l'Agence, représentant près de 80% l'Agence (en MDH)

du total du secteur en 2023, ont enregistré une
hausse respectivement de 4% et 11% par rapport
à 2022 et 2021, pour s'établir à 1528.919 MDH. 1.474.953
Les prévisions de clôture pour 2024 indiquent
une hausse de 3% des actifs des EEP du
périmètre de l'ANGSPE, ramenant ce montant à
1.580.121 MDH.

1.580.121

1.528.919

1.379.188

En 2023, cinq entités concentrent à elles seules
65% du total des actifs des EEP du périmètre de
l’'ANGSPE. Il s'agit du Groupe CDG, du Groupe
OCP, de l'ONEE, du Groupe CAM et du Groupe
BAM.

2021 2022 2023 2024*

(*)Probabilités de côture

1H.2. Prévisions sur la période 2025-2027

Le tableau, ci-après, présente les prévisions des principaux indicateurs sur la période 2025-
2027 pour les EEP constituant le périmètre de l’'ANGSPE :

Moyenne
(2025-2027)

Millions de DH

293 848 323 349 294 921

Chiffre d'Affaires 267 567

Charges d'Exploitation Hor:

Dn 186 669 189 083 203 044 192 932
Charges de Personnel 34 282 34 807 36 694 35 261
Valeur Ajoutée Î 116 418 134 682 148 166 133 088
Résultat d'Exploitation 49 530 67 358 78 924 65 271
Résultat Net 17 986 37 319 45 501 33 602
Total des Actifs - 1594 800 1626 676 1643 292 1621 589

Les principaux indicateurs des EEP du périmètre de l'Agence devraient connaître une
croissance soutenue au cours de la période 2025-2027. Ainsi, les EEP du périmètre de
l'ANGSPE devraient enregistrer les évolutions suivantes :

- Une augmentation significative du chiffre d'affaires et de la valeur ajoutée à partir de
2025, avec une moyenne annuelle respective de 294.921 MDH et 133.088 MDH sur la
période 2025-2027 ;

M



- Une évolution progressive des charges d'exploitation (hors dotations) avec une
moyenne annuelle de 192.932 MDH. Les charges de personnel suivraient cette même
tendance à la hausse sur les trois prochaines années ;

-  Une tendance haussière des résultats d'exploitation et des résultats nets, ce qui se
traduira par une amélioration de la rentabilité des EEP du périmètre de l'ANGSPE ;

- Un renforcement continu des actifs sur la période 2025-2027, témoignant de l'effort
d'investissement des EEP du périmètre de l'Agence prévu pour cette période.

IV. RELATIONS FINANCIERES ENTRE L’ETAT ET LES EEP

Les relations financières entre l'Etat et les EEP consistent en des transferts croisés comprenant
l'appui de l'Etat au profit les EEP et les contributions de certains EEP au Budget Général de
l'Etat (BGE).

L'appui de l'Etat en faveur des EEP prend la forme de subventions d’équipement et/ou de
fonctionnement, d'apports en capital ou de dotations en fonds propres.

L’augmentation constatée, au cours des dernières années, des montants de l'appui de l’Etat
en faveur des EEP résulte des effets conjugués de plusieurs facteurs notamment l'accélération
des transferts aux EEP de nouvelles activités qui étaient assurées, auparavant, par
l'administration, le rythme soutenu de création d'établissements publics à caractère non
marchand pour la prise en charge de missions de service public et l'accroissement du soutien
financier accordé à certains EEP affectés par les effets des crises successives (ONEE, RAM .>.

En plus de leurs contributions fiscales, les EEP versent au BGE des produits sous forme de
dividendes, de parts de bénéfices, de contributions budgétaires ou de redevances pour
occupation du domaine public et d'autres revenus.

Le volume des transferts des EEP au budget de l'Etat dépend de plusieurs facteurs,
principalement les indicateurs financiers (résultat net, chiffre d'affaires, trésorerie, etc.) et les
besoins de financement des programmes d'investissement des entités concernées.

(| convient de souligner que plus de 200 EEP bénéficient de soutien budgétaire de l'Etat, alors
que le nombre de ceux qui contribuent au budget de l'Etat ne dépasse pas 25 entités.

Ainsi, la présente section traite des aspects suivants :
-  Transferts budgétaires de l'Etat vers les EEP ;
-  Taxes parafiscales affectées aux EEP ;
-  Produits versés par les EEP au BGE ;
-  Contributions fiscales des EEP.
IV.1. Transferts budgétaires de l’Etat aux EEP

Les versements effectués en 2023 au profit des EEP marchands représentent 30% du montant
total des transferts de l'Etat vers les EEP.

Entre 2014 et 2023, les fonds débloqués en faveur des EEP ont enregistré un taux de
croissance annuel moyen (TCAM) de 11,08%.

yN



RAPPORT SUR LES ETABLISSEMENTS ET ENTREPRISES PUBLICS

Evolution des transferts de l'Etat aux EEP (MDH)

65.687 68207

55.879
40.687
npm1 30700 33310 33213
25.519 26.301 26.476 ë | |

2014 2015 2016 2017 2018 2019 2020 2021 2022 2023 2024{*)
( Prévisions

Les transferts du BGE au profit des EEP au titre de 2023 se sont élevés à 65.687 MDH, soit un
taux de réalisation de 93% par rapport aux prévisions (70.766 MDH).

La répartition sectorielle montre que les transferts budgétaires de l'Etat aux EEP, en 2023,
sont, essentiellement, destinés aux secteurs prioritaires, à savoir l'éducation, l'enseignement
supérieur et la formation (29.428 MDH), l'agriculture et la pêche (8.474 MDH), l'eau, l’énergie
et les mines (6.766 MDH), le secteur du transport (5.058 MDH) et le secteur de la santé et du
développement social (4.073 MDH).

Répartition sectorielle des transferts de l'Etat aux EEP en 2023

Autres : 18,1%

Secteur de la santé et

du développement
social : 6,2% \

Education,
Enseignement supérieur
et formation : 44,8%

Transports:7,7%/ —

Energie, Mines et //
Eau : 10,3%

Agriculture et Pêche : 12,9%

En 2023, les déblocages ont été répartis comme suit : 52% ont été alloués au fonctionnement
des EEP subventionnés (34.186 MDH), 33% à l'équipement (22.077 MDH) et 15% à
l'augmentation de capital (9.423 MDH), Cette ventilation se décompose comme suit :

- Pour les EEP non marchands, un total de 46.076 MDH a été débloqué, dont
32.508 MDH pour le fonctionnement et 13.568 MDH pour l'équipement. Ces versements
ont bénéficié, essenticlloment, aux AREF (23.088 MDH), aux ORMVA (3.393 MDH), aux
CHU (2.744 MDH), à l'ONOUSC (2.669 MDH), à l'OFPPT (1.145 MDH), à l'ANEF
(1.099 MDH), à l'ONSSA (1.071 MDH) et aux ABH (499 MDH) :

S



- Pour les EEP marchands, 19.611 MDH ont été versés, dont 8.509 MDH pour
l’'équipement, 1.679 MDH pour le fonctionnement et 9.423 MDH pour les augmentations
de capital. Ces versements ont été attribués notamment à l'ONEE (5.343 MDH), à
l'ONCF (3.019 MDH) à la SNRT (1.517 MDH, hors 400 MDH versés à titre exceptionnel)
et à la RAM (1.500 MDH).

Répartition des transferts par catégorie en 2023

EP non marchands 32 508 13568
0% 20% 40% 60% 80% 100%

MAug. de Capital OFonct. MEquip.

Par ailleurs, les prévisions pour 2024, actualisées à fin août, s’élèvent à 68.207 MDH et sont
réalisées à hauteur de 53%.

IV.2. Taxes parafiscales affectées aux EEP

Le soutien de l’'Etat aux EEP ne se limite pas aux subventions et aux dotations allouées à
certains EEP par le BGE mais englobe également d'autres concours financiers. (| s’agit
notamment du produit des taxes parafiscales perçues par certains organismes.

Le montant total des produits de ces taxes est passé de 3.575 MDH en 2014 à 5.644 MDH en
2023. Le graphique, ci-dessous, retrace l'évolution du produit total desdites taxes entre 2014
et 2024 (prévisions de clôture) :

Evolution des taxes parafiscales bénéficiant aux EEP au titre de la
période 2014-2024 (en MDH)

4,816 5.644

5.997
4840 4114 As 50s — ——
[ l Ï l‘ | ‘_l I l

2014 2015 2016 2017 2018 2019 2020 2021 2022 2023 Prévu
2024

Les principaux EEP bénéficiaires des taxes parafiscales en 2023 sont :

- L'OFPPT avec un montant de 3.327 MDH au titre de la Taxe de la Formation
Professionnelle (TFP) collectée par la CNSS et reversée à l’Office. Cette taxe représente
59% du montant total des taxes parafiscales perçues par les EEP ;

J


RAPPORT SUR LES ETABLISSEMENTS ET ENTREPRISES PUBLICS

- L’ONP avec 410 MDH au titre de la taxe d'affrètement pour la pèche des espèces
pélagiques ;

-  La NARSA avec 266,8 MDH au titre des diverses taxes instituées à son profit (taxe des
assurés, assurances, carburant, automobile, Centres de Visites Techniques.…) ;

-  Les CCIS avec 200,4 MDH au titre du décime additionnel de la taxe professionnelle ;
-  L’ONMT avec 195 MDH au titre de la taxe de la promotion touristique ;

- _ La SNRT avec 194,7 MDH au titre de la Taxe pour la Promotion du Paysage Audiovisuel
National (TPPAN), collectée par l'ONEE, les Régies de Distribution et les Sociétés
Délégataires ;

- _ L’ONICL avec 145,4 MDH au titre de la Taxe de commercialisation des céréales et des
légumineuses.

Les produits de la Taxe Parafiscale à l'Importation (TPI) recouvrés par l'ADII ont atteint, en
2023, un montant de 627 MDH qui a été affecté aux EEP bénéficiaires comme suit : AMDIE
(294 MDH), EACCE (242 MDH), ANPME (52 MDH) et làa MDA (39 MDH).

Au titre de l'année 2024, le montant prévu des taxes parafiscales est estimé à 5.997 MDH.
IV.Z. Produits versés par les EEP au BGE

Les transferts entre l'Etat et les EEP prennent la forme de flux financiers envers l'Etat sous
forme de dividendes, de parts de bénéfices, de produits de monopole, de contributions
budgétaires, de redevances pour l'occupation du domaine public et d'autres revenus.

Les produits versés par les EEP au BGE (hors produits de cession d'actifs et de privatisation),
ont atteint 13.987 MDH au titre de la Loi de Finances pour l’année budgétaire 2023, soit un
taux de réalisation de 85% par rapport aux prévisions initiales (16.464 MDH). Les principaux
versements ont été effectués par OCP SA (7.441 MDH), l’'ANCFCC (4.000 MDH) et Bank AI
Maghrib (937 MDH).

Les produits de 2023, réalisés à hauteur de 13.987 MDH, sont en légère hausse de 6% par
rapport à l'année 2022 (13.146 MDH). Cette évolution résulte, en partie, de l’amélioration des
dividendes et des contributions versées par certains EEP notamment OCP SA et l'ANCFCC,
suite à la reprise des activités de ces organismes par rapport aux deux dernières années.

Concernant [a Loi de Finances pour l’année budgétaire 2024, les prévisions initiales au titre
des produits à provenir des EEP, hors produits de cession d'actifs et de privatisation, sont de
15.480 MDH alors que les prévisions de clôture s’élèvent à 18.485 MDH (+19%).

Les réalisations cumulées de ces produits à fin août 2024 totalisent Un montant de 8.317 MDH
versés principalement par les EEP suivants : OCP (3.000 MDH), ANCFCC (2.000 MDH), Bank
Al Maghrib (2.636 MDH dont 2.156 MDH au titre de parts de bénéfice), ONDA (120 MDH au
titre de redevances pour l'occupation du domaine public), Office des Changes (140 MDH),
Marsa Maroc (134 MDH} et ANRT (120 MDH}.

Le Projet de Loi de Finances pour l’année budgétaire 2025 prévoit le versement d'un
montant de 19.546 MDH au titre des produits à provenir des EEP et ce, hors produits de
cession d'actifs et de privatisation. Ces prévisions enregistrent Une hausse de 26% par rapport

S



aux prévisions de la Loi de Finances pour l’année budgétaire 2024 hors produits de cession
d'actifs et de privatisation (15.480 MDH).

Concernant les produits de cession d’actifs et de privatisation, leurs réalisations en 2023
ont été établies à 1607 MDH, représentant 18% des prévisions initiales (9.000 MDH).

Les prévisions de clôture 2024 de ces produits sont évaluées à 5.980 MDH contre un montant
prévu de 9.000 MDH. Les réalisations, à fin août 2024, sont de 1.700 MDH, représentant 28%
des prévisions de clôture.

Les projections de 2025 des produits de cession d’actifs et de privatisation sont arrêtées à
92.000 MDH.

Les contributions des EEP au BGE au titre des dividendes, des parts de bénéfice, des
redevances d’occupation du domaine public et d'autres redevances et contributions ont
atteint entre 2014 et 2023, un montant annuel moyen de 10.215 MDH versés, principalement,
par quatre contributeurs, à savoir : OCP, ANCFCC, IAM et Bank Al-Magbhrib.

Le graphique suivant retrace l'évolution des réalisations et des prévisions au titre des produits
provenant des EEP (hors produits de cession d'actifs et de privatisation) sur la période 2014-
2025 :

Contribution des EEP au Budget Général de l'Etat (hors cession d'actifs et

sation) au titre de 2014-2025 (EN MDH)

18485 19:546

13.146 18.087
10.544 10.711
9.780 8957 7083 8158 9285 29.594 l | l

2014 2015 2016 2017 2018 2019 2020 2021 2022 2023 2024(*) 2025 (**)

( Prévisions de clôture, (**) Prévisions



RAPPORT SUR LES ETABLISSEMENTS ET ENTREPRISES PUBLICS

IV.4. Contribution fiscale des EEP

En 2023, la contribution fiscale des EEP au titre de l'IS, de l’IR et de la TVA a atteint un montant
de 26.638 MDH (hors Contribution Sociale de Solidarité sur les Bénéfices, estimée
à 1.716 MDH), en hausse de 7% par rapport à 2022 et représentant environ 16% de la recette

globale au titre de ces impôts.

Contribution fiscale des EEP au titre de la période 2020-2023

OIS OIR MTVA ETotal

RSx 26.638
20.117 20.580
15.157
13.089
29.140
6510 ° 7.154 7.589 6.961
"'°“W' conR =N cu
2020 2021 2022 2023



2ème Partie : LES EEP, ACTEURS MAJEURS
DU DEVELOPPEMENT ECONOMIQUE ET
SOCIAL DU PAYS

l. DEVELOPPEMENT DES RESEAUX D’INFRASTRUCTURES

1.1. Réseaux des Transports
1.1.1, Transport autoroutier

Le trafic autoroutier a enregistré une croissance de 8% en 2023 (14.600 v/j contre 13.600 v/j
en 2022) contre 6% enregistré en 2022 et le taux de télépéage s'est établi à 58% en 2023
contre 57% en 2022,

Ainsi, le chiffre d’affaires de 2023 à connu une amélioration significative de +341 MDH (+10%)
par rapport à 2022, pour atteindre 3.725 MDH.

En 2023, ADM a réalisé un résultat net bénéficiaire de 1.065 MDH contre une perte de
669 MDH en 2022, sous l'effet de l'amélioration du résultat financier (+67%) liée, en grande
partie, à l’'amélioration des taux de change.

Le montant des investissements réalisés en 2023 s’est établi à 901 MDH, représentant 55% des
prévisions de l’exercice (1.650 MDH).

Les dettes de financement s’élèvent à fin 2023 à 39.474 MDH (dont 2.300 MDH au titre du
crédit de TVA) contre 39.186 MDH en 2022,

A fin juin 2024, le chiffre d'affaires d'’ADM totalise 1.826 MDH contre 1.688 MDH pour la même
période de l'année 2023.

Selon la tendance observée lors du premier semestre 2024, le chiffre d'affaires à fin 2024
devrait s’établir à 4.025 MDH soit une hausse de 8% par rapport à 2023.

Le programme d'investissement réalisé, à fin juin 2024, à hauteur de 42% des prévisions
budgétaires, affiche un total de 853 MDH, alors que les prévisions de clôture tablent sur un
montant d'investissement de 2.054 MDH.

En prévisions triennales, le chiffre d'affaires d'ADM devrait atteindre 4.318 MDH en 2025,
4.556 MDH en 2026 et 4.807 MDH en 2027.

Le programme d'investissement prévoit, essentiellement, la réalisation de la Continentale
Rabat-Casablanca, la construction du projet Tit Mellil-Berrechid et la réalisation des nœuds de
Sidi Maarouf et Ain Harouda et devrait atteindre 7,74 MMDH sur la période 2025-2027, réparti
comme suit : 2.658 MDH pour 2025, 2.450 MDH pour 2026 et 2.630 MDH pour 2027.

Par ailleurs, et suite au Message de Sa Majesté le Roi Mohammed VI, que Dieu L'assiste,
adressé, le O8 novembre 2023, aux participants à la 4°"° édition du Forum pour
l'investissement en Afrique, annonçant l’extension du réseau autoroutier à 3.000 km à l'horizon
2030, soit plus de 1.000 km de nouvelles autoroutes, les concertations sont en cours entre les
parties concernées dans l'objectif de la mise au point du nouveau programme d'aménagement

yN


RAPPORT SUR LES ETABLISSEMENTS ET ENTREPRISES PUBLICS

et d’'investissement et du plan de son financement, en soulignant que ce programme entre
dans le cadre des travaux de préparation de la Coupe du monde 2030.

CHIFFRE D'AFFAIRES - ADM (MDH) RESULTATS - ADM (MDH)
2008
3725 4.025 1711 1938
3.207 5.383 1448
106
400
42
-669
2021 2022 2023 2024* 2021 2022 2023 2024*
E RESULTAT NET m RESULTAT D'EXPLOITATION
(*) Probabilités de clôture (*) Probabilités de clôture
L1.2. Transport ferroviaire
L'année 2023 est caractérisée par une croissance soutenue de l'activité « voyageurs », avec

un flux additionnel de plus de 7 millions de voyageurs par rapport à 2022 (+15%). Les trains AIl
Boraq ont transporté, durant sa 5°"° année d'exploitation, 5,2 millions de passagers, soit une
évolution de 25% comparée à l’année 2022.

Ainsi, le nombre de voyageurs transportés en 2023 a atteint 53 millions. L'ONCF prévoit, dans
l'optique de maintenir la performance de l'activité voyageurs, une croissance de 4% en 2024,
soit plus de 55 millions de voyageurs.

En termes de fret, l'ONCF a pu transporter, en 2023, plus de 17 millions de tonnes de
marchandises, dont 50% proviennent du transport des phosphates (8,7 millions de tonnes de
phosphates).

Le chiffre d’affaires (CA) réalisé en 2023 est de 4.353 MDH (4.905 MDH en consolidé), en
amélioration de 7% par rapport à 2022 sous l’effet notamment de la bonne performance de
l'activité « voyageurs » (+15%). L'activité marchandises a enregistré un chiffre d'affaires en
légère amélioration (+1%) et les recettes des phosphates ont connu une baisse de 25% en
volume et de 17% en valeur par rapport à 2022.

Les investissements réalisés, à fin 2023, sont de l'ordre de 1.133 MDH, représentant 43% du
budget (2.617 MDH). Ce taux s'explique par le décalage du programme d'acquisition du
matériel roulant sous l'effet de la perturbation des chaînes d'approvisionnement à
l'international.

A fin juin 2024, l'ONCF a réalisé un chiffre d’affaires de 2.178 MDH (2.557 MDH en consolidé),
soit une hausse de 12% par rapport à juin 2023 (+16% en consolidé), alors que les prévisions de
clôture de 2024 tablent sur un CA de 4.694 MDH (5.628 MDH en consolidé) en hausse de 8%
par rapport à 2023 (+15% en consolidé) tirée, principalement, par la hausse prévisionnelle des
revenus de transport des voyageurs.

Les investissements réalisés à fin juin 2024 ont atteint 811 MDH, soit Un taux de réalisation de
21%. Les prévisions de clôture de 2024 sont de 1.243 MDH représentant 33% des prévisions

annuelles (3.808 MDH).



L’endettement à fin 2023, de l’ordre de 42.500 MDH, a enregistré une légère baisse de 2% en
relation avec la variation favorable des cours de change en 2023. Les prévisions de clôture de
2024 prévoient une légère hausse de 0,3% pour atteindre 42.638 MDH.

Les prévisions triennales consacrent une évolution soutenue du chiffre d’affaires devant
atteindre 5.133 MDH en 2025, 5.553 MDH en 2026 et 6.051 MDH en 2027.

Les prévisions du programme d'investissement de l'ONCF pour la période 2025-2027 s’élèvent
à 9.783 MDH (2.969 MDH en 2025, 3.640 MDH en 2026 et 3.174 MDH en 2027).
Ce programme sera dédié, principalement, à l’acquisition du nouveau matériel roulant, la
construction des ateliers d'entretien et la maintenance des infrastructures.

Ce programme ne tient pas compte du plan de développement ferroviaire à engager dans le
cadre de la préparation à l'organisation de la Coupe du monde 2030 pour un coût estimé à
87 MMDH et intégrant plusieurs composantes notamment l'extension de la LGV de Kénitra
vers Marrakech et le développement d’un Réseau Express Régional (RER) au niveau des
agalomérations de Casablanca, de Rabat et de Marrakech.

A ce sujet, les concertations seront accélérées en vue de mettre en place un contrat-
programme Etat-ONCF devant asseoir et définir les composantes de ce plan de
développement et son montage de financement.

CHIFFRE D'AFFAIRES - GROUPE ONCF (MDH) RESULTATS - GROUPE ONCF (MDH)
5.628 2021 2022 2023 2024*
4.592 3905 [
3.964
-291
-503 Œ
-1.074 #La0 _1.240
-1.596
-2,543
© RESULTAT NET æ RESULTAT D'EXPLOITATION
2021 2022 2023 2024*
(*) Probabilités de clôture (*) Probabilités de clôture

1.1.3. Transport aérien
L1.3.1. Royal Air Maroc

En 2023, le Groupe Royal Air Maroc a atteint des résultats financiers remarquables,
enregistrant le plus haut résultat net de la dernière décennie, avec une marge nette de 2,2%.
Cette performance a été soutenue par une hausse significative de 57% du chiffre d'affaires par
rapport à 2022, largement stimulée par une forte demande de voyages et favorisée par la
levée des restrictions de déplacement imposées jusqu'en 2021 en raison de la pandémie.

Ainsi, la Compagnie a transporté près de 7,2 millions de passagers et retrouve 96% du niveau
de trafic pré-pandémie et ce, malgré une taille de la flotte réduite de 10% par rapport à 2019,
en soulignant que les performances réalisées en 2023 sont en hausse par rapport au niveau de
2022 en trafic et en offre de 42% et 32% respectivement.

Le coefficient de remplissage a atteint un niveau record de 77%, en hausse par rapport à 2022
de 5 points, ce qui a permis de mieux rentabiliser les vols.

A



RAPPORT SUR LES ETABLISSEMENTS ET ENTREPRISES PUBLICS

Ainsi, la RAM a réalisé en 2023, un chiffre d’affaires de 19.707 MDH (19.567 MDH en consolidé),
en amélioration de 57% par rapport à 2022 (+52% en consolidé). Le résultat net, quant à lui,
s‘est établi à 442 MDH (1.385 MDH en consolidé) en amélioration de 122% par rapport à 2022
(+191% en consolidé).

En 2023, la RAM a réalisé des investissements s'élevant à 1.110 MDH, marquant une hausse de
198% par rapport à 2022, correspondant principalement aux acomptes payés à hauteur de
100 millions de dollars pour l'acquisition de deux avions.

L'endettement de la RAM, établi à 7.860 MDH à fin 2023 (7.531 MDH en consolidé), a diminué
dc 12% par rapport à 2022 (-14% en consolidé).

A fin avril 2024, la Compagnie a transporté près de 3,3 millions de passagers, en évolution de
2,7% par rapport à la même période de l'année 2023, avec un coefficient de remplissage de
76%.

Par ailleurs, le chiffre d’affaires à fin avril 2024 (8.807 MDH) a augmenté de 5% par rapport
aux réalisations de la même période de 2023. Le résultat net, quant à lui, s'est établi à
- 541 MDH contre -907 MDH réalisée pour la même période de 2023.

En termes de prévisions de clôture de 2024, le chiffre d'affaires est estimé à 19.864 MDH
corrélé à une augmentation de 4,5% du trafic aérien par rapport à 2023 et devant atteindre
7,5 millions de passagers.

Les perspectives de la Compagnie sont prometteuses, renforcées par la signature en 2023
d'un contrat-programme mettant en place une feuille de route pour le développement de
l'activité de la RAM. Ce plan prévoit l'expansion de la flotte de Royal Air Maroc de 50 à
200 avions d’ici 2037, l'ouverture de plus de 100 nouvelles destinations internationales et
46 lignes domestiques, ainsi que la diversification des sources de croissance et de revenus.
L'objectif est d'atteindre Un chiffre d'affaires de 94 MMDH et de transporter 31,6 millions de
passagers, avec un taux de remplissage de 82%.

Ce nouveau plan de développement permettra de repositionner la RAM en tant qu'acteur
incontournable, leader du transport aérien africain, aux ambitions internationales, pour
accompagner le Royaume dans sa stratégie de développement touristique ainsi que pour
accueillir la Coupe du monde 2030.

CHIFFRE D'AFFAIRES - GROUPE RAM (MDH)

19.567
12.899

6.363

2021 2022 2023

RESULTATS - GROUPE RAM (MDH)

2,178

1.385
Œ -858

-1.,527

P

2021 2022 2023

© RESULTAT NET H RESULTAT D'EXPLOITATION

A



1.1.3.2. Office National des Aéroports

Le trafic aérien a atteint un niveau record inégalé, de 27,1 millions de passagers en 2023,
surpassant de 8% les chiffres d'avant la crise sanitaire et en hausse de 31,55% par rapport à
l'année 2022 et de 5,4% par rapport aux prévisions budgétaires de 2023. L'évolution du trafic
entre 2019 et 2023 se présente comme suit :

Mouvements des passagers (en milliers)
27.091
25 076
20 592
9989
7150 -
2019 2020 2021 2022 2023

Ainsi, le chiffre d’affaires de 2023 s’élève à 4.710 MDH en hausse de 21,6% par rapport à 2022
et de 4,4% par rapport aux prévisions de 2023, alors que le résultat net est passé de 323 MDH
en 2022 à 1.066 MDH en 2023 (+230%), avec une marge nette de 23%.

Les investissements réalisés en 2023 s’élèvent à 1.400 MDH contre des prévisions
budgétaires de 2.384 MDH, soit un taux de réalisation de 59%.

À fin 2023, l'endettement de l'ONDA s'élevait à 7.305 MDH, enregistrant une baisse de 8% par
rapport à 2022. Les prévisions de clôture de 2024 indiquent une diminution supplémentaire
de 11% des dettes de financement devant s’établir à 6.521 MDH.

Pour l'exercice 2024, le trafic aérien devrait atteindre 30,1 millions de passagers, en hausse
de 11% par rapport aux réalisations de 2023. Le résultat net devrait se situer à 722 MDH et le
montant des investissements atteindrait 1.775 MDH.

Le programme d'investissement est évalué à un montant de 12,3 MMDH pour la période 2025-
2027 et sera dédié, en grande partie, aux extensions des capacités des aéroports de
Mohammed V, de Rabat-Salé, de Marrakech, d'Agadir, de Tétouan, de Tanger, de Fès et d'AI
Hoceima. Ce programme permettra également de soutenir la croissance du secteur touristique
et le plan de développement de la RAM.

En termes de perspectives du secteur aéroportuaire, il est envisagé de procéder à la mise en
place d'un nouveau modèle institutionnel et organisationnel visant notamment la
transformation de l’Office en société anonyme dans l’objectif de renforcer son autonomie de
gestion, de créer les conditions favorables à l’accélération du développement du secteur
aéroportuaire par son ouverture au privé et ce, à travers la filialisation des activités
commerciales et la mise en œuvre des opérations de partenariat.

M



RAPPORT SUR LES ETABLISSEMENTS ET ENTREPRISES PUBLICS

CHIFFRE D'AFFAIRES - ONDA (MDH) RESULTATS - ONDA (MDH)
5.178 T00 1.454
4.710 S 1.066,
= äîza û 9
2423 !?
-644
-996
2021 2022 2023 2024*
2021 2022 2023 2024* EIRESULTAT NET E RESULTAT D'EXPLOITATION
(*) Probabilités de clôture (*) Probabilités de clôture

LT1.4. Déplacements urbains
L1.4.1. Société Casa Transports

La Société Casa Transports prévoit la réalisation de plusieurs lignes de tramway et de Bus à
Haut Niveau de Service (BHNS) et ce, dans la perspective d’assurer une offre de transport, des
solutions adaptées et des services innovants afin de fluidifier la mobilité au sein de Casablanca.

Le linéaire total des lignes de tramway en exploitation a atteint 48 Km à fin 2023, en soulignant
que les lignes de BHNS L5 et L6 mises en service le 01/03/2024, viennent compléter l’offre de
transport public de la capitale économique et s'intègrent dans l’offre de transport en commun
en site propre programmée dans le cadre du Plan de Développement du Grand Casablanca.

De même, la société a procédé à la mise en service, en septembre 2024, des lignes T3 et T4
du tramway.

L'année 2023 a été marquée par une reprise progressive de l’activité. Ainsi, le chiffre d’affaires
de cet exercice s’est établi à 250 MDH contre 263 MDH en 2022 G5%) et le résultat net à
-123 MDH contre -346 MDH enregistré au titre de l'exercice précédent. Le programme
d'investissement réalisé en 2023 a atteint 1.652 MDH.

A fin juin 2024, les réalisations d'investissement s'établissent à 1.176 MDH avec des prévisions
de clôture estimées à 2.157 MDH, Le chiffre d'affaires réalisé, à fin juin 2024, s'est établi à
144 MDH. Les prévisions de clôture de l’exercice tablent sur un montant de 370 MDH.

Le programme d'investissement prévisionnel au titre de la période 2025-2027 portera sur une
enveloppe totale de 1.021 MDH dont 828 MDH pour 2025, 102 MDH pour 2026 et 91 MDH
pour 2027.

1.1.4.2. Société Rabat Région Mobilité

La Société Rabat Région Mobilité (RRM) est chargée de la conception, de la réalisation et de
l'exploitation du tramway de la conurbation Rabat-Salé-Témara.

À la suite de sa transformation institutionnelle, la Société a élargi son champ d'action au-delà
du tramway, intégrant ainsi divers autres domaines de la mobilité urbaine, Elle est désormais
habilitée à mettre en œuvre et gérer toutes les activités liées au transport public urbain, ainsi
que d'autres services publics complémentaires à caractère commercial ou industriel,

nécessaires pour une meilleure gestion de la mobilité dans sa zone d'intervention.



En 2023, le réseau du tramway de Rabat a enregistré une fréquentation annuelle de 41 millions
de voyages, marquant une hausse de 9,55% par rapport à 2022. Le chiffre d'affaires pour
'année 2023 s'est établi à 154,7 MDH, restant quasiment stable par rapport à 2022
(154,4 MDH), avec une progression de 11% des ventes de titres de transport, atteignant
141,8 MDH,

Le résultat net a connu, quant à lui, une dégradation en passant de -4 MDH en 2022 à -36
MDH en 2023, en soulignant que la société a finalisé en 2023 une opération de maintenance
lourde des 19 rames doubles de 65 mètres linéaires, après 600.000 km de service.

L'endettement de la société s’est établi à 2.035 MDH en 2023 en baisse de 9% par rapport à
2022.

En termes de prévisions de clôture de 2024, la société prévoit de réaliser un chiffre d'affaires
de 177 MDH, soit une augmentation de 14% par rapport à 2023 et un programme
d'investissement 32 MDH.

RRM prévoit des investissements estimés à 3.989 MDH au titre de la période 2025-2027,
réparti comme suit : 842 MDH pour 2025, 1.5594 MDH pour 2026 et 1.553 MDH pour 2027,
avec le lancement de chantiers structurants liés au développement du réseau de Transports
Collectifs en Site Propre (TCSP), au renforcement de l’offre bus et à la mise à niveau des
parkings sous gestion de la société.

12. Secteur Portuaire
L2.1. Agence Nationale des Ports

En 2023, le volume global de trafic réalisé a atteint 88,4 millions de tonnes, marquant une
légère hausse de 1,4% par rapport à l'année précédente (87,2 millions de tonnes). L'activité
s’est concentrée principalement autour des ports de l'axe Mohammedia - Casablanca - Jorf
Lasfar qui ont assuré le transit d’environ 75,3% du trafic global des 10 ports gérés par l'ANP.

Le chiffre d'affaires de 2023 s’élève à 2.512 MDH (2.770 MDH en consolidé), enregistrant une
hausse de 20% par rapport à 2022 (+19,6% en consolidé). Le résultat net a également
progressé, passant de 47,1 MDH en 2022 à 105,2 MDH en 2023, soit une hausse de 123%.
Le résultat net consolidé a atteint 164 MDH à fin 2023, en hausse de 184 MDH par rapport à
l'année précédente.

Les dettes de financement du Groupe ANP se sont réduites de 6% par rapport à 2022, s'élevant
à 6.869 MDH à fin 2023.

Au premier semestre 2024, le volume global du trafic traité a atteint 48 millions de tonnes,
en hausse de 17,3% par rapport à la même période de 2023 et le chiffre d'affaires s'est établi à
1.368 MDH (1.472 MDH en consolidé), en hausse de 17,1% par rapport à 2023 (+16,5% en
consolidé).

Les investissements réalisés par l'ANP au premier semestre 2024 ont atteint 176 MDH
(195 MDH en consolidé), en baisse de 18% par rapport à la même période de 2023 (-20% en
consolidé).

Les prévisions de clôture pour 2024 prévoient un trafic d'environ 89,2 millions de tonnes (+1%
par rapport à 2023), un chiffre d'affaires de 2.573 MDH, en hausse de 2% par rapport à 2023

VN



RAPPORT SUR LES ETABLISSEMENTS ET ENTREPRISES PUBLICS

et Un résultat net prévisionnel de 137,4 MDH, en augmentation de 31%. Le programme
d'investissement devrait être réalisé à hauteur de 978 MDH, soit un taux de réalisation de 74%
des prévisions budgétaires.

Le plan pluriannuel d'investissement de l'ANP pour la période 2025-2027 prévoit une
enveloppe globale de 1.873 MDH, dont 745 MDH pour 2025, 562 MDH pour 2C26 et 566 MDH
pour 2027. Ce plan inclut des projets structurants notamment le renforcement des digues de
protection pour sécuriser les zones côtières contre les risques d'érosion et d’'inondation,
garantissant ainsi la protection des installations portuaires et des communautés riveraines.

En tormes de perspectives, l'ANP à initié une étude pour sa transformation en société anonyme
(SA) et la consolidation de son modèle, visant un repositionnement optimal de son activité et
la séparation des missions de régulation et d’exploitation commerciale.

CHIFFRE D'AFFAIRES - ANP (MDH) RESULTATS - ANP (MDH)
2,512 2.573 856 433
2,067 2092
186
ds 187
46 m 7
— p =
2021 2022 2023 2024* 2021 2022 2023 2024*
E RESULTAT NET MRESULTAT D'EXPLOITATION
(*) Probabilités de clôture (*) Probabilités de clôture

L2.2. Agence Spéciale Tanger Med

En 2023, le commerce maritime mondial a enregistré une croissance de 3%, atteignant
12,4 milliards de tonnes avec des perspectives favorables pour 2024 en dépit des tensions
géopolitiques.

Le complexe portuaire Tanger Med continue d'affirmer son [eadership en Méditerranée et en
Afrique, consolidant son rôle en tant que plateforme de référence pour les échanges
commerciaux nationaux. Premier port en Méditerranée et en Afrique, le Groupe TMSA s'appuie
sur le réseau de Marsa Maroc, composé de 24 terminaux à conteneurs et vracs répartis dans
10 ports à travers le pays.

Le Groupe TMSA est également un acteur clé dans l'aménagement de plus de 3.000 hectares
de zones d'activités économiques, abritant plus de 1.300 entreprises générant un chiffre
d'affaires de 155 MMDH (+16,5% par rapport à 2022), dans des secteurs stratégiques tels que
l’'automobile, l'aéronautique, le textile, l’agro-alimentaire et la logistique,

En 2023, le port Tanger Med a traité 122,44 millions de tonnes de marchandises (+13,6% par
rapport à 2022) et 8,62 millions d'Equivalent Vingt Pieds (EVP) (+13,4% par rapport à 2022),
atteignant plus de 95% de sa capacité nominale, avec des résultats en avance de quatre ans
sur les objectifs fixés.

Le secteur passagers a également connu une reprise significative, avec 2,7 millions de
passagers accueillis en 2023, soit une augmentation de 30% par rapport à 2022, retrouvant

ainsi les niveaux d’avant la pandémie.



En parallèle, la plateforme industrielle de Tanger Med a attiré un investissement total de
6,15 MMDH, créant 14.500 nouveaux emplois. Le développement des zones d'activités s'est
renforcé avec l‘installation de 85 nouvelles entreprises, représentant un investissement privé
de 2,35 MMDH et générant 9.439 nouveaux emplois.

Le Groupe Tanger Med a réalisé un chiffre d'affaires de 8.944 MDH en 2023, principalement
porté par le pôle portuaire et logistique à hauteur de 7.969 MDH, soit une hausse de 12% par
rapport à 2022 (8.017 MDH). Le résultat net consolidé de 2023 s'élève à 2.190 MDH,
enregistrant une augmentation de 55% par rapport à 2022 (1.416 MDH).

Les investissements du Groupe en 2023 se sont chiffrés à 1.493 MDH, soit une baisse de 49%
par rapport à 2022 (2.943 MDH). Les dettes de financement se sont établies à 18.933 MDH,
en baisse de 4% par rapport à 2022.

Au premier semestre 2024, les investissements réalisés ont atteint 388 MDH, avec des
prévisions de clôture estimées à 3.608 MDH. Le chiffre d’affaires réalisé au premier semestre
2024 s'élève à 4.959 MDH, en hausse de 21% par rapport à la même période de l’exercice
précédent, avec des prévisions de clôture estimées à 9.291 MDH.

Les projections pour la période 2025-2027 prévoient un chiffre d'affaires de 9.795 MDH,
10.223 MDH et 10.832 MDH respectivement en 2025, 2026 et 2027. Les investissements
prévus s'élèvent à 2.204 MDH pour 2025, 3.086 MDH pour 2026 et 1.188 MDH pour 2027,
avec des projets structurants portant notamment sur l'extension du port de Tanger Med
Passagers et l'aménagement des zones industrielles.

CHIFFRE D'AFFAIRES - GROUPE TMSA (MDH) RESULTATS - GROUPE TMSA (MDH)
8.94 29.291 262
cr 8.017 3584 û
E 2.994
2.525 Ss 2.377

1.451 1.416

2021 2022 2023 2024* 2021 2022 2023 2024*

E RESULTAT NET = RESULTAT D'EXPLOITATION

(*) Probabilités de clôture (*) Probabilités de clôture

12.3.  Nador West Med

En 2023, NWM a poursuivi la réalisation des travaux d'infrastructures portuaires, atteignant un
taux de réalisation de 95%. La finalisation de ces travaux ainsi que le lancement des
superstructures du port sont prévus pour le deuxième semestre 2024.

Durant l'année 2023, deux conventions spécifiques ont été signées avec les partenaires
concernés pour financer l'approvisionnement du port en eau potable et en électricité.

NWM a réalisé, cn 2023, un résultat net positif à hauteur dc 153 MDH contre un déficit de
229 MDH enregistré en 2022.

L'endettement total s'est élevé à 4.763 MDH en 2023, avec des prévisions de clôture de 2024
estimées à 7.075 MDH, en hausse de 48,5% par rapport à 2023.

yN



RAPPORT SUR LES ETABLISSEMENTS ET ENTREPRISES PUBLICS

NWM a investi 1366 MDH en 2023, soit un taux de réalisation de 49% par rapport aux
prévisions budgétaires arrêtées à 2.760 MDH, Pour 2024, les investissements prévisionnels
s’élèvent à 2.772 MDH, en hausse de 103% par rapport à 2023, avec 478 MDH réalisés à fin
juin 2024. Les prévisions pour 2025-2026 s’élèvent à 975 MDH, dont 826 MDH pour 2025 et
149 MDH pour 2026.

Concernant la connectivité du port, le financement de l’autoroute Nador-Guercif a été mobilisé
grâce à des prêts de la BAD et de la BID, avec une mise en service prévue pour 2027. Pour la
liaison ferroviaire, les études techniques sont achevées et le montage de financement est en
cours de négociation.

Pour la composante « zones d’activité », une première phase de 800 hectares sera mise en
service en même temps que le port. Une filiale, créée en 2023, sera chargée du développement,
de l’aménagement, de la gestion et de la commercialisation de cette zone, pour un coût
prévisionnel de 2,5 MMDH Chors coût du foncier).

II. MISE EN ŒUVRE DES STRATEGIES SECTORIELLES
H.T. Agriculture

Depuis le lancement du Plan Maroc Vert, le secteur a bénéficié d'une amélioration substantielle,
avec une croissance annuelle nettement supérieure à celle du PIB national.

Toutefois, la dynamique de croissance du secteur a ralenti sous l’effet du réchauffement
climatique et d'un stress hydrique prolongé.

Dans ce contexte et malgré une augmentation de 9% du cumul pluviométrique lors de la
campagne 2023-2024 par rapport à la campagne précédente, une baisse a été constatée dans
la récolte des principales céréales (31,2 millions de quintaux en baisse de 43%) et ce, en raison
d'une séquence climatique de six années très difficiles et une répartition temporelle des
précipitations caractérisée par un retard des pluies entrainant une sécheresse longue au début
de la campagne affectant négativement le semis des cultures d'automne.

Dans ce cadre, la stratégie « Génération Green 2020-2030 », lancée en février 2020 suite aux
Hautes Orientations Royales, vise la consolidation des acquis du Plan Maroc Vert en
répondant aux nouveaux défis du secteur. À cet effet, la stratégie repose sur deux fondements
prioritaires :

- Le premier fondement accorde la priorité à l’élément humain à travers la
contribution à l'émergence d'une nouvelle génération de classe moyenne agricole, la
création d'une nouvelle génération de jeunes entrepreneurs par la mobilisation et la
valorisation des terres collectives et ce, en s'appuyant sur une nouvelle génération de
mécanismes d'accompagnement par le recours aux plateformes de services digitaux ;

- Le deuxième fondement tient à la pérennisation de la dynamique de
développement agricole par la consolidation des filières agricoles, la modernisation
des circuits de distribution des produits agricoles et l'instauration d'uUne agriculture plus
résiliente et éco-efficiente, à travers le doublement de l'efficacité hydrique,
la conservation des sols agricoles et l’'accompagnement des agriculteurs dans la

transition vers les énergies renouvelables.



Ainsi, en vue de la relance de la dynamique de la production agricole et de la réussite des
objectifs de la stratégie « Génération Green », Sa Majesté le Roi Mohammed VI, que Dieu
L'assiste, a appelé, lors du Discours Royal à l'occasion de la Fête du Trône du 29 juillet 2024,
à la mise à jour continue des leviers de la politique nationale de l'eau et à la définition d'un
objectif stratégique, quelles que soient les circonstances : garantir l’eau potable à tous les
citoyens et couvrir 80% au moins des besoins d’irrigation sur tout le territoire national.

De même, Sa Majesté le Roi Mohammed VI, que Dieu L'’assiste, a donné Ses Hautes
Instructions en vue de la mise en œuvre optimale des différentes composantes du Programme
National pour l'Approvisionnement en Eau Potable et l’Irrigation 2020-2027 (PNAEPI.

Les EEP relevant du Département de l'Agriculture contribuent à la mise en œuvre de cette
stratégie notamment : les ORMVA, l'ADA, l'INRA, l'ONSSA, Biopharma, le LOARC, l'EACCE
(Morocco FoodEx), l'ANDZOA, l'ONCA, la SONACOS, l'ONICL, etc,

H.1.1.  Agence pour le Développement Agricole

L'ADA joue un rôle central dans la coordination, la planification et le suivi des projets
d'agriculture solidaire, ainsi que dans la promotion de l'investissement agricole à travers les
Partenariats Public-Privé (PPP). L'Agence soutient également le développement de la
commercialisation des produits du terroir et encourage l'entrepreneuriat des jeunes dans le
secteur agricole.

En 2023, l'ADA a réalisé des projets importants notamment des PPP sur 121.331 ha de terres
agricoles répartis sur 1.680 projets, avec un investissement prévisionnel de 23 MMDH et la
création de 67.000 emplois permanents.

Ces projets incluent également la valorisation des terres collectives agricoles, avec des
contributions importantes à la finalisation des décrets relatifs aux aides financières pour les
membres des collectivités ethniques et les jeunes.

Le programme d'agrégation agricole de nouvelle génération a progressé avec l'approbation
de 31 projets et l'attestation de 78 projets, représentant un investissement prévisionnel de
13 MMDH.

En 2023, l'ADA a structuré son offre d'appui à l'entrepreneuriat, mis en service une plateforme
digitale dédiée et a lancé la deuxième édition du concours national AGRIYOUNG INNOVATE.
La plateforme a permis l'examen de 6.875 idées de projets, avec 813 approuvées. Les projets
de valorisation des terres collectives ont couvert 4.600 ha et 29 projets d'agriculture solidaire
pour un investissement de 584 MDH.

En termes de prévisions de clôture de 2024, le montant d'investissement prévu pour
157,53 MDH, sera réalisé à hauteur de 148 MDH.

Pour la période 2025-2027, l'ADA prévoit de continuer à soutenir la nouvelle stratégie agricole
« Génération Green » et de renforcer les actions de promotion des produits du terroir.
L'enveloppe budgétaire de l’Agence pour cette période est estimée à 436 MDH, répartie entre
le budget d'investissement (228 MDH) et le budget d'exploitation (208 MDH).

A



RAPPORT SUR LES ETABLISSEMENTS ET ENTREPRISES PUBI| s

IL1.2. Offices Régionaux de Mise en Valeur Agricole

En 2023, les ORMVA ont continué à déployer les actions prévues dans le cadre de la stratégie
Génération Green 2020-2030, en mettant en place des mesures pour atténuer l'impact du
déficit pluviométrique et des conditions climatiques défavorables, ainsi que la situation
critique liée aux niveaux de remplissage des barrages.

Les ORMVA ont poursuivi l'élargissement de la reconversion collective à l'irrigation localisée,
portant à 276.032 ha la superficie convertie, soit 41% du réseau d'irrigation. L'année 2023 a
également été marquée par la mise en œuvre du projet intégré d'agriculture solidaire et l’appui
aux jeunes promoteurs pour développer une classe moyenne d'agriculteurs.

Entermes d'assurance agricole, la couverture sociale a bénéficié à 416.439 agriculteurs (+6,4%
par rapport à 2022) et l’assurance climatique a été étendue à 254.349 ha, représentant 48%
de l'objectif fixé pour 2030.

Face aux conditions hydriques défavorables, certaines zones d'irrigation ont subi des
restrictions d'irrigation voire des suspensions dans cinq périmètres (Doukkala, Moulouya,
Haouz, Tafilalet et Ouarzazate).

Dans ce contexte, le volume d'eau lâché en 2023 s'élève à 938 Mm£, contre 851 Mm* en 2022
et 1.189 Mm: en 2021, pour une superficie irriguée de 377.917 ha, soit 56% du réseau d'irrigation.

Les investissements des ORMVA en 2023 ont atteint 2.475 MDH, en hausse de 13% par rapport
à 2022, représentant 80% des prévisions budgétaires (3.109 MDH), sans inclure le projet
d'interconnexion entre les bassins de Sebou et de Bouregreg, réalisé par l'ORMVA du Gharb.

A ce sujet, les ORMVA du Gharb (ORMVAG), des Doukkala (ORMVAD) et du Loukkos
(ORMVAL) ont été chargés de la réalisation des projets de transfert d'eau notamment entre
bassins hydrauliques. Les coûts des projets lancés par les trois Offices s'élèvent
respectivement à 6 MMDH, à 15 MMDH et à 840 MDH.

Ces projets permettront le transfert de volumes d’eau de l’ordre de 470 Mm: pour l'ORMVAG,
100 Mm* pour l’'ORMVAL et 60 Mmê pour l’ORMVAD. |l convient de souligner que le projet
d'interconnexion du bassin de Sebou au bassin du Bouregreg confié à l'ORMVAG a été achevé
avec une mise en service effectuée le 28/08/2023, ce qui a permis un lâché d'un volume d'eau
de 440 Mm* à fin septembre 2024. Quant aux projets portés par l'ORMVAD et l'ORMVAL, ils
enregistrent des taux de réalisation respectifs de l'ordre de 90% et 40%.

Concernant l'exercice 2024, les ORMVA ont réalisé à fin juin, des investissements atteignant
1.514 MDH, soit un taux de réalisation de 35%, avec des prévisions de clôture au titre de 2024
qui tablent sur un investissement à hauteur de 3.423 MDH, représentant 75% des prévisions
de l’exercice.

Pour la période 2025-2027, le programme d'investissement des ORMVA porte sur une
enveloppe globale de 11.230 MDH, répartie comme suit : 3.210 MDH en 2025, 3.510 MDH en
2026 et 4.510 MDH en 2027. Ce programme vise à poursuivre la réalisation du Programme
National d'Economie d'Eau d'Irrigation (PNEEI), des travaux d'aménagement hydro-agricole
ainsi que les projets inscrits dans le cadre de la stratégie « Génération Green 2020-2030 », tels
que l'agriculture solidaire, l’agrégation, la promotion de l’entrepreneuriat des jeunes et la

digitalisation des services agricoles.



IL1.3.  Agence Nationale de la Conservation Foncière, du Cadastre et de la Cartographie

Le plan de développement de l'ANCFCC pour la période 2022-2025 prévoit l'établissement de
plus de 2 millions de titres fonciers (dont un million de titres issus de l'Immatriculation Foncière
d'Ensemble (IFE}) et la couverture de 6 millions d'hectares supplémentaires du territoire
national par l'immatriculation foncière (y compris les biens de l’Etat et ses démembrements).

En termes de réalisations au titre de 2023, l'ANCFCC a produit 462.509 titres fonciers, dont
211.624 issus de l'immatriculation foncière dans le monde rural, en hausse de 5% par rapport à
2022 couvrant une superficie de 1609.234 Ha.

Le nombre de certificats délivrés a progressé de 8% pour atteindre 1,977.744 certificats.
Le nombre des inscriptions des droits réels sur les livres fonciers a, en revanche, accusé une
baisse de 4% se situant à 1,.000.564 inscriptions.

Au niveau des réalisations financières, le chiffre d’affaires de 2023 à connu une hausse de 5%,
soit 8.467 MDH contre 8.029 MDH en 2022, ce qui a permis une amélioration de la
contribution de l'Agence au BGE avec un montant de 4.000 MDH en 2022 et en 2023 contre
des prévisions initiales arrêtées, respectivement, en 2022 et 2023 à hauteur de 3.280 MDH et
3.500 MDH.

Le programme d'investissement de l'Agence prévu au titre de 2023 pour 3.012 MDH a
enregistré un taux de réalisation de 12% en raison du report de certains projets.

Les recettes réalisées, à fin juin 2024, sont établies à 4.293 MDH, en légère hausse de 3% par
rapport à la même période de l’exercice précédent alors que les prévisions de clôture tablent
sur un montant de 8.800 MDH.

Sur des crédits prévisionnels de 3.479 MDH, les engagements concernant le programme
d'investissement s'élèvent, à fin juin 2024, à 2.782 MDH, soit un taux de réalisation de 80%,
Les prévisions de clôture seraïent de 3.067 MDH, soit 88% des prévisions budgétaires.

Les recettes prévisionnelles seraient de 9.000 MDH/an sur la période 2025-2026
et 9.500 MDH en 2027.

Le programme d'investissement de l’Agence est estimé à une enveloppe globale de
10.630 MDH sur la période 2025-2027. Ce programme est ventilé comme suit : 3.644 MDH en
2025, 3.550 MDH en 2026 et 3.436 MDH en 2027.

Les principaux chantiers de l’'Agence au titre de 2025 portent sur l’établissement de
546.000 titres fonciers, la couverture par l'immatriculation d'une superficie de 12 million
d'hectares, la délivrance de 2,2 millions certificats de propriété, l'inscription sur les livres
fonciers de 1,2 million de formalités et la poursuite de la généralisation de l'immatriculation
foncière à travers son ouverture à 35 communes rurales outre la consolidation des acquis en
matière de dématérialisation.

A



RAPPORT SUR LES ETABLISSEMENTS ET ENTREPRISES PUBLICS

CHIFFRE D'AFFAIRES - ANCFCC (MDH) RESULTATS - ANCFCC (MDH)
8800 1.417
8467 es
sn
732
8.091 82.029 l v 5g9 631 58s
2021 2022 2023 2024* 2021 2022 2023 2024*
RESULTAT NET # RESULTAT D'EXPLOITATION
(*) Probabilités de clôture (*) Probabilités de clôture

H.1.4. Agence Nationale pour le Développement des Zones Oasiennes et de l’Arganier

La stratégie de développement, à l'horizon 2030, des zones oasiennes et de l'arganier (ZOA)
vise à accélérer leur développement en se basant sur trois principaux axes : i/ accroître la
résilience des territoires et des écosystèmes face au changement climatique, ii/ mettre l'accent
sur l’amélioration du bien-être social des populations rurales et urbaines et iii/ internationaliser
l'économie de la zone, en ciblant particulièrement les secteurs à forte valeur ajoutée pour
renforcer la compétitivité.

Le Programme Global Intégré de Développement des Zones Oasiennes et de l’Arganier (PGID-
ZOA) repose sur plusieurs composantes stratégiques complémentaires, tenant notamment
aux impacts environnementaux et climatiques, à l'amélioration des équipements publics
comme l'éducation et la santé, au développement durable des petits centres urbains, à la
connectivité routière, ainsi qu'à l'amélioration des conditions de vie des populations.

Le coût du PGID-ZOA s'élève à 157 MMDH, répartis sur 1.818 projets. La mise en œuvre de ce
programme est financée à hauteur de 63 MMDH par l’Etat. Le reste, soit près de 92,6 MMDH,
sera mobilisé, en grande partie, auprès des partenaires nationaux et internationaux.

A fin 2023, les investissements dans les zones oasiennes et de l’arganier ont atteint
12,23 MMDH, dont 1156 MMDH financés par les Départements ministériels et organismes
publics, 553,28 MDH par l'ANDZOA et 111,3 MDH par la coopération internationale.

L'exécution du budget d'investissement alloué à l'ANDZOA au 30/06/2024 montre un taux
d'engagement de 88,47% par rapport au total des crédits de 244,23 MDH et un taux de
paiement de 31,41% par rapport au total des engagements de 216,08 MDH.

Pour la période 2024-2027, l'ANDZOA projette de mobiliser une enveloppe globale de
2,28 MMDH et qui porte sur des projets de partenariat et d’autres soumis aux différents
bailleurs de fonds internationaux.

H1.2. Mines, Energie et Eau
11.2.1. Secteur des Phosphates

En 2023, dans le cadre de son programme d'investissement vert, |le Groupe OCP a mis en
service deux nouvelles usines de dessalement à Jorf Lasfar et Benguerir, atteignant
l'autosuffisance en eau non conventionnelle à Jorf Lasfar et initiant l'approvisionnement en

eau potable des villes de Safi et El Jadiga.



L'année 2023 a également été marquée par le lancement d’‘une 3°" émission d'obligations
subordonnées perpétuelles de 5 MMDH, la souscription d’un prêt vert de 100 M€ auprès de la
SFI pour la construction de 4 centrales solaires et l'attribution par Moody's d’une notation
inaugurale Investment grade « BAA3 », soulignant la position de leader du Groupe dans le
secteur des engrais phosphatés.

Le chiffre d'affaires du Groupe s’est établi à 91.277 MDH en 2023, en baisse de 20% par rapport
à 2022, principalement en raison de la baisse des prix de vente, malgré des prix d'intrants
relativement stables par rapport à 2021. Le résultat net a reculé de 49% pour atteindre
14.369 MDH.

Le programme d’investissement de 2023 a été réalisé à hauteur de 27.400 MDH, marquant
une hausse de 37% par rapport à l’année précédente, tandis que les dettes de financement ont
légèrement augmenté de 2% pour atteindre 61.235 MDH (hors dettes financières courantes).

À fin juin 2024, le chiffre d’affaires a augmenté de 15% par rapport à la même période de 2023,
atteignant 43.248 MDH, tandis que les dépenses d’investissement ont bondi de 64% pour
s’établir à 19.753 MDH.

Les prévisions de clôture au titre de 2024 tablent sur un chiffre d’affaires de 102.648 MDH, en
hausse de 12% par rapport à 2023, un résultat net de 16.505 MDH en augmentation de 15% et
des réalisations en matière d'investissement estimées à 44.800 MDH (+64%),

Pour la période 2025-2027, le Groupe OCP prévoit un investissement total de 139.156 MDH,
réparti comme suit : 45.000 MDH en 2025, 52.000 MDH en 2026 et 42.156 MDH pour 2027.

CHIFFRE D'AFFAIRES - GROUPE OCP (MDH) RESULTATS - GROUPE OCP (MDH)
114.574 40.382
102.648
84.300 1127 28.18
" 23.250
18.866
l Ë 14.369 16.505
2021 2022 2023 2024* 2021 2022 2023 2024*
EIRESULTAT NET m RESULTAT D'EXPLOITATION
(*) Probabilités de clôture (*) Probabilités de clôture

H.2.2. Hydrocarbures et Mines

En 2023, l'ONHYM a continué à mettre en œuvre la stratégie de recherche des hydrocarbures
et minière, axée sur l’augmentation de la production et le développement de l'emploi. Ainsi, 13
sociétés collaborent avec l‘Office dans la recherche d'hydrocarbures sur une superficie totale
de 230.523 km* couvrant 28 permis onshore et 46 permis offshore. De même, l'Office porte
37 projets de recherche minière, dont 14 projets de métaux de base et précieux et 3 dédiés
aux roches et minéraux industriels.

En 2024 et concernant l'activité Midstream, l'ONHYM a réalisé plusieurs missions stratégiques
dans le domaine du transport et du stockage de gaz naturel et d'hydrocarbures liquides,
incluant le projet du Gazoduc Nigéria-Maroc, où des avancées ont été enregistrées dans la

yN



RAPPORT SUR LES ETABLISSEMENTS ET ENTREPRISES PUBI| s

finalisation et l'optimisation du tracé maritime et terrestre et la préparation de la phase des
appels d’offres pour la construction du Gazoduc. Aussi, les travaux de validation de l'Accord
Intergouvernemental (IGA) et de l’Accord Pays Hôte (HGA) lancés à la fin du mois d’août 2024
constituent une avancée décisive pour les perspectives de ce projet stratégique.

Le chiffre d'affaires de l'ONHYM pour 2023 s'élève à 493 MDH, marquant une hausse de 51%
par rapport à 2022. Cette performance est largement attribuable aux prestations de transport
de gaz naturel via le GME au profit de l'ONEE, suite à la mise en place du reverse flow depuis
l'Espagne. Le résultat net pour 2023 s'élève à 188 MDH, en baisse de 45% par rapport à 2022.

En termes de prévisions de clôture 2024, l'ONHYM prévoit un chiffre d'affaires de 482 MDH,
en recul de 2% par rapport à 2023, avec un résultat net estimé à 142 MDH (-24%) et des
investissements de 200 MDH.

Ces investissements concernent, principalement, le projet gazier de Tendrara, la maintenance
du GME, la réalisation du premier tronçon Kenitra-Mohammedia du Gazoduc Dorsale
Atlantique ainsi que les études du projet Gazoduc Nigéria-Maroc.

Le programme d'investissement de l'ONHYM sur la période 2025-2027 porte sur une
enveloppe globale de l’ordre de 900 MDH, dédiée, principalement, aux activités Midstream
(223 MDH), à la production des hydrocarbures (141 MDH), à l’exploration pétrolière
(108,5 MDH) et à l'exploration minière (76 MDH).

11.2.3. Energies Renouvelables

Le programme de développement des Energies Renouvelables (EnR), qui fait l’objet d'un suivi
particulier par Sa Majesté le Roi Mohammed VI, que Dieu L'’assiste, constitue une
composante principale de la stratégie de transition énergétique et contribue à la réduction de
la dépendance énergétique devant passer de 97% en 2018 à 82% en 2030.

Pour atteindre ces objectifs, des orientations ont été données pour relever la part des énergies
renouvelables dans le mix électrique de 42% en 2020 à 52% à l’'horizon 2030, correspondant
à une capacité additionnelle de production d'’électricité de sources renouvelables de
10.000 MW répartie entre le solaire (4.5500 MW), l'éolien (4.200 MW) et l'hydro-électricité
(1.300 MW).

Par ailleurs, MASEN a vu ses missions élargies par la Circulaire du Chef du Gouvernement
n° 3/2024 du 11 mars 2024 relative à l'Offre Maroc pour le développement de la filière de
l'hydrogène vert qui a désigné MASEN comme point focal auprès des investisseurs potentiels
et membre du Comité de Pilotage et du Comité d'Investissement institués pour la gouvernance
de ladite filière.

En termes de réalisation du programme de développement des EnR, la capacité installée en
EnR à fin 2023 est de 4.607 MW, soit plus de 41% du mix électrique national, contre un objectif
initial de 42% en 2020, en soulignant que compte tenu du programme en cours d'exécution,
la part des EnR dans le mix électrique en 2027 atteindrait 56%, ce qui dépasserait l'objectif
arrêté pour 2030 à 52%.

La capacité installée en EnR susvisée de 4.607 MW se compose à hauteur 827 MW en projets
solaires, 2010 MW en projets éoliens et 1.770 MW en projets hydroélectriques.

A



En 2023, deux projets ont été mis en exploitation, totalisant 500 MW, à savoir Nassim
Boujdour de 300 MW et Aftissat 2 de 200 MW, réalisés par le secteur privé.

Les prévisions de clôture de 2024 prévoient une capacité additionnelle de 370 MW en éolien,
comprenant les projets de Repowering de Koudia Al Baida (100 MW) et de Jbel Lahdid
(270 MW). Par conséquent, la capacité totale en énergies renouvelables (EnR) devrait
atteindre 4.977 MW à fin 2024, représentant ainsi 45% du mix électrique national.

Le portefeuille de projets EnR que MASEN prévoit de réaliser entre 2023 et 2027 porte sur
une capacité additionnelle de 4.028 MW, outre une capacité de 333 MW à réaliser par le
secteur privé dans le cadre de la loi n° 13-09 relative aux énergies renouvelables.
Cette nouvelle capacité de 4.028 MW nécessitera un investissement de plus de 47 MMDH.

Sur le plan financier, MASEN a enregistré en 2023 un chiffre d'affaires de 1.608 MDH, en hausse
de 53% par rapport à 2022 et un résultat négatif de 446 MDH, en stagnation par rapport à
l'année précédente.

L'endettement de MASEN a reculé de 10% par rapport à 2022, s'établissant à 16.882 MDH à
fin 2023.

En termes de prévisions de clôture de 2024, MASEN prévoit un chiffre d'affaires de
2.798 MDH, en hausse de 74% par rapport à 2023 et un résultat net déficitaire de 1.032 MDH.
L'endettement s’établirait à 20.796 MDH, en hausse de 23%.

11.2.4, Secteur de l'Electricité et de l’Eau Potable
11.2.4.1. Office National de l'Electricité et de l'Eau potable

Dans le cadre du repositionnement stratégique de l'ONEE et de sa restructuration
institutionnelle, visant à réviser son modèle économique et financier et sa transformation en
société anonyme conformément à la loi-cadre n° 50-21 relative à la réforme des EEP, une étude
a été lancée en mars 2023,

Cette étude porte sur l’évaluation des options de repositionnement stratégique de l'Office
dans un contexte marqué par des mutations profondes du secteur de l'’énergie à l’échelle
nationale (transition énergétique, développement massif des EnR, l'ouverture accrue du
marché à la concurrence, la décarbonation, la mobilité électrique, l’'hydrogène vert...), outre les
impacts du stress hydrique prolongé exigeant un changement de paradigme en matière de
gestion de l'offre et de la demande de l’eau.

Malgré ce contexte, l'ONEE a réussi, avec le soutien des pouvoirs publics, à poursuivre ses
missions de service public. Les principales réalisations de l’Office font ressortir ce qui suit :

ONEE Branche Electricité (BE)

La puissance installée à fin 2023 a atteint 11.474 MW contre 11.055 MW à fin 2022, en hausse
de 3,79%.

Les ventes d’énergie électrique (en volume) pour l’année 2023 ont atteint 34.312 GWh contre
33.437 GWh cn 2022, soit unc évolution dc 2,6% en volume ct +4,3% cn valeur.

A fin 2023, l'énergie électrique totale appelée a atteint 43.991 GWh, contre 42.299 GWh en
2022, soit une augmentation de 4%.

A



RAPPORT SUR LES ETABLISSEMENTS ET ENTREPRISES PUBI| s

La production nationale, y compris /la production privée, s'est élevée, à fin 2023, à
42.409,3 GWh contre 41.420,4 GWh en 2022. Elle à permis de satisfaire 96,4% de la demande
d'énergie globale, contre 97.9% à fin 2022.

Ainsi, les importations d’énergie se sont élevées à 2.311,1 GWh en 2023 contre 1.867,5 GWh à
fin 2022, et ont contribué à satisfaire 5,3% de la demande en 2023 contre 4,4% en 2022, étant
souligné que la part des exportations et des autres consommations (pompage STEP,
auxiliaires.…) s'élève à 2,3% en 2022 et 1,7% en 2023.

Les réalisations des investissements de l’exercice 2023 atteignent 3.259 MDH, soit Un taux de
réalisation dc 65% par rapport aux prévisions initiales (5.035 MDH) ct Unc baisse de 18% par
rapport aux réalisations de 2022.

S’agissant des prévisions de clôture 2024, elles s’établiraient à 4.270 MDH. Les prévisions du
budget d'investissement pour 2025 s'élèvent à 9.036 MDH. La hausse importante du budget

d'investissement. projetée en 2025, est la résultante de la programmation de nouveaux projets
structurants, notamment la STEP El Menzel et le renforcement du réseau Sud de transport.

ONEE Branche Eau (ONEE-BO)

Afin de faire face au stress hydrique qui sévit au Maroc, l'ONEE-BO a poursuivi la mise en
œuvre de ses plans d’action visant la sécurisation de l’alimentation en eau potable des villes
et du milieu rural.

Les projets mis en service au cours de l'exercice 2023 ont permis d’atteindre les principaux
résultats suivants :

- Production d’eau potable de 1.353 Mm:* contre 1.324 Mm* en 2022 soit une légère
augmentation de 2% ;

- Renforcement des installations de production par l’équipement d'un débit
supplémentaire de 173.800 m°/j, dont 1.300 m°/j par dessalement, et la pose d'environ
700 km de conduites d'adduction et de distribution :

-  Amélioration du rendement global du réseau de distribution en passant de 73,7% en
2022 à 75,3% en 2023 grâce aux différentes actions visant la réduction des pertes :

-  Desserte d'une population rurale additionnelle d'environ 26.000 habitants, ce qui a
porté le taux d'accès à l'eau potable en milieu rural à 98,5% contre 98,4% à fin 2022 ;

-  Achèvement des travaux de réalisation de 14 nouvelles stations d'épuration (STEP),
pour une capacité d’épuration totale de l’ordre de 20.876 m°/j et un taux de dépollution
de 87,9%.

Les réalisations des investissements de l'année 2023 se sont élevées à 3.564 MDH
représentant un taux de réalisation de 58% par rapport au budget prévisionnel (6.105 MDH).
Ces réalisations se répartissent sur les 3 axes suivants :

- Alimentation en Eau Potable (AEP) urbaine :1.775 MDH
-  AEP rurale :1.084 MDH
- Assainissement liquide :705 MDH.

S



S'agissant des prévisions de clôture 2024, elles seraient de 4.741 MDH. Quant aux prévisions
du budget d'investissement pour l’exercice 2025, elles s’élèvent à 4.,752 MDH.

ONEE (réalisations et prévisions financières)

Le chiffre d'affaires de l'ONEE s’est établi à 41.419 MDH en 2023, en légère hausse de 1% par
rapport à 2022. Le résultat net est déficitaire de 11.407 MDH et en amélioration de 9.526 MDH
sous l'effet, principalement, de l'amélioration des résultats d'exploitation et financier,
respectivement, de 37% et 80%.

Les réalisations d'investissement en 2023 ont atteint globalement 6.823 MDH, sur un budget
total de 11.140 MDH, soit Un taux de réalisation global de 61%.

Pour l’année 2024, les prévisions en termes d'investissement sont établies à 9.921 MDH,
répartis à hauteur de 5.180 MDH pour la branche électricité (52%) et 4.741 MDH pour la
branche eau (48%).

Les réalisations d'investissement, à fin juin 2024, ont atteint 2.507 MDH, représentant 27,82%
des prévisions de clôture (9.011 MDH).

S'agissant de la période 2025-2027, l'Office prévoit un plan d’investissement d'une enveloppe
globale de 40.179 MDH, répartie comme suit: 13.788 MDH pour 2025, 15.021 MDH pour
2026 et 11.3770 MDH pour 2027.

CHIFFRE D'AFFAIRES - ONEE (MDH) RESULTATS - ONEE (MDH)
*
A ds 2021 2022 2023 2024
40.987 423 2.030
——l
-7.329
- -11.407 -11.478
-18.250
2021 2022 2023 2024* -20.983
© RESULTAT NET m RESULTAT D'EXPLOITATION
(*) Probabilités de clôture (*) Probabilités de clôture

H.2.4.2. Régies de Distribution

Le secteur de la distribution d'eau et d'électricité est actuellement en pleine réforme visant
des transformations profondes à travers la création des Sociétés Régionales Multiservices
(SRM) conformément à la loi n° 23-21 relative aux SRM.

Ces nouvelles entités devraient permettre une gestion plus agile et performante des services
de distribution, grâce à un nouveau mode de gouvernance avec comme objectif de remédier
aux contraintes du schéma actuel, caractérisé par un chevauchement des investissements et
une multiplicité des intervenants (Régies, ONEE, délégataires privés).

Le cadre juridique prévoit la création progressive des SRM en trois phases sur une période de
18 mois, avec une couverture complète de toutes les régions d'ici 2025, Quatre SRM seront
opérationnelles, en 2024, dans les régions de Casablanca-Settat, de Marrakech-Safi, de Souss-
Massa et de l'Oriental.

yN



RAPPORT SUR LES ETABLISSEMENTS ET ENTREPRISES PUBI| s

Parallèlement, les Régies continuent à mettre en œuvre leurs plans d'action, en vue d'assurer
une alimentation continue en eau et en électricité, moderniser les services clients, renforcer
les investissements, améliorer les rendements des réseaux et protéger l'environnement.

En 2023, le nombre d'abonnés est passé à environ 7,44 millions contre 7,28 millions en 2022,
avec une prévision de 7,6 millions d'abonnés à fin 2024.

Le chiffre d'affaires des Régies est passé de 9.080 MDH en 2022 à 9.787 MDH à fin 2023.
Les prévisions de clôture au titre de 2024 prévoient un chiffre d'affaires de 10.286 MDH.

Le résultat net s'est établi en 2023 à 702 MDH contre 519 MDH en 2022. Les prévisions de
clôture de 2024 tablent sur un résultat net de 510 MDH.

En réponse à la crise liée au stress hydrique, les Régies ont renforcé leurs investissements pour
améliorer les performances des réseaux de distribution. Ainsi, les rendements des réseaux
d'eau et d'électricité ont enregistré, en 2023, des taux respectifs de 75,55% et 93,26%, avec
des prévisions pour 2024 estimées à 77,94% et à 93,57% respectivement.

Les investissements réalisés par les Régies se sont élevés à 2.494 MDH en 2023, en hausse de
41% par rapport à 2022.

À fin juin 2024, ces investissements ont atteint 1.137 MDH. Les prévisions de clôture tablent
sur des réalisations à hauteur de 4.121 MDH.

Le programme d'investissement des Régies pour la période 2025-2027 se présente comme
suit : 5.896 MDH en 2025, 5.134 MDH en 2026 et 3.435 MDH en 2027.

11.2.4.3. Agences des Bassins Hydrauliques

Conformément aux Hautes Instructions Royales visant à accélérer la réalisation du
Programme National pour l’Approvisionnement en Eau Potable et l'Irrigation 2020-2027
(PNAEPI) et à actualiser sa consistance, un investissement supplémentaire important lui a été
consenti, portant son budget global de 115 MMDH à 143 MMDH.

De même et en relation avec les défis liés à la persistance du stress hydrique prolongé,
Sa Majesté le Roi Mohammed VI, que Dieu L'assiste, a appelé, lors du Discours Royal à
l'occasion de la Fête du Trône du 29 juillet 2024, à la mise à jour continue des leviers de la
politique nationale de l'eau et à la définition d'un objectif stratégique, quelles que soient les
circonstances : garantir l’eau potable à tous les citoyens et couvrir 80% au moins des
besoins d'irrigation sur tout le territoire national.

Les ABH contribuent de manière déterminante, à côté des autres EEP intervenants dans le
secteur de l'eau dans l’élaboration, l'actualisation et le déploiement de la stratégie de l’'Eau
notamment à travers leurs missions qui couvrent l'ensemble des cycles de l'eau allant de la
planification, à la gestion des allocations en eau, à la préservation du domaine public
hydraulique et à l'exercice de la police de l’eau.

Ainsi et conformément aux Hautes Orientations Royales, les ABH sont appelées à accélérer
les diligences et les évaluations requises et à mobiliser les moyens nécessaires pour garantir
une contribution efficace à la mise à jour des leviers de la politique nationale de l'eau, et ce à
travers notamment :

S



-  La coordination, à l'échelon de chaque de bassin hydraulique, de la mise en œuvre
optimale des différentes composantes PNAEPI, et qui concernent notamment le
parachèvement du programme de construction des barrages, la réalisation des grands
projets de transfert d’eau entre bassins hydrauliques, l’accélération de la réalisation des
projets prévus en matière de dessalement de l’eau de mer et d’épuration des eaux usées
réutilisées ;

- Le renforcement de la police de l’eau pour en faire un levier efficace en matière de lutte
contre la surexploitation de la ressource, le pompage anarchique et l’anticipation des rejets
non contrôlés ;

-  La consolidation de la gouvernance du secteur de l'eau notamment par le renforcement
des capacités es ABH en matière de planification, de gestion et de protection des
ressources en eau ainsi que par la mise en place des contrats de gestion participative des
ressources en eau et des nappes.

En termes d'investissement, les réalisations des 10 ABH au titre de 2023 s'élèvent à 535 MDH.
Les prévisions de clôture de 2024 tablent sur des réalisations à hauteur de 802 MDH alors que
les investissements projetés au titre de 2025 s’élèvent à 673 MDH.

H.3. Tourisme
11.3.1. Office National Marocain du Tourisme

En 2023, l'ONMT a intensifié ses efforts pour accompagner la mise en œuvre de la nouvelle
feuille de route stratégique du secteur du tourisme pour la période 2023-2026 et vise un
objectif d'attirer 17,5 millions de touristes d'ici 2026 et de positionner le Maroc parmi les
10 destinations les plus prisées.

Le programme d'investissement prévu pour la réalisation de cette feuille de route s’élève à
3.300 MDH sur la période 2024-2026.

À fin décembre 2023, le tourisme marocain a affiché de bonnes performances en dépit des
effets liés au séisme survenu dans la région d’AI Haouz en septembre 2023. Ces performances
se présentent comme suit :

- Un accroissement des arrivées de 34% par rapport à 2022, soit près de 14,52 millions
de touristes ;

-  Des recettes frôlant les 105 MMDH, en hausse de 12% par rapport à 2022 ;

- Un renforcement de 35% des nuitées dans les Etablissements d’Hébergement
Touristiques Classés (EHTC), avec 25,6 millions de nuitées enregistrées ;

Les investissements ont atteint, en 2023, un taux d’engagement de 95%, soit une enveloppe
de 2.000 MDH sur des prévisions de 2.110 MDH et des paiements de l’ordre de 1.000 MDH
(50%).

Les recettes globales encaissées par l'ONMT, au titre de 2023, sont de l’ordre de 1.245 MDH
dont 750 MDH au titro de la feuille dc route, 195 MDH au titre de la taxe de promotion
touristique et 300 MDH au titre de la subvention d'investissement.

VN



RAPPORT SUR LES ETABLISSEMENTS ET ENTREPRISES PUBI| s

À fin août 2024, environ 11,8 millions de touristes ont franchi les postes frontières,
enregistrant une hausse de 16% par rapport à la même période de l'année précédente.

Les nuitées ont atteint 18,7 millions, en hausse de 7% par rapport à la même période de 2023.
Quant aux recettes touristiques, elles se sont élevées à 76,4 MMDH, en augmentation de 6,7%
par rapport à la même période de 2023.

En termes de prévisions de clôture de 2024, le programme d'investissement de l'Office sera
réalisé à hauteur de 1.400 MDH, soit 58% des prévisions budgétaires.

Pour la mise en œuvre de son plan d'action au titre de la période 2025-2026, l'ONMT prévoit
une enveloppe budgétaire, en termes d’engagement, de 2.5778 MDH en 2025 et 2.600 MDH
en 2026.

H1.3.2. Société Marocaine d’Ingénierie Touristique

La SMIT a bénéficié en 2023 d'une subvention de l’Etat d'un montant de 2.209 MDH, dont
1.028 MDH pour l’'accompagnement des programmes et projets touristiques et 1150 MDH
destinés au financement du Programme FORSA.

L'année 2023 a également été marquée par le [lancement de la 2°"° édition du programme
Forsa, qui a reçu, au titre des deux éditions, 300.000 candidatures sur la plateforme forsa.ma.
À date, 21.200 porteurs de projets ont été financés par le programme Forsa, dont 10.000 lors
de la 1°° édition et 11.200 au titre de la 2°7° édition.

Le chiffre d’affaires de la SMIT pour 2023 s'élève à 123 MDH contre 121 MDH en 2022, dont
47% provenant des prestations rémunérées. Le résultat net est arrêté à 112 MDH en 2023,
marquant une baisse de 18% par rapport à 2022

Pour l’exercice 2024, le programme d'investissement est estimé à 1.428 MDH, dont 85%
(1.220 MDH) seront dédiés à l’accompagnement des projets et programmes de
développement touristiques, y compris une enveloppe de 591 MDH allouée au renforcement
des produits au niveau des filières de la Feuille de Route et de 167 MDH pour l’appui à la
TPE/PME touristique.

Les prévisions de clôture pour 2024 s'établiront à 1601 MDH en termes de dépenses et
1.204 MDH en termes de recettes. Le chiffre d'affaires prévisionnel est de 81 MDH, avec des
réalisations atteignant 33,5 MDH à fin juin 2024. Le résultat net devrait atteindre 39 MDH en
hausse de 27,8 MDH par rapport à 2023,

Pour l’année 2025, il est prévu de réaliser un programme d'investissement de 1.124 MDH dédié
principalement à l’accompagnement et au suivi de la réalisation des plans d’action de la feuille
de route engagés dans les filières touristiques au niveau régional pour 492 MDH, à
l'accélération de l'exécution des chantiers lancés visant à améliorer l’attractivité des
destinations et des produits pour 217 MDH ainsi qu'aux autres programmes (TPME,
Qariati/Mdinti, Aghroud, etc.) pour 415 MDH.

A



H.4. Poste, Audiovisuel et Télécommunications
I1.41. Barid AIl Maghrib

En 2023, le chiffre d’affaires de BAM SA s’est établi à 740,4 MDH, en baisse de 1,6% par rapport
à 2022. Le résultat net, arrêté à 133,5 MDH, est en hausse de 90% par rapport à 2022, grâce à
la bonne performance du résultat financier suite à la hausse des plus-values réalisées par les
OPCVM gérés par ABB.

En termes consolidés, le Groupe BAM a réalisé, en 2023, un produit d'exploitation de
3.493 MDH, en hausse de 14% par rapport à 2022, dégageant ainsi un résultat net de 271 MDH,
contre une perte de 115 MDH en 2022.

À fin juin 2024, le chiffre d’affaires consolidé s'est établi à 1896 MDH (contre 1.477 MDH
enregistré au titre de la même période en 2023), tandis que les prévisions de clôture tablent
sur un montant de 3.786 MDH (contre 2.977 MDH en 2023). Les investissements réalisés par
le Groupe à fin juin 2024 s'élèvent à 107 MDH (contre 73 MDH au titre de la même période en
2023), avec des prévisions de clôture estimées à 219 MDH (contre 172 MDH en 2023).

Le programme d'investissement pour la période 2025-2027 est estimé à 1.101 MDH, réparti
comme suit : 404 MDH en 2025, 368 MDH en 2026, et 329 MDH en 2027.

En termes de perspectives, il est prévu de relancer la réforme postale et du service postal
universel dans le cadre d’un nouveau contrat-programme basé sur la revue du modèle
économique du Groupe compte tenu du déclin structurel de l’activité courrier. Ce contrat
s'attèlera principalement au développement d’'une offre intégrée à destination des e-
commerçants, le renforcement des capacités de la plateforme de confiance numérique (Barid
eSign), l’industrialisation du tri colis, et la valorisation du patrimoine foncier à travers les projets
OPCI outre la mutualisation des centres et axes de Transport Courrier et Messagerie en vue
d'une optimisation des coûts.

H.4.2. Audiovisuel
H1.4.2.1. Société Nationale de Radiodiffusion et de Télévision

En 2023, la SNRT a intensifié ses efforts pour répondre progressivement aux exigences de son
cahier des charges, tout en s'adaptant à un environnement en pleine mutation numérique. La
SNRT a également œuvré à l'amélioration continue de son offre de services, au renforcement
de sa part de marché et à la fidélisation de son audience. Ces efforts ont conduit à une
stabilisation voire une légère progression des taux d'audience, avec des résultats notables :

- Audience journalière : 17,5% en 2023 contre 16% en 2022 ;

-  Audience en prime-time (de 20h50 à 22h30) : 28,9% en 2023 contre 26% en 2022 ;

-  Radio Mohammed VI reste la radio n° 1 la plus écoutée au Maroc avec 5 millions
d’auditeurs.

Le financement des activités et des programmes de la SNRT, en 2023, a été assuré
principalement grâce aux produits suivants : la subvention de l'Etat de 1.,517 MDH (hors
400 MDH versés à titre exceptionnel), le produit de la Taxe de la Promotion du Paysage
Audiovisuel National (TPPAN) de 195 MDH (en baisse de 43% par rapport à 2022) et les ventes
des espaces publicitaires de 175 MDH.

M



RAPPORT SUR LES ETABLISSEMENTS ET ENTREPRISES PUBLICS

Les montants totaux des produits et des charges, comptabilisés au titre de 2023, s’élèvent
respectivement à 1.452 MDH et à 2.041 MDH, dégageant ainsi un résultat net de -589 MDH.

A fin juin 2024, les produits d'exploitation ont atteint 560 MDH (sur une prévision annuelle de
1.557,5 MDH), dont un chiffre d’affaires de 159 MDH, alors que le montant dépensé en
investissement s’est établi à 25 MDH.

11.4.2.2. Société d'Etudes et de Réalisations Audiovisuelles

2M est la première chaîne en termes de part de marché global marocain brut des
investissements publicitaires avec 61,8% suivie d’Al Aoula avec 17,2% et de Medi1TV avec 7,2%.

Les indicateurs d’activités de la SOREAD-2M relatifs à l'année 2023 se présentent comme
suit :

- _ Audience journalière : 29,2% en 2023 contre 32% en 2022 ;
- Audience en prime-time (de 20h50 à 22h30) : 22,4% contre 24% en 2022.

Sur le plan financier, les activités de la SOREAD 2M de 2023 ont été financées par le chiffre
d'affaires propre de 383 MDH et une subvention de l’Etat de 326,51 MDH dont 30 MDH versés
à titre exceptionnel.

Le résultat net de 2023 fait ressortir un solde négatif de 327 MDH contre -177 MDH en 2022,
ce qui s’est traduit par l'aggravation de la situation nette ayant atteint -764 MDH contre
-437 MDH en 2022 et -260 MDH à fin 2021 (pour un capital social de 359 MDH), exigeant ainsi
‘engagement d'urgence des mesures de redressement de la situation financière de la société.

Le budget de la SOREAD au titre de 2024 a été établi sur la base des objectifs visant la
réalisation des synergies permettant des économies à travers la concrétisation du pôle public,
‘augmentation des recettes publicitaires et l'optimisation des charges.

Les charges d'exploitation prévisionnelles sont estimées à 666 MDH, Quant au budget
d'investissement prévu au titre de 2024, il s’élève à 30 MDH.

La Société table sur un retour à l’équilibre avec des résultats positifs de l'ordre de 30 MDH en
2024, 33 MDH en 2025 et 28 MDH en 2026.

H.4.3. Agence Nationale de Réglementation des Télécommunications

L'état d’avancement de la mise en œuvre des principales composantes du plan d’'action, validé
gdans le cadre de la Note d'Orientations Générales (NOG) du secteur des télécommunications,
diffusée par circulaire du Chef du Gouvernement en 2020, peut être retracé comme suit :

-  Entermes de Haut débit, [e taux de réalisation du Programme National du Haut Débit
(PNHD-1) s’établit à 97% de l’objectif initial (soit 10.420 localités) alors que le
programme PNHD-2 visant la couverture de 1.800 localités en 4G à horizon 2026 a été
lancé ;

-  S'agissant du Très Haut Débit à Fibre Optique de Bout en Bout (THD-FTTH), les
échanges avec les opérateurs globaux se trouvent à un stade avancé dans l’objectif de
déployer les infrastructures cn fibre optique pour attoindre 4,4 millions de ménages
pouvant accéder à un service THD-FTTH (au minimum de 100 MB) et ce, avant fin 2026 :

- Pour la connectivité internationale, la capacité globale par fibre optique est de

9.760 Gbps en 2023 contre 2.170 Gbps en 2018 et 495 Gbps en 2013.



Durant les trois dernières années, les investissements cumulés des opérateurs représentent
22% de leurs revenus et dépassent très largement les moyennes mondiales et européennes.
Ce trend se poursuivra et devrait s'accentuer dans le cadre de la stratégie Maroc Digital 2030.

A ce sujet, il y lieu de souligner que l’'ANRT assure un suivi régulier de l’état d'avancement de
la réalisation du plan d’action susvisé et publie, régulièrement, des informations détaillées sur
le niveau de la qualité des services Voix et Data.

Par ailleurs, et dans le cadre de la préparation de la Coupe du Monde 2030 et conformément
à la stratégie 2030 du secteur des télécommunications, le projet de couverture de la 5G a été
lancé dans l'objectif d'atteindre une couverture de 5G de 25% de la population en 2026 et 70%
à fin 2030 en assurant Un niveau de couverture de 100% pour les villes hôtes des évènements
sportifs de la Coupe du Monde 2030.

En termes de réalisations financières et à fin juin 2024, l'ANRT a réalisé un chiffre d'affaires de
450,76 MDH et prévoit la clôture de l'exercice 2024 avec un chiffre d'affaires de 688,5 MDH.

Le résultat net réalisé, à fin juin 2024, s’élève à 105 MDH et les prévisions de clôtures sont
prévues pour 130 MDH.

Les projections 2025-2027 en termes de chiffres d'affaires se présentent comme suit :
753,5 MDH pour 2025, 808,5 MDH pour 2026 et 820,5 MDH pour 2027.

Il RENFORCEMENT DE LA  COHESION  SOCIALE ET
TERRITORIALE

11.1. Education et Formation Professionnelle

HILT1.1. Académies Régionales de l’Education et de la Formation

La feuille de route 2022-2026 vise à bâtir une école publique de qualité, articulée autour de
trois piliers essentiels : l’enseignant, l'élève et l'établissement scolaire, Cette stratégie se traduit
par plusieurs programmes clés, visant à améliorer la qualité de l’enseignement notamment à
travers l'approche TARL (Teaching At the Right Level) au profit de 340.000 élèves, la
méthode de « l'enseignement explicite » pour laquelle 11.000 enseignants ont été formés et
l'expérience pilote des « Ecoles pionnières » dans 626 établissements primaires. Ces initiatives
s'appuient sur le Projet d'Etablissement Intégré, un outil opérationnel visant à transformer la
vie scolaire, améliorer la qualité des apprentissages de base, réduire la déperdition scolaire et
favoriser l'épanouissement des élèves,

Pour l'année scolaire 2023-2024, le système éducatif marocain a enregistré des avancées
notables avec un effectif total de 8 millions d’élèves, dont 85% sont scolarisés dans le public,
etune parité quasi-atteinte avec 48,9% de filles. Le nombre d'établissements scolaires a atteint
12.133, dont 6.731 situés en milieu rural, L'offre scolaire a été renforcée par l'ouverture de
237 nouvelles écoles, dont 65% en zones rurales. Le taux de scolarisation a également
progressé, atteignant 80% au préscolaire, 100% au primaire et 80% au secondaire collégial.

Concernant la lutte contre le décrochage scolaire, le taux d’abandon a diminué de 12%, passant
de 334.664 élèves en 2021-2022 à 294.458 en 2022-2023 et environ 50.000 élèves en
situation de décrochage ont réintégré le système scolaire au début de l'année.

M



RAPPORT SUR LES ETABLISSEMENTS ET ENTREPRISES PUBI| s

En matière d’appui social, 4.459.478 élèves ont bénéficié de l’Initiative Royale « Un million de
cartables », 1.040.615 élèves ont bénéficié de la cantine scolaire, et 580.266 élèves, dont 83,3%
en milieu rural, ont bénéficié du transport scolaire.

En 2023, les réalisations d'investissement des AREF ont atteint 6.059 MDH, avec des
prévisions pour 2024 s'’élevant à 6.859 MDH.

À fin juin 2024, les investissements réalisés étaient de 4.120 MDH. Les prévisions de clôture
pour l'année s'élèvent à 6.800 MDH.

Pour les années 2025, 2026 et 2027, les prévisions de païiements pour les AREF s'élèvent
respectivement à 7.516 MDH, à 8.278 MDH et à 8.959 MDH.

HI.1.2. Universités

Conformément à la vision stratégique de la réforme de l'enseignement 2015-2030, approuvée
par Sa Majesté le Roi Mohammed VI, que Dieu L'assiste, la loi-cadre n° 51-17 du 9 août 2019
a pour objectif de créer une nouvelle école marocaine axée sur : i/ la promotion de l’individu
et le progrès de la société, ii/ le renouvellement des métiers de l'enseignement, et ii/ l'adoption
d’un modèle pédagogique innovant, développant l’esprit critique, l’'épanouissement et les
valeurs citoyennes universelles.

Pour l’année scolaire 2023-2024, le système d'enseignement supérieur comprend
12 universités publiques regroupant 158 établissements ainsi que 73 établissements dédiés à la
formation des cadres. Par ailleurs, 5 universités ont été créées dans le cadre de Partenariats
Public-Privé  (PPP), comptant 45 établissements. Le système inclut également
2 établissements publics sous gestion PPP, une université publique à gestion privée et 3 autres
établissements de formation. En outre, on compte 5 universités privées comprenant
33 établissements de formation, ainsi que 129 établissements d'enseignement supérieur privés
indépendants des universités.

L'effectif global des étudiants inscrits s'élève à 1.301.519, soit une augmentation de 6,8% par
rapport à 2022-2023. Le nombre d'étudiants dans les établissements ne relevant pas des
universités a également progressé de 15,5%, atteignant 61.000 en 2023-2024. Le nombre de
nouveaux inscrits s’est ainsi établi à 343.489.

L'effectif des enseignants est passé à 22.468, soit une augmentation de 3,9%, tandis que celui
du personnel administratif a atteint 13.467, en hausse de 2,7%. Toutefois, le ratio moyen
étudiants/enseignant reste élevé à 57:1, ce qui représente un défi pour la qualité de
l'encadrement et de la recherche, De même, le taux d'encadrement administratif est de 96:1,
rapport qui est également élevé,

La capacité d'accueil a progressé de 3%, atteignant 582.200 places en 2023-2024, grâce à la
réalisation de projets dans plusieurs universités, dont la création de cing nouveaux
établissements. Le nombre de diplômés du système d'enseignement supérieur en 2021-2022
s'élève à 181.866, avec une majorité (77%) provenant des universités publiques.

La capacité litière des cités universitaires a augmenté de 13%, pour atteindre 59.400 lits en
2023-2024. En termes de soutien financier, 409.013 étudiants ont bénéficié de bourses.

En termes de réalisations budgétaires des Universités, les païements d'investissement ont

atteint 794 MDH à fin 2023, soit un taux de réalisation de 22%.



À fin juin 2024, les réalisations en matière d’investissement se sont élevées à 298 MDH,
représentant un taux de réalisation de 24%.

Sur la période 2025-2027, les universités prévoient un programme d'investissement réparti
comme suit : 2.465 MDH pour 2025, 5.017 MDH pour 2026 et 3.867 MDH pour 2027.

H1.1.3. Office de la Formation Professionnelle et de la Promotion du Travail

Conformément à la feuille de route de développement de la formation professionnelle,
présentée le 4 avril 2019 devant Sa Majesté le Roi Mohammed VI, que Dieu L'assiste, l'OFPPT
poursuit ses efforts pour réformer et moderniser l’écosystème de la formation.

L'Office poursuit la réalisation du programme des centres de formation de nouvelle génération
et qui porte sur la création de 12 Cités des Métiers et des Compétences (CMC) multisectorielles,
multifonctionnelles et mutualisées, intégrées dans des écosystèmes régionaux. Ces cités
abritent des filières à fort potentiel d'emploi, favorisant ainsi l'intégration professionnelle des
jeunes.

À ce jour, six CMC sont déjà opérationnelles, avec une capacité de 21.865 places pédagogiques,
représentant 64% de la capacité cible de 34.000 stagiaires pour les 12 cités, en soulignant que
les six CMC restantes enregistrent des avancées significatives en termes de construction et/ou
d'équipement et leur ouverture est prévue en 2025.

A fin août 2024, les engagements autorisés pour le programme des CMC s'élevaient à
4.900 MDH, tandis que les paiements effectués ont atteint un montant de 3.200 MDH.

La restructuration et la diversification de l’offre de formation demeurent des priorités, avec le
lancement de 163 nouvelles filières, portant le portefeuille actuel à 444 filières, soit 73% de
l'objectif global. En parallèle, le développement du dispositif de formation se poursuit, avec la
construction de 20 nouveaux EFP en 2024, inscrits dans le cadre des conventions signées
devant Sa Majesté le Roi Mohammed VI, que Dieu L'assiste, et celles conclues avec les
Régions, ainsi que des partenariats avec la Fondation Mohammed V pour la Solidarité (FMVS)
et la Fondation Mohammed VI pour la Réinsertion des Détenus (FMVRD). Ainsi, pour l’année
académique 2024-2025, l'OFPPT disposera d’une offre de formation de près de 414.855 places
pédagogiques.

Le budget global de l'OFPPT pour 2024 s’élève à 6.437 MDH, marquant une augmentation de
13% par rapport à l’exercice 2023. Ce budget inclut 1.2177 MDH dédiés au programme
d'investissement, dont 727 MDH destinés aux CMC et 490 MDH pour les autres dispositifs de
l'OFPPT.

Les recettes prévisionnelles de la taxe professionnelle de la formation (TFP) pour 2024 sont
estimées à 3.407 MDH.

Le budget d'investissement de 2024 prévu pour 1.217 MDH a été réalisé à hauteur de 440 MDH
à fin juin 2024. Les prévisions pour 2025-2027 atteignent respectivement 2.156 MDH, 701
MDH et 456 MDH.

yN



RAPPORT SUR LES ETABLISSEMENTS ET ENTREPRISES PUBI| s

I1.2. Santé et Prévoyance Sociale
H1.2.1. Centres Hospitaliers Universitaires

Conformément aux Hautes Orientations Royales en vue d'assurer une offre de soins
répondant aux attentes des citoyens, le Maroc s'est engagé dans une vaste réforme de son
système de santé pour offrir des services de soins de qualité à travers des structures efficientes
et performantes. Le secteur public de la santé a bénéficié, ces dernières années, d'un
accroissement soutenu de l‘effort de l'Etat, visant à renforcer les moyens mis à la disposition
des acteurs et à accompagner la réforme en cours dans ce secteur.

L'année 2023 a été marquée par le renforcement de l'offre de soins hospitaliers avec
l’inauguration du nouveau CHU de Tanger par Sa Majesté le Roi Mohammed VI, que Dieu
L’assiste, en date du 28 avril 2023. De plus, l’achèvement des travaux de construction du CHU
d'Agadir est prévu pour fin 2024 alors que le projet de construction du CHU de Laäyoune a
déja démarré, Les autres projets en phase de lancement concernent les CHU d'Errachidia, de
Guelmim et de Béni Mellal.

Par ailleurs, les travaux de construction du nouvel hôpital Ibn Sina de Rabat, avec un
investissement évalué à 6 MMDH, avancent à un rythme soutenu pour une inauguration prévue
en 2026. Ce complexe, construit sur un terrain de 13 hectares, comprendra un hôpital général
de 1.044 lits et un CHU ultramoderne doté des technologies médicales les plus avancées.

Le secteur de la santé a également posé les jalons juridiques d'une nouvelle gouvernance avec
la mise en place des Groupements Sanitaires Territoriaux, de la Haute Autorité de la Santé, de
l'Agence Marocaine des Médicaments et des Produits de Santé ainsi que de l'Agence
Marocaine du Sang et de ses Dérivés.

Par ailleurs, des efforts sont déployés pour l'implantation d'un système d'information
hospitalier (SIH) destiné à assurer la collecte, le traitement et l'exploitation des données
relatives au système de santé, avec un suivi des patients via le Dossier Médical Partagé, pour
un coût global estimé à 1,2 MMDH.

En 2023, les réalisations d'investissement en termes de paiements pour les CHU ont atteint
488 MDH.

Pour l'année 2024, les prévisions budgétaires en investissement sont estimées à 507 MDH.
Les investissements des CHU ont atteint, à fin juin 2024, 51 MDH, tandis que les prévisions de
clôture sont estimées à 350 MDH,

Le volume d'investissement prévisionnel pour les années 2025, 2026, et 2027 s'élève,
respectivement, à 702 MDH, 781 MDH et 729 MDH.

H1.2.2. Caisse Marocaine des Retraites

Les déficits techniques et structurels des régimes gérés par la CMR continuent de se creuser
et devraient conduire à l'épuisement des réserves en 2028.

Le projet de réforme des régimes des ponsions civiles ost, actuellement, en cours d'examen on
concertation avec les partenaires économiques et sociaux et devrait s'appuyer sur le scénario,
validé auparavant et s'articulant autour des principaux objectifs ci-après :

- Assurer la viabilité du système et garantir une redistribution transparente et équitable ;

VS



- Construire un système de retraite compatible avec les capacités économiques du pays ;
- Sauvegarder les droits acquis des retraités et des affiliés actuels à la date de la réforme.

Par ailleurs, la CMR poursuit l'exécution de son plan stratégique 2023-2026, tel que défini dans
le contrat-programme conclu avec l‘Etat pour la période 2022-2024, structuré en six axes :
l'expérience client, la gestion des fonds de réserves, le capital humain, l’excellence
opérationnelle, l'image et la communication ainsi que la gestion des transformations.

À l'approche de la fin de cette feuille de route, la CMR a entamé en 2024 une actualisation de
sa vision stratégique et son plan pour la période 2025-2027. Durant cette période, la Caisse
continuera de poursuivre les objectifs suivants :

- Le déploiement des axes d'amélioration de l'expérience client ;

- L'investissement dans le capital humain, en développant l’expertise, les compétences et
la culture d‘excellence ;

- La transition vers une digitalisation axée sur l'innovation, l'expérimentation et les
technologies de rupture ;

- Le renforcement de l'excellence opérationnelle et la maîtrise des coûts à travers une
consolidation de la gouvernance des données et une culture de pilotage basée sur les
données ;

- Le développement et la valorisation des synergies et des partenariats avec les opérateurs
publics.

Le solde technique de l’ensemble des régimes s’est établi, à fin 2023, à -9.871 MDH se
traduisant par une forte contraction des fonds de réserve, actuellement de 65.800 MDH, dont
l'épuisement est prévu en 2028. Les prévisions pour 2025-2027 confirment cette tendance de
dégradation.

1H1.2.3. Caisse Nationale de Sécurité Sociale

La CNSS est chargée de la mise en œuvre du chantier Royal relatif à la généralisation de la
protection sociale qui fixe les objectifs suivants :

-  L'extonsion de l'assurance maladic obligatoire (AMO) à 22 millions de bénéficiaires
supplémentaires en 2022 ;

-  L'extension des allocations familiales au profit de 7 millions d'enfants à partir de fin
2023:

- _ L'élargissement de la base des adhérents aux régimes de retraite au profit de 5 millions
d'actifs d'ici 2025 ;
- La généralisation des Indemnités pour Perte d'Emploi (IPE) à l'horizon 2025.
A cet égard, les réalisations, à fin mai 2024, montrent que 9,9 millions de personnes sont
couvertes par le régime des travailleurs salariés et retraités et 10,5 millions par le régime
« AMO-TADAMON » dont 3,9 millions assurés principaux et 6,6 millions ayants-droit, De même,

la population couverte par les régimes « AMO-TNS » et « AMO-ACHAMIL » est de 3,8 millions
d'individus.

VN



RAPPORT SUR LES ETABLISSEMENTS ET ENTREPRISES PUBI| s

Ainsi et tenant compte de l’ensemble des régimes de couverture (CNSS, CNOPS, Mutuelle des
Forces Armées Royales, etc.), 31,5 millions de personnes sont couvertes par l'AMO
représentant 84% de la population marocaine, dont 24,2 millions de personnes assurées par la
CNSS et 7,3 millions par les autres acteurs.

Les cotisations des bénéficiaires versées par l’Etat à la CNSS au titre du régime AMO-
TADAMON totalisent 15,51 MMDH à fin septembre 2024.

Après la généralisation réussie de l'AMO, le Gouvernement a lancé, en décembre 2023,
le régime de l'Assistance Sociale Directe (ASD} au profit des ménages pauvres et vulnérables
qui ne bénéficiont pas des régimes d'allocations familiales selon la réglementation en vigueur.

Le plan d'action stratégique de la CNSS pour 2024-2026 s'articule autour de plusieurs objectifs
notamment l’accélération de la généralisation de la protection sociale, la transformation
digitale de la gestion de la caisse, l'amélioration de la qualité de service, la fiabilisation des
dispositifs de recouvrement et de lutte contre la fraude sociale, la maîtrise des dépenses de
l'AMO, le renforcement du capital humain et de [la communication interne et externe.

Dans le cadre de la dématérialisation et de la digitalisation des processus de gestion ainsi que
de la simplification des procédures et de l'innovation, le plan stratégique prévoit de
dématérialiser plusieurs opérations notamment la feuille de soins, le tiers payant, la gestion
des réclamations des assurés et les processus de recouvrement.

HH1.3. Développement territorial, urbanisme, habitat et aménagement
HI.3.1. Développement du Monde Rural
H1.3.1.1. Programme d'Electrification Rurale Globale

Depuis le lancement du Programme d'Electrification Rurale Global (PERG) en 1996, et jusqu'à
fin 2023, les réalisations se traduisent par :

-  Electrification par raccordement aux réseaux : 41.847 villages ont été raccordés,
permettant l'accès à l'électricité pour 2.158.674 foyers.

-  Equipement par kits photovoltaïques individuels :

e 51559 foyers dans 3.663 villages entre 1998 et 2009, dont 3.505 villages
(50.086 foyers) ont été reprogrammés au réseau électrique en réponse à la
demande croissante des habitants et au développement du réseau ;

e 19.438 foyers dans 900 villages dans le cadre du projet solaire pour les
Communes INDH entre 2015 et 2018.



cation rurale cumulé (%)

9953 9964 9972 9978 9983 9986 — 9988
43

9895 | 9915
9850
98,10
97,40 l l

2011 2012 2013 2014 2015 2016 2017 2018 2019 2020 2021 2022 2023

Ainsi, la population totale ayant bénéficié de l’électrification dans le cadre du PERG est estimée
313 millions d'habitants et le taux d'électrification rurale global Jans toutes les régions du pays
atteint 99,88% à fin 2023.

En 2023, 198 villages ont été électrifiés par réseau interconnecté, apportant l'électricité à
4.569 foyers ruraux, soit environ 24.000 habitants.

À fin 2023, le montant cumulé des investissements réalisés dans le cadre du PERG s'élève à
25.287 MDH.

Les réalisations cumulées du PERG à fin juillet 2024 ont permis l'électrification, par
raccordement aux réseaux de 41.922 villages regroupant 2.160.756 foyers, pour un taux
d’électrification rurale de 99,89%.

Le programme PERG 2023-2027 vise l’électrification de 834 villages, comprenant
18.316 foyers. De plus, il prévoit l'électrification de 1,950 écoles et de 800 mosquées
supplémentaires au cours de la période 2023-2025,

H1.3.1.2. Programme … d'Approvisionnement Groupé en Eau potable des
populations Rurales

Le taux d’accès à l'eau potable en milieu rural est passé de 14% enregistré à fin 1994 à 98,5%
à fin 2023.

w l l l l l l l

1995 2005 2010 2015 2020 2021 2022 2023

M


RAPPORT SUR LES ETABLISSEMENTS ET ENTREPRISES PUBLICS

Le taux d'accès susvisé de 98,5% constitue une moyenne nationale, en soulignant que
certaines provinces restent en dessous de ce taux. Dans ce cadre, l'ONEE-Branche Eau
prévoit de continuer l’effort de généralisation à ces zones afin d'y garantir un minimum de
couverture de 80%. Ces zones sont souvent caractérisées par l’absence de ressources en eau
facilement mobilisables, la dispersion et l’enclavement.

A cet effet, le budget réservé à l’alimentation en eau potable rurale pour l'exercice 2024 s’élève
à 1.317 MDH, ce qui permettra d'atteindre un taux d’accès moyen national de 98,8% en milieu
rural pour une population bénéficiaire additionnelle d'environ 38.948 habitants.

Pour la période 2025-2027, lc programme d'investissement totalisc 5.254 MDH ct visc à porter
le taux d'accès au monde rural à 98,95% d'ici 2027.

12,978 12,984
98,95%

2023 2024 2025 2026 2027

HH1.3.2. Holding Al Omrane

En 2023, le Groupe HAO a initié une transformation stratégique, à travers un audit de ses
performances, une redéfinition de sa vision et de son modèle économique avec comme
objectif de conclure un nouveau contrat-programme avec l'Etat.

Les taux de réalisation du Groupe sur les mises en chantier et les achèvements se situent entre
38% et 52%, à l'exception des achèvements « Partenariats » qui ont atteint Un taux de 86%.
Malgré cette baïsse, le volume d’investissement a atteint 4.548 MDH, soit un taux de réalisation
de 105% par rapport aux prévisions budgétaires.

Les principales réalisations physiques de 2023 peuvent être résumées comme suit :

-  Mise en chantier de 20 projets pour 6.548 unités de production nouvelle (taux de
réalisation de 47%) ;

-  Achèvement de 46 projets pour 10.832 unités de production nouvelle (taux de
réalisation de 51%).

L'activité financière du Groupe a été satisfaisante, avec des recettes de ventes de 4.729 MDH,
soit un taux de réalisation de 116% par rapport aux prévisions budgétaires.

Le stock des produits finis a baissé de 8,5%, passant d'une valeur comptable nette (VCN) de
17.578 MDH en 2022 à 16.084 MDH en 2023.

Les subventions reçues dans le cadre des opérations conventionnées se sont élevées à

2.008 MDH, en baisse de 7,2% par rapport à 2022.



En 2023, le chiffre d'affaires du Groupe s’est établi à 4.266 MDH, en légère baisse de 2% par
rapport à 2022. Le résultat net a affiché un déficit de 1.1770 MDH en 2023 contre un résultat
positif de 224 MDH en 2022.

Au 30 juin 2024, le Groupe Al Omrane a enregistré une progression de 24% de son chiffre
d'affaires par rapport au premier semestre 2023, atteignant 2.171 MDH. Les investissements
réalisés à fin juin 2024 ont atteint 2.288 MDH, en hausse de 11% par rapport à la même période
de 2023

Pour 2024, le Groupe prévoit :

- La mise en chantier de 16.679 unités de production nouvelle (+155% par rapport à
2023):

- _ L'achèvement de 28.908 unités de production nouvelle (+167%) ;

- La mise en œuvre de 10.673 unités dans le cadre du nouveau dispositif d'aide au
logement, dont 7.587 en partenariat avec le secteur privé et 3.086 en propre.

Ainsi, les prévisions de clôture pour 2024 prévoient un chiffre d'affaires de 5.583 MDH, en
hausse de 31% par rapport à 2023 et un résultat net de 157 MDH contre -1170 MDH en 2023.

Pour la période 2025-2027, le Groupe compte capitaliser sur les avancées réalisées en 2024,
pour consolider ses performances comme suit :

- Un accroissement du chiffre d'affaires pour atteindre 5.246 MDH en 2025, 5.427 MDH
en 2026 et 5.640 MDH en 2027 ;

- Une amélioration du résultat net consolidé devant s’établir à 254 MDH en 2025, à
318 MDH en 2026 et à 290,1 MDH en 2027.

Le programme d'investissement pour cette période est estimé à 18.914 MDH, réparti comme
suit : 6.433 MDH en 2025, 6.510 MDH en 2026, et 5.971 MDH en 2027.

CHIFFRE D'AFFAIRES - HAO (MDH) RESULTATS - HAO (MDH)
5.583
566

s0 4335 4.266 266 322 157
l -1.170

2021 2022 2023 2024* 2021 2022 2023 2024*

E RESULTAT NET B RESULTAT D'EXPLOITATION

(*) Probabilités de clôture {*) Probabilités de clôture

H1.3.3. Société Rabat Région Aménagement

A fin 2023, les engagements cumulés au titre du programme Rabat Ville Lumière (RVL), objet
de la Convention-Cadre 2014-2018 signée devant Sa Majesté le Roi Mohammed VI, que Dieu
L'assiste, ont atteint 9.485 MDH, représentant 97% dudit programme.

yN


RAPPORT SUR LES ETABLISSEMENTS ET ENTREPRISES PUBI| s

Les engagements cumulés au titre des conventions spécifiques (hors programme RVL)
s’élèvent, à fin 2023, à 13.018 MDH représentant 69% du coût total (18.862 MDH) des projets
inscrits dans ces conventions.

Le portefeuille des projets confiés à la SRRA comprend 317 projets, dont 143 relevant du RVL.
L'état d’avancement physique à fin 2023 indique l’achèvement de 139 projets RVL et 79 projets
hors RVL. De plus, 4 projets du programme RVL et 68 autres projets conventionnés sont en
cours de réalisation, tandis que 27 projets hors RVL sont en phase d’études ou de lancement.

Au titre de 2023, la société a réalisé un total d’investissement de 3.747 MDH, en hausse de
32% par rapport à 2022, soit un cumul (dopuis 2015) dc 16.5530 MDH réparti entre lc
programme RVL (8.484 MDH) et hors RVL (8.046 MDH).

Au cours de l'année 2023, la Société a conclu 33 nouvelles conventions de maîtrise
d’ouvrage (MOD) déléguée et 8 avenants aux conventions en cours pour un montant de
2.724 MDH et aui portent sur la réalisation de projets relevant des différents axes de
développement de la ville de Rabat et de sa région.

La SRRA prévoit l’'engagement, en 2024, d’un programme d’investissement de 170 MDH pour
les projets RVL et de 2.961 MDH pour les projets hors RVL, soit un investissement global
cumulé de 3.131 MDH.

Le chiffre d’affaires prévisionnel au titre de 2024 est estimé à 126 MDH en baisse de 44% par
rapport à 2023, en raison de la baisse prévue du montant des ventes dans la Zone
d'Accélération Industrielle (ZAI).

L'investissement prévisionnel au titre de l’année 2025 est de 1.514 MDH consacré entièrement
aux engagements des projets hors RVL. En termes de paiement, il est prévu une enveloppe
globale de 3.176 MDH dont 185 MDH dédiés aux projets RVL. Les prévisions d'investissement
de 2026-2027 sont évaluées à 1.108 MDH.

H1.3.4. Société Casa-Aménagement

La SCA gère un portefeuille de 40 projets pour un coût global de 10.453 MDH.
Ses interventions majeures concernent principalement la mobilité, avec notamment le
développement des infrastructures de mobilité Zone Casablanca Ouest, l'aménagement et le
dédoublement de la route régionale côtière RR322 reliant les communes de Cherrat,
Bouznika, et El Mansouria dans la Province de Benslimane ainsi que les travaux de voiries au
niveau de la Préfecture d'arrondissement de Sidi Bernoussi.

En 2023, le taux d’engagement cumulé sur le programme d’'investissement a atteint 72%, soit
des engagements cumulés de 6.946 MDH.

En 2024, la SCA a initié plusieurs nouveaux projets et études notamment l’aménagement de
la voirie à l'intérieur de la ville de Mohammedia pour 500 MDH, le complexe sportif et de loisirs
dans la zone "Al Manbaa” à Tit Mellil pour 60 MDH, et l’'aménagement du jardin Halhal à
Lahraouine, Province de Mediouna, pour 18,3 MDH.

À fin juin 2024, la société avait réalisé des investissements en termes d’engagements d’un
montant de 408 MDH, un montant qui devrait atteindre près de 800 MDH à fin 2024.

yN



En 2025, l’activité de la société portera sur la poursuite de la réalisation des projets en cours
et le lancement des études et des travaux de nouveaux projets dont les conventions sont en
cours de finalisation ou de signature.

IH1.4. Promotion de l’offre à l’export
H1.4.1. Etablissement Autonome de Contrôle et de Coordination des Exportations

Le volume des exportations agro-alimentaires a atteint 4,02 millions de tonnes, en 2023, en
baisse de 16% par rapport à l’année précédente. En valeur, le montant de ces exportations
établi 83.142 MDH con 2023 contre 81.236 MDH en 2022.

Le secteur agro-alimentaire constitue l'un des principaux secteurs générant des recettes en
devises, représentant 19% des exportations totales à fin 2023.

En 2023, dans le cadre de la promotion des exportations, Morocco Foodex a mené diverses
actions notamment la participation marocaine à plusieurs salons et foires internationaux.

Le budget de promotion de l'EACCE pour 2023, fixé à 109 MDH, a été exécuté à hauteur de
94%, Les prévisions de clôture pour 2024 s'élèvent à 120 MDH. Les budgets prévus pour 2025,
2026, et 2027 sont également estimés à 120 MDH par an.

Le plan d'action de l'EACCE pour l'année 2025 inclut la participation marocaine à divers salons
internationaux, la mise en place d'une mission B2B en Afrique de l’Est pour promouvoir les
produits de la pêche et l‘organisation d’une mission incoming ciblant les importateurs d'Europe
de l’Est.

Ce plan prévoit également la création d’une plateforme digitale pour mettre en valeur le
potentiel exportable du Maroc, le développement d’un concept architectural unifié pour le
pavillon marocain et la promotion du label de durabilité de Morocco Foodex,

HI.42. _ Agence Marocaine de Développement des Investissements et des
Exportations

Dans le cadre de sa principale mission relative à la promotion de l'offre du Maroc en matière
d'investissement et d'exportation, l'AMDIE poursuit son plan d'action 2024-2026 visant à
promouvoir les opportunités d'investissement et de l'offre exportable du Maroc et à attirer
les prospects potentiels pour leur implantation dans le pays.

Dans ce cadre, l'Agence a soutenu près de 289 projets privés, dont 119 ont été approuvés
pour un montant d'investissement cumulé de 70 MMDH avec l'objectif de création de
30.000 emplois directs.

L'AMDIE prévoit, en 2024, d'accompagner environ 250 projets, totalisant un montant
d'investissement prévisionnel de 140 MMDH et la création de plus de 72.000 emplois directs.

En matière de promotion des exportations, l’année 2023 a été marquée par une approche
qualitative, efficiente et orientée vers les résultats. Ainsi, l'Agence a réalisé 236 actions
commerciales, dont 123 visites d’investisseurs potentiels.

En 2023 et au premier semestre 2024, 78 actions promotionnelles ont été organisées, dont
52 participations à des forums internationaux et salons spécialisés, ciblant 20 marchés
internationaux, dont 5 marchés stratégiques.

M



RAPPORT SUR LES ETABLISSEMENTS ET ENTREPRISES PUBLICS

Le budget total de 2023 était de 488 MDH, avec 380 MDH pour l'exploitation et 108 MDH
pour l'investissement, réalisé à hauteur, respectivement, de 77% et 37%.

Pour 2024, le budget total prévu est de 655 MDH, répartis entre 496 MDH pour l'exploitation
et 159 MDH pour l’investissement, avec des prévisions de réalisation respectives de 80% et
70%.

Pour la période 2025-2027, l'AMDIE prévoit l'intensification de ses efforts pour la réalisation
d'un programme ambitieux de promotion des exportations et de développement des
investissements à travers l'organisation de plus de 200 actions et manifestations par an.

IV. FONDS ET INSTITUTIONS FINANCIERES PUBLIQUES

IV.1. Fonds Hassan Il pour le Développement Economique et Social

Les engagements cumulés du Fonds. depuis sa création, ont atteint 53.446 MDH, ce qui
correspond, pour la période 2000-2023, à un rythme d'engagement annuel moyen de l'ordre
de 2.300 MDH.

Le montant de ces engagements tient compte de la contribution de 2.000 MDH accordée au
« fonds spécial dédié à la gestion des effets du séisme qu'a connu le Royaume du Maroc » et
de l’annulation d'une somme de 62 MDH suite à la clôture de certaines conventions
notamment l’appui au développement touristique du littoral Mdiq-Fnideq pour un montant de
50 MDH.

Les décaissements effectués en 2023 ont atteint un montant de 3.523 MDH et concernent
notamment :

- 2.000 MDH sous forme de contribution financière au Fonds Spécial pour la gestion des
effets du tremblement de terre ayant touché le Royaume du Maroc ;

- 854 MDH sous forme d’apports en capital dans le cadre de la réalisation des CMC ;
- 170 MDH pour le programme de mise en valeur de la Médina de Salé 2019-2023 ;

- 130 MDHautitre du programme d’appui et de financement de l’entrepreneuriat dans le
monde rural « Al Moustatmir Al Qarawi » ;

- 100 MDH au titre du programme complémentaire de mise en valeur de la Médina
d'Essaouira 2018-2023.

Le montant cumulé des décaissements a atteint, à fin 2023, un cumul de 43.281 MDH
représentant 81% des engagements souscrits depuis la création du Fonds.

Les recettes de 2023 ont été établies à 1.151 MDH, dont 519 MDH au titre des produits
financiers, 357 MDH au titre du remboursement des avances et 275 MDH concernant la
restitution d'une partie des arriérés au titre de l'impôt sur les produits de placement à revenus
Fixes (IPPRF).

S



Ainsi, les ressources financières cumulées du Fonds Hassan Il, à fin 2023, ont atteint une
somme globale de 64.748 MDH répartie comme suit

- Versements de l’Etat : 44.095 MDH
-  Produits financiers : 14.132 MDH
-  Divers (restitution de l'IPPRF) : 1.694 MDH
-  Remboursement des avances, des prêts et autres : 4.827 MDH

Le 1° semestre de l’année 2024 n'a enregistré aucun engagement additionnel. À ce titre, les
décaissements réalisés, à fin juin 2024, ont atteint un montant de 509 MDH et ont concerné
notamment le projet CMC (413 MDH), le programme de la mise en valeur de la médina de
Rabat (31 MDH), le programme de traitement des constructions menaçant ruine dans
l'ancienne médina de Casablanca (3O MDH) ainsi que les déblocages effectués dans le cadre
de l’appui à l'investissement industriel (26 MDH).

En prévision de clôture de 2024, les décaissements devraient atteindre 2.611 MDH et qui se
rapportent principalement aux programmes suivants :

- 760 MDH au titre du programme de financement accordé pour l’Entrepreneuriat dans
le monde rural « AL MOUSTATMIR AL QARAWI » ;

- 455 MDH au titre des programmes de réhabilitation et de mise en valeur de médinas ;

- 376 MDH au titre du programme de financement des Cités des Métiers et des
Compétences.

Sur la période 2025-2027, les décaissements sont estimés comme suit : 1837 MDH en 2025,
1.673 MDH en 2026 et 2.234 MDH en 2027.

IV.2. Fonds Mohammed VI pour l’'Investissement

Depuis sa création, |le FM61 intensifie les diligences et les concertations pour la mise en œuvre
de son plan d’action visant l'accélération des investissements dans les secteurs productifs et
prioritaires, en s'appuyant sur une approche axée sur la mobilisation des financements du
secteur privé, Ce plan d'action est structuré en deux dimensions :

1. Prises de participation dans les grands projets stratégiques et d’infrastructures
dans l’objectif de réaliser des projets structurants et renforcer la souveraineté nationale
dans des secteurs clés. Les concertations sont en cours avec les donneurs d'ordre
publics de projets d'infrastructures pour accélérer l’identification et la mise en œuvre
de projets structurants et attirer les investisseurs privés dans le tour de table et le
financement de ces projets ;

2. Fonds thématiques et sectoriels : à l’issue de l'Appel à Manifestation d'Intérêt (AMD
lancé en 2023, le Fonds a sélectionné 15 sociétés de gestion des fonds thématiques avec
une première enveloppe de 4,5 MMDH, mobilisant 13,5 MMDH supplémentaires auprès
des bailleurs de fonds. Ces fonds, d'une taille globale de 18 MMDH, cibleront divers
secteurs clés comme les PME, l'industrie, le tourisme et l’agriculture, avec un impact
attendu de 50 MMDH sur cinq ans.

yN



RAPPORT SUR LES ETABLISSEMENTS ET ENTREPRISES PUBI| s

De même, le Fonds est en cours d’évaluation des résultats d’Un autre AMI, lancé en
concertation avec le Département chargé de la transition numérique et la CDG, pour la
sélection de sociétés de gestion des fonds startups afin de soutenir le développement de
l'écosystème de l'innovation et des nouvelles technologies.

En vue de la diversification des instruments de financements pour réponde aux besoins
des entreprises, le FM61 a lancé, en mars 2024, le fonds Cap Access avec une enveloppe de
4 MMDH pour soutenir les entreprises marocaines en besoin de fonds propres. Ce fonds, géré
par la SNGFE, collabore avec les banques pour distribuer des produits de dette subordonnée,
facilitant ainsi l'accès au financement pour les entreprises avec des projets d'investissement
viables.

Le FM&I a lancé également un autre produit nommé « Cap Hospitality » visant à accélérer la
Mmise à niveau des Etablissements Hôteliers Touristiques Classés (EHTC), avec pour objectif la
modernisation de 25.000 chambres d'hôtels en anticipation des événements sportifs
internationaux que le Maroc accueillera.

IV.3. Fonds d’Equipement Communal

Au terme de l'exercice 2023, les attributions de prêts par le FEC ont atteint plus de
2,41 MMDH, en recul de 51% par rapport à 2022 et ont concerné le financement de 46 projets
dans 10 secteurs d’intervention et qui portent sur un investissement total de plus de 5,3 MMDH
au profit de 21 Collectivités Territoriales.

Quant aux engagements de prêts à fin 2023, ils ont enregistré un niveau exceptionnel de plus
de 4,3 MMDH, en hausse de 60% par rapport à 2022 et ce, compte tenu du financement de
l'interconnexion des deux bassins du Sebou et du Bouregreg suite au stress hydrique.

Ces engagements ont porté sur la réalisation de 55 projets, couvrant 10 secteurs
d'intervention au profit de 25 Collectivités Territoriales, pour un investissement global de près
de 10,7 MMDH.

Les décaissements de prêts, au titre de 2023, se sont établis à plus de 4 MMDH, en hausse
de plus de 38% par rapport à l'année précédente. Ces financements ont porté sur la réalisation
de 117 projets couvrant différents secteurs d'infrastructures et de superstructures tant en
milieu urbain que rural.

Les indicateurs financiers du FEC se présentent comme suit :

- Le Produit Net Bancaire (PNB) s'est établi à 669 MDH à fin 2023, en quasi-stagnation
par rapport au niveau enregistré l'année dernière :

- Le Résultat Net (RN) a atteint 199 MDH au titre de l'exercice 2023, en baisse de 41% par
rapport à 2022, tenant compte de la contribution de la Banque au Fonds spécial de la
gestion du tremblement de Terre d'Al Haouz.

Quant aux prévisions d'activité relatives aux exercices 2024 et 2025, elles se présentent
comme suit :

- Le montant des Engagements serait de 3.100 MDH en 2024 et de 3.263 MDH au terme
de l’année 2025 ;

S



- Les Décaissements se situeraient à 2.700 MDH en 2024 pour atteindre 3.000 MDH en
2025:

- Le Produit Net Bancaire (PNB) serait de 675 MDH en 2024 et de 680 MDH à fin 2025 ;
- Le Résultat Net (RN) s’établirait à 355 MDH en 2024 et atteindrait 358 MDH en 2025.
IV.4. Caisse de Dépôt et de Gestion

L'année 2024 marque le lancement par la CDG de son plan stratégique « CAP 2030 », articulé
autour de quatre axes complémentaires : redéfinir son positionnement dans le secteur financier,
explorer de nouveaux domaines d'intervention, renforcer les instruments associés et
restructurer son portefeuille historique, tout en dynamisant ses ressources.

Dans ce cadre, la CDG a engagé plusieurs chantiers dans les domaines prioritaires suivants :

- _ L'investissement dans de nouveaux secteurs tels que l’eau, l'efficacité énergétique, la
souveraineté alimentaire et l’infrastructure haut débit ;

- L'investissement dans les domaines historiques de la CDG, incluant l’immobilier locatif,
la promotion immobilière, le développement de zones d'activités économiques et le
capital-investissement ;

- L'investissement dans les infrastructures nécessaires pour la Coupe du monde 2030, à
travers la signature de partenariats stratégiques visant à renforcer les infrastructures et
améliorer les services du pays.

Sur le plan financier, le produit net bancaire (PNB) a atteint 1.044 MDH en 2023 contre
589 MDH en 2022, en hausse de 77%. Le résultat net s’est établi à -884 MDH, en hausse de
685 MDH par rapport à l'année précédente.

A fin juin 2024, le PNB s’est élevé à 446 MDH, marquant une baisse de 19,8% par rapport à la
même période de 2023, alors que le résultat net a atteint 565 MDH, en hausse de 9,9% par
rapport à 2023.

Le PNB consolidé s'est établi à 10.254 MDH en 2023 contre 5.653 MDH à fin 2022, en hausse
de 81%, tandis que le résultat net part du groupe a atteint 1.371 MDH contre -2.022 MDH à fin
2022.

Les projections pour 2025-2027 prévoient, au niveau social, un résultat net de 1.794 MDH pour
2025, 1.018 MDH pour 2026, et 745,65 MDH pour 2027.

Le programme d'investissement consolidé du Groupe CDG s'est élevé à 3.417 MDH en 2023 et
devrait atteindre 5.461,2 MDH en 2024. Les prévisions pour 2025, 2026 et 2027 sont
respectivement de 4.888 MDH, de 2.718,4 MDH et de 2.794,8 MDH.

IV.5. Société Nationale de Garantie et de Financement de l'Entreprise

En 2023, l’activité globale de la SNGFE a permis de mobiliser un volume de crédits de
54,14 MMDH pour un engagement de plus de 35,1 MMDH au titre de 86.790 opérations, en
faveur des entreprises et des particuliers.

VN



RAPPORT SUR LES ETABLISSEMENTS ET ENTREPRISES PUBI| s

Les engagements au titre de l'activité « entreprises » en 2023 ont atteint 32,8 MMDH,
permettant la mobilisation d'un volume de crédits de 50,2 MMDH pour financer plus de
68.420 opérations en faveur des entreprises.

Le programme Intelaka, lancé en février 2020 suite aux Hautes Orientations Royales pour
faciliter l’accès au financement des jeunes porteurs de projets, autoentrepreneurs et TPE a
permis l’octroi de plus de 2.670 crédits pour un volume de 1 MMDH en 2023.

L'activité de crédit par décaissement, visant à appuyer des programmes d’'investissement pour
l'économie verte et la rénovation hôtelière a également enregistré un volume d'engagements
de 254,6 MDH pour 10.043 opérations en 2023.

Le programme de Garantie en faveur des EEP (FGEEP) a permis de garantir 7 crédits pour un
montant global de près de 10 MMDH.

Le Fonds Innov Invest (FII), destiné à soutenir les projets innovants, a réalisé 11 opérations
d'investissement en 2023, totalisant près de 96 MDH. Le FII a également consacré 242,5 MDH
pour structurer trois fonds d’amorçage et de capital risque, mobilisant près de 700 MDH.

En 2023, l’activité de garantie en faveur des particuliers a concerné 17.983 bénéficiaires, avec
des crédits mobilisés de plus de 3,3 MMDH et des engagements de près de 2 MMDH.
Les produits FOGARIM et FOGALOGE ont joué un rôle clé dans cette activité.

La fenêtre participative « DAAMA TAMWIL » a enregistré une croissance de 72% en 2023, avec
des engagements de 340 MDH.

Le bilan de la SNGFE au 31 décembre 2023 s’élève à 13,1 MMDH, contre 1,1 MMDH en 2022,
résultant du transfert, intervenu le 1°" janvier 2023, des actifs et passifs ainsi que des
engagements hors bilan des cinq fonds gérés initialement pour le compte de l'Etat. Le PNB a
atteint 922,43 MDH et le résultat net s'est établi à 517 MDH, en forte augmentation par rapport
à l’année précédente.

Pour la période 2024-2025, les prévisions de production de la SNGFE totalisent 36.011 MDH
en 2024 et 37.844 MDH en 2025.



3ème Partie: MISE EN ŒUVRE DE LA
REFORME DU SECTEUR DES EEP

Le chantier de réforme des EEP a été érigé comme priorité nationale suite aux Hautes
Orientations Royales, notamment celles contenues dans le Discours Royal à l'occasion de la
Fête du Trône du 29 juillet 2020, appelant à réaliser avec diligence une réforme profonde du
secteur public pour corriger les dysfonctionnements structurels des EEP, garantir une
complémentarité et une cohérence optimales entre leurs missions respectives et, /n fine,
rehausser leur efficience économique et sociale.

Les contours de ce chantier de réforme ont été définis à travers deux textes de référence
publiés en juillet 2021, à savoir :

- Laloi-cadre n° 50-21 relative à la réforme des EEP ;

-  La loi n° 82-20 portant création de l'Agence Nationale de Gestion Stratégique des
Participations de l’Etat et de suivi des performances des Etablissements et Entreprises
Publics (ANGSPE).

Ce chantier de réforme tient également compte de la nécessité de s'aligner sur les dispositions
du projet d'amendement de la Loi Organique relative à la Loi de Finances qui prévoit
l'élargissement de son champ d’application aux établissements publics non marchands.

Dans le cadre de l'implémentation de ce chantier et parallèlement au plan d'action engagé par
l'Agence Nationale pour la mise en œuvre de la Politique Actionnariale de l'Etat et des mesures
de réforme à engager pour les EEP de son périmètre, le Ministère de l'Economie et des
Finances a adopté une feuille de route déclinant de manière intégrée et exhaustive, l'ensemble
des mesures à engager pour la mise en œuvre de cette réforme pour le secteur des EEP du
périmètre piloté par ce Ministère.

Cette feuille de route a été conçue sur la base d’une approche reposant sur une cohérence
globale et une convergence de l'ensemble des actions envisagées autour des objectifs de la
réforme notamment la rationalisation de la taille du portefeuille public, l'amélioration de la
qualité de service, la valorisation de synergies et des complémentarités, le renforcement des
performances, l'amélioration de la qualité de la gestion et de la gouvernance, l’optimisation
des modèles économiques et financiers des EEP, l’ancrage des principes de transparence et
de reddition des comptes et l'allègement de la pression sur le budget de l'Etat.

Cette feuille de route intègre également un plan d’action, en cours de réalisation, pour la
refonte du dispositif de gestion des opérations de liquidation des EEP.

Ainsi, la présente section fait le point sur l'état d'avancement du projet de réforme à travers
les axes ci-après :

-  Elaboration des textes juridiques prévus dans le cadre de la réforme ;

- Plan d’action d'amélioration de la gouvernance et opérations de restructuration des EEP
du périmètre de l'ANGSPE ;

A



RAPPORT SUR LES ETABLISSEMENTS ET ENTREPRISES PUBLICS

-  Programme des opérations de restructuration et actions d’amélioration de la
gouvernance des EEP du périmètre piloté par le MEF ;

- Refonte du dispositif encadrant les opérations de liquidation.

L'état d’avancement des différentes composantes de ce projet de réforme peut être récapitulé
comme suit :

I. Elaboration des textes juridiques prévus dans le cadre de la
réforme

Outre la mise en place et l’exécution d’un programme d'opérations de restructuration des EEP,
le chantier de la réforme des EEP à mettre en œuvre, conformément à la loi-cadre précitée,
sur une période de 5 ans (2021-2026) porte sur :

- La mise en place des textes législatifs et réglementaires tout en s’alignant sur les
dispositions du projet d'amendement de la Loi Organique relative à la Loi de Finances ;

- Lamise en place et le déploiement de la Politique Actionnariale de l'Etat.
1.1. Réforme de là Loi Organique relative à la Loi de Finances

Dans le cadre de l'accompagnement du chantier de réforme des finances publiques et tout en
s’'inspirant des meilleures pratiques internationales, le Gouvernement prépare un projet
d'amendement de la Loi Organique relative à [a Loi de Finances (LOF) en vue de consolider la
transparence et de renforcer la soutenabilité des finances de l’Etat notamment à travers
l'intégration dans [e champ d'application de ladite Loi Organique, les établissements publics
non marchands investis de missions de service public et considérés ainsi comme un
prolongement de l’Etat.

A ce titre et selon le projet d'amendement, les opérations des budgets des établissements
publics non marchands seront prévues, autorisées, exécutées et contrôlées dans les mêmes
conditions que les opérations du budget général, notamment en matière d'application :

- Des règles financières et budgétaires : ces règles englobent notamment la prévision
des ressources et des charges par la loi de finances tout en adoptant le caractère
évaluatif des budgets ;

- De l’approche de performance axée sur les résultats : à travers notamment l’adoption
de la nomenclature programmatique, ainsi que la concordance entre les programmes
desdits étahlissements et les programmes de rattachement relevant des Départements
de tutelle ;

- Des règles comptables, incluant la tenue d’une comptabilité budgétaire, en plus
d’une comptabilité générale.

1.2. Textes législatifs et réglementaires pour le déploiement de la loi-
cadre n° 50-21

La feuille de route établie dans ce cadre porte sur un total de 19 textes législatifs et
réglementaires dont 8 textes ont été adoptés et publiés, 4 ont été mis dans le circuit

d'approbation et 7 projets de textes sont en cours d'élaboration.



La situation détaillée de ces textes peut être récapitulée comme suit :

> Huit (8) textes législatifs et réglementaires ont été approuvés et publiés au Bu//etin
Officiel :

-  Orientations Stratégiques de la Politique Actionnariale de l’Etat approuvées par le
Conseil des Ministres tenu le 1er juin 2024 ;

-  Loi n° 76-20 portant création du Fonds Mohammed VI pour l'Investissement (FM6D
promulguée par le Dahir n° 1-20-103 du 31 décembre 2020 ;

-  Loi n° 40-22 fixant le nombre d'administrateurs indépendants ainsi que les conditions
et la procédure de leur nomination dans les organes délibérants des entreprises
publiques promulguée par le Dahir n° 1-23-52 du 12 juillet 2023 ;

- Décret n° 2-22-581 du 26 janvier 2023 relatif aux modalités de nomination des
représentants de l'Etat siégeant au sein des organes délibérants des EEP ;

- Décret n° 2-22-582 du 26 janvier 2023 relatif aux modalités de nomination et de
rémunération des membres indépendants siégeant au sein des organes délibérants des
Etablissements Publics ;

- Décret n° 2-22-796 du 26 janvier 2023 relatif à la composition de l'Instance de
concertation sur la Politique Actionnariale de l'Etat et son mode de fonctionnement ;

-  Décret n° 2-2-964 du 08 décembre 2022 relatif à la nomination des représentants de
l’Etat dans le Conseil d'Administration de l'ANGSPE ;

-  Décret n° 2-23-128 du 11 avril 2023 complétant le décret n° 2-13-24 du 26 février 2013
fixant la liste des établissements publics soumis au contrôle d'accompagnement.

S Quatre (4) projets de textes législatifs et règlementaires sont mis dans le circuit
d’approbation :

-  Projet de loi fixant les conditions de restructuration des sociétés de développement
relevant des collectivités territoriales ;

-  Projet de la Politique Actionnariale de l'Etat ;

-  Projet de décret fixant les cas dans lesquels des contrats-programmes doivent être
conclus entre l'Etat et les EEP ;

-  Projet de décret portant approbation du Code des bonnes pratiques de gouvernance
des EEP.

-

> Sept (7) projets de textes en cours d'élaboration

-  Projet de loi relatif à la réforme de la gouvernance et du contrôle financier des EEP, ce
projet de loi est en cours de finalisation en concertation avec les partenaires concernés
pour recueillir leurs avis et propositions avant de le mettre dans le circuit d'adoption ;

- Projet de loi visant la mise en place d’'un régime des privatisations à travers
l'amendement de la loi n° 39-89 autorisant le transfert d'entreprises publiques au
secteur privé ;

A



RAPPORT SUR LES ETABLISSEMENTS ET ENTREPRISES PUBI| s

-  Projet de loi portant création de l'Instance centrale de la liquidation des EEP ;

-  Projet de loi relatif aux mesures législatives devant régir les opérations de création des
entreprises publiques dont la création ne relève pas du domaine de la loi et les prises
de participation des EEP dans le capital des entreprises privées ;

-  Projet de décret relatif à l’'évaluation du domaine public mis à [a disposition des EEP ;

- Projet de décret relatif aux modalités d'’émission de l'avis de l'ANGSPE sur les
opérations de capital et de portefeuille prévues au niveau des articles 7 et 8 de la loi n°
82-20 ;

- Projet d'arrêté approuvant le nouveau qguide méthodologique relatif à la
Contractualisation entre l'Etat et les EEP y compris le modèle type de contrat-
programme.

(| convient de noter que ces textes législatifs et règlementaires seront mis dans le circuit
d'adoption dès l’achèvement des études et des consultations y afférentes.

1.3. Politique Actionnariale de l’Etat

La Politique Actionnariale de l'Etat (PAE), portée par l'ANGSPE conformément à la loi n° 82-
20 portant sa création, est l’un des projets structurants de la réforme du secteur des EEP, telle
que définie par la loi-cadre n° 50-21 relative à la réforme des EEP. Cette politique traduit les
Orientations Stratégiques et les objectifs globaux de l'actionnariat de l’Etat, son rôle dans la
gouvernance des EEP et la manière dont il met en œuvre cette politique. Elle permet de définir
d'une façon claire et durable le rôle, [e positionnement et le mode d'intervention de l'Etat en
tant qu'actionnaire.

Le Conseil des Ministres, réuni sous la présidence de Sa Majesté le Roi Mohammed VI, que
Dieu L'assiste, le premier juin 2024, a approuvé les Orientations Stratégiques de la Politique
Actionnariale de l'Etat. Ces Orientations Stratégiques définissent les priorités, les objectifs et
les principes directeurs qui guideront la gestion et l'évolution du secteur des EEP. Elles offrent
un cadre de référence stable et prévisible, clarifiant les attentes de l'État en tant qu'actionnaire.

Dans un contexte national et international en mutation, ces Orientations Stratégiques visent à
doter le secteur des EEP d'une Politique Actionnariale dynamique et agile. Elles permettront
de relever les défis actuels et futurs, tout en assurant un pilotage stratégique performant pour
ces entités aux forts enjeux socio-économiques.

Les Orientations Stratégiques, au nombre de sept, se déclinent comme suit :

» Orientation 1 : Consacrer le secteur des EEP comme levier stratégique pour la
consolidation de la souveraineté nationale à travers le soutien des efforts de l'Etat dans
un ensemble de secteurs vitaux, en particulier l'énergie, la santé, l'eau, la sécurité
alimentaire, l’'environnement, la connectivité et la mobilité ;

» Orientation 2 : Faire du secteur des EEP un moteur de l’intégration continentale et
internationale à même de contribuer à répondre aux enjeux géostratégiques et garantir
les intérêts du Royaume et de contribuer au renforcement de la coopération Sud-Sud
en particulier avec les pays africains frères ;

S



» Orientation 3 : Faire du secteur des EEP un pilier pour la dynamisation de
l'investissement privé, à travers la mise en place de partenariats volontaristes avec le
secteur privé dans une logique de complémentarité et de renforcement de la
contribution du secteur privé dans la dynamique économique nationale ;

» Orientation 4 : Faire du secteur des EEP un catalyseur d'une économie compétitive et
un véhicule de partage de la valeur ajoutée et de promotion de l’emploi productif, à
travers notamment le soutien de modèles économiques viables et agiles en phase avec
les exigences de régulation, l’'environnement concurrentiel et les opportunités de
marchés ;

» Orientation 5 : Eriger le secteur des EEP en acteur actif de l'équité territoriale au service
de l'inclusion économique et sociale, financière et numérique, et ce dans le cadre de
régionalisation avancée tout en assurant une équité des territoires et en garantissant un
accès équitable des citoyens à des services publics de qualité ;

»

» Orientation 6 : Faire du secteur des EEP un gestionnaire responsable des ressources
s'inscrivant ainsi dans les Objectifs de Développement Durable à travers le
renforcement de la contribution des EEP en faveur de la promotion d'une gestion
responsable des ressources naturelles et du raffermissement de la résilience du pays
face aux défis du changement climatique ;

» Orientation 7 : Renforcer le rôle exemplaire des EEP en matière de gouvernance et de
performance en veillant à mettre en place une gestion active de son portefeuille public
de ses participations ou de désengagement, dans l'objectif d’une valorisation optimale
du patrimoine matériel et immatériel des EEP et d'une amélioration de leurs
performances.

Dans ce cadre, et suite à l’approbation des Orientations Stratégiques, l'ANGSPE a procédé à
l'élaboration du projet de PAE ainsi que du projet de son plan de mise en œuvre qui ont été
délibérés par le Conseil d'Administration de l'Agence lors de sa réunion du O3 juillet 2024.

Ainsi, et suite à l'avis favorable émis, en date du 19/09/2024, par l’Instance de Concertation
sur la PAE, cette politique sera soumise à l'approbation du Conseil du Gouvernement, ce qui
permettra à l’'Agence de lancer son déploiement.

1.4. Réforme du dispositif de gouvernance et de contrôle financier de
l’Etat sur les EEP

Ce projet de loi est en cours d’élaboration dans le cadre d’une approche reposant sur les
Hautes Orientations Royales et les recommandations du Nouveau Modèle de Développement
(NMD) tout en assurant un alignement sur les dispositions de la loi-cadre n° 50-21 relative à la
réforme des EEP.

Le projet de texte révèle cinq inflexions majeures :

- Le renforcement de la maîtrise du portefeuille public par la mise en place d’un registre
de ce portefeuille ;

- L'ancrage des bonnes pratiques de gouvernance ;

-  La généralisation progressive du contrôle financier ;

yN



RAPPORT SUR LES ETABLISSEMENTS ET ENTREPRISES PUBLICS

- La modulation du contrôle et sa dynamisation sur la base de la qualité de la
gouvernance et de la gestion des EEP ;

- _ Le renforcement de la transparence et de la reddition des comptes.

A travers ses nouveaux apports, le projet de loi vise à atteindre les principaux objectifs ci-
après :

-  L'ancrage des pratiques de bonne gouvernance notamment par la responsabilisation
de l'organe délibérant sur le pilotage stratégique de l'EEP en harmonie avec les
orientations des politiques publiques, le renforcement des dispositifs de gestion des
risques, l'accélération du processus de digitalisation, la généralisation de la
contractualisation interne et la mise en place de plans de communication consacrant les
règles de reddition des comptes et de transparence ;

- _ L'allégement et la modulation du contrôle financier pour l’orienter principalement vers
l'appréciation des performances, l'évaluation de la gouvernance et la prévention des
risques en consacrant les objectifs de protection des deniers publics et des patrimoines
des EEP ;

- Lamise en place d’un registre visant Un suivi régulier, intégré et exhaustif de l'évolution
du portefeuille public et de sa performance.

Ce projet de texte tiendra compte du projet d'amendement de la LOF et sera partagé avec les
principaux partenaires pour sa mise au point avant son introduction dans le circuit d'adoption.

Il. Déploiement de la réforme des EEP du périmètre de
l’ANGSPE

Depuis son opérationnalisation, l'ANGSPE a défini un plan d’action qui s'articule autour de
plusieurs chantiers prioritaires visant notamment à renforcer la gouvernance, à accompagner
les opérations de Transformation en Sociétés Anonymes (TSA), à conduire les restructurations
sectorielles, à contribuer à la mise en place des textes législatifs et réglementaires concernant
la réforme, à encadrer l'évolution du portefeuille relevant de son périmètre, à mettre en œuvre
la consolidation des comptes et à mettre en place un dispositif de pilotage de la performance
des EEP de son périmètre.

L’état d’avancement du plan d'action précité peut être retracé comme suit :

S Amélioration de la gouvernance des EEP du périmètre stratégique

Les principales actions engagées en matière d’amélioration de la gouvernance des EEP du
périmètre de l'Agence concernent ce qui suit :

-  La cooptation des représentants de l'ANGSPE, en tant que représentants de l'Etat
actionnaire au niveau des organes de gouvernance des entités faisant partie de son
périmètre ;

-  L'élaboration et la diffusion en juillet 2023 d'une procédure de désignation des
membres et administrateurs indépendants dans les organes délibérants des EEP avec
comme objectif prioritaire la nomination d’'un ou plusieurs Administrateurs
Indépendants (AI) dans 34 entreprises publiques. Dans ce cadre, 26 EEP (75% de

VS



l'objectif) ont adopté ou entamé l'adoption de la procédure ou prévoient de le faire en
2024, en soulignant que sept {7) entreprises publiques disposent déjà d’AI :

-  L'institution, suite à la cooptation des représentants de l'Agence dans les organes
délibérants des EEP de son périmètre, de 27 comités spécialisés outre la revue des
missions de 6 comités pour y intégrer la dimension risque ou les aspects liés à la
nomination et à la rémunération ;

-  Le lancement de la digitalisation des organes de gouvernance dans l’objectif de
pérenniser les bonnes pratiques de gouvernance en favorisant la sécurité, la
confidentialité et la traçabilité des processus de décisions et de remontée de
l'information.

En outre, l'ANGSPE a lancé, le 12 septembre 2024, un projet ambitieux visant à promouvoir les
bonnes pratiques de gouvernance au sein des EEP, Ce projet marque le coup d'envoi d'une
transformation significative dans le cadre de la réforme du secteur des EEP.

Cette transformation repose sur une approche globale de la gouvernance, articulée autour de
quatre axes fondamentaux : (i) le renforcement du cadre juridique et réglementaire, Çii) les
bonnes pratiques de gouvernance et de fonctionnement des organes délibérants et des
comités spécialisés, Çiii) la digitalisation des instances de gouvernance, et (iv) la montée en
compétence à travers la formation ainsi que la conduite du changement.

Le lancement du projet a également été l'occasion d’annoncer « GUIDE », le premier label
marocain dédié à la gouvernance des EEP. Ce label, inspiré par la norme internationale ISO
37000 et développé en partenariat avec l'Institut Marocain de Normalisation (IMANOR), a pour
objectif d’instaurer un nouveau standard d’excellence et de transparence dans le secteur
public, en encourageant les meilleures pratiques de gouvernance.

L'Agence prévoit la poursuite de l’implémentation de sa feuille de route en y intégrant d'autres
actions tenant notamment à l’évaluation des organes de gouvernance, à la conclusion de
contrats de performance entre ces organes et les dirigeants des EEP et la formation des
administrateurs de l'Agence appelés à siéger dans lesdits organes délibérants.

S Opérations de restructuration

Les principales opérations de restructuration concernent les EEP opérant dans les secteurs
suivants :

Audiovisuel : la restructuration des EEP de ce secteur vise leur consolidation en un pôle
unique et intégré dans l’objectif de créer une holding audiovisuelle publique viable et pérenne,
capable de prospérer dans le paysage médiatique en constante évolution. L'ANGSPE assure
le pilotage et le suivi de la mise en œuvre de cette restructuration et coordonne avec
l'ensemble des partenaires concernés.

Dans ce cadre, la SNRT a procédé, en avril 2024, à l’acquisition de 86,3% du capital de Radio
Méditerranée Internationale (RMI), et à l’acquisition, en juillet 2024, de 100% de MEDI1 TV. D’un
autre côté, le processus de rattachement de SOREAD 2M à la SNRT est en cours. Les
prochaines étapes clés comprennent ainsi [e parachèvement du rattachement de SOREAD 2M
à la SNRT et le lancement d’une étude pour la mise en œuvre opérationnelle de la
restructuration en vue de la création d'une holding audiovisuelle publique forte, compétitive

A



RAPPORT SUR LES ETABLISSEMENTS ET ENTREPRISES PUBI| s

et mieux équipée pour relever les défis de l’avenir de ce secteur, et d'en définir le business
model et la gouvernance.

Energie : Dans ce secteur, plusieurs chantiers majeurs ont été menés dans le cadre de sa
restructuration institutionnelle :

-  Leprocessus de création des Sociétés Régionales Multiservices (SRM), qui bénéficieront
du transfert des actifs de l'ONEE, en contrepartie de la prise en charge du passif y
associé ;

-  Lestravaux de la refonte de la convention tripartite Etat-ONEE-MASEN, datant de 2010,
visant à arrêter de nouvelles conditions techniques et commerciales de réalisation des
projets des énergies renouvelables (EnR), ce qui devra améliorer les synergies entre les
deux entités dans la perspective d’atteindre les objectifs fixés en matière de mix
énergétique, en préservant les fondamentaux financiers de l'ONEE et de MASEN et en
rationalisant le recours aux finances publiques :

-  La relance du processus de transfert des actifs des énergies renouvelables de l'ONEE à
MASEN et la mise en œuvre sur proposition de l'ANGSPE d’une résolution transitoire au
différend de facturation des projets « Noor PVI» en vue d'y apporter une solution
définitive dans le cadre de la nouvelle convention tripartite ;

-  La poursuite dans des conditions globalement satisfaisantes de la mise en œuvre du
protocole d'accord entre l'État et l'ONEE, conclu en novembre 2022, sous la supervision
du Comité de Suivi, présidé par l'ANGSPE, a permis d'améliorer la soutenabilité
financière de l'Office. Dans ce cadre, et afin de consolider sa situation bilancielle, 'ONEE
a lancé plusieurs études pour la valorisation de ses actifs, tant ceux liés à la production
que ceux non essentiels à l'exploitation ;

-  Dans le cadre des changements institutionnels ayant touché l'écosystème de l'ONEE,
une étude portant sur la redéfinition du positionnement stratégique de l’Office est en
cours d’exécution, l'ANGSPE en préside le comité de pilotage. De son coté, MASEN a
entrepris la valorisation de ses actifs et le réajustement de ses modes d'intervention, en
vue d'accompagner plus efficacement la montée en puissance des activités et
l'accélération de son plan de développement.

Banques-Finances : L'ANGSPE a relancé le projet d'étude pour mener une réflexion sur un
schéma permettant d'optimiser la participation de l'Etat dans ce secteur et la mise en place
éventuelle d'un pôle financier public annoncé dans le rapport sur les EEP accompagnant le
projet de loi de finance de 2022. L'étude, en cours de lancement, par l'ANGSPE veillera à
prendre en compte les aspects de neutralité concurrentielle, de complémentarité avec les
établissements financiers du secteur privé, ainsi que les synergies et complémentarités,
prônées par la loi cadre n° 50-21 relative à la réforme des EEP, entre les établissements
financiers à capitaux publics.

De même, l'Agence assure l'accompagnement de plusieurs EEP dans la préparation des leurs
projets de restructuration, notamment :

- ONCF: accompagnement dans la conclusion d’un contrat-programme Etat-
ONCF incluant la structuration du financement du projet de la LGV Kenitra-Marrakech.
Ainsi, que dans l'élaboration du projet de texte de transformation de l'Office en SA :

VS



-  ADM : le protocole d’accord, conclu avec l’Etat en octobre 2023, vise à mettre en œuvre
des mesures à court terme contribuant au redressement de la situation financière de la
société, à travers notamment, le remboursement du crédit de TVA. || prévoit également
la mise en place d’une démarche permettant la conclusion d’un nouveau contrat-
programme entre l'Etat et ADM ;

- SNTL : Accompagnement dans la restructuration et le repositionnement stratégique de
la société ;

- RAM : Accompagnement dans l'élaboration du contrat-programme et dans sa mise en
œuvre ;

- Barid Al Maghrib : Accompagnement pour la mise en place d'un nouveau plan
stratégique et l'engagement de la réforme postale instaurant le Service Universel Postal
ainsi que pour l'élaboration d’un schéma de valorisation du patrimoine de BAM en vue
de rentabiliser les fonds propres de l’'ensemble BAM / ABB.

S TIransformation des établissements publics en sociétés anonymes (SA)

Dans le cadre de la mise en œuvre des dispositions de la loi-cadre n° 50-21 relative à la réforme
des EEP, notamment ses articles 16, 17 et 18, et de la loi n° 82-20 portant création de l'ANGSPE,
notamment son article 28, l'Agence accompagne les établissements publics relevant de son
périmètre et exerçant une activité marchande dans leur processus de transformation en
société anonyme. L'objectif étant notamment d’améliorer leur gouvernance, de diversifier leurs
sources de financement et d’accroitre leurs performances. Des dialogues stratégiques ont été
menés à l’initiative de l'Agence avec un premier groupe d'établissements publics qui seront
transformés en SA et ont abouti à :

-  La finalisation des projets de lois de transformation en SA du FEC, la MAP et l'ONP en
vue de leur introduction dans le circuit législatif ;

- La mise en circuit d’adoption des projets de lois de transformation de l'OMPIC et de
l'ONHYM. Celui concernant, l’ONDA est en cours de finalisation :

-  Le lancement d'études de positionnement stratégique d’autres établissements publics
concernés devant permettre de délimiter [e champ d'intervention des futures sociétés
anonymes et leurs relations avec leurs écosystèmes respectifs (ONEE, ANP, LOARC et
Fonds Hassan Il pour le Développement Economique et Social).

S Encadrement de l’évolution du portefeuille des EEP relevant du périmètre de
l’'ANGSPE

Dans l'attente de l'adoption du décret prévu par l’article 9 de la loi n° 82-20 portant création
de l’'ANGSPE, l'Agence a mis en place un dispositif qui encadre le traitement des demandes
d'avis d'autorisations des opérations de portefeuille et sur le capital, engagées par les EEP
relevant du périmètre de l’'Agence.

Ainsi, depuis son opérationnalisation, l'Agence a traité plusieurs demandes d'avis et
d'autorisations concernant ces opérations de portefeuille et sur le capital, émanant soit
directement des EEP, soit à travers le Ministère de l’Economie et des Finances.

Depuis avril 2023, l'ANGSPE a reçu 52 demandes d'avis, dont 38 ont reçu Un avis favorable et
5 un avis défavorable.



RAPPORT SUR LES ETABLISSEMENTS ET ENTREPRISES PUBLICS

Le traitement de ces demandes constitue également l’occasion pour l'Agence d’engager des
réflexions sur le portefeuille des filiales et participations de son périmètre et de proposer des
actions de rationalisation et d’optimisation les concernant.

> Consolidation des comptes de l'Etat actionnaire en normes IFRS

Conformément à l’article 5 de la loi n° 82-20, l'ANGSPE a pour mission d'élaborer des états
financiers consolidés de l’Etat actionnaire reflétant fidèlement l'actif, le passif, la situation
financière et les résultats des établissements et entreprises publics (EEP).

Dans ce cadre, le projet de mise en place de la consolidation des comptes de l'Etat Actionnaire
en normes IFRS, lancé par l'ANGSPE aboutira à un dispositif qui sera déployé et exploité sur
un système d'information dédié, devenant ainsi l'une des principales sources d'information du
système de pilotage de la performance des EEP relevant du périmètre de l’Agence.

L'objectif principal de ce projet est d'instaurer une présentation financière uniforme et
transparente au sein des EEP relevant du périmètre de l'ANGSPE,. || vise également à garantir
la cohérence et l'harmonisation des traitements comptables, la fiabilité et la traçabilité de
l'information produite, la facilitation de la prise de décision éclairée, une meilleure
identification et gestion du risque de l'État actionnaire, ainsi que la facilitation de l'accès au
marché financier international.

La dernière phase du projet est entamée et consiste en la préparation de la collecte des
données relatives aux entités à consolider, le chiffrage des impacts et la production des
comptes consolidés de l'Etat actionnaire.

S Mise en place du dispositif de pilotage de la performance

En vertu de sa mission de gestion et de suivi des performances des EEP, l’'Agence a lancé un
projet visant à mettre en place un dispositif de pilotage de la performance au sein de son
bérimètre. La mise en place de ce dispositif permettra à l'ANGSPE d'évaluer et d'apprécier la
performance des EEP, de mettre en place une architecture de pilotage globale, de normaliser
les outils de pilotage au sein des EEP et de renforcer le dialogue de gestion et la culture de la
performance entre l'ANGSPE et les EEP,

Les différentes structures du périmètre seront évaluées selon une approche multidisciplinaire

englobant non seulement la performance financière et opérationnelle mais aussi la maîtrise

des risques liés à leurs activités et à leurs bilans. Cette évaluation tiendra compte des

spécificités de chaque entité (moyens disponibles, contraintes structurelles, facteurs

conjoncturels, etc.).

III. Programme des opérations de restructuration et actions
d’amélioration de la gouvernance des EEP du périmètre

piloté par le MEF
1H1.1. Approche d’identification des opérations de restructuration

Les opérations de restructuration se caractérisent par des complexités et des difficultés tenant
à plusieurs dimensions d'ordre stratégique, institutionnel, organisationnel et social et
nécessitent des concertations élargies aux ministères de tutelle, aux EEP concernés et aux

autres parties prenantes.



La réussite de ces opérations de restructuration nécessite de s'appuyer sur une vision
sectorielle devant reposer sur la mise en place d’une stratégie de développement sectoriel qui
doit déterminer, entre autres, les objectifs, les moyens et l'organisation institutionnelle et
opérationnelle de mise en œuvre de ladite stratégie sectorielle.

En outre, l'animation institutionnelle du déploiement de la stratégie sectorielle doit être alignée
sur les recommandations du Nouveau Modèle de Développement consacrant le principe de
séparation entre les fonctions de planification, de contrôle et de régulation devant être
maintenues au sein de l'Administration, alors que l’opérationnalisation des activités devrait
être confiées aux EEP ou au secteur privé.

Dans le cadre de cette vision, chaque ministère sectoriel est appelé à proposer, sur la base des
orientations de la stratégie sectorielle dûment actualisée, le schéma institutionnel et
organisationnel adéquat devant intégrer la proposition d'un plan de restructuration et de
repositionnement des EEP relevant du secteur concerné.

Par ailleurs, la restructuration des EEP interpelle les ministères de tutelle en vue de procéder
à l’actualisation voire la revue de leurs stratégies sectorielles, ce qui permettrait de disposer
d'une vision claire sur les opérations de restructuration à engager pour les EEP relevant de
leurs secteurs respectifs.

Les cas des secteurs de l'habitat et de l'urbanisme ainsi que celui de la santé sont illustratifs,
dans la mesure où ces deux secteurs ont arrêté sur la base d’une vision sectorielle, le schéma
institutionnel cible devant porter la stratégie sectorielle. IIs ont procédé, à cet effet, par voie
législative, à la mise en place d'un plan de restructuration des EEP sous leur tutelle, en
cohérence avec la réorganisation préconisée pour leurs secteurs respectifs.

Dans ce cadre, le MEF a engagé des concertations avec certains Départements, les EEP sous
leur tutelle et les parties prenantes pour mettre en place un programme de restructuration des
EEP en fonction des enjeux stratégiques, financiers, économiques et opérationnels des
stratégies sectorielles et des organismes concernés.

Ces concertations sont menées selon une approche reposant sur des critères tenant
notamment au renforcement de l’efficience économique et sociale, à l’amélioration de la
qualité de service, à la valorisation des synergies et des complémentarités, à la suppression
des chevauchements de missions des acteurs publics, à la réduction de l’appel au budget de
l'Etat et au retrait des marchés matures qui peuvent être mieux portés par le secteur privé.

Cette approche tient également au respect des principes énoncés par la loi-cadre n° 50-21
précitée notamment en termes de progressivité dans la mise en œuvre, de préservation des
droits acquis ainsi que la concertation avec l’ensemble des acteurs concernés.

Dans ce cadre, des concertations ont été engagées avec plus 10 Départements sectoriels et
des réunions ont été tenues au cours du premier semestre 2024, en vue d'examiner les
Oopérations de restructuration proposées et d'arrêter une vision partagée autour du
programme de réforme à soumettre à la validation avant le lancement de son exécution.

Ce programme de restructuration intègre aussi les opérations de restructuration identifiées
dans le cadre des opérations des audits externes menées par le MEF et qui ont été focalisées,

A



RAPPORT SUR LES ETABLISSEMENTS ET ENTREPRISES PUBLICS

au cours des dernières années, sur les audits stratégiques et de réforme institutionnelle et
organisationnelle

Les travaux réalisés, à date, ont permis d’identifier un programme global d'opérations de
restructuration, réparties en deux catégories d’opérations :

-  Les opérations de restructuration en cours d'exécution ou ayant un niveau de maturité
avancé et qui concernent une soixantaine d'EEP ;

-  Les opérations en cours d'évaluation, de réflexion et de concertation et qui n’ont pas
encore atteint le niveau de maturité requis et qui nécessitent, par conséquent, des
analyses ct des concertations approfondies.

En plus, les concertations engagées avec les EEP ont permis de mettre en place un programme
d'actions spécifiques visant l’amélioration de leur gouvernance, de leur contrôle financier ainsi
que d'autres actions d'appui notamment en matière de recouvrement des créances.

IHM.2. Présentation des opérations de restructuration

Les programmes des opérations de restructuration et des actions spécifiques peuvent être
présentés comme suit :

S Opérations en cours d'exécution ou ayant un niveau de maturité avancé
(soixantainc d’EEP):

-  Secteur de la santé : le plan de restructuration engagé à travers la loi-cadre n° 06-22
relative au système national de santé, porte sur la création de la Haute Autorité de la
Santé (HAS), de l'Agence marocaine des médicaments et des produits de santé, de
l'Agence marocaine du sang et de ses dérivés et de 12 Groupements Sanitaires
Territoriaux (GST).

Les 12 GST susvisés viennent remplacer tous les établissements de santé du secteur
public relevant de son ressort territorial, notamment les CHU, à l'exclusion,
toutefois, des établissements de santé régis par des textes législatifs ou réglementaires
particuliers, des établissements de santé militaireset des bureaux communaux
d'hygiène et ce, conformément au Dahir n° 1-23-50 du 28 juin 2023 portant
promulgation de la loi n° O8-22 relative à la création des groupements sanitaires
territoriaux.

De même, |l a été procédé à l’adoption et à la publication de la loi n° 32-24 portant
dissolution et liquigation de la Ligue Nationale de Lutte contre les Maladies
Cardiovasculaires, dont l’opération de liquidation est en cours de mise en œuvre.

Parallèlement, une étude est en cours de réalisation pour la transformation de l'IPM en
SA et la revue de son modèle économique.

Par ailleurs, un projet est en cours d'évaluation pour la restructuration des activités
d’assurance maladie.

-  Scctour de la distribution : la loi n° 83-21 prévoit la mise en place de 12 Sociétés
Régionales Multiservices (SRM) à capital public avec possibilité d'ouverture, à l'avenir,
dudit capital au privé et se traduira, à terme, par la dissolution de 12 Régies de

A



Distribution et l'intégration aux SRM des 12 Directions Régionales de Distribution
relevant de l'ONEE ;

-  Secteur de l’urbanisme et de l’habitat : en application des Hautes Orientations
Royales visant la mise en œuvre du programme d'aide au logement et
l'accompagnement de la rénovation de la planification urbaine et territoriale, il est
envisagé de procéder à un regroupement des 30 Agences Urbaines en 12 Agences
Régionales d’Urbanisme et d'Habitat. Le projet de loi n° 64-23 portant création des
agences régionales de l'urbanisme et de l’habitat a été mis dans le circuit d'adoption ;

-  Secteur de l’investissement : ce projet a pour objet principal la dynamisation des
investissements, à travers le renforcement des missions de ces Centres et la mise en
place d'une gouvernance unifiée et décentralisée de l'investissement en transformant
les décisions des Commissions régionales unifiées d'investissement, présidées
désormais par les CRI, en décisions exécutoires.

S Opérations de restructuration en cours d'évaluation et de concertation :

Les travaux et concertations en cours seront poursuivis en vue d'identifier d'autres secteurs et
EEP sujets à restructuration, ce qui permettra de déterminer la taille optimale du portefeuille
public à moyen terme en vue de répondre aux principes et objectifs tracés dans le cadre de la
réforme des EEP.

Les EEP concernés relèvent des secteurs de l’agriculture, de l'enseignement supérieur, de
l'habitat, de la logistique, de l'énergie ainsi que dans le domaine du développement social et
territorial,

> Opérations spécifiques :

Un plan d'action a été engagé auprès de plusieurs EEP en vue de l'identification des actions
d'amélioration de leur gouvernance, de leur gestion, du recouvrement de leurs créances ainsi
que l’adaptation du contrôle financier. Les secteurs concernés sont: l’éducation,
l'enseignement supérieur, le tourisme, l'agriculture, l’infrastructure et l'eau.

IV. Refonte du dispositif encadrant les opérations de liquidation
IV.1. Portefeuille public en liquidation

Le Portefeuille public en cours de liquidation compte, à fin 2023, 81 EEP dont 16 Etablissements
Publics, 15 SA à Participation Directe du Trésor, 24 SA à participation indirecte majoritaire et
26 SA à participation indirecte minoritaire. Les Etablissements Publics relevant des
Collectivités Territoriales (Régies de Transport, Régies de distribution d’eau et d'électricité et
autres) représentent 16% dudit portefeuille, soit 13 Régies.

Par ailleurs, le constat général fait ressortir une lenteur du processus de liquidation des EEP
qui s'étale souvent sur plusieurs années et occasionne des charges relativement importantes.
Certaines entités, dont la décision de dissolution a été prise depuis plusieurs décennies, sont
toujours juridiquement en vie pour les besoins de la liquidation.

Ainsi, les efforts ont été poursuivis pour un meilleur pilotage des opérations de liquidation des
EEP et ce, en mobilisant tous les partenaires concernés (MEF, Départements de tutelle, EEP
concernés et liquidateurs).

VN



RAPPORT SUR LES ETABLISSEMENTS ET ENTREPRISES PUBLICS

IV.2. Réforme du dispositif encadrant les opérations de liquidation

La loi-cadre n° 50-21 relative à la réforme des EEP prévoit des dispositions visant à encadrer
les opérations de liquidation. Elle prévoit également la création d'une Instance Centrale
chargée d'accélérer lesdites opérations de liquigation et de prendre toutes mesures
nécessaires afin d'assainir le stock actuel et futur des EEP en liquidation.

A cet effet, une étude portant sur la réforme du dispositif encadrant les opérations de
liquidation des EEP a été lancée avec comme objectif de proposer des mesures pour
surmonter les nombreux dysfonctionnements que connait ce processus (absence d'un
référentiel juridique et procédural unifié des mécanismes de mise en œuvre et de suivi des
opérations de liquidation, multiplicité des intervenants, etc.).

La nouvelle dynamique enclenchée par la réforme profonde du secteur des EEP représente
une réelle opportunité pour une refonte et Un recadrage du processus de liquidation dans son
intégralité et la conduite des opérations de liquidation avec célérité et rigueur, en vue de
dépasser les retards constatés générant des risques financiers pour le budget de l’Etat.

Les objectifs de l’étude susvisée se présentent comme suit :
-  Refonte du dispositif réglementaire régissant les opérations de liquidation ;
-  Levéo des facteurs de blocage des opérations de liquidation ;

-  Harmonisation du mode de nomination, de rémunération et de professionnalisation des
liquidateurs ;

-  Meilleur encadrement de la mise en œuvre des opérations de liquidation ;

-  Conception d'un système de suivi informatisé des opérations de liquidation.



gème Partie : SYNERGIES PUBLIC-PRIVE ET
CONTRIBUTION DES EEP A
L’AMELIORATION DU CLIMAT DES
AFFAIRES

. RENFORCEMENT DE L’EFFICACITE DE GESTION DES EEP
ET SYNERGIES PUBLIC-PRIVE

L1. Consolidation de la démarche contractuelle Etat-EEP

Les contrats-programmes donnent aux EEP une visibilité par rapport aux stratégies
sectorielles adoptées par le Gouvernement et une lisibilité quant à leurs projets et objectifs et
constituent une base d’évaluation permanente et d’amélioration des performances techniques
et financières.

Le développement de la relation contractuelle entre l’Etat et les EEP, couplé à l'amélioration
de leur mode de gouvernance et de contrôle, permettra l'ancrage de la culture de
rosponsabilité, de roddition des comptes ot dc transparence des EEP ainsi que le renforcement
de leur viabilité, l'exécution efficiente des politiques publiques et des stratégies sectorielles.

En 2025, il a été procédé à l’évaluation et au suivi du bilan rétrospectif du contrat-programme
Etat-RADEEMA (2020-2022) et du contrat-programme Etat-CMR (2022-2024). Cet exercice
a été caractérisé également par la signature d’un nouveau contrat-programme Etat-
RADEEMA.

Concernant les nouveaux projets de Contrats-Programmes, ils sont menés selon une
nouvelle approche reposant sur une vision stratégique, clairement définie et partagée avec les
parties prenantes dans l'objectif de la refonte du modèle économique de ces entités sur la
base de schémas institutionnels clairs, d'une politique d'investissement visant plus d'impact et
de performance ainsi que des plans d'affaires viables et soutenables. Ainsi, plusieurs projets
se trouvent dans leurs phases de cadrage ou d’initiation notamment avec l'ONCF, ADM,
l’Entraide Nationale (EN), l'INRA, la SNTL et GBAM.

Sur le plan réglementaire et pour accompagner les EEP dans le processus de
contractualisation, les travaux de déploiement de la loi-cadre n° 50-21 relative à la réforme des
EEP se poursuivent pour l'adoption du projet de décret fixant les cas dans lesquels les
contrats-programmes doivent être conclus entre l'Etat et les EEP. Ledit projet de décret a été
finalisé en concertation avec le SGG dans la perspective de son adoption en Conseil de
Gouvernement.

Il convient de signaler que le ledit projet de décret prévoit la publication par arrêté du ministre
chargé des finances d'un nouveau guide méthodologique de la contractualisation
accompagné de modèles-types de contrats. En plus des contrats-programmes, ce projet de
guide, en cours de finalisation, doit clarifier les modalités d’élaboration et de structuration des
documents et dispositifs ci-après :

JN



RAPPORT SUR LES ETABLISSEMENTS ET ENTREPRISES PUBI| s

-  Les contrats de performances à conclure entre les dirigeants des EEP et leurs organes
délibérants :

- Les contrats d'objectifs internes à conclure entre le management et les personnes
occupant des postes de responsabilité au sein de l'EEP ;

- Les obligations de services publics ayant pour objectif d’arrêter les modalités de
financement des activités confiées à l'EEP en l’absence de ressources dédiées ;

-  L'exercice d'un reporting climat des EEP en vue de la contribution à l'accélération des
objectifs de la transition verte.

1.2. Partenariat Public-Privé
L2.1. Révision du cadre juridique et institutionnel du PPP

Dans l’objectif de la relance du Partenariat Public-Privé (PPP), il a été procédé à la refonte du
cadre juridique régissant les contrats de PPP en vue de lever les obstacles au développement
de ce mode de réalisation des investissements et des ouvrages publics. À cet effet, la loi n° 46-
18 modifiant et complétant la loi n° 86-12 relative aux contrats de PPP a été publiée au Bu//etin
Officiel le 19 mars 2020.

L’entrée en vigueur de cette loi nécessite la publication de l’ensemble des textes
réglementaires prévus pour son application. Dans ce cadre, quatre décrets d'application et
trois arrêtés ont été publiés. Ainsi, tous les textes ont été publiés, à l'exception de deux arrêtés
spécifiques aux Collectivités Territoriales. || s'agit du projet d'arrêté de pré-qualification des
candidats qui est en phase avancée de finalisation et du projet d'arrêté de définition et
d'actualisation du programme national annuel et/ou pluriannuel des projets.

Les principaux apports de ce nouveau cadre juridique consistent en la mise en place de la
Commission Nationale du PPP (CNPPP) présidée par le Chef du Gouvernement et dont les
missions portent, essentiellement, sur la définition des orientations générales et de la
stratégie nationale en matière de PPP et l'élaboration du programme national des projets
PPP.

L2.2. Opérationnalisation de la Commission Nationale du PPP (CNPPP)

En perspective de l’entrée en vigueur du nouveau cadre juridique, le MEF a engagé les travaux
pour un déploiement efficient de la CNPPP en vue de donner un nouvel élan aux projets PPP.
Les principales missions de la CNPPP concernent ce qui suit :

-  Arrêter les orientations générales et la stratégie nationale en matière de PPP : la
CNPPP établit les lignes directrices essentielles pour le développement des projets PPP
dans le cadre d'une vision cohérente et intégrée ;

- Définir le programme national des projets PPP : sur proposition des personnes
publiques concernées, la CNPPP met en place un programme annuel ou pluriannuel des
projets éligibles aux contrats de partenariat.

Parallèlement, en vue de l’anticipation des travaux d’élaboration du programme national de
projets PPP, des concertations ont été engagées avec les Départements Ministériels et les
partenaires concernés en vue d’échanger autour de la démarche de collecte des projets PPP

S



et de structuration du programme national et de recueillir les attentes et les propositions en
matière d’orientations et d’objectifs stratégiques à assigner au programme national de PPP.

Dans ce cadre, les concertations engagées courant juin et juillet 2024 ont concerné la
Délégation Générale à l'Administration Pénitentiaire et à la Réinsertion et les Départements
chargés de l'Industrie, de l'Equipement et de l'Eau, de la Jeunesse, de la Santé, de la Transition
Energétique, de l'Education Nationale, de l'Enseignement Supérieur et de l'Agriculture.

Les Départements susvisés ont été accompagnés par des EEP sous leur tutelle dans l’objectif
de développer une vision intégrée et structurée des projets PPP par secteur et par filière
d'activité pour garantir l'efficacité et [a cohérence globale du programme national de PPP,

Les attentes et les propositions, formulées dans ce cadre, ont adressé plusieurs thématiques,
notamment :

-  Cibler les secteurs prioritaires présentant un potentiel de PPP en plus des secteurs
classiques pour couvrir les secteurs sociaux (santé, éducation etc.) afin d'accélérer
l'investissement et de contribuer, efficacement, aux priorités nationales en matière de
développement économique et social ;

-  Accélérer la mise en place et le lancement de l'exécution du programme national de
PPP en vue de contribuer à la consolidation des marges budgétaires par la réalisation
en mode PPP d'une part importante de la commande publique à définir ;

-  Accompagner l’émergence d’équipes qualifiées pour gérer les projets PPP, renforcer
leurs compétences et diffuser les bonnes pratiques.

Ainsi, les concertations seront poursuivies avec l'ensemble des partenaires concernés en vue
de mettre au point un programme national de projets à réaliser selon le mode PPP et de définir
les grandes lignes des orientations générales et de la stratégie nationale en matière de PPP
et qui seront présentées à l'approbation de la CNPPP devant tenir sa 1°'° réunion dès
publication des textes requis pour l'entrée en vigueur de la nouvelle loi sur les PPP.

1.2.3. Suivi des projets PPP

En attente du déploiement du mécanisme de planification dans le cadre du programme
national pluriannuel des projets PPP, la situation actuelle des projets PPP se présente comme
suit :



RAPPORT SUR LES ETABLISSEMENTS ET ENTREPRISES PUBLICS

> Projets en cours de réalisation

Projets PPP en cours de réal‘isation

Agriculture/
Ministère chargé
de l'Agriculture

Dessalement pour
l‘irrigation  dans la
zone de Dakhla

Coût d'investissement de 2,5 MMDH, dont :
- 2,16 MMDH pour le dessalement et parc éolien
- 338 MDH pour le réseau d'irrigation
Capacité de production de 37 Mm#/an, dont :
- (rrigation : 30 Mm/an
-  Eau potable : 7 Mm#/an (ville Dakhla et ses environs).
Superficie irriguée : 5.000 ha
Capacité du Parc Eolien : 40 MW (extensible à 60 MW)
Durée du contrat : 22 ans
Durée de construction : 2 ans
Démarrage des travaux : 2022

Eau potable et
irrigation/
ONEE

Dessalement de l’eau
de mer dans la
Région de
Casablanca-Settat

Coût d’investissement : 6,5 MMDH
Production de 300 millions de m#/an dont 200 millions
pour la phase 1 :
- (rrigation : 50 Mm#/an
-  Eau potable : 250 Mm#/an
Durée du contrat : 30 ans
Durée de construction de la phase 1 : 34 mois
Démarrage des travaux : 10 juin 2024

Projets PPP dont l’évaluation préalable est réalisée

Irrigation et eau
potable/
Ministère chargé
de l’'Agriculture

Dessalement de l’eau
de mer pour
l‘irrigation  dans la
région de Guelmim
Oued Noun

Coût d’investissement : 2,03 MMDH
Production d’eau dessalée de 47 Mm#/an, dont :
- lrrigation : 37 Mm#/an
-  Eau potable : 10 Mm*/an
Superficie irriguée : 5.040 ha
Durée du contrat : 30 ans
Durée de construction : 3 ans
Avancement : préparation en cours du dossier d'appel à la
concurrence

Agriculture/
Ministère chargé
de l’'Agriculture

Irrigation de 30.000
ha dans la région du
Gharb

Coût d’investissement : 2,99 MMDH

Superficie irriguée : 30.000 ha

Durée du contrat : 30 ans

Durée de construction : 2 ans

Avancement : préparation en cours du dossier d'appel à la
concurrence

Par ailleurs, le projet de mise en place d’une unité pharmaceutique de production de sérums,
vaccins et produits biologiques initié par l'Institut Pasteur du Maroc a eu l’accord pour sa
réalisation en PPP en janvier 2019. Toutefois, un accord a été signé entre le Gouvernement
Marocain et Maroc Biotechnologies en juillet 2021 à Fès, sous la Présidence Effective de
Sa Majesté le Roi Mohammed VI, que Dieu L'assiste, après l’avènement de la crise Covid 19.
Cet accord vise à doter le Royaume de capacités industrielles et biotechnologiques complètes
et intégrées, dédiées à la fabrication de vaccins et de produits biologiques au Maroc, envers
l'autosuffisance vaccinale au Maroc, en Afrique et à l'international.

Un contrat cadre pour gérer la relation commerciale entre [e partenaire privé et l'IPM pour une
durée de trois ans est en cours de mise en place dans l'attente de formaliser un contrat de
PPP.



> Projets en cours d’évaluation préalable

-  Projet de gazoduc inscrit dans le cadre du programme d'infrastructure de gaz naturel
liquéfié. Ce gazoduc reliera [e terminal gazier (qui sera réalisé au port Nador West Med)
au Gazoduc Maghreb Europe (GME). Il reliera également le GME aux bassins de
demande de Kenitra et Mohammedia ;

-  Projet d'irrigation dans la zone de Sidi Rahal à partir de la station de dessalement de
Casablanca (8.000 had.

1.3. Amélioration des délais de paiement des EEP

Lors de son Discours Royal à l'occasion du 65°"° anniversaire de la Révolution du Roi et du
Peuple du 20 août 2018, Sa Majesté le Roi Mohammed VI, que Dieu L’assiste, a donné ses
Hautes Orientations pour remédier aux problèmes liés aux retards de paiement, en particulier
ceux impliquant le secteur public et ce, compte tenu de leur impact significatif sur la pérennité
des entreprises et la dynamisation du tissu économique.

A la lumière de ces Hautes Orientations, le Gouvernement a initié une série de mesures portant
essentiellement, sur des actions de sensibilisation, de dématérialisation de la commande
publique, de publication périodique des délais de paiement et de l’adaptation de la
règlementation notamment en matière de garantie des droits de l'entreprise. Ces efforts
concertés ont abouti à une amélioration notable dans le respect des délais de paiement du
secteur public.

Dans ce cadre, la mise en place de l’Observatoire des Délais de Paiement (ODP) en novembre
2017 a revêtu une importance capitale au regard de la pertinence et la cohérence de la vision
de l’Observatoire ainsi qu'aux actions engagées pour améliorer les pratiques de paiement des
entreprises.

Lors de sa sixième réunion tenue le 11 juin 2024, l'Observatoire a examiné les actions mises en
place pour améliorer les délais de paiement et a pris note des résultats positifs du premier
bilan de la mise en œuvre du nouveau dispositif de sanctions pécuniaires introduit par la loi
n° 69-21 modifiant la loi n° 15-95 formant code de commerce et édictant des dispositions
transitoires particulières relatives aux délais de paiement, en vigueur depuis le 1" juillet 2023.
Ce premier bilan annonce des perspectives favorables pour la consolidation de l’équilibre des
relations entre les entreprises et la réduction des délais de paiement dans le secteur privé.

Le 4°"° rapport de l'Observatoire des Délais de Paiements (ODP), publié en juillet 2024,
confirme la tendance positive observée dans les délais de paiement du secteur public.
Cette amélioration reflète les efforts conjoints de l'Etat, des Collectivités Territoriales et des
EEP. Ainsi, le délai moyen de paiement des EEP poursuit sa tendance baissière, atteignant
34,2 jours en juin 2024, soit une baisse de 21,7 jours par rapport à décembre 2018 et de 25,8
jours par rapport au seuil légal fixé à 60 jours.

A fin juin 2024, 103 EEP ont réussi à enregistrer des délais de paiement inférieurs ou égaux à
30 jours (55%) et 64 EEP ont réalisé des délais de paiement qui se situent entre 31 jours et
60 jours (34%). Toutefois, 21 EEP ont connu une augmentation de leurs délais de paiement qui
sont supérieurs à 60 jours (11%).

VN



RAPPORT SUR LES ETABLISSEMENTS ET ENTREPRISES PUBI| s

1.4. Contribution à la stratégie Digital Morocco 2030

Le Gouvernement a lancé, en date du 25/09/2024 la stratégie nationale
« Maroc Digital 2030 » (Digital Morocco 2030), qui vise une transformation numérique
globale, favorisant à la fois la compétitivité économique et l'inclusion sociale grâce à des
services publics améliorés, une économie numérique robuste et un écosystème innovant de
talents.

Cette stratégie est structurée en deux principales composantes portant, respectivement, sur
la digitalisation des administrations et des services publics pour faire passer le Maroc à la 50°M°
place au niveau mondial et la dynamisation de l'économie numérique pour produire des
solutions marocaines et créer de la valeur et de l’emploi.

Au vu de leurs missions, deux Etablissements Publics, en l’occurrence l'ADD et l'ANRT, jouent
un rôle déterminant dans la mise en œuvre de cette stratégie.

A ce titre, l'ADD poursuit la réalisation de sa feuille de route visant de faire du digital un
véritable levier de transformation numérique en vue d'une administration efficiente et une
société connectée et inclusive. Cette feuille de route, devant être actualisée et adaptée par
rapport aux orientations de la nouvelle stratégie digitale, est structurée autour de quatre axes
de développement :

-  L'accélération de la transformation digitale de l’administration on vue de structurer on
profondeur les services publics et de renforcer leur efficacité, leur transparence et leur
rapidité ;

- Le développement accéléré de l’économie digitale et de l’innovation pour ériger le
Maroc en un Hub digital et technologique de référence en Afrique :

- Le renforcement de l’inclusion sociale visant la promotion de la culture d'usage approprié
du digital et l'inclusion financière des populations fragiles ;

- Le renforcement de l’environnement et de la confiance digitale, par l'adaptation de la
réglementation à l’évolution digitale et l'élaboration d'un programme de formation aux
nouveaux métiers du digital.

De son côté, l'ANRT assure le suivi de son plan d'action visant l'accélération des
investissements des opérateurs de télécommunication en vue de la mise en œuvre, dans les
délais prescrits, du « Plan National du Haut Débit 2 » visant l'extension des réseaux de haute
connectivité, L'Agence a également lancé le projet de couverture de la 5G dans l’objectif
d'atteindre Une couverture de 70% à fin 2030.

Par ailleurs, les EEP mènent une profonde mutation de leurs processus internes visant la
digitalisation des services publics offerts aux usagers et l'accélération de l'économie
numérique en harmonie avec la stratégie digitale.

À ce titre, plusieurs EEP ont élaboré leurs stratégies de transformation digitale en phase avec
les grands chantiers qu’ils portent, notamment :

-  La digitalisation de la CNSS qui s'inscrit dans la mise en place du chantier de la
généralisation de la couverture sociale en développant des systèmes d'information
ouverts aux parties prenantes et permettant la prise en charge de façon automatisée

A



des diverses prestations rendues aux assurés, et ce à travers des plateformes
dématérialisées permettant une forte réduction des délais de service ;

-  La CMR a entrepris un vaste programme de digitalisation à travers l'automatisation
progressive de l’ensemble de ses processus « métier et support », avec comme objectif
l'amélioration de la qualité des services rendus aux affiliés, aux retraités et aux ayants
droit en leur offrant une expérience 100% digitale ;

-  L’ANCFCC poursuit son plan de transformation numérique à travers le projet de mise
en ligne d'un géoportail permettant l'e-commerce des produits cartographiques et de
mise en place d'un cadastre multicouches numérique ;

-  La digitalisation de Barid AIl Maghrib qui contribue aux efforts de la simplification des
procédures de transition vers la signature électronique ;

-  L'ONCF qui a adopté une approche centrée sur le client, avec une digitalisation
continue des services de réservation et de suivi en temps réel des trains.
Le développement d'applications mobiles et de plateformes numériques vise à
améliorer l'expérience des voyageurs et à faciliter l'accès aux informations de
transport :

-  MASEN et ONEE qui intègrent des outils numériques avancés pour optimiser la gestion
de la production d'énergic.

Dans la même dynamique, le MEF/DEPP a mis en place des systèmes d'information pour un
meilleur accompagnement des EEP à travers la digitalisation des processus métiers,
notamment :

-  La généralisation de la collecte de données des EEP via le système MASSAR permettant
le suivi de leurs activités, de leurs performances et la génération des reporting et des
rapports d'évaluation et d'analyse ;

- Le déploiement de la plateforme AD@E dans l’ensemble des Etablissements Publies
soumis au contrôle préalable ou spécifique qui a permis le traiîtement de près de
250.000 Ordres de Paiement en 2023.

[.5. Mise en place d’un projet de pilotage des performances des EEP

L’évaluation des impacts liés au déploiement du chantier de la réforme des EEP nécessite la
mise en place d’un outil structuré et intégré permettant le suivi, le contrôle et l’appréciation
des performances économiques, financières et techniques des EEP, l'anticipation de leurs
risques dans leurs relations budgétaires avec l'Etat, le suivi de la qualité de leur gestion et de
leur gouvernance ainsi que d'autres dimensions qui seraient nécessaires pour asseoir un
reporting régulier et transparent à même de mesurer le degré d’atteinte des objectifs tracés
par la réforme et qui visent, /n fine, le rehaussement de l'efficience économique et sociale de
l'action des EEP et l'ancrage des règles de transparence et de reddition des comptes.

Ce chantier devrait s'imbriquer en harmonie, en complémentarité et en synergie avec d’autres
chantiers en cours de développement, dans le cadre du projet de la réforme des EEP,
notamment :

VN



RAPPORT SUR LES ETABLISSEMENTS ET ENTREPRISES PUBLICS

» Le projet d'amendement de [a Loi Organique relative à la Loi de Finances ;

» Le projet de consolidation des comptes qui sera développé dans une logique de
convergence avec les pratiques comptables internationales ;

» Le projet de loi relatif au contrôle financier et la gouvernance en cours de finalisation
orienté pour renforcer la transparence, fiabiliser la gestion, consolider la gouvernance
et visant à faire du contrôle financier un outil pertinent en matière d'évaluation des
performances et de de prévention des risques ;

»  Le projet de mise en place d’un dispositif de suivi et de gestion des risques des EEP dans
leurs relations budgétaires avec l'Etat ;

» L'accompagnement des engagements pris par le pays en matière de transition
budgétaire verte, de développement durable et des objectifs de la Contribution
Déterminée Nationale ;

» Le chantier en cours de finalisation au niveau de l'ANGSPE en relation avec le pilotage
des performances des EEP relevant de son périmètre.

Ce projet sera développé sous forme d’une plateforme informatique intégrée devant couvrir,
dans une première étape, les segments d’évaluation des performances, de gestion des risques
budgétaires, de reporting climat et de suivi de la gouvernance des EEP, Ce projet peut être
élargi par la suite pour intégrer d’autres dimensions notamment les instruments de gestion et
le suivi des recommandations des organes de contrôles et de gouvernance.

1.6. Normalisation et lutte contre le blanchiment
L6.1. Normalisation comptable
1.6.1.1. Bilan du Conseil National de la Comptabilité

Au titre de l'année 2023, le Conseil National de la Comptabilité (CNC) a adopté et a publié
5 avis. Ces avis sont émis par Madame la Ministre de l’Economie et des Finances, en sa qualité
de présidente du CNC, en application des dispositions du décret n° 2-88-19 du 16 rabii [1 1410
(16 novembre 1989) instituant ce Conseil tel qu’il a été modifié et complété, Il s'agit en
l’occurrence des avis suivants :

- Avis n° 23 du CNC du 25 avril 2023 relatif au Plan Comptable des Associations et autres
organismes à but non lucratif ;

-  Avis n° 24 du CNC du 14 juin 2023 fixant les principes et critères de la comptabilité
normalisée tenue sur la base de traitements informatiques ;

-  Avis n° 25 du CNC du 14 juin 2023 relatif aux règles comptables spécifiques applicables
aux syndicats des copropriétaires ;

-  Avis n° 26 du CNC du 24 juillet 2023 complétant l’avis n° 5 relatif aux comptes
consolidés ;

-  Avis n° 27 du CNC du 27 septembre 2023 relatif au traitement comptable des
contributions versées au « Fonds spécial pour la gestion des effets du tremblement de
terre ayant touché le Royaume du Maroc ».

A



Le Comité Permanent de ce Conseil a également examiné plusieurs questions comptables
concernant :

- Le traitement comptable des infrastructures hippiques transférées à la Société Royale
d'Encouragement du Cheval (SOREC) et celles mises à sa disposition ;

- La demande émanant de l'Autorité de Contrôle des Assurances et de la Prévoyance
Sociale (ACAPS) visant à reporter l'application de la norme |FRS 17 relative aux
« contrats d'assurance » aux états financiers de certaines sociétés marocaines
d’assurance.

1.6.1.2. Modernisation du cadre comptable Marocain

Le projet de mise à niveau du cadre comptable national a été lancé en collaboration avec la
Banque Mondiale et l'Ordre des Experts Comptables (OEC). Ce projet vise à mettre à jour et à
moderniser le cadre comptable marocain pour en faire un levier de transparence,
d'amélioration du climat des affaires au Maroc et d’attrait des investissements notamment
étrangers.

Le projet du CGNC révisé a été examiné par le Comité Permanent du Conseil National de la
Comptabilité (CNC) lors de sa réunion tenue le 28 février 2024, à l'issue de laquelle il a été
convenu de valider ledit projet et de mener des concertations avec les parties prenantes au
sujet de ce projet.

Aussi, le Comité Permanent du CNC a convenu lors de sa réunion du 9 mai 2024 d'instituer
cinq commissions techniques pour apprécier les remarques à recevoir de la part des
différentes parties consultées et de prendre en charge les propositions émises au sujet de ce
projet.

Par ailleurs, il est à signaler qu'une feuille de route du projet a été élaborée de concert avec
les partenaires et qui prévoit, notamment :

-  La finalisation du projet du CGNC révisé en tenant compte des résultats des
consultations avec les parties prenantes ;

-  La validation du projet d’'amendement de la loi n° 9-88 relative aux obligations
comptables des commerçants et du projet du CGNC révisé au niveau des instances de
gouvernance du CNC :

- L'introduction de l'amendement de la loi précitée dans le circuit d'approbation.
1.6.1.3. Projet de loi relatif aux états financiers consolidés

Le projet de loi relatif aux états financiers consolidés vise à doter notre pays d'un texte
législatif général définissant des règles homogènes de consolidation des comptes et ce, afin
de mettre à la disposition des investisseurs, des actionnaires et des différentes parties
prenantes une information comptable et financière de qualité. Les principaux apports de ce
projet se présentent comme suit :

- Elargissement du champ des entités assujetties à la consolidation des comptes :

-  Soumission des états financiers consolidés au même dispositif de contrôle et
d'approbation que les comptes sociaux ;

VN



RAPPORT SUR LES ETABLISSEMENTS ET ENTREPRISES PUBI| s

-  Précision de la norme de consolidation à adopter (soit des normes internationales ou la
norme nationale) par chaque catégorie d'entités soumise à l'obligation de consolidation
des comptes :

-  Application de sanctions financières pour toute non-conformité aux dispositions de la
loi,
Ce projet de loi a été validé par le Comité Permanent du CNC lors de sa réunion tenue le
28 décembre 2023 et a été mis dans le circuit d'adoption, en précisant qu’une consultation
publique a été lancée, au niveau du site web du SGG, pour recueillir les avis et les propositions
du public concernant ce projet de loi.

1.6.2. Lutte contre le Blanchiment de Capitaux et le Financement du Terrorisme

Le Maroc, membre fondateur du Groupe de l'Action Financière du Moyen-Orient et de l'Afrique
du Nord (GAFIMOAN), a été placé sous surveillance renforcée par le GAFI Ç« liste grise ») en
matière de blanchiment de capitaux et de financement du terrorisme (LBC/FT) lors de la
réunion plénière du 25 février 2021 Le rapport d’évaluation mutuelle du dispositif national
relatif à la LBC/FT ainsi que le rapport du Groupe d’Examen de la Coopération Internationale
(ICRG)/GAFI) ont souligné des insuffisances dans l'implication des professions non financières
désignées, un manque de sensibilisation aux risques de LBC/FT, ainsi que des lacunes dans la
supervision et le contrôle de ces entités,

En date du 14 juin 2021, la loi n° 12-18 modifiant et complétant le Code pénal et la loi n° 43-05
relative à la lutte contre le blanchiment de capitaux, ont été publiées. Les nouvelles
dispositions de ces lois visent à renforcer le dispositif législatif national de lutte contre le
blanchiment de capitaux et le financement du terrorisme (LBC/FT) et à l’adapter aux normes
internationales adoptées en la matière. Aussi, la loi n° 43-05 a élargi le champ des personnes
physiques et morales qui y sont assujetties pour couvrir également les experts comptables et
les comptables agréés.

Le Ministère de l'Economie et des Finances a été désigné pour superviser et contrôler les
personnes assujetties relevant de son domaine de compétences, en l’occurrence les experts
comptables, les comptables agréés, les sociétés holdings offshore, les casinos et les
établissements des jeux de hasard, conformément à l'article 4 de la loi précitée.

Depuis lors, plusieurs mesures ont été mises en place pour assister et accompagner les experts
comptables et comptables agréés, dont notamment :

-  Une lettre circulaire datée du 3 mars 2022 définissant les exigences en matière de
LBC/FT pour les professionnels comptables :

- Un guide pratique en arabe et français visant à aider les professionnels à appréhender
et à appliquer les exigences légales ;

- Des actions de sensibilisation et de formation renforcées, avec des rencontres
régionales organisées en partenariat avec l'Autorité Nationale du Renseignement
Financier (ANRF) et d’autres institutions ;

- Le Maroc a participé aux entretiens avec les experts du GAFI en janvier 2023.

A



Le 24 février 2023, le GAFI à décidé de retirer le Maroc de la « liste grise », reconnaissant ainsi
la conformité du dispositif national aux normes internationales en matière de LBC/FT.
Cette décision a été confirmée lors de l'Assemblée Générale du GAFI à Paris.

Pour maintenir cette conformité, le Ministère a établi un plan d'action pour 2024, axé sur :
-  La sensibilisation et la formation des experts comptables et comptables agréés ;
- Le renforcement de la coordination avec les organismes de lutte contre la LBC/FT ;

- L’accompagnement des instances ordinales pour améliorer les dispositifs internes de
LBC/FT et suivre les risques y associés.

Il. CONSOLIDATION DE LA GOUVERNANCE ET DE LA
TRANSPARENCE DU PORTEFEUILLE PUBLIC

HL.1. Projet d’actualisation du Code des bonnes pratiques de
gouvernance des EEP

L'élaboration d’un nouveau Code des bonnes pratiques de gouvernance des EEP traduit la
volonté de s’adapter aux évolutions des pratiques et des référentiels relatifs à la gouvernance
d'entreprise au niveau national et international.

Ce chantier vise à s’aligner principalement sur les lignes directrices de l'OCDE de 2015, relatives
aux pratiques de bonne gouvernance d'entreprises et aux dispositions de référence en matière
de gouvernance prévues par l’arsenal juridique national en particulier la loi-cadre n° 50-21
relative à la réforme des EEP et la loi n° 17-95 relative aux sociétés anonymes telle qu’elle a
été modifiée et complétée.

Ce chantier a été mené dans une approche participative et de concertation avec une trentaine
d'EEP et d’'autres acteurs de référence en matière de gouvernance notamment la Cour des
Comptes, le Conseil de la Concurrence, la Banque Mondiale, l'AMMC, l'Agence ONU FEMMES,
le Club des Femmes Administrateurs. Ces travaux ont débouché sur une version du projet de
Code qui a été soumise au processus de consultation publique en juillet 2023, par la
Commission Nationale de Gouvernance d’Entreprise (CNGE).

Les recommandations formulées, à l'issue de cette consultation publique, ont été prises en
compte et validées au niveau de la CNGE dans le cadre d'une commission constituée suite aux
orientations du Chef du Gouvernement.

Ledit projet de Code et le projet de décret y afférent ont été mis dans le circuit d'adoption et
ce, en application des dispositions de l'article 38 de la loi-cadre n° 50-21 relative à la réforme
des EEP.

Les concertations sont en cours avec le Secrétariat Général du Gouvernement (SGG) en vue
de finaliser le Code. Parallèlement, un plan d'action est en cours de mise en place et sera
déployé, après la publication du décret portant approbation dudit Code.

Ce plan d’action sera mis en œuvre avec comme principaux objectifs d'améliorer l'image des
EEP auprès du public, de positionner ces entités en tant qu’acteurs majeurs dotés d'une
gouvernance exemplaire et responsable et de favoriser leur contribution à la création de
valeur. Ce plan porte sur les principaux axes suivants :

VN



RAPPORT SUR LES ETABLISSEMENTS ET ENTREPRISES PUBI| s

- Rationalisation de la taille des organes délibérants et consécration du rôle des comités
spécialisés ;
- Mise en place d‘un vivier d'administrateurs indépendants ;

- Adaptation et généralisation des instruments de gouvernance (règlement intérieur,
chartes etc.) :

- Engagement de campagnes de sensibilisation et de communication ciblées, visant à
disséminer les nouvelles pratiques de gouvernance introduites par le Code ;

- Renforcement de la prise en charge des questions liées à la conduite responsable des
entreprises ;

- Amélioration de la transparence notamment à travers des publications financières et extra-
financière, mettant notamment l'accent sur les aspects liés au changement climatique, aux
projets d’adaptation, à la responsabilité sociétale de l'entreprise (RSE) et au reporting
Environnemental, Social et Gouvernance (ESG).

11.2. Renforcement des audits externes

Sur la période 2000-2023, 92 opérations d'audit ont été réalisées et ont concerné 106 EEP.
Ces opérations d'audit externe ont permis de mettre en évidence des insuffisances au niveau
de l'alignement stratégique du portefeuille de certains organismes publics, de modes de
portage de certaines activités, de l’éloignement des missions de base, de la vulnérabilité des
modèles économiques et d'autres carences touchant au cadre institutionnel.

De même, ces opérations ont révélé des dysfonctionnements liés aux modes organisationnels
et aux systèmes de gestion des EEP audités notamment au niveau des systèmes de
gouvernance, d'information, de pilotage et de gestion.

En vue d'un alignement sur les objectifs de la réforme du secteur des EEP et conformément
aux dispositions de la loi-cadre n° 50-21 précitée, les opérations d'audit externe ont fait l'objet
d'une réorientation pour les focaliser davantage sur les audits stratégiques pouvant déboucher
sur des opérations de restructuration des EEP visant à renforcer les synergies et les
complémentarités et à identifier des schémas institutionnels et organisationnels adéquats pour
un portage efficient des politiques publiques et des stratégies sectorielles.

Dans ce cadre, les programmes annuels d'audit externe des exercices 2022, 2023 et 2024 ont
été établis sur la base d'une approche reposant sur des critères d'évaluation prédéfinis
(stratégique, gestion, gouvernance, maturité du dispositif de contrôle interne, du système
d'information et de la gestion des risques, enjeux économiques et financiers de chaque EEP).

Le programme d'’audit externe de 2024, défini sur la base de l'approche précitée et validé par
le Chef du Gouvernement, prévoit les opérations suivantes :

-  Audit stratégique, institutionnel, organisationnel et de gestion de l'Office des Changes
(OC);

-  Audit opérationnel, de gestion et des performances de l'Agence Nationale de la Sécurité
Routière (NARSA) ;

-  Audit opérationnel, de gestion et des performances de l'Université Ibn Tofail ;

M



-  Audit opérationnel, de gestion et des performances de l’'Agence Urbaine de
Casablanca ;

- Audit opérationnel, de gestion et des performances de l'AREF Casablanca-Settat.

En 2023, les opérations de suivi et d'évaluation de la mise en œuvre des recommandations
des audits externes ont concerné un portefeuille diversifié de 18 EEP.

L'activité de suivi de mise en œuvre des recommandations des auditeurs a porté, au cours de
l'exercice 2023, sur les opérations d’audit externe réalisées au cours de la période 2017-2022.
Ainsi, et sur 1375 recommandations, 686 recommandations ont été réalisées à fin 2023, soit un
taux moyen global de réalisation de 50% contre 43% en 2022, marquant ainsi une amélioration
de 7 points, en soulignant que ledit taux de réalisation n'intègre pas les EEP dont le suivi à été
transféré, en 2023, à l'ANGSPE (BAM, Marchica Med, SAO (Agadir, Tamansourt et Marrakech),
ONP, TMSA et SOREC).



RAPPORT SUR LES ETABLISSEMENTS ET ENTREPRISES PUBLICS

5ème Partie : LES EEP AU SERVICE DE LA
TRANSITION VERTE

L'évolution des réflexions sur les enjeux environnementaux s'est intensifiée au fil des
décennies, avec une prise de conscience croissante à l’échelle internationale. Depuis les années
1960, des jalons importants ont marqué cette progression notamment avec la publication de
Silent Spring en 1962, qui a alerté sur les dangers des pesticides. La Conférence de Stockholm
en 1972 et le rapport Brundtland en 1987 ont établi les fondements d'une approche holistique
des problèmes environnementaux et ont jeté les bases pour de futures initiatives en matière
de développement durable appelant à un équilibre entre les dimensions environnementales,
économiques et sociales.

Les années 1990 ont vu la signature d'accords internationaux majeurs, dont la Convention-
cadre des Nations Unies sur les changements climatiques (CCNUCC) en 1992 et le Protocole
de Kyoto en 1997, introduisant les premiers engagements contraignants pour la réduction des
émissions de gaz à effet de serre.

Les Objectifs de Développement Durable (ODD) faisant partie de l‘'Agenda 2030 pour le
Développement Durable et l'Accord de Paris ont été adoptés en 2015, marquant ainsi un
tournant décisif dans la gouvernance climatique mondiale et représentant un consensus
mondial sur l‘importance de prendre des mesures immédiates et ambitieuses pour préserver
la planète pour les générations futures.

Les conférences des Parties tenues depuis la COP 22 à Marrakech jusqu'à celles tenues en
Glasgow, à Charm El-Cheikh et à Dubaï ont poursuïivi cette dynamique, en insistant sur
‘accélération de la transition énergétique et la mobilisation des financements pour les pays en
développement. La COP 29 prévue à Bakou en 2024 visera à évaluer les progrès réalisés et à
renforcer les stratégies climatiques mondiales.

En parallèle à ces engagements internationaux, la RSE constituant Uune approche globale et un
evier essentiel pour intégrer les enjeux environnementaux et sociétaux dans les plans de
gouvernance et de croissance de l'entreprise, offre un cadre de référence fondamental en vue
d'un développement harmonieux du secteur des EEP.

En adoptant des pratiques responsables, les EEP contribuent, activement, à l’'accélération de
la transition verte, à la réduction de leur empreinte carbone, à la rationalisation de la
consommation de l’eau et à la protection des ressources, Cette démarche s'inscrit pleinement
dans l'agenda de durabilité, en réponse aux objectifs fixés par les accords internationaux et
es Hautes Orientations de Sa Majesté le Roi Mohammed, que Dieu L'assiste.

Cette conduite responsable permet de forger un secteur des EEP engagé dans l'intégration
des risques climatiques dans ses règles de gestion et de communication extra financière en
matière de climat conformément aux standards internationaux.

Ainsi, l’objectif de la présente section, intégrée pour la première fois dans le rapport sur les
EEP accompagnant le projet de la loi de Finances, s'inscrit dans le cadre d'un plan d'action
engagé pour la mise en place d’'un dispositif de reporting climat des activités des EEP visant à
asseoir les bases de mesure, de suivi et d’évaluation des performances des EEP en matière de

N



développement durable et de leur contribution aux efforts et aux engagements du pays en
matière de transition verte.

Cette section est structurée en deux parties traitant, respectivement, la genèse des
engagements souscrits par le Maroc en matière de développement durable et de transition
verte et les bonnes pratiques de certains EEP dans ces domaines.

l. Développement durable et transition verte au Maroc

1.1. Action Climatique du Maroc : un engagement continu du pays

Le Maroc s'est distingué par son engagement continu dans la lutte contre les changements
climatiques. Dès le Sommet de la Terre à Rio en 1992, le Royaume a intégré les principes du
développement durable dans ses politiques nationales et a ratifié la CCNUCC en 1995, puis le
Protocole de Kyoto en 2002. En 2016, le Maroc a renforcé son engagement en ratifiant l'Accord
de Paris et en soumettant sa première Contribution Déterminée au Niveau National (CDN),
fixant un objectif de réduction des émissions de gaz à effet de serre de 42% à l’horizon 2030.

En 2021, cet engagement a été réévalué à la hausse avec un objectif plus ambitieux de
réduction de 45,5%, reflétant la volonté de notre pays de renforcer son action climatique. Le
Maroc prévoit d'actualiser sa CDN d'ici 2025, en intégrant des analyses d'impact social et des
considérations liées à l'égalité des genres.

En parallèle, le Maroc a adopté les 17 Objectifs de Développement Durable (ODD) en 2016,
succédant aux Objectifs du Millénaire pour |le Développement (OMD). Ces ODD, qui couvrent
les aspects économiques, sociaux et environnementaux du développement durable, sont au
cœur des politiques publiques marocaines, visant à harmoniser ces dimensions de manière
intégrée.

L’organisation de la COP 22 à Marrakech en 2016 à marqué un tournant dans l’engagement
climatique du Maroc, offrant une plateforme pour discuter de la mise en œuvre de l'Accord de
Paris. Cette conférence a notamment permis de consolider les engagements des pays vers la
neutralité carbone d'ici 2050, et un sommet africain en marge de l'événement a mis en lumière
la vulnérabilité du continent africain face au réchauffement climatique.

En 2022, unc mission d'assistance technique a été mobilisée pour la formulation de la Stratégic
Bas Carbone Quantitative à Long Terme du Maroc, ayant comme obijectif principal
‘élaboration de plans d'action sectoriels pour la décarbonation à long terme dans divers
secteurs.

L'ambition de cette stratégie est d'assurer une transition bas-carbone ambitieuse et résiliente
face aux effets extrêmes des changements climatiques, tout en offrant des opportunités pour
les opérateurs socio-économiques, des gains de productivité, de compétitivité et la création
d'emplois. La stratégie se basera sur des scénarios de modélisation des trajectoires technico-
économiques et des émissions de Gaz à Effet de Serre (GES) à long terme, ainsi que sur les
orientations du nouveau Modèle de Développement.

Le processus de modélisation de la Stratégie Nationale Bas-Carbone Quantitative (SNBC),
lancé fin 2022, a conduit à la finalisation du Rapport de la SNBC. Ce rapport détaille les
résultats et objectifs sectoriels chiffrés de la trajectoire nationale des émissions Net Zéro d'ici

A



RAPPORT SUR LES ETABLISSEMENTS ET ENTREPRISES PUBLICS

2050, ainsi que l’élaboration des plans sectoriels de décarbonation pour les sept secteurs
majeurs : Energie, Industrie, Bâtiment, Transport, Forêt, Agriculture et Déchets/Économie
circulaire.

En matière de conduite responsable des entreprises, le Maroc a adhéré aux Principes
Directeurs de l'OCDE sur la Conduite Responsable des Entreprises en 2018, renforçant son
engagement en matière de diligence et de RSE. Dans ce cadre, le Maroc a créé un point de
contact national (PCN) pour le suivi de ces principes.

1.2. Choix du développement durable consacré par la Constitution de 2071

La Constitution de 2011 consacre le développement durable comme un droit fondamental.
L'article 31 affirme l'engagement de l'Etat à mobiliser ses moyens pour garantir aux citoyens
l'accès aux conditions nécessaires pour jouir des droits, y compris le droit au développement
durable. Par ailleurs, l'article 35 souligne la promotion d'un développement humain et durable,
en parallèle avec la liberté d'entreprendre, afin de préserver les ressources naturelles et les
droits des générations futures.

L'article 71 de la Constitution place également la gestion de l'environnement et des ressources
naturelles parmi les domaines régis par la loi, conférant ainsi au développement durable une
importance constitutionnelle et législative. L'article 136 consacre le développement durable en
tant que responsabilité collective.

1.3. Développement durable dans le Nouveau Modèle de Développement

Le NMD place le développement durable au cœur de ses recommandations, avec un focus
particulier sur l'accélération de la transition énergétique par l'augmentation de la part des
énergies renouvelables et la gestion durable des ressources naturelles notamment l’eau.
Le NMD encourage l'économie verte, la gestion efficace des déchets, et propose une meilleure
coordination institutionnelle pour renforcer la gouvernance environnementale.

En parallèle, le NMD recommande de réduire les disparités régionales en promouvant
l'inclusion sociale et la participation citoyenne. Il appelle à l'éducation et à la sensibilisation
pour instaurer une culture de durabilité, tout en soutenant la recherche et l'innovation pour
favoriser l'adoption de technologies propres. Ces mesures sont destinées à créer un modèle
de développement durable, résilient et équitable pour le Maroc.

[.4. Charte Nationale de l’Environnement et de Développement Durable

Conformément aux engagements internationaux du Maroc, le Gouvernement a initié plusieurs
réformes politiques, institutionnelles, juridiques et socio-économiques pour poser les bases du
développement durable. Ce processus a été renforcé par l'adoption de la Charte Nationale
de l’Environnement et du Développement Durable (CNEDD), conformément aux directives
de Sa Majesté le Roi Mohammed VI, que Dieu L'assiste, à l'occasion du Discours du Trône
du 30 juillet 2009.

La CNEDD définit les droits et devoirs environnementaux, ainsi que les principes et valeurs
encadrant les activités des secteurs public et privé, en vue d'assurer le développement
durable. Elle engage également les pouvoirs publics, les collectivités territoriales, les acteurs

économiques et la société civile à respecter ces principes.



En mars 2014, la loi-cadre n° 99-12 portant Charte Nationale de l’Environnement et du
Développement Durable a été adoptée, établissant le développement durable comme un socle
des politiques publiques au Maroc. L'article 13 de cette loi stipule que les établissements
publics et les entreprises d'Etat doivent intégrer des mesures de développement durable dans
leurs politiques sectorielles, tout en tenant compte des spécificités de chaque secteur.

1.5. Stratégie nationale de développement durable

L'opérationnalisation des Orientations Stratégiques de la CNEDD a été concrétisée par
l'adoption de la Stratégie Nationale de Développement Durable (SNDD), le 25 juin 2017 lors
du Consoil des Ministres. Alignée sur l'Agenda 2030, cotte stratégic visc à opérer une transition
vers une économie verte et inclusive, en prenant en compte les défis environnementaux tout
en renforçant le développement humain, la cohésion sociale et la compétitivité économique.

La SNDD repose sur quatre piliers du développement durable : économique, social,
environnemental, et culturel. Elle définit sept grands enjeux, chacun décliné en axes
stratégiques avec des objectifs et des mesures à mettre en œuvre.

Lors de [a première évaluation à mi-parcours en 2021, la SNDD a ajusté ses plans d'action pour
intégrer les orientations du NMD publié en 2020.

Dans ce cadre, la CDN actuelle du Maroc soumise dans le cadre de l'Accord de Paris, fixe les
engagements conditionnés et engagements non conditionnés :

-  Les engagements non conditionnés visent une réduction des émissions de GES de
18,3% au moyen de politiques et mesures nationales autofinancées par le pays ;

- Les engagements conditionnés dépendent du soutien financier et technique
international et visent une réduction supplémentaire des émissions de GES pour
atteindre une réduction totale de 45,5%.

L'ambition marocaine est d'accélérer la transition énergétique notamment à travers les
énergies renouvelables, tout en renforçant la résilience face aux impacts du changement
climatique.

1.6. Plan Climat National

La gouvernance climatique au Maroc fait face à des défis institutionnels, juridiques, financiers
et technologiques, nécessitant une consolidation des efforts à travers la structuration des
projets d'adaptation et d'atténuation, la mobilisation des financements, et le renforcement de
la connaissance et de la surveillance climatiques. Le Plan Climat National 2030 (PCN 30)
constitue le cadre de coordination et de développement d'une politique climatique nationale
à moyen et long terme, permettant de répondre de manière proactive aux défis du
changement climatique.

Dans le cadre des objectifs de renforcement des écosystèmes marocains, le PCN 30 priorise
l'adaptation des secteurs et ressources clés. En matière d’atténuation, le plan vise à atteindre
les engagements du Maroc grâce à des mesures sectorielles couvrant l’énergie, l’agriculture,
les transports, les déchets, les forêts, l'industrie, et l'habitat. Ce plan consolidera les objectifs
d'atténuation de toutes les stratégies et plans d'action sectoriels.

VN



RAPPORT SUR LES ETABLISSEMENTS ET ENTREPRISES PUBLICS

Il. Bonnes Pratiques des EEP en matière de développement
durable et de transition verte

En vue de structurer et renforcer l'efficacité des financements publics et privés dans l'atteinte
des objectifs du NMD et de la CDN, un programme de Transition Budgétaire Verte (TBV) a été
lancé au sein du MEF avec l'appui de l'Agence Française de Développement (AFD).

Ce programme, étalé sur la période 2023-2027, a pour ambition d'aligner les finances
publiques sur les enjeux climatiques, à travers l'atténuation et l'adaptation aux effets du
changement climatique, tout en développant la finance climat. Ses objectifs incluent, entre
autres, la mise en place d'un cadre institutionnel pour la coordination de la gestion climatique,
l'étiquetage climat des budgets et l'usage d'instruments financiers tels que les obligations
vertes.

Le secteur des EEP constitue une composante principale du programme TBV, dans la mesure
où ces EEP interviennent dans la quasi-totalité des secteurs à forts impacts sur
l'environnement (eau, énergie, mines, BTP, aménagement, transport, logistiques, agriculture.…).

Ainsi, les EEP sont invités au respect des normes climatiques, ce qui permettra de répondre
aux attentes croissantes des investisseurs en matière de critères ESG (environnemental, social,
gouvernance) et facilite leur accès au financement durable.

Dans ce cadre, les EEP sont appelés à intégrer pleinement la transition écologique dans leur
stratégie, avec des mécanismes incitatifs et des politiques d'achats privilégiant les produits et
services verts. [Is doivent également développer des outils de reporting environnemental et
intégrer l'analyse des risques climatiques dans leur gestion.

Les activités des EEP exerçant des pratiques avancées en matière de limitation des émissions
de gaz à effet de serre peuvent être présentées comme suit :

H.1. Groupe OCP

Le Groupe OCP se distingue en tant que précurseur de la transition verte avec le lancement,
en 2023, de l’ambitieux Programme Vert 2023-2027, doté de 130 MMDH, axé sur le
développement durable et la décarbonation des activités du Groupe.

Ce programme vise à produire 20 millions de tonnes d'engrais décarbonnés d'ici 2027, grâce
à un investissement de 20 MMDH dans la production locale d'ammoniaque vert, réduisant ainsi
la dépendance aux importations.

ll'inclut également un plan de 11 MMDH pour développer 5 GW d'énergies renouvelables,
couvrant les besoins énergétiques du Groupe, ainsi que 23,5 MMDH pour des projets de
dessalement et de réutilisation des eaux usées, garantissant son autonomie hydrique.

OCP SA est la seule entreprise publique au Maroc à publier ses données climatiques selon les
normes de la Task Force on Climate Related Financial Disclosures (TCFD), qui constitue le
système le plus exhaustif et le plus exigeant en matière de reporting climatique.

Ainsi, le Groupe OCP est un acteur clé dans la réduction des gaz à effet de serre (GES),
contribuant à hauteur de 27,5% des objectifs du Maroc pour 2030. Le Groupe OCP vise la
neutralité carbone d’ici 2030 pour les scopes 1 (émission de l'activité propre de l'entreprise)

S



et 2 (émissions indirectes liées à l’énergie), et 2040 pour les scopes 1, 2 et 3 (émissions
indirectes significatives).

La stratégie énergétique du Groupe inclut une transition vers 100% d'électricité renouvelable
d'ici 2026 et une couverture complète de sa consommation en eau par des sources non-
conventionnelles.

L'empreinte carbone du Groupe OCP en 2021 est estimée à 19,9 millions de tonnes de CO2,
dont 16,1 millions relèvent du scope 3, avec une contribution significative des engrais azotés
et des matières premières importées.

H1.2. Tanger Med Special Agency

Le Groupe TMSA poursuit une ambition de neutralité carbone d'ici 2030 pour l’ensemble de
ses opérations. Sa feuille de route, établie en 2022, prévoit d'atteindre zéro carbone en
développant des infrastructures de connexion des navires à quai et en augmentant la
production d'énergie renouvelable.

Ces initiatives majeures incluent :

-  Le développement de centrales photovoltaïques et de connexions électriques pour
navires à quai :

- L'amélioration de l’efficacité énergétique par le remplacement des solutions lumineuses
conventionnelles, la mise en place de systèmes de management énergétique ISO 50001,
et l'introduction de solutions Smart Grid ;

- La mise en œuvre d'un plan d'action pour la valorisation des ressources, avec des
projets de traitement des eaux usées, gestion des déchets, et production de
biocarburant.

En matière de mobilité durable, le groupe prévoit de développer des infrastructures pour les
véhicules électriques et à hydrogène vert, de convertir sa flotte de véhicules et d'installer des
bornes de recharge.

Les réalisations en 2023 comprennent le déploiement de 24 véhicules électriques, l'installation
de 10 bornes de recharge, et l’incitation financière pour l'acquisition de véhicules électriques
et hybrides.

I1.3. Moroccan Agency for Sustainable Energy

Le programme de développement des Energies Renouvelables (EnR), constituant une
composante centrale de la stratégie de transition énergétique du Maroc, vise à atteindre une
part des EnR dans le mix électrique national de 52% en 2030, par la réalisation d'une capacité
de production d’électricité à partir de sources renouvelables de 10.000 MW.

La capacité installée en EnR à fin 2023 représente 41% du mix électrique national et atteindra
56% en 2027.

En outre, MASEN a été désignée comme point focal pour le développement de la filière de
‘hydrogène vert, qui constitue un vecteur efficace pour la conversion et l'alimentation en
énergie verte des activités et des filières dans tous les secteurs économiques (industrie,
mobilité, dessalement, transport etc.).

M



RAPPORT SUR LES ETABLISSEMENTS ET ENTREPRISES PUBI| s

I1.4. Office National des Chemins de Fer

L'ONCF continue de progresser dans sa démarche de réduction de l'empreinte carbone et de
promotion des pratiques durables, s'inscrivant dans la « Stratégie Innovante et Intégrée du
Rail à l'horizon 2030 ». Parmi les réalisations notables de 2023 :

-  Transition énergétique : La part de l'énergie verte dans le mix électrique a atteint 90%
en novembre 2023, contre 25% en 2022. Un audit d’efficacité énergétique a également
été réalisé, avec une stratégie élaborée pour renforcer la neutralité carbone du secteur ;

- Éco-conduite : Pratiques adoptées pour environ 225 trains par jour, réduisant
considérablement l’'empreinte carbone malgré une augmentation des voyages en train ;

-  Green Bonds : L'ONCF a reconduit la certification de sa première émission obligataire
verte, garantissant que les fonds sont exclusivement utilisés pour des projets à impact
environnemental positif ;

- Consommation d'eau : Baisse de 21% de la consommation d'eau par rapport à 2022,
avec la mise en place d'une station de traitement des eaux comme mesure non
conventionnelle ;

-  Économie circulaire : Valorisation de 2.348 tonnes de déchets pour la maintenance du
matéricl roulant :

-  Résilience : Poursuite du déploiement du schéma directeur de prévention des risques
sur le réseau ferroviaire, conformément aux directives en vigueur dans ce cadre ;

-  Projet de liaison à grande vitesse : Intégration de la dimension environnementale dans
le projet Kenitra-Marrakech, avec un schéma directeur et une Assistance
Environnementale et Sociale (AMO E&S) mises en place.

I1.5. Société Autoroutes du Maroc

ADM a intensifié ses efforts en matière de développement durable à travers deux grands
programmes :

- Programme Vert:

e  Reboisement : Plantation de 1.955 hectares avec 939.800 arbres et arbustes
adaptés aux régions autoroutières ;

e Lutte contre l’érosion : Techniques de génie biologique et ensemencement de
35 hectares de talus, production de 150.000 plants et création de
10.000 journées de travail ;

e  Préservation des ressources : Traitement des eaux usées pour l’arrosage des
espaces verts, réduction de la consommation d’eau de 4 millions de m* grâce au
compactage à sec, et prétraitement des eaux pluviales dans des bassins
déshuileurs ;

e Recyclage et réduction des déchets : Valorisation des matériaux pour
l'entretien des chaussées et réduction de 81% de l’utilisation du papier entre 2019

et 2022.



- Programme Azur :

e Energie durable : Installation de panneaux photovoltaïques dans quatre gares
de péage et remplacement des luminaires conventionnels par des LED dans 50%
des sites ;

e  Mobilité électrique : Mise en place de 33 bornes de recharge électrique sur le
réseau autoroutier et installation d’infrastructures pour véhicules électriques
dans 55% des aires de repos.

H1.6. Caisse de Dépôt et de Gestion

Le nouveau plan stratégique 2024-2030 de la CDG confirme la détermination du Groupe à
renforcer son rôle d'acteur majeur dans la construction d'un avenir durable et inclusif.

Ainsi, toutes les Branches du Groupe ont lancé des projets visant à atténuer l'impact
environnemental et à promouvoir une utilisation responsable des ressources, dont notamment
la CDG Capital, qui a adopté une politique RSE et obotenu une attestation de maturité « [ISO
26000 » avec un niveau « Avancé ».

Cette politique se traduit par plusieurs initiatives significatives :

-  Financement Durable : Depuis 2017, CDG Capital a été accréditée par le Green Climate
Fund (GCF) pour la mise en œuvre de financements verts, soulignant son engagement
envers des projets respectueux de l’environnement ;

- Financement Vert : Assistance à l'ONCF pour la structuration de la première émission
obligataire certifiée green dans le secteur des infrastructures, d’un montant d'un milliard
de dirhams ;

- (nvestissement Socialement Responsable : Lancement du fonds « CKG ISR
SELECTION », le premier fonds d'investissement socialement responsable au Maroc
dans la catégorie actions, intégrant systématiquement des critères environnementaux
dans la gestion des investissements ;

-  Formation et Sensibilisation : Organisation de sessions de formation pour les clients
et les collaborateurs sur les risques environnementaux et sociaux :

- Engagement International : Participation en tant que membre fondateur de
l'International Development Finance Club à une étude sur les ODD réalisée en 2022.

Par ailleurs, d'autres EEP participent également à des projets d'adaptation au changement
climatique, en particulier dans les secteurs de l'eau et de l'agriculture, à l’instar de l'ADA,
l'ANDZOA, les ORMVA, les ABH et l'ONEE, contribuant ainsi au renforcement de la résilience
face aux défis climatiques et environnementaux.



RAPPORT SUR LES ETABLISSEMENTS ET ENTREPRISES PUBLICS

ANNEXES



ANNEXE 1-A

I- LISTE DES ETABLISSEMENTS ET ENTREPRISES PUBLICS -271-

1.1- Etablissements Publics -228-

Sigle Raison sociale

AASIM AGENCE POUR L'AMENAGEMENT DU SITE DE LA LAGUNE DE MARCHICA

AAVER AGENCE POUR L'AMENAGEMENT DE LA VALLEE DU BOU REGREG

BH (10) AGENCE DU BASSIN HYDRAULIQUE

ADHA AGENCE DE DEVELOPPEMENT DU HAUT ATLAS

ADa ÀAGENCE POUR LE DEVELOPPEMENT AGRICOLE

aop AGENCE DE DEVELOPPEMENT DU DIGITAL

Ds | “ AGENCEDE DEVELOPPEMENT SOCIAL

ALEM AGENCE DE LOGEMENTS ET D'EQUIPEMENTS MILITAIRES

ANDIE AGENCE MAROCAINE DE DEVELOPPEMENT DES INVESTISSEMENTS ET DES EXPORTATIONS

AMDL AGENCE MAROCAINE DE DEVELOPPEMENT DE LA LOGISTIQUE

AMEE ÀAGENCE MAROCAINE POUR L'EFFICACITE ENERGETIQUE

AMMPS AGENCE MAROCAINE DE MEDICAMENTS ET DES PRODUITS DE SANTE

AMsD ÀAGENCE MAROCAINE DU SANG ET DE SES DERIVES

AMSSNUR AGENCE MAROCAINE DE SURETE ET DE SECURITE NUCLEAIRES ET RADIOLOGIQUES

ANAM AGENCE NATIONALE DE L'ASSURANCE MALADIE

ANAPEC AGENCE NATIONALE DE PROMOTION DE L'EMPLOI ET DES COMPETENCES

ANAS AGENCE NATIONALE D'AIDE SOCIALE

ANCFCC | AGENCENATIONALE DE LA CONSERVATION FONCIERE, DU CADASTRE ET DE LA CARTOGRAPHIE

ANDA AGENCE NATIONALE POUR LE DEVELOPPEMENT DE L'AQUACULTURE

ANDZOA AGENCE NATIONALE POUR LE DEVELOPPEMENT DES ZONES OASIENNES ET DE L'ARGANIER

sm | AGENCE NATIONALE D'EVALUATION ET D'ASSURANCE QUALITE DE L'ENSEIGNEMENT SUPERIEUR ET DE LA RECHRCHE _
SCIENTIFIQUE

ANEF AGENCE NATIONALE DES EAUX ET FORETS

ANEP AGENCE NATIONALE DES EQUIPEMENTS PUBLICS

As AGENCE NATIONALE DE GESTION STRATÉGIQUE DES PARTICIPATIONS DE L’ETAT ET DE SUIVI DES PERFORMANCES DES
ETABLISSEMENTS ET ENTREPRISES PUBLICS

ANLCA AGENCE NATIONALE DE LUTTE CONTRE L'ANALPHABETISME

ANP AGENCE NATIONALE DES PORTS

ANPMA AGENCE NATIONALE DES PLANTES MEDICINALES ET AROMATIQUES

ANPME AGENCE NATIONALE POUR LA PROMOTION DE LA PETITE ET MOYENNE ENTREPRISE

aNR ÀAGENCE NATIONALE DES REGISTRES

ANRAC AGENCE NATIONALE DE RÉGLEMENTATION DES ACTIVITÉS RELATIVES AU CANNABIS

ANRE AUTORITE NATIONALE DE REGULATION DE L'ELECTRICITE

ANAT ÀAGENCE NATIONALE DE REGLEMENTATION DES TELECOMMUNICATIONS



RAPPORT SUR LES ETABLISSEMENTS ET ENTREPRISES PUBLICS

ANNEXE 1-A
1.1- Etablissements Publics -228- (suite)

jgle Raïson sociale

ANRUR AGENCE NATIONALE POUR LA RENOVATION URBAINE ET LA REHABILITATION DES BATIMENTS MENAÇANT RUINE

ANSR AGENCE NATIONALE DE LA SECURITE ROUTIERE

TI ‘AGENCE POUR LA PROMOTION ET LE DEVELOPPEMENT ECONOMIQUE ET SOCIAL DES PREFECTURES ET PROVINCES DU
NORD DU ROYAUME

A AGENCE POUR LA PROMOTION ET LE DEVELOPPEMENT ECONOMIQUE ET SOCIAL DE LA PREFECTURE ET DES
PROVINCES DE LA REGION ORIENTALE DUROYAUME ——

= AGENCE POUR LA PROMOTION ET LE DEVELOPPEMENT ECONOMIQUE ET SOCIAL DES PROVINCES DUSUD DU
ROYAUME

ARCHIVES ARCHIVES DU MAROC

AREF (12) ACADEMIE REGIONALE D'EDUCATION ET DE FORMATION

AU(30) AGENCE URBAINE

BNRM BIBLIOTHEQUE NATIONALE DU ROYAUME DU MAROC

CADETAF CENTRALE D'ACHAT ET DE DEVELOPPEMENT MINIER DE TAFILALET ET FIGUIG

CaG (12) CHAMBRE D'AGRICULTURE

cn (3 | emavene D'annsanaT

« (CAISSE DE COMPENSATION

ccs (12) CHAMBRE DE COMMERCE, D'INDUSTRIE ET DE SERVICES

cm CENTRE CINEMATOGRAPHIQUE MAROCAIN

cG (CAISSE DE DEPOT ET DE GESTION

CR (CAISSE POUR LE FINANCEMENT ROUTIER

cHu() CENTRE HOSPITALIER UNIVERSITAIRE

CMAM CAISSE MAROCAINE DE L'ASSURANCE MALADIE

CMR CAISSE MAROCAINE DES RETRAITES

CNESTEN CENTRE NATIONAL DE L'ENERGIE, DES SCIENCES ET DES TECHNIQUES NUCLEAIRES

CNRA CAISSE NATIONALE DE RETRAITES ET D'ASSURANCES

CNRST CENTRE NATIONAL DE LA RECHERCHE SCIENTIFIQUE ET TECHNIQUE

Ns (CAISSE NATIONALE DE LA SECURITE SOCIALE

cPM (4) CHAMBRE DES PECHES MARITIMES

CRI (12) CENTRE REGIONAL D'INVESTISSEMENT

EACCE ETABLISSEMENT AUTONOME DE CONTROLE ET DE COORDINATION DES EXPORTATIONS

EHTP ECOLE HASSANIA DES TRAVAUX PUBLICS

eN ENTRAIDE NATIONALE

ENAM ECOLE NATIONALE D'AGRICULTURE DE MEKNES

ENSA ECOLE NATIONALE SUPERIEURE DE L'ADMINISTRATION

ENSMR ECOLE NATIONALE SUPÉRIEURE DES MINES DE RABAT



PROJET DE LOI DE FINANCES POUR L'ANNEE 2025 |

ANNEXE 1-A
1.1- Etablissements Publics -228- (suite et fin)

Sigle Raison sociale

FDSHII FONDS HASSAN II POUR LE DEVELOPPEMENT ECONOMIQUE ET SOCIAL
FEC FONDS D'EQUIPEMENT COMMUNAL

FFIEM FONDS DE FORMATION PROFESSIONNELLE INTER-ENTREPRISES MINIERES

lav INSTITUT AGRONOMIQUE ET VETERINAIRE HASSAN I1

IMANOR INSTITUT MAROCAIN DE LA NORMALSATION

INRA INSTITUT NATIONAL DE LA RECHERCHE AGRONOMIQUE

INRH INSTITUT NATIONAL DE RECHERCHES HALEUTIQUES

PM | insmTurPasteuR OUMAROC

IPSMGCA INSTITUT PRINCE SIDI MOHAMMED DES TECHNICIENS SPECIALISES EN GESTION ET COMMERCE AGRICOLE
ISCAE GROUPE INSTITUT SUPERIEUR DE COMMERCE ET D'ADMINISTRATION DES ENTREPRISES
LOARC LABORATOIRE OFFICIEL D'ANALYSES ET DE RECHERCHES CHIMIQUES DE CASABLANCA
Map AGENCE MAGHREB ARABE PRESSE

MoA MAISON DE L'ARTISAN

oc OFFICE DES CHANGES

onco OFFICE DE DEVELOPPEMENT DE LA COOPERATION

OFPPT OFFICE DE LA FORMATION PROFESSIONNELLE ET DE LA PROMOTION DU TRAVAIL
omnc OFFICE MAROCAIN DE LA PROPRIETE INDUSTRIELLE ET COMMERCIALE

ONcA OFFICE NATIONAL DU CONSEILAGRICOLE

ONCF (OFFICE NATIONAL DES CHEMINS DE FER

ONDA OFFICE NATIONAL DES AEROPORTS

ONEE OFFICE NATIONAL DE L'ELECTRICITE ET DE L'EAU POTABLE

ONHYM OFFICE NATIONAL DES HYDROCARBURES ET DES MINES

ONICL OFFICE NATIONAL INTERPROFESSIONNEL DES CEREALES ET DES LEGUMINEUSES
ONMT OFFICE NATIONAL MAROCAIN DU TOURISME

‘oNousc OFFICE NATIONAL DES OEUVRES UNIVERSITAIRES SOCIALES ET CULTURELLES

onp OFFICE NATIONAL DES PECHES

ONssa OFFICE NATIONAL DE SECURITE SANITAIRE DES PRODUITS ALIMENTAIRES

ORMVA (S) OFFICE REGIONAL DE MISE EN VALEUR AGRICOLE

RADEE (12) REGIE AUTONOME DE DISTRIBUTION D'EAU ET D'ELECTRICITE

TNMV THEATRE NATIONAL MOHAMED V

UNIVERSITES (13) UNIVERSITES



RAPPORT SUR LES ETABLISSEMENTS ET ENTREPRISES PUBLICS

ANNEXE 1-A

1.2- SOCIETES ANONYMES -43-

igle Raison sociale
ADER AGENCE DE DEDENSIFICATION ET DE REHABILITATION DE LA MEDINA DE FES
ADM SOCIETE NATIONALE DES AUTOROUTES DU MAROC
ASMAINVEST ASMAINVEST
BaM BARID AL-MAGHRIB
BIOPHARMA SOCIETE DE PRODUCTIONS BIOLOGIQUES ET PHARMACEUTIQUES VETERINAIRES
caMm CREDIT AGRICOLE DU MAROC
(CASATRANSPORTS | SOCIETE CASABLANCATRANSPORTS
DIYAR ALMADINA DIVAR AL MADINA
FMP FONDS MAROCAIN DE PLACEMENTS
FMGl FONDS MOHAMMED VI POUR L'INVESTISSEMENT
HAO HOLDING AL OMRANE
laM ITISSALAT AL-MAGHRIB
IDMAI SAKAN SOCIETE IDMAI SAKAN
ITHMAR ALMAWARID | _ ITHMARAL MAWARID
2N JARDIN ZOOLOGIQUE NATIONAL
LABOMETAL LABORATOIRE METALLURGIQUE D'ETUDES ET DE CONTROLE
MAROCIEAR DEPOSITAIRE CENTRAL - MAROCLEAR
MASEN MOROCCAN AGENCY FOR SUSTAINABLE ENERGY
Moss LA MAROCAINE DES JEUX ET DES SPORTS
Ma MOROCCO INVESTISSEMENT AUTHORITY
NWM SOCIETE NADOR WEST MED
o OFFICE CHERIFIEN DES PHOSPHATES SA
ram “ | ComPAGNIE NATIONALE DE TRANSPORT AERIEN ROYAL AIR MAROC
SALIMA HOLDING SOCIETE ARABE LIBYO-MAROCAINE HOLDING
saPT SOCIETE D'AMENAGEMENT POUR LA RECONVERSION DE LA ZONE PORTUAIRE DE TANGER VILLE
SIE SOCIETE D'INGENIERIE ENERGETIQUE
SMAEX SOCIETE MAROCAINE D'ASSURANCE À L'EXPORTATION
sMiT SOCIETE MAROCAINE D'INGÉNIERIE TOURISTIQUE
SNED “ | “ SOCIETE NATIONALE D'ETUDES DU DETROIT DE GISRALTAR
SNGFE (Ex-CCG) SOCIETE NATIONALE DE GARANTIE ET DE FINANCEMENT DE L'ENTREPRISE
SNRT SOCIETE NATIONALE DE LA RADIOFFUSION ET DE TELEVISION
SNTL SOCIETE NATIONALE DES TRANSPORTS ET DE LA LOGISTIQUE
SOCAMAR SOCIETE DE COMMERCIALISATION D'AGRUMES ET AUTRES FRUITS ET LEGUMES AU MAROC |
SODEP SOCIETE D'EXPLOITATION DES PORTS
SONACOS SOCIETE NATIONALE DE COMMERCIALISATION DE SEMENCES
SONADAC SOCIETE NATIONALE D'AMENAGEMENT COMMUNAL
SONARGES SOCIETE NATIONALE DE REALISATION ET DE GESTION DES EQUIPEMENTS SPORTIFS
SOREAD SOCIETE D'ETUDES ET DE REALISATIONS AUDIOVISUELLES "SOREAD""
SOREC SOCIETE ROYALE D'ENCOURAGEMENT DU CHEVAL
SOTADEC SOCIETE TANGEROISE D'EXPLOITATIONS COMMERCIALES
SRRA SOCIETE RABAT REGION AMENAGEMENT
TMPA TANGER MED PORT AUTHORITY
TMSA AGENCE SPECIALE TANGER MEDITERRANEE



PROJET DE LOI DE FINANCES POUR L'ANNEE 2025 |

ANNEXE 1-B

I- EEP DU PERIMETRE DE L'AGENCE NATIONALE DE GESTION STRATEGIQUE DES PARTICIPATIONS DE L'ETAT ET DE SUIVI DES

PERFORMANCES DES EEP - 57 -

11.1.- Etablissements Publics -15-

Raïson sociale

AASIM AGENCE POUR L'AMENAGEMENT DU SITE DE LA LAGUNE DE MARCHICA

AAVBR AGENCE POUR L'AMENAGEMENT DE LA VALLEE DU BOU REGREG

ANCFCC AGENCE NATIONALE DE LA CONSERVATION FONCIERE, DU CADASTRE ET DE LA CARTOGRAPHIE
ANP AGENCE NATIONALE DES PORTS

coG CAISSE DE DEPOT ET DE GESTION

HEc FONDS D'EQUIPEMENT COMMUNAL

FDSHIL FONDS HASSAN Il POUR LE DEVELOPPEMENT ECONOMIQUE ET SOCIAL

LOARC LABORATOIRE OFFICIEL D'ANALYSES ET DE RECHERCHES CHIMIQUES DE CASABLANCA
Map AGENCE MAGHREB ARABE PRESSE

OMPic OFFICE MAROCAIN DE LA PROPRIETE INDUSTRIELLE ET COMMERCIALE

ONCF OFFICE NATIONAL DES CHEMINS DE FER

ONDA OFFICE NATIONAL DES AEROPORTS

ONEE OFFICE NATIONAL DE L'ELECTRICITE ET DE L'EAU POTABLE

ONHYM OFFICE NATIONAL DES HYDROCARBURES ET DES MINES

onp OFFICE NATIONALDES PECHES

11.2.- Sociétés Anonymes -42-

1- Sociétés Anonymes à participation directe de l'Etat - 35 -

Sigle
aDM SOCIETE NATIONALE DES AUTOROUTES DU MAROC

Bam BARID AL-MAGHRIB

BIOPHARMA SOCIETE DE PRODUCTIONS BIOLOGIQUES ET PHARMACEUTIQUES VETERINAIRES
cam CREDIT AGRICOLE DU MAROC

DIVAR ALMADINA DIVAR AL MADINA

FM6I FONDS MOHAMMED VI POUR L'INVESTISSEMENT

Ha0 HOLDING AL OMRANE

IDMAISAKAN SOCIETE IDMAI SAKAN

ITHMAR AL MAWARID ITHMARAL MAWARID

PN JARDIN 200LOGIQUENATIONAL

SOCIETE LA MAMOUNIA,

SOCIETE LA MAMOUNIA

MAROCLEAR DEPOSITAIRE CENTRAL - MAROCIEAR
MASEN MOROCCAN AGENCY FOR SUSTAINABLE ENERGY
Mois LA MAROCAINE DES JEUX ET DES SPORTS

ma MOROCCO INVESTISSEMENT AUTHORITY
um SOCIETE NADOR WEST MED

oæ ocpsa



RAPPORT SUR LES ETABLISSEMENTS ET ENTREPRISES PUBLICS

ANNEXE 1-B
1- Sociétés Anonymes à participation directe de l'Etat - 35 - (suite et fin)

Raîson sociale

SAEDM SOCIETE D'AMENAGEMENT ET DE DEVELOPPEMENT DE MAZAGAN

sIE SOCIETE D'INGENIERIE ENERGETIQUE

SNED SOCIETE NATIONALE D'ETUDES DU DETROIT DE GIBRALTAR

SNRT SOCIETE NATIONALE DE LA RADIOFFUSION ET DE TELEVISION

SODEP SOCIETE D'EXPLOITATION DES PORTS
SONADAC SOCIETE NATIONALE D'AMENAGEMENT COMMUNAL

SOREAD SOCIETE D'ETUDES ET DE REAUSATIONS AUDIOVISUELLES "SOREAD"

SRRA SOCIETE RABAT REGION AMENAGEMENT

TMSA AGENCE SPECIALE TANGER MEDITERRANEE

.2- Sociétés Anonymes détenues, exclusivement ou conjointement par l'Etat, les établissements publics ou les entreprises
Publiques -7-

Raison sociale

je
ASMA INVEST ASMAINVEST
laM SOCIETE ITISSALAT AL-MAGHRIB

SALIMA HOLDING SOCIETE ARABE LIBYO-MAROCAINE HOLDING

SOCIETE TANGEROISE D'EXPLOITATIONS COMMERCIALES



ANNEXE 2
LISTE DES ETABLISSEMENTS PUBLICS EN COURS DE DISSOLUTION ET DES
ENTREPRISES PUBLIQUES EN COURS DE LIQUIDATION - 81 - (1/2)

Sigle Raison Sociale
AIR SENEGAL INTERNATIONAL | AIR SENEGAL INTERNATIONAL
AOÛLI MINES D'AOULI
ATLAS BLUE | ATLAS BLUE
BNDE BANQUE NATIONALE POUR LE DEVELOPPEMENT ECONOMIQUE
CITE DEUX DES JEUNES
“ om CHARBONNAGES DU MAROC ï]
CFPM | CONDITIONNEMENT DES FRUITS ET PRIMEURS
CHARIKA SOCIETE CHARIKA
caMa CIMENTERIE MAGHREBINE
cmso CITE MAROCAINE DE SIDI OTHMANE
COMAGRI | COMPAGNIE MAROCAINE DE GESTION DES TERRES AGRICOLES
| cOMAPRA COMPAGNIE MAROCAINE DE COMMERCIALISATION DES PRODUITS AGRICOLES
COTEF | _ COMPLEXE TEXTILE DE FES
CRNMDA CAVES DES ROCHES NOIRES
fe) | CITE TROIS DES JEUNES
eus CITE UN DES JEUNES
DIAFA | SOCIETE MAROCAINE HOTELIERE ET TOURISTIQUE DIAFA
EDITIONMI EDITIONS MAROCAINES ET INTERNATIONALES
ELKHEIR | SOCIETE EL KHEIR
EUROCHEQUE EUROCHEQUE MAROC
GEFS | LES GRANDS ENTREPÔTS FRIGORIFIQUES DU SOUSS
HALA FISHERIES HALA FISHERIES
HOLEXP | HOLDING EXPANSION
IMEC INSTITUT MAROCAIN D'ESSAIS ET DE CONSEILS
JADIVET | JADIDA VETEMENTS
METRAGAZ MAINTENANCE EXPLOITATION DE GAZODUC MAGHREB-EUROPE
MMA | PECHINEYM.MA
| NEW SALAM SOCIETE NEW SALAM H
OCE | OFFICE DE COMMERCIALISATION ET D'EXPORTATION
obi | OFFICE DE DEVELOPPEMENT INDUSTRIEL
PALMBAY PALMBAY
PERLITE PERLITE ROCHE
PROMAGRUM | PROMOTION DES AGRUMES AU MAROC
RAD REGIE AUTONOME DE DISTRIBUTION DE CASABLANCA
RAFC | REGIE AUTONOME DES FRIGORIFIQUES DE CASABLANCA
RAID REGIE AUTONOME DE DISTRIBUTION D'EAU ET D'ELECTRICITE DE TANGER
RATAG | REGIE AUTONOME DES TRANSPORTS URBAINS D'AGADIR
RATC REGIE AUTONOME DES TRANSPORTS DE CASABLANCA
RATF | REGIE AUTONOME DES TRANSPORTS URBAINS DE FES
RATM | REGIE AUTONOME DES TRANSPORTS URBAINS DE MEKNES
RATMA | REGIE AUTONOME DES TRANSPORTS URBAINS DE MARRAKECH



RAPPOI UR LES ETABLISSEMENTS ET ENTREPRISES PUBLICS

ANNEXE 2
LISTE DES ETABLISSEMENTS PUBLICS EN COURS DE DISSOLUTION ET DES
ENTREPRISES PUBLIQUES EN COURS DE LIQUIDATION - 81 - (2/2)
soon Sociale
RATR REGIE AUTONOME DES TRANSPORTS URBAINS DE RABAT-SALE
ï RATS REGIE AUTONOME DES TRANSPORTS DE SAFI
RATT REGIE AUTONOME DES TRANSPORTS URBAINS DE TANGER
RDE REGIE AUTONOME DE DISTRIBUTION D'EAU ET D'ELECTRICITE DE TETOUAN
j RED RABAT ELECTRICITE DISTRIBUTION ASSAINISSEMENT LIQUIDE
REP-MARINE Il REP MARINE
sABR SABR AMENAGEMENT
CHAINE HOTELIERE SAFIR
SBCIETŒRABE D'INETISSEMENT AGRICOLE |
[ SOCIETE AGRICOLE DE SERVICES AU MAROC
SOCIETE CIVILE IMMOBILIERE SEBTA
[F SCIME] Ï SCIMEN |
SCIRM SOCIETE CIVILE IMMOBILIERE ROSE MARIE
SCORE U SOCIETE DES CONSIGNATAIRES REUNIS
SCS (filiale ONHYM) SOCIETE CHERIFIENNE DES SELS
scva SOCIETE COOPERATIVE VINICOLE D'AIT SOUALA
[ scvM SOCIETE COOPERATIVE VINICOLE DE MEKNES
SEFERIF SOCIETE D'EXPLOITATION DES MINES DU RIF
SEPYK SOCIETE D'EXPLOITATION DE LA PYROTHINE DE KETTARA
SERECAF SOCIETE D'ETUDE ET DE REALISATION DE LA CHAINE DE FROID AU MAROC
SGAM KANTARA SGAM AL KANTARA
SIMEF SOCIETE D'INDUSTRIES MECANIQUES ET ELECTRIQUES DE FES
SINCOMAR SINCOMAR
E SLIMACO SOCIETE DE CONDITIONNEMENT DES AGRUMES POUR LE GHARB
sMADA SOCIETE MAROCO ARABE DE DEVELOPPEMENT AGRICOLE
SNDE SOCIETE NATIONALE DE DEVELOPPEMENT DE L'ELEVAGE
[ SÎ\IPP S})CIEÇE NÏAVTVIONALEÎDES PRODUITS ËETROLI ËR; ä
SOCICA SOCIETE CHERIFIENNE DE LA CITE OUVRIERE MAROCAINE DE CASA
SOCOBER SOCIETE DE CONDITIONNEMENT DES AGRUMES DE BERKANE
SOCOCHARBO SOCIETE COMMERCIALE DE CHARBONS ET BOIS
SODEA SOCIETE DE DEVELOPPEMENT AGRICOLE |
SODEVI SOCIETE DE DEVELOPPEMENT VITICOLE
SODIP SODIP
[ SOGETA l SOCIE'HÈ bÈGESTION DES TERÈES AGRICOLES |
SONARP SOCIETE DE NAVIGATION, D'ARMEMENT ET DE PECHE
SOPLEM SOCIETE DE PLANTATION ET D'EMBALLAGE OULED MAHALLA
SORASRAK SOCIETE REGIONALE D'AMENAGEMENT TOURISTIQUE DE SAIDIA
TELECART SOCIETE DE TELEDETECTION, DE CARTOGRAPHIE ET DE TOPOGRAPHIE
UIM UNION INDUSTRIELLE DE MONTAGE ÿ
VINICOOP SOCIETE COOPERATIVE VINICOLE DES BENI SNASSEN



ANNEXE 3-A
Bilan des opérations de privatisation régies par l’article 1°" de la loi n° 39-89

Sociétés transférées -1/3-

RECETTES
TE sIG SECTEUR D'ACTIVITÉ
EN MDH
33,34 27,00
février 1993 SODERS Fabrication de levure
2,39 1,60
avril 1993 CHELCO Confection de vêtements 32,00 10,20
juin 1993 40,00 94,30
en Transpon_t:rr:s{r: de passagers et
juillet 1993 me se 35,00 111,60
juillet 1993 PETROM Distribution de produits pétroliers 51,00 145,00
! |
août 1993 CIOR Fabrication de ciment 51,00 614,00
octobre 1993 SNEP Production de chlore, soude et PVC 20,00 364,30
CIOR Fabrication de ciment 34,00 329,20
rs n Transpnn-t=rrestre de passagers et P sn
messagerie
SHELL Distribution de produits pétroliers 50,00 450,00
février 1994 DRAGON-GAZ Distribution de produits pétroliers 50,00 0,90
mars 1994 CMH Distribution de produits pétroliers 50,00 100,10
35,00 89,30
avril 1994 SOFAC Crédit à la consommation
18,37 40,00
MOBIL MAROC Distribution de produits pétroliers 50,00 110,00
mai 1994
TOTAL MAROC Distribution de produits pétroliers 50,00 300,00
7634 1DH
août 1994 MODULEC Equipement électromécanique
848 Gratuit
septembre 1994 CTM-LN Transport terrestre 18,46 48,70
20,00 46,00
GENERALTIRE Industrie de pneumatiques -
octobre 1994 2,21 4,30
sN Holding financier 15,63 361,10
novembre 1994 sN Holding financier 51,00 1669,00
14,01 455,30
décembre 1994 BMCE Finance- Banque commerciale
3,00 82,90
avril 1995 BMCE Finance- Banque commerciale 26,00 1243,40
juin 1995 CIOR Fabrication de ciment 222 10,00
EQDOM Finance-Crédit 18,00 72,00
e — Industrie Textle, flés et fl retors de c en
coton, fils à coud
SICO-CENTRE Industrie Textile, prêt-à-porter 30,00 1,60
réeome cn nn 8998 | 1DH
SIMEF t l
juillet 1995 électriques 10,00 \ Gratuit
SOCHEPRESS Distribution de journaux 40,00 ] 24,00
août 1995 SOFAC Crédit à la consommation 0,81 1,50

A


RAPPORT SUR LES ETABLISSEMENTS ET ENTREPRISES PUBLICS

ANNEXE 3-A
Bilan des opérations de privatisation régies par l’article 1°" de la loi n° 39-89
Sociétés transférées -2/3-
RECETTES
ATE SIGLE SECTEUR D’ACTIVITI
ENMDH
septembre 1995 — SOTRAMEG Production d'alcool de mélasse 60,00 8,70
novembre 1995 _ EQDOM Finance Crédit aux consommateurs 1,54 5,00
mars 1996 SAMIR Raffinerie du pétrole 30,00 1504,80
mai 1996 [soMas Distribution de produits pétroliers 56,04 78,40
MAPROC Industrie cuir, chaussures 28,50 1DH
juin 1996 SAMIR Raffinerie du pétrole 1,11 47,30
SONASID Industrie Sidérurgie 35,00 42040 _
septembre 1996 sMI Mine-Argent 36,07 234,50
octobre 1996 FERTIMA Industrie-Engrais 30,00 120,10
TT Mine-Cobalt 40,00 88,00
janvier 1997 SAMINE Mine-Fluorine 35,00 38,50
SOMIFER Mine-Cuivre 34,20 68,40
avril 1997 FPZ Industrie-Fonderie de plomb 26,00 39,00
CNIA Compagnie d'assurance 78,57 310,20
mai 1997 SAMIR Raffinerie du pétrole 60,90 3157,50
scp Raffinerie du pétrole 66,33 425,70
BMCE Finance- Banque commerciale 10,80 744,30
juin 1997 13,00 84,50
sMI Mine-Argent
20,00 130,30
CIOR Fabrication de ciment 0,0045 0,04
octobre 1997
[SONASID Industrie Sidérurgie 62,00 837,10
mars 1998 SONASID Industrie Sidérurgie 3,00 3060 |
SAMIR Raffinerie du pétrole 5,77 296,10
juin 1998 4,30 27,80
scp Raffinerie du pétrole
3,00 16,30
novembre 1998 _ |SAMIR Raffinerie du pétrole 1,00 42,60
FERTIMA Industrie-Engrais 51,00 230,00
octobre 1998
RANCH ADAROUCH Elevage de bovins 50,00 33,00
décembre2000 _ SOTRAMEG Production d'alcool de mélasse 6,22 0,70
janvier 2001 \SNEP Production de chlore, soude et PVC 5,30 18,30
février 2001 laM Télécommunications 35,00 23345,00
mai 2002 |SICOME Industrie-Textile prêt-à-porter 11,40 2,20
octobre 2002 FERTIMA Industrie-Engrais 1,00 75,40
FERTIMA Industrie-Engrais 3,00 14,10
juin 2003
RT Tabacs 80,00 14 080,00
juillet 2003 SONIR p PR e 0 72,97 22,00
distribution de journaux
septembre 2003 | SOMACA Montage de véhicules 26,00 65,00

A



PROJET DE LOI DE FINANCES POUR L'ANNEE 2025 l

ANNEXE 3-A
Bilan des opérations de privatisation régies par l’article 1°" de la loi n° 39-89
Sociétés transférées -3/3-
A E RECETTES
DATE SIGLE SECTEUR D’ACTIVITÉ PART CÉDÉE %
EN MDH
décembre 2004 14,90 8896,20
IAM Télécommunications
janvier 2005 16,00 12 400,00
SUTA 93,94 518,60
SUCRAFOR 87,46 88,30
Transformation de la betterave et
septembre 2005 =
de la canne à sucre en sucre blanc
SUNABEL 94,53 237,30
SURAC 95,00 523,50
octobre 2005 SOMACA Montage de véhicules 12,00 30,00
juillet 2006 IAM Télécommunications 0,10 98,60
août 2006 RT Régie des Tabacs 20,00 4.020,00
septembre 2006 SOMATHES Agro-alimentaire 100,00 539,00
mai 2007 COMANAV Transport maritime 75,93 1182,20
juin 2007 DRAPOR Dragage des ports 100,00 327,60
juin 2007 JIaM Télécommunications 4,00 457130
SUTA 3,45 27,50
SUCRAFOR 3,45 3,50
s- Transformation de la betterave et
juin 2010 ;
de la canne à sucre en sucre blanc
SUNABEL 4,62 11,60
SURAC 5,00 27,50
fuiltet2on <m îrlul!atlun et commercialisation du mnan 515
juillet 2016 MARSA MAROC Exploitation des ports 40,00 192980
juillet 2019 JaM Telecommunication 8,00 8888,00



RAPPORT SUR LES ETABLISSEMENTS ET ENTREPRISES PUBLICS

ANNEXE 3-B
Bilan des opérations de privatisation régies par l’article 1°" de la loi n° 39-89
Hôtels transférés
DATE DENOMINATION DE L’HOTEL RECETTE EN MDH

février 1993 Amandiers 5,00
mars 1993 Tarik 15,20
septembre 1993 Basma 50,00
avril 1994 Toubkal 38,50
avril 1994 Volubilis 35,00
mai 1994 Transatlantique-Meknès 41,00
juin 1994 Les Iles 20,00
septembre 1994 Malabata 55,00
septembre 1994 Rissani 8,10
décembre 1994 Casablanca (Hyatt Regency) 180,00
décembre 1994 Zalagh 17,25
janvier 1995 Azghor 14,55
avril 1995 Doukkala 22,17
avril 1995 Oukaïmeden 3,01
mai 1995 Tour Hassan 50,00
mai 1995 Les Mérinides 30,00
septembre 1995 Friouato 13,00
septembre 1996 Splendid 0,30
octobre 1998 Tinsouline 5,50
octobre 1998 TransAtlantique- Casa 14,00
décembre 1998 Les Almoravides 24,50
décembre 1998 Les Dunes d'or 74,00
septembre 1999 Saghro 6,60
janvier 2001 Rose du Dadès 7,20
juillet 2001 Riad 10,00
novembre 2001 Madayaq 7,82



ANNEXE 4

Bilan des opérations de cession régies par l’article 9 de la loi n° 39-89

Situation au 30 septembre 2024

ATION RECETTES EN MDH
2002 Cession de 20 % du capital de la Banque Centrale Populaire (BCP) 544,00
2004 Cession de 21 % du capital de la BCP 768,00
2006 Cession de 7,5 % du capital de BMCE Internationale-Madrid 21,00
2011 Cession de 20 % du capital de la BCP au BPR 5300,00
2012 Cession de 10% du capital de la BCP 3306,00
2014 Cession de 6 % du capital de la BCP 2100,00
2015 Cession de 40% du capital de la société Mer Verte 43,00
2016 Cession de 33,24 % du capital de la SOMED 570,00
2019 Cession de 100% du capital de la Société d'Aménagement Ryad 900,00
2021 Cession de 35% du capital de la société Marsa Maroc 5305,32
2021 Cession de 10,34% du capital de la société Foncière UIR 110,40
2023 Cession de 49% du capital de la SAXEDM 1607,1
2024 Cession de 26% du capital de la Société La Mamounia 1700

S/TOTAL (B)



RAPPORT SUR LES ETABLISSEMENTS ET ENTREPRISES PUBLICS

ANNEXE 5
Affectation des recettes des opérations de privatisation

Situation au 30 septembre 2024

Recettes de

Période privatisation(en Part en %
MDH)

Recettes émanant des opérations de privatisation (liste annexée à la loi n° 39-89)

Etat (BGE) 1993-2024 63 574 64,1%
Fonds Hassan Il pour le Développement Economique | 001-2024 sm 34,6%
et Social

Fonds National de Soutien aux Investissements 2011-2014 327 0,3%
Fonds-de Développement Industriel et des 2015-2018 965 1,0%
Investissements

S/Total (A) = 99 188 100%

Autres recettes (article 9 de la loi n° 39-89)

Etat (BGE) 2002-2024 22275 100,00

S/Total (B)

Total général (A+B) - 121 463 100,00



PROJET DE LOI DE FINANCES POUR L'ANNEE 2025 |
ANNEXE 6

PRINCIPAUX INDICATEURS ECONOMIQUES ET FINANCIERS
DES ETABLISSEMENTS ET ENTREPRISES PUBLICS

REALISATIONS 2021 - 2023
(En Millions de DH)

VARIATION
ue É …

Chiffre d'Affaires 285 482 331 905 3320704 0,0%
Charges d'Exploitation (*) 228 583 298 683 279128 -7%
dont Charges de Personnel 39053 41 183 43208 & 5%
Valeur Ajoutée 97164 83 979 97698 16%
Résultat d'Exploitation Bénéficiaire (**) 41772 51 478 37323F -27%
Résultat d'Exploitation déficitaire (**) 10594 28 336 216904 23%

Résultat Courant bén

jaire (**) 35520 42149 32744F _ -22%

Résultat Courant déficitaire (**) 13041 35 357 220354 38%
Résultat Net bénéficiaire (**) 25506 34 220 26366 W _ -23%
Résultat Net déficitaire (**) 9485 33 176 17088 48%
Impôt sur les Sociétés 9746 10101 6567 W -35%
Investissements 64164 76 752 81285 À 6%
Dettes de Financement 296 706 328 206 326488 _ -1%
Capacité d'Autofinancement 52063 40224 3858 4%
Fonds Propres 642221 655 085 695 382 6%
Total du bilan 1737041 1845 276 1931 606 À 5%

(*)Hors dotations d'exoloitation
(”)Hors CNSS et CMR



RAPPORT SUR LES ETABLISSEMENTS ET ENTREPRISES PUBLICS

ANNEXE 7

TRANSFERTS DE L'ETAT AUX EEP

REALISATIONS A FIN 2023, PREVISIONS ACTUALISEES DE LA LOI DE FINANCES POUR L'ANNEE BUDGETAIRE 2024 ET REALISATIONS À FIN AOUT 2024 (EN MDH) (1/4)

atisées de 2024

m à 2025
EEP MARCHANDS
anven 166750 - 5000 - 0.00 - 5000 - 0.00
masun 1550 - 820 - 820 - 820 - 820
n 6084 80,00 - - 8000 7001 - - 7001
Casablance Améragement 20000 3000 - - 30,00 3000 - - 3000
MV pourl'investissement 50,00 - - - - - - è -
Hador WestMed 06.02 500,00 Z ë 500,00 20000 - - 20000
oncr 301904 168926 - 50000 21826 75400 - 500,00 125400
our 13472 - 4000 - 40,00 - 4000 - 4000
oure 54287 14572 - 400000 | sesn 6200 - 4000,00 4062.00
r. 20000 - 400,00 - 400.007 - 400,00 5 00.00
ns 30150 200,00 - - 20000 - - -
sà 4000
su 2870 - 1500 - 15.00 - 1500 - 15.00
DL ESSAOUIRA CULTURE - 1500 - - 15,00 1500 - - 15,00
sr 6200
sT 204470 38970 - - 38970 17800 - - 17800
se 1200 - 1200 - 1200 - 1200 - 1200
soaT 1517,00 500,00 98470 6783 — 216363 300,00 97820 67833 1957.13
SOREAD-2M 29652 6500 2100 100,00 186,00 6500 2100 100,00 186,00
65235 45000 = - 45000 26000 = n 26000
E 250
SNGFE (Ex-CS) 497,00 26800 - - 26800 200 - - 200
us - 1000 - - 1000 1000 - - 1000
cm 1600.00



ANNEXE 7

TRANSFERTS DE L'ETAT AUX EEP

REALISATIONS A FIN 2023, PREVISIONS ACTUALISEES DE LA LOI DE FINANCES POUR L'ANNEE BUDGETAIRE 2024 ET REALISATIONS À FIN AOUT 2024 (EN MDH) (2/4)

Préviions actuaisées de 2024 Résliations à fin soût 2024

Réaliations à fin 2023

Fonct Aug. apitai Aug-caphal
EEP NON MARCHANDS
—0n 49942 44374 147,74 - 59148 17282 51,00 - 223,92
pn 10100 5500 6300 - 11800 4000 5675 - 9675
20D 15170 35,00 5600 - 2100 = 5 5 {
ADHATIAS 5 444,60 = n 44460 - = n =
ANRUR 53,00 6000 17,00 - 77100 ; ; Z -
20s 12000 10,00 14000 - 15000 - 7000 - 7000
ue 395,00 295,00 - - 395,00 = 5 & -
AMDIE 5000 2000 4473 - 13473 = 5 ; :
ampt. 15400 18370 32,00 7 22570 - = - -
mc 55,00 840 4801 - 5641 840 an - 3611
AMSSNUR 35,50 250 3650 - 4000 - 15,00 - 15,00
ANAPEC m 11400 27430 G 388,30 - 187,36 - 187,36
anDa 60,55 12055 32,86 - 15341 - 1440 - 1440
anozon. 220,00 152,00 6100 - 213,00 65,00 3525 - 10025
ANGSPE 100,00 2000 8000 - 100,00 2000 8000 - 100,00
anep 186,00 50,00 140,00 - 190,00 “ 5 3 ;
AnF 1099,00 17000 802,00 - 27200 100,00 400,50 - 500,50
nn 27380 450,00 75,00 - 525,00 225,00 37,50 - 262,50
anpMA 840 5.00 200 - 1400 - = n =
ANDME 300,00 372,00 - - 37200 300,00 - - 300,00
annac 50.00 2000 3000 - 50.00 2000 3000 - 50.00
nn 200 3800 - 000 - 19,00 - 19,00
avou 0.00 8000 - - 8000 8000 - - 8000
æpD0 11000 8000 - - 8000 8000 - - 8000
00s 230,00 3400 S = 84,00 8000 = = 8000
APON & APDO & APDS 500,00 - - 500,00 - - n -

Arives du Maroc 10,00 - 10,00 - 10,00 - 10,00 - 10,00


RAPPORT SUR LES ETABLISSEMENTS ET ENTREPRISES PUBLICS

ANNEXE 7

TRANSFERTS DE L'ETAT AUX EEP

REALISATIONS A FIN 2023, PREVISIONS ACTUALISEES DE LA LOI DE FINANCES POUR L'ANNEE BUDGETAIRE 2024 ET REALISATIONS À FIN AOUT 2024 (EN MDH) (3/4)

n actuaisées de 2024 Réslisations àfin

Réaliations à fin 2023

Fonct Aue. capital Aug. caphal Toni

EEP NON MARCHANDS
ncF 2308821 5347,89 2286479 - 2821268 | 139666 15602,95 - 1699961
Agences Urbaines 676,10 23000 575,00 - 805,00 182,00 356,80 ; 488,80
sr 37,00 200 37,00 - 4600 - 18,50 - 18,50
cs 3489 - 4100 - 4100 - 41,00 - 4100
cm 8920 520 5900 - 6420 520 5900 - 6420
om 13574 - 9605 - 96.05 - 9605 = 9605
n 103,00 103,00 - - 103,00 2346 - - 2346
Chambres d'agrculture 15034 8085 87,00 - 16785 3640 62,08 - 0848
(Chambres d'Atisanat 2895 - 2908 - 2909 - 2908 - 2909
Chambres des Pêches Maritimes 18,30 200 600 - 200 - 481 - 481
ur 290,00 5000 480,00 - 530,00 = = « Z
us 1208,00 50,00 00,00 - 250,00 - 450,00 - 50,00
cuu 455,62 2000 41000 - 430,00 ë = = ë
( MedVi Marrakec 45413 2000 410,00 = 430,00 = = 2 -
CiMedViOuida 218,98 2000 222,00 & 24200 = 5 & -
OH Tanger 11800 10,00 400,00 - 410,00 - 20000 - 200,00
OH Agadir - 5000 - 5000 = 5 & -
uesTen 13055 4110 8545 - 12655 2055 42,73 - 6328
us 4128 1578 8820 - 103,98 - 5720 - 5720
œ 300,00 7000 23000 - 300,00 7000 23000 - 300,00
u 3000 2000 22,00 $ 42.00 - = 5 2
enam 10035 2600 7300 - 29,00 17,00 39,65 - 5665
ensa 35,00 5,00 3000 - 35,00 500 3000 - 35,00
Ense. 83,00 840 7800 - 8640 840 3900 - 4740
ENTRADE NATIONALE 415,40 4000 415,00 - 455,00 - 207,50 â 207,50

A HASSANI 23548 8400 20000 - 284,00 58,00 11000 - 16800



ANNEXE 7

TRANSFERTS DE L'ETAT AUX EEP
REALISATIONS A FIN 2023, PREVISIONS ACTUALISEES DE LA LOI DE FINANCES POUR L'ANNEE BUDGETAIRE 2024 ET REALISATIONS À FIN AOUT 2024 (EN MDH) (4/4)
évisions actumlisées de 2024 élisations à finaoût 2024

Réaliations à fin 2023

Fonct Aue. capital Toni Aug- caphal

EEP NON MARCHANDS

ê8.

mn 20065 14600 16606 ; 31206 25,00 2200 B
ms 27450 6690 13200 - 19.50 3160 78s - 10445
vu 3700 1000 3700 - 4700 - = 3 ë

pstarsocn 1420 500 1050 - 1550 250 sn - sn
scx —23 - 5188 3 5188 - 2534 - 2594
sm 3000 - 3000 - 3000 - 3000 - 3000
m 33479 62 29340 - 29966 62 293,40 - 29966
mon 6000 11000 - - 11000 700 - - 7000
00c 36.00 - 4200 - 4200 - 2100 - 2100
orvrr 114550 106000 76600 z 1826.00 - 15000 - 15000
onca 37450 13704 31984 - 45638 6900 17500 5 24400
onouse 266945 14000 255450 ë 269450 4000 152336 - 1963,36
ns 107100 76000 597,28 ë 135728 200,00 25000 ë 49000
c 3 Z P ë 878 5 878 - 878
onva. 339335 292186 35000 E 32186 — 1562 202,00 ë 153829
mn 2300 - 2100 - 2100 - 1050 - 1050
Universtéses tab.c'enseen.sup- 162428 177537 186015 , 3655.56 22000 57038 ë 70038

2405,7 38902,1 5 6 980,7 241822 36 441,7



RAPPORT SUR LES ETABLISSEMENTS ET ENTREPRISES PUBLICS

ANNEXE 8

RECETTES DES PRINCIPALES TAXES PARAFISCALES PERCUES AU TITRE DES ANNEES BUDGETAIRES 2021, 2022 et 2023
PAR LES ETABLISSEMENTS ET ENTREPRISES PUBLICS : REALISATIONS AU TITRE DES LOIS DE FINANCES 2021, 2022 ET 2023

AMMC

ANPME
EACCE

MDA

AMDIE

Caisse de Compensation

ccIs

Chambres d'Artisanat

Chambres de Pêche
Maritime

NARSA ( ex CNPAC)

Entraide Nationale

INRH

opco
OFPPT

ONICL
ONMT
OoNP

SNRT

Taxe parafiscale (en MDH) | 2021 2022 2023
Taxe parafisclae de contrôle du marché boursier 1186 9,72 9,20
Taxe Parafiscale à l’Importation (Plafond) 52,26 52,26 52,26
Taxe Parafiscale à l’Importation (Plafond) 240,00 200,00 241,70
Taxe Parafiscale à l’Importation (Plafond) 34,93 40,00 39,19
Taxe parafiscale sur les tapis Estampillés 0,04 0,03
Total 34,97 40,03 39,19
Taxe parafiscale à l'importation y compris le
Ç 292,77 293,97 293,97
solde à affecter par le CA
Amendes de Transport (AMT) 0,47 0,09 0,03
Décime Additionnel de la Taxe Professionnelle 200,49 130,69 200,40
Décime Additionnel de la Taxe Professionnelle 119,23 112,75 82,36
Décime Additionnel de la Taxe Professionnelle 10,00 22,87 16,10
Taxe des Assurés 142,34 152,01 164,48
Assurances 35,76 39,07 41,33
Carburant 291 4,18 3,26
Automobile 14,80 20,21 21,34
Centres de Visite Technique 28,39 36,43
22022 243,86 266,84
Surtaxe d'Abattage 6,68 4,78 7,77
Prélèvement sur le Pari Mutuel Urbain sn Tès se
Marocain
Taxe parafiscale sur les tapis Estampillés 0,04
Total 255,22 192,03 | __ 153,58 |
Taxes de Recherche Halieutique 14,79 12,76 15,28
Taxe d'Affrètement pour la pêche des espèces A ; N
pélagiques
Total 14,79 12,76 15,28
Taxe de Développement Coopératif 084 0,73 0,28
Taxe sur la Formation Professionnelle 2973,00 2877,00 3327,00
Taxe de commercialisation des céréales et des
Mn 137,60 176,83 145,43
légumineuses
Taxe aérienne 164,08 - e
Taxe de Promotion Touristique (TPT) 40,00 20,00 195,00
Taxe d'Affrètement pour la pêche des espè
axe d'Affrètement pour la pêche des espèces 1800 2050 a10,4
pélagiques
Taxe pour la Promotion du Paysage Audiovisuel s75D sr en

National (TPPAN)

5 062,79 281639 | 564350 |



ANNEXE 9

PRODUITS PROVENANT DES ETABLSSEMENTS ET ENTREPRISES PUBLICS AU PROFIT DU BUDGET GENERAL DE L'ETAT :
REAUSATIONS DE LA LOI DE FINANCES 2023 ET PREVISIONS DES LOIS DE FINANCES 2024 ET 2025 (EN MDH)

DESIGNATION DES RECETTES Réalisations LF 2023 | Prévisions LF2024 | Prévisions PLF 2025

|Produits à provenir c'organismes financ

Produt à provenir de Bank A-Maghrib 573 17000 30000
Dividendes à provenirdu Crédit Agricole du Maroc (CAM) 1000 500
Produit à provenir du Fonds d'Equipement Communal(FEC) 1000 1500
Produs à provenir de l'ffice des Changes (OC) 1500 1400 1500
Dividendes à provenirdes participations de l'Etat dans ls socétés et organismes internationaux ms

Centrale de Résssurance (SCR} 365 200 200

|Produis des monopoles, parts de bénéfices et contributions des établissements publcs

mmn srémtetrénasmeatmrtitars | iml œl 1m

; de Productions Biologiques, Pharmaceutiques et Vétérinaires (BIOPHARMA) 17 20 00

Royale d'Encouragement du Cheval (SOREC) ma 250 100

 Marocaine 'Ingénierie Touristique (SMIT) 200

Dividendes à provenir des participations financières de l'Etat dans diverses sociétés 2502 2330 8393

|Redevances pour l'occupation du domaine publicet autres produits

|Redevances pour l'occupation du domaine public provenant de l'Office National des Aéroports (ONDA) 2800 1200 1500
Redevances pour l'occupation du domaine publi provenant de l'Agence Nationale des Pors (ANP) 1100 u00
Produts divers

Produits de licences à provenir d'opérateurs de élécommunications 2s

JTOTAL DES PRODUITS PROVENANT DES EEP 135874 258800

Produits de cession des partcipations d l'Etat 1607 2000 2000

[rora censraL 155945 24 2800 285460


RAPPORT SUR LES ETABLISSEMENTS ET ENTREPRISES PUBLICS

ANNEXE 10

INVESTISSEMENTS DES EEP PAR SECTEUR (EN MDH) (1/2)

SECTEUI

TMSA 1493 2204

CASA TRANSPORTS 1652 948 828

NWM 1366 2772 826

ONCF 1133 3808 2969

oNDA 1400 1775 3594

LS ADM 901 2054 2658

ET TRANSPORT

ANSR 669 633 619

ANP 515 978 745

CFR 12 1420 1419

AUTRES EEP 1248 cRebe 1499

ORMVAs 2475 4563 3210

ANCFCC 373 3479 3644

ONSSA 367 329 375

ONCA 85 135 246

AGRICULTURE ET e E = ==
PECHE MARITIME

SOREC 52 56 56

ADA 47 55 60

AUTRES EEP 1355 2042 2072

GROUPE HAO 4548 5466 6433

SRRA 3747 3131 1514

APDs 2449 1929 1829

HABITAÏ' URBANISME CASA AMENAGEMENT 632 759 759

DEVELDï… ENT IDMAJ SAKAN 275 293 293

TERRITORIAL AAVBR 282 219 219

ALEM 202 790 767

AUTRES EEP 451 506 493

GROUPE OCP 27400 44800 45000

ONEE 6823 9921 13788

REGIES DISTRIBUTION 2494 4033 5896

ENERGIE, MINES, EAU es = se =

ET ENVIRONNEMENT
CONHYM 194 521 458
AUTRES EEP 62 5732 7597

CN EN
N



PROJET DE LOI DE FINANCES POUR L'ANNEE 2025 l

ANNEXE 10

SOCIAL, SANTE
EDUCATION ET
FORMATION

TOURISME ET
ARTISANAT

CDG GROUPE
FDSHII
CAM
BAM
AUTRES EEP 30 170
AREFs 6059 7516
UNIVERSITES 794 2465
OFPPT 385 2156
CHUs 488 507 702
INRA 137 196 248
oNoUsc 90 100 140
IAV 98 111 106
EN 69 249 206
INRH 39 41 38
CMR 8 58 31
ANAM 3 76 11
AUTRES EEP 195 864 889
1THMAR CAPITAL 109 146 89
sMIT 59 462 415
ONMT 92 92 92
MDA 52 S 9
AMDL 345 303 545
ADD 164 227 300
SNRT 87 185 185
AMDIE 108 159 720
AUTRES EEP 149 217 345
TOTAI 853 1091 2094
TOTAL GLOBAI 81285 132067 | 137700

{*) Après approbation des budgets

E

INVESTISSEMENTS DES EEP PAR SECTEUR (EN MDH) (2/2)

EEP



Annexe 11 Azazeall Y JÉS 5 Sl sl 0 Ÿ Aino 5 L 11 Æ3 dald
FICHE SIGNALETIQUE DES PRINCIPAUX EEP

GROUPE SOCIETE NATIONALE é BJU duil 5li Às ûll de gane
DES AUTOROUTES DU MAROC Autoroutes du Maroc 6+}AÂL_I Byludd
SIGLE ADM (MAISON MERE) L eS)
CAPITALSOCIAL " MilfionsdeDH — ps uode | el d 5
DATE DE CREATION ‘ [ d |

CLASSIFICATION

JURIDIQUE P
CONSTRUCTION ET

ACTIVITE EXPLOITATION DES p
AUTOROUTES

CATEGORIE MARCHAND
TOTALE

PARTICIPATION _ ;

eoanaue ( DIRECTE cNN
INDIRECTE

( Consolidés selon IFRS —

Indicateurs économiques et financiers
consolidés du Groupe ADM (*) En Millions de Dhs …;….1_

MMŒŒ

Effectif (du groupe) âs saxdi)
Charges de personnel 249 229 249 Gts S
Charges d'exploitation HD 1467 1819 2313 Ébaaid GlGal G5s JME CIS
Chiffre d'Affaires 3778 A 015 4731 EDdadli ,
Valeur ajoutée 2567 1583 2674 Réundti As
Impôt sur les Sociétés 31 29 30 SËI e ds
Résultat Net part du groupe 436 -910 1294 uel e
CAF 893 -824 1023 SVN J pl 596
Total actif 74 668 74 040 76 108 Jy0ÿl E gape
Fonds propres 22 476 21509 22 569 Assan Jgt
Dettes de financement 36 673 36 885 37 282 sD C 5s
Investissements (paiements) 872 664 901 (Cdelaÿt) Ss LUI
Gouvernance (Maison mère) Al >
Nombre de réunions Erp ec
Conseil d'administration PTETTT « EN sJS ds Certification des comptes
Comité d'audit PE 6 ‘mvm comptes ïî dl
Comité stratégie e s97377 , 55 50 certifiés RE — igle 500
IM 2022 # 2023

ul Indicateurs d’activité

Nombre de véhicules (s1s 5 1000) 25:t B CLS Al d
par jour ( 1000 unités )

2021 2022 2023



Annexe 11 Azazeall Y JÉS 5 Sl sl 0 Ÿ Aino 5 L 11 Æ3 dald
FICHE SIGNALETIQUE DES PRINCIPAUX EEP

GROUPE AGENCE NATIONALE m= ctpattidjaiaie Aissir da es

DES PORTS P r
sll Informations de base Aole Ciesl»n fs
SIGLE ‘ ANP (MAISON MERE) Alussall je)
CAPITAL SOCIAL ‘ Millions de DH 2062,8 pæ33 d9de eliis Yl JLN p
DATE DE [ ] C
CREATION | 01/12/2006 ll
CLASSIFICATION ;J v
SoRibiqué \ ETABLISSEMENT PUBLIC OS Cn
[ DEVELOPPEMENT ET MAINTENANCE A
ACTIVITE | DES PORTS ET REGULATION DE És US
| L'ACTIVITE PORTUAIRE
ï
CATEGORIE | MARCHAND —

Indicateurs économiques et financi:
consolidés du Groupe ANP (*)

({*) Consolidés selon la norme marc

E e se EnMilionsdeDhs = passcee

Indicateurs 2021 2022 2023 El pèige
Effectif (du groupe) 2302 2328 2327 (Âs gandll) Guossiuue) sS
Charges de personnel 348 352 398 Gedivd C0 S
Charges d'exploitation HD 1519 1363 1422 claass Ghuist qqs PUIUY CIS
Chiffre d'Affaires 2182 2317 2770 CDldrdli É
Valeur ajoutée 1302 1516 1873 déun) AN
(Impôt sur les Sociétés 42 36 79 US SEN S uy
Résultat Net part du groupe -16 -20 155 él G
CAF 678 874 939 5l J p 546
(Total actif 23 028 23 755 24 855 Jpa3) E sane
Fonds propres 7 941 9841 9 859 AN Jl
Dettes de financement 7139 7286 6 869 Jagaill G ps
(Investissements (paiements) 1591 911 515 <û\c—\à"l\)ûp}nﬁu‘l\
r —"
Nombre de réunions pF =
Conseil d'administration - 2 — 53671 Gs pc th
Comptes 2021 ds
Comité d'audit - 2 — é t es 22 —L d

# 2021 2022 # 2023

ul Indicateurs d’activité

Conteneurs (hors TMSA y/c privé) en 1 000 EVP Trafie global (hors TMSA) (Millions T)
(52m5 1000) Gilydall su (0b asale) jaç0ll ÂSn

91,0 87,2

2021 2022 2023 2021 2022 2023



Annexe 11 Azazeall Y JÉS 5 Sl sl 0 Ÿ Aino 5 L 11 Æ3 dald
FICHE SIGNALETIQUE DES PRINCIPAUX EEP

GROUPE POSTE MAROC

257 Gkall à » Àe sans

Informations de base

SIGLE BAM (MAISON MERE) ] Al ja)
CAPITAL SOCIAL Millions de DH — 1191,4 c æs ds | PSCTRS PUN
DATEDECREATION | 07/08/1997
( CLASSIFICATION IEREN
bür RQUE | SOCIETE D'ETAT
| COURRIER / MESSAGERIE/ — Sloust 22309 GLJLe3V '
ACTIVITE POSTE DIGITALE / SERVICES SE E P 5;Ë|
CATEGORIE

PARTICIPATION
PUBLIQUE PE STE
INDIRECTE

Aze ganll Ln

({*) Consolidés selon la norme marocai

Indicateurs économi
consolidés du Groupe POSTE MAROC (*) mtc depr

ETE

Sahgall Al 4..ALAÀ‘ …‘v,.:.}…‘v

Effectif (du groupe) 8737 8466 8374 Âs ganall ) Guass uel se ;
Charges de personnel 1416 1420 1414 Gsess su ANS
Charges d'exploitation HD 3086 3389 4153 Ckacaial cSS sù JSN S |
Chiffre d'Affaires 2941 3075 3493 dl ËJ\
Valeur ajoutée 1280 1114 752 AéLna us
Impôt sur les Sociétés 268 37 198 US $ËS 5 dn
Résultat Net part du groupe 379 -114 285 uel
Total actif 86 925 102 541 105 002 Jyati &J‘“‘
Fonds propres 3056 2836 3009 As J
\Dettes de financement 1401 2036 3112 Jagaill es
\Investissements (paiements) 109 359 218 (Glelaÿ) «:«Ukä:—«‘!\‘
Gouvernance (Maison mère) AASAN

ebluati As ésLadi
Nombre de réunions l agell us
Certification des comptes

Conseil d'administration “
certifiés 5023 Loile 5sLalt

# 2021 2022 m2023

ul Indicateurs d’activité

Nombre de comptes CCP (1000)

(4000) & fail u58 cu 35 Nombre de comptes CEN (1000)

bs pab51 Ggaue CLl 38

3815 4391

2021 2022 2023 2021 2022 2023



Annexe 11 Azazeall Y JÉS 5 Sl sl 0 Ÿ Aino 5 L 11 Æ3 dald
FICHE SIGNALETIQUE DES PRINCIPAUX EEP

GROUPE CREDIT AGRICOLE \‘/ u Dl pa,All de
DU MAROC p p p E rrr TVA0S S —
ull _ Informations de base Acle A ——
SIGLE CAM (MAISON MERE) ] Al ja)
(CAPITALSOCIAL | C 042277 — 1 e ]
DATEDECREATION | 01/06/2004
(CLASSIFICATION A E E E
Hiapieus | FILIALE PUBLIQUE
ACTIVITE BANCÇAIRE | ASa dueie
doogas daJla dueie

CATEGORIE \ INSTITUTION FINANCIERE PUBLIQUE

PARTICIPATION
PUBLIQUE [ DIRECTE
INDIRECTE

Aze ganll Ln

(*) Consolidés selon IFRS

En Millions de Dhs ps

Effectif (du groupe) 3865 3874 3918 (s ganall) uel us
Charges de personnel 1196 1207 1232 Gs '—ë"‘£‘
PNB 4347 3966 3743 iua) 55 A
Valeur ajoutée s543 5173 4976 déLadi Â._.ﬂ\‘
Impôt sur les Sociétés 195 77 24 MS HËN IS Âs
Résultat Net part du groupe 406 69 42 iuat @:J\‘
Total actif 130 600 142 718 140 140 Jpal E su
Fonds propres 12 033 12 751 13 522 Asu J\,-‘n\
Dettes de financement 13 662 18 919 14 535 Daseill O s8
uf Gouvernance (Maison mère) RSN VIN
Nombre de réunions rr ékuall S éauadl
Conseil de surveillance œ >: MEN G ue Certification des comptes
Comité des grands risques 21 3 E REN PR ts 2003 — ||Lele 61<48
Comité de nomination et de 10 RE TPE
Témunération =2021 2022 m2023

ul Indicateurs d’activité

Base de la dientèle petits agriculteurs Nombre de coopératives financées
GHN jäue Ge p Dlaall Ss l Agadll cL plailiaus
100 086 fUs 1102 768

717

2021 2022 2023 2021 2022 2023



Annexe 11 Aza gaall SV JÉS 5 SLs sl 0Y dn J 11 53 és
FICHES SIGNALETIQUES DES PRINCIPAUX EEP

GROUPE CAISSE DE DEPOT ‘ l ' A pl g EIANN G gake de 5as
ET DE GESTION E
—2 rales

SIGLE CDG (MAISON MERE) Auus sl j4)
CAPITAL SOCIAL Millions de DH 12 304,8 645 dsde ] eliis Yl JLN p
DATE DE 1 =
CREATION cd es
CLASSIFICATION TPE VEREE
JURIDIQUE p G
ACTIVITE Écepi el
CATEGORIE dl

Indicateurs économi
consolidés du Gro

Effectif (du groupe) 6715 6643 6608 (4 ganal) Guass uel ds ‘
Charges de personnel 2228 2470 2575 Cs udl u_.ns‘
PNB 9960 5653 10 254 él 553 5.\:J\î
Impôt sur les Sociétés 2179 1318 1430 As ÉN IS Lu p
Résultat Net part du groupe 1629 -2 022 1371 uel u
Total actif 324 693 339 632 355 463 Jyssl E_,Aæ-ﬂi
Fonds propres 19 846 18 087 19 718 AI3n JI gayl
uë Gouvernance AcSAN

ebluati As ésLadi
Nombre de réunions prores ull ls b

Certification des comptes
Commission de surveillance - 4 - PEPEN
Z Comptes = (SEVAN
Comité d’audit et des èMfÉi 2022 h—\'°v/ su
Comité stratégie et

ité st ü J, dn nl
investissement Æ = 2021 2022 m2023 ?

u Indicateurs d'acti

Investissements (paiements en Millions de Dhs) (phlzall GaDle Gl Iaÿ) IL

4805
3417

2021 2022 2023



Annexe 11 As gaalf CN Jl y Cs 5all 0Y An GUs 11 53 és
FICHES SIGNALETIQUES DES PRINCIPAUX EEP

CAISSE MAROCAINE DES
RETRAITES

rales

Informations G

SIGLE As je)
CAPITAL SOCIAL el JJl p
DATEDE EN . 4e
CREATION C es
CLASSIFICATION Tt A
JURIDIQUE | qs
ACTIVITE | DES RETRAITES DU SECTEUR És sd EUs
| PUBLIC
f 1
CATEGORIE | ORGANISME SOCIAL | 2

Indicateurs éc
de la CMR

‘Effectlf Gratiiuuell ds
äCharges de personnel 136 141 145 Gs CANS

miques et financi
EnMillionsdeDhs »>c

(Cotisations et contributions 36 517 41266 40 285 Éslan lll 5 OS
Pensions et prestations 45 331 47 648 50 157 Sasis CL
Solde technique -8 815 -6 381 =9-871 sé EU
îFonds propres 71005 69 687 64 996 AIN J pl
Total actif 73 761 73 402 69163 Js3 E sans
3lnvestissements (paiements) 19 19 8 dstehsÿ) G L ÉN

Gouvernance
ibbuait ds ésuadi
Nombre de réunions sll su e ue

Conseil d'administration ' 2 l p Certification des comptes

Comité d'audit et des risques - 3 - JH, éc s1 — ;:ä _

Comité permanent de “certifiés 2023 tle 50

L>
# 2021 2022 m 2023

Nombre d’affiliés | cA se Nombre de pensionnés ué fl se

2021 2022 2023 2021 2022 2023



Annexe 11 Aza gaall SV JÉS 5 SLs sl 0Y dn J 11 53 és
FICHES SIGNALETIQUES DES PRINCIPAUX EEP

CAISSE NATIONALE DE cribasll ägaisal)
ésspaute

SECURITE SOCIALE ENES cÉ lais Ÿl ELact

sets | CNSs CR

CAPITALSOCIAL | Millions de DH - p> dode el Jl u5

DATE DE Ï

CREATION | 13/12/1959 cd

CLASSIFICATION [ à P Tt A

Tn pique | ETABLISSEMENT PUBLIC PR A Cs
| GESTION DU REGIME DE LA P

ACTIVITE | SECURITE SOCIALE s=
3

CATEGORIE | ORGANISME SOCIAL c

de la CNSS e e En Millions de Dhs # xhs

p méicateurs © 0m Q0 20s J |
Effectif 4793 5192 5070 Cpassi dl e
Charges de personnel 1360 1486 1120 es É AS
Régîme Général (RG) plati

Cotisations et contributions 29295 30725 34879 dasLudll 0NS) 52l

Pensions et prestations 27947 30967 31545 ctasstfy ct |

Solde technique 1348 -242 3335 é

Fonds propres 89734 90679 94 949 A JI5I |

Total actif 96582 97155 102 049 IpAVlE qn |
Assurance Matadie Obligatoire (AMO) vadiqe sl cl

Cotisations et contributions 10485 11971 13551 haaLu) p cS

Pensions et prestations 8596 9487 10756 Btassti p ct |

Solde technique 1889 2484 2795 é

Fonds propres 38788 44209 47661 B5N JIN

Total actif 40887 44539 48337 JpVie pn |
Investissement (paiements) c> 15 118 33 (éhehith c LN

(*)Y compris RG, AMO et Unité

E Gouvernance AolsSl PUF
unl ls Éstadi

Médicale

N éuni “l us
lombre:de réunions E Certification des comptes
Conseil d'administration 2 — JS se
comptes = pTra]
comréouër RE 1 E es rs | 5s — ( S
# 2021 2022 m 2023
Mille unité écas A
su Indicateurs d’activité Ms _— é
(Ol alail SN) age Cyaad) sljal ous GRVN UE GILAYI udl cp stad l sE
Nombre de salariés déclarés (RG En Millions) (Dl BAIl ssds n CH0d)

Population couverte AMO (Assurés et ayants droit en Millions)

2021 2022 2023 2021 2022 2023



Annexe 11 Aza gaall SV JÉS 5 SLs sl 0Y dn J 11 53 és
FICHES SIGNALETIQUES DES PRINCIPAUX EEP

GROUPE AL OMRANE Olyaad) de gane
al os ne

sll Informations Générales Acle Cl glen —
SIGLE { HAO (MAISON MERE) ] rN
CAPITAL SOCIAL 21040 n ï el d 5
DATEDECREATION | 15/12/2004 RRERIEER
CLASSIFICATION 1E E u
Tapete | SOCIETE D'ETAT
ACTIVITE
CATEGORIE

T

PARTICIPATION ; A â

... ( DIRECTE âz gonll Ln Ll
INDIRECTE

Indicateurs économiques et financiers
consolidés roupe AL OMRANE (*)

{*) Consolidés selon la norme marocaine

En Millions de Dhs — p5use

Indicateurs 2021 SN yéise
Effectif (du groupe) 969 946 898 (s ganall) Guass uel se
Charges de personnel 532 548 5s5 Cuess sll CENS
Charges d'exploitation HD 3463 3470 3108 Cuaasdll clusa) qs DIRUl CIS
Chiffre d'Affaires 4104 4355 4266 CDloleall ,
Valeur ajoutée 1092 780 936 An d
Impôt sur les Sociétés 110 158 101 MS SEN S d e
Résultat Net part du groupe 266 224 1170 @.4h e
CAF -157 218 -978 GtN J Al sé
Total actif 63 078 64 706 65 732 Jpal E gane
Fonds propres 5847 5896 4 588 A3 Jigati
Dettes de financement 4 623 4578 5089 Casdil} Gs
Investissement (paiements) 4 386 4846 4548 (Ctetsyt) C Ll
= —
unl ls Éstadi
Nombre deréunione syaèue Certification des comptes
Conseil de surveillance - 1 - 2E ls r = =
Comité d'audit - 3 - RIPN certifiés u .

# 2021 2022 _ 2023

ul Indicateurs d’activité

(Basgdfi) GAUSS] ae (éang côti) LN Chan q Ls Cs
MISES EN CHANTIER EN 1000 UNITES TITRES FONCIERS CREES en 1000 unités

2021 2022 2023 2021 2022 2023



Annexe 11 Aza gaall SV JÉS 5 SLs sl 0Y dn J 11 53 és
FICHES SIGNALETIQUES DES PRINCIPAUX EEP

MOROCCAN AGENCY FOR masen Asä el) AUS 5Ù)
Moroccan Agency - —…
SUSTAINABLE ENERGY (or Soar Énorgy Aat ull SUN

rales

Informations G

SIGLE e
CAPITALSOCIAL 18/03/2010 gelésyl dl 5
DATE DE É
CREATION ce
lerassiricATION - PRODUCTION D'ENERGIE es
CLASSIFICATION dobssk SI z US
Mrpate RENOUVELABLE G
MARCHAND

acisE t v mP=—————— =

TOTALE

( DIRECTE
CATEGORIE INDIRECTE

s et financ

Indicateurs économ
En Millions de Dhs — asdgt

de MASEN
m&.&_
Effecllf Cuesbicuall se
|Charges de personnel 101 99 ns cs UIS
‘Charges d'exploitation HD 1981 1590 2550 Euauasall ciliat cugs JSl CANS
(Chiffre d'Affaires 1403 1048 1608 cauad 5
Valeur ajoutée -477 -429 -840 PPPRER
|Impôt sur les Sociétés 8 Z 43 As e p
Résultat Net -179 -446 -446 A
1 CAF -141 2 757 IN ul 58
iTatal actif 24 184 25 131 22 676 Js Es
Fonds propres 4423 3922 3422 Rs J
Dettes de financement 18219 18790 16 882 dasai us

Gouvernance (Ss

ebluati As ésLadi

Nombre de réunions agalt us A

1 Certification des comptes
Conseil d’Administration 2 E 535l ds 2 E
Comité Stratégie et Investissement 4 0R E » As N . 2022 \_ï ,
Comité d'audit et des risques 3: - ; ME SHl Gést d . Ss
Comité des nominations, de rémunérations 010 RASN, Cs gell, Cn ds 1

2021 æ 2022 #2023

ml Indicateurs d’act

Investissements (paiements en Millions de Dhs) (paljall Gudles ul haÿl) c L

195

2021 2022 2023



Annexe 11 Aza gaall SV JÉS 5 SLs sl 0Y dn J 11 53 és
FICHES SIGNALETIQUES DES PRINCIPAUX EEP

GROUPE OCP Œ ds pôil gaxdl

ocrm Llä p

es Informations Générales âe C1 ——

SIGLE OCP SA (MAISON MERE)
(CAPITALSOCIAL || Millions de DH 8288 PR
DATEDECREATION | 07/08/1920
W
JURIDIQUE

CATEGORIE MARCHAND

TOTALE
PARTICIPATION I ; . ,
PUBLIQUE \ DIRECTE 0000 88% Ara aall An L

INDIRECTE

(*) Consolidés selon IFRS

En Millions de Dhs
Effectif (du groupe} 20 101 20 587 21170 de ,._;.ll) RE TR E
|Charges de personnel 10 550 1615 1518 Osasdiuel CIS
HLUN q SRS CIS
Charges d'exploitation HD 50157 78271 55252 ë =
q P ctacsd
|Chiffre d'Affaires 84 300 114 574 91277 CDdlalsal) É5
Valeur ajoutée 34775 sn 40 863 Al Laill
Impôt sur les Sociétés 4164 6122 2105 ts ât ds du ll
Résultat Net part du groupe 16 326 28185 14 369 obual) Gs
Total actif 181998 226 012 249 937 JyaYl Egane
Fonds propres 86 200 108 052 117 051 É5N JI gaŸl
Dettes de financement (non à è ù à
vs 50 954 59877 61235 (Gtat $) Jasaill cs
Investissement (paiements) 13135 20 050 27 400 JEsls SVl (l LS
Gouvernance (Maison mère) AASAN z
tituali ls désLadi
Nombre de réunions PRRRS

Certification des comptes

Conseil d'administration -- 2 EJN Gs
2 = 2021 FFVR)

… 2022
Comité d'audit et és t certifiés 2073 — ||Lele 6<l
des risques 3 3Hsd,

=2021 =2022 2023

uu INndicateurs d’activité LUEN EJ è se
(cb 1000) ésiau! 31s C jiLe (&b 1000) plä5l Bläuzill Gl iLa
Exportations produits dérivés (1000 T) Exportations phosphate brut (1000 T)

9854

2021 2022 2023 2021 2022 2023



Annexe 11 As gaalf CN Jl y Cs 5all 0Y An GUs 11 53 és
FICHES SIGNALETIQUES DES PRINCIPAUX EEP

es Informations Générales
SIGLE OFPPT | As d 5e)
CAPITAL SOCIAL &s sy ] el JJl p
cDFŒÎTËN | 01/05/1974 d
Êä ETABLISSEMENT PUBLIC 3 pig Cn
|
CATEGORIE NON MARCHAND ‘ se

Al 5

Indicateurs é miques et financiers

de l'OFPPT -
Effectif 75999 8833
Charges de personnel 1912 1970
Charges d'exploitation HD 2182 2928 F 139 Clauaioll cuuss) cygs MRLS Câ
Chiffre d'Affaires 2757 3936 4331 cDdad 5)
Résultats Nets 575 449 671 Aduali us
Valeur Ajoutée 2490 2973 2213 däuznals Al
Investissement (paiements) 930 500 385 («=«t:—Wt) Cs uS
uf Gouvernance As PE
- "
Nombre de réunions upl us pl
Certification des comptes
Conseil d'administration EZ 2 N n E
Comité Stratégie et él 5 dn sl ce 2022 @s
P ec d e corités | 55 [t es
és 4J avecrésente
6

Comité d’audit
# 2021 2022 H2023

u Indicateurs d’acti

(Bang 1000) Cx psiall ue Aules y JUN
CAPACITE EN NOMBRE DE STAGIAIRES (1000 unité)

2021 2022 2023



Annexe 11 Aza gaall SV JÉS 5 SLs sl 0Y dn J 11 53 és
FICHES SIGNALETIQUES DES PRINCIPAUX EEP

GROUPE OFFICE NATIONAL / e crlas!i CSSaNl Àe sans
DES CHEMINS DE FER — Araaatt tSutt
SIGLE ONCF ( MAISON MERE) 0
CAPITAL SOCIAL Millions de DH 37 724,8 gelis Ÿl JU 55
DATE DE [ —
ON | 05/08/1963 | utl 246
CLASSIFICATION n 8 v
és | ETABLISSEMENT PUBLIC H éaogse éuaibe | él Cs
ACTIVITE | TRANSPORT FERROVIAIRE Sl JI EN IBERE
ï
CATEGORIE | MARCHAND —

(*) Consolidés selon IFRS

Indicateurs économiques et fi
olidés du Groupe ONCF (

EnMillions de Dhs — mosgat

Effectif du groupe (**) 8800 8682 8708 dc gandll) GuasS ud as
\Charges de personnel 1255 1310 1364 Ct GS
Charges d'exploitation HD 2972 3191 3 361 cLacaidl qlussl 55 PEIYI CAS
\Chiffre d'Affaires 3964 4 592 4905 <Dlelre) â,
Valeur ajoutée (Acti Ferroviaire) 2124 2738 2936 An d
(Impôt sur les Sociétés 56 64 39 US p S L p
Résultat Net part du groupe -1596 -2543 -1009 él G
\CAF 72 RSEE 1123 SVU J sé
Total actif 75 041 73704 70 207 Jpaÿl E sn
îFonds propres 25 679 23 318 22 712 AGsNau J gaÿi
Dettes de financement 42 141 43 565 42 570 d gaill Gs
\Investissements (paiements) 1609 1196 1133 (Ssghayh) CLSN

(**) :Non compris les effectifs du LPEE et de la SCIF dont la consolidation est faite par mise en équivalence

uf Gouvernance —— SP PR
unl ls Éstadi

Nombre de réunions sll su A
Certification des comptes
Conseil d'administration m=w2- 3 s35 5 x
AFs & = G N
Comité d'auditetet | S r 3; Ls cu 207 -
Risques 5052 2 B5l G6s sl certifiés P Lpule éoLe
Comité stratégie et JSN y dn Vl d 1
investissement e
#æ2021 2022 - 2023
u Indicateurs d’acti
(6sDL) cuâlad às (U cudte) Us Ln ps
Nomiite de vorageurs (Milions devoyageurs) Tonnage marchandise transportée (Millions de Tonnes)

2021 2022 2023 2021 2022



Annexe 11 Aza gaall SV JÉS 5 SLs sl 0Y dn J 11 53 és
FICHES SIGNALETIQUES DES PRINCIPAUX EEP

OFFICE NATIONAL Es nl u_.}g_,.“ ESal

DES AEROPORTS
SIGLE GD
CAPITAL SOCIAL el Jl u5
és es
ACTIVITE cerpaperrs
CATEGORIE | Zcä
M Indicateurs économ
de l'O En Millions de Dhs nl

Indicateurs 2022 2023 N pÂige
Effectif 2466 2593 Gs se
Charges de personnel 853 1012 1151 Cs udl c-l_J\S‘
Charges d'exploitation HD 1779 2072 2294 Claasollcusat qs JNESUŸI CÉNS
Chiffre d'Affaires 2123 3875 4 710 CDldlrdli É
Valeur ajoutée 1346 2965 3717 AäLznals Al
Impôt sur les Sociétés 1 16 12 As 5s ds
Résultat Net -996 323 1066 uel 5
CAF -15 1548 1691 SVN J A sÉ
Total actif 14 880 15 183 15 157 JIl E sn
Fonds propres 3655 3974 5036 É51 J 5
Dettes de financement 7199 7989 7 305 ds 05s
Investissements (paiements) 764 1045 1400 ÿü\;\ﬂ\) —:«Uhäï«—«‘l‘î
= S
Nombre de réunions PS Certification des comptes
conseid'administraion RE 5 É37 e Hh…‘mÎ ==
Comité de Gouvernance t BIZI PRFCEN) e 202 uÏÎ,.1L\
2023 =

Comité d'audit — 4 é

m2021 #2022 2023

u Indicateurs d'acti

(HSN uDte) LSN An

Mouvements Passagers (en millions de passagers)

2021 2022 2023



Annexe 9 Aza gaall SV JÉS 5 SLs sl 0Y dn J 955 d=LI
FICHES SIGNALETIQUES DES PRINCIPAUX EEP

OFFICE NATIONAL DES ON CN ys gyase ll pyiba5ti GSl
HYDROCARBURES ET DES MINES “ “““’—“JW-“>“'“”' Cdlaall 9
» ——
SIGLE f ÏÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿoÿNÿﬁÿYÿMÿ ÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿÿ As zl 305
CAPITALSOCIAL | Millions de DH 1580,36 conviése el J 3
désien | 17/08/2005 | cd
CATEGORIE ‘ COMMERCIAL PPA

EnMillionsde Dhs 250el

Indicateurs

Effectif Greasiuall ds
Charges de personnel Cs AN SS
Charges d'exploitation HD Ds cs
Chiffre d'Affaires CDldadi É3
Valeur ajoutée décze) Al
Impôt sur les Sociétés EN éN S Lu e
è

rSVAUI J pl SÉ

dysi Es

Assan Jl

Gouvernance

Nombre de réunions l ggdi us

ebluati As ésLadi

Certification des comptes

;l d'administrati 536l ds
Conseil d'adinistrtion - 1 - S = e
Comptes S —Il

certifiés lls SL

203
Comité d’audit et 5 2
des risques VHSN GSS A

# 2021 2022 # 2023

u Indicateurs d'acti

Investissements (paiements en Millions de Dhs) (paljall Gudles ul haÿl) c L

ms E N

2021 2022 2023



Annexe 11 Azagaall CY él y Cs gall 2 Ÿ An 5 A 11 53 és
FICHE SIGNALETIQUE DES PRINCIPAUX EEP

DE TRANSPORT AIN == t mt 7
ROYAL AIR MAROC n A
u |Nformations de base Ade ——
SIGLE RAM (MAISON MERE) Al ja)
CAPITAL SOCIAL Millions de DH 5 628,7 es op | TS ]
DATEDECREATION | 18/06/1957 ] 9;3“‘-“‘ És

CLASSIFICATION
Hiapieus | FILIALE PUBLIQUE
ACTIVITE TRANSPORT AERIEN

CATEGORIE MARCHAND

Torace (S
PARTICIPATION T ; ;
PUBLIQUE M DIRECTE ! Aze ganll Ln
INDIRECTE [

{*) Consolidés selon la norme IFRS

En Millions de Dhs muet

Effectif (du groupe) 4 610 3293 3526
Charges de personnel 2220 2 445 2865
Chiffre d'Affaires 6363 12899 19567
Impôt sur les Sociétés 57 86 142 US JËN E Àu p
Résultat Net part du groupe -2 773 -1527 1385 èl GS
Total actif 21969 21 434 23 393 Jpaÿl Egane
Fonds propres 2975 1256 2683 As3 J pl
Dettes de financement 9606 8766 7531 ds O es
Investissements (paiements) 373 373 1110 (estelaÿh) Ss LS
uf Gouvernance (Maison mère) AolsSIl S—U
unl ls Éstadi
Nombre de réunions e Certification des comptes
Conseil d'Administration 4 — Él d
Comité Audit et risques E - D55A), 5 t | | Comptes = <
GALLEE 20ms | e sL
Comité stratégie et investissement 2 E JU, dun 6 l d
Comité Rémunération, Nomination et Gowernance | 3 4 RISN 5 Ch Cl 1
# 2021 2022 # 2023

ul Indicateurs d’activité

Trafic passagers (Millions) (Oste) cy fl

2021 2022 2023



Annexe 11 p e d e E 11 # &sLd
FICHE SIGNALETIQUE DES PRINCIPAUX EEP

GROUPE AGENCE SPECIALE TANGER MED ZE JAN/-dail> Aolsl) AUS 51l Àe gane
TANGER MEDITERRANEE sPEciat AGENCY C177 dus géall el
u |Nformations de base Acle =—
SIGLE TMSA (MAISON MERE) L eS)
CAPITALSOCIAL |" Milfions de DH 37951 ï el d 5
DATEDECREATION | 23/08/2002 Ï[ uf“Ü‘ és
CLASSIFICATION , E
JURIDIQUE | SOCIETE D'ETAT ‘ es
[)) Développement et gestion s——

CATEGORIE MARCHAND
TOTALE

PARTICIPATION
PUBLIQUE [ DIRECTE

E ue goall ds
INDIRECTE [

Indicateurs économiques et financiers
consolidés du Groupe TMSA (*)

{*) Consolidés selon la norme marocaine

En Millions de Dhs ms

Indicateurs

Effectif (du groupe) 2999 2954 3038 As ganall) Gyatäiuell se
Charges de personnel 1002 1031 1096 e GS

c apû LSN G9 JIBLAII CIS
Charges d'exploitation HD 3249 3416 3651 à \
Chiffre d'Affaires 7179 8017 8944 CDldadll ,
Valeur ajoutée 5101 s688 6 414 Al Ll
Impôt sur les Sociétés 347 319 346 As e dl
Résultat Net 1451 1416 2190 eblal) su
CAF 1450 1416 774 NN Ja s0/ 56
Total actif 40 950 41647 42 517 pl E sn
Fonds propres 15 935 16 732 18193 AN J pl
Dettes de financement 14 803 19 687 18 933 daseill G 53
Investissements (paiements) 2246 2943 1493 {cstglah) Cl LSN

(**) Compte consolidé: intégration globale de Marsa Maroc

u Gouvernance (Maison mère) AcISAN ——
unl ls Éstadi

Nombre de réunions PRn ;
ation des comptes
Conseil de surveillance 2021
coniËisterkairer > E d ls 7 ——
S rvesisoent M E PPRREE E cerûfiés e =
Comité d'auditet desrisques MEN 93000 E PRENES
w2021 2022 m2023

El Indicateurs d’activité
e (Bas5) CIUUN spj ds

Nombre de conteneurs (en millions) Trafic camions TIR (unité)

2021 2022 2023 2021 2022 2023



ANNEXE 12
LISTE DES ETABLISSEMENTS ET ENTREPRISES PUBLICS ET AUTRES ORGANISMES SOUMIS
AU CONTROLE FINANCIER DE L'ETAT CLASSES PAR TYPE DE CONTRÔLE (*)
CONTROLE PREALABLE - 198 - (1/3;

1- Etablissements Publics

AGENCE DU BASSIN HYDRAULIQUE

ADA AGENCE POUR LE DEVELOPPEMENT AGRICOLE

AMDL AGENCE MAROCAINE DE DEVELOPPEMENT DE LA LOGISTIQUE

AMEE AGENCE MAROCAINE POUR L'EFFICACITE ENERGETIQUE

AMSSNUR AGENCE MAROCAINE POUR LA SECURITE ET LA SURETE NUCLEAIRES ET RADIOLOGIQUES

ANAM AGENCE NATIONALE DE L'ASSURANCE MALADIE

ANAPEC AGENCE NATIONALE DE PROMOTION DE L'EMPLOI ET DES COMPETENCES

ANEF AGENCE NATIONALE DES EAUX ET FORETS

ANR | AGENCE NATIONALE DES REGISTRES

ANRAC AGENCE NATIONALE DE RÉGLEMENTATION DES ACTIVITÉS RELATIVES AU CANNABIS

ANRUR AGENCE NATIONALE POUR LA RENOVATION URBAINE ET LA REHABILITATION DES BATIMENTS MENAÇANT RUINE

ANDA AGENCE NATIONALE POUR LE DEVELOPPEMENT DE L'AQUACULTURE

ANDZOA | |_AGENCE NATIONALE POUR LE DEVELOPPEMENT DES ZONES OASIENNES ET DE L'ARGANIER

79s AGENCE NATIONALE D'EVALUATION ET D'ASSURANCE QUALITE DE L'ENSEIGNEMENT SUPERIEUR ET DE LA RECHRCHE
SCIENTIFIQUE

ANEP AGENCE NATIONALE DES EQUIPEMENTS PUBLICS

ANLCA AGENCE NATIONALE DE LUTTE CONTRE L'ANALPHABETISME

ANPMA AGENCE NATIONALE DES PLANTES MEDICINALES ET AROMATIQUES

ANSR AGENCE NATIONALE DE LA SECURITE ROUTIERE

APDO AGENCE POUR LA PROMOTION ET LE DEVELOPPEMENT ECONOMIQUE ET SOCIAL DES PROVINCES DE L'ORIENTAL

ARCHIVES ARCHIVES DU MAROC

AREF(12) — | ACADEMIE REGIONALE D'EDUCATION ET DE FORMATION

AU(30) AGENCE URBAINE

BNRM | BIBLIOTHEQUE NATIONALE DU ROYAUME DU MAROC

CADETAF CENTRALE D'ACHAT ET DE DEVELOPPEMENT MINIER DE TAFILALET ET FIGUIG

CAG (12) CHAMBRE D'AGRICULTURE

CAR(12) CHAMBRE D'ARTISANAT

e | CAISSE DE COMPENSATION

Ccis (12) CHAMBRE DE COMMERCE, D'INDUSTRIE ET DE SERVICES

ccM CENTRE CINEMATOGRAPHIQUE MAROCAIN

CFR CAISSE POUR LE FINANCEMENT ROUTIER

(*) Hors EEP en cours de liquidation



RAPPORT SUR LES ETABLISSEMENTS ET ENTREPRISES PUBLICS

ANNEXE 12
LISTE DES ETABLISSEMENTS ET ENTREPRISES PUBLICS ET AUTRES ORGANISMES SOUMIS
AU CONTROLE FINANCIER DE L'ETAT CLASSES PAR TYPE DE CONTRÔLE (*)
CONTROLE PREALABLE - 198 - (2/3)

I- Etablissements Publics (suite)

Sigle Raison sociale
CHU (7) CENTRE HOSPITALIER UNIVERSITAIRE
CNESTEN CENTRE NATIONAL DE L'ENERGIE, DES SCIENCES ET DES TECHNIQUES NUCLEAIRES
| CNRST CENTRE NATIONAL DE LA RECHERCHE SCIENTIFIQUE ET TECHNIQUE
CPM (4) CHAMBRE DES PECHES MARITIME
EACCE ETABLISSEMENT AUTONOME DE CONTROLE ET DE COORDINATION DES EXPORTATIONS
EHTP ECOLE HASSANIA DES TRAVAUX PUBLICS
EN ENTRAIDE NATIONALE
ENAM ECOLE NATIONALE D'AGRICULTURE DE MEKNES
ENSA ECOLE NATIONALE SUPERIEURE DE L'ADMINISTRATION
ENSMR | ECOLE NATIONALE SUPÉRIEURE DES MINES DE RABAT
FFIEM FONDS DE FORMATION PROFESSIONNELLE INTER-ENTREPRISES MINIERES
IAV INSTITUT AGRONOMIQUE ET VETERINAIRE HASSAN II
IMANOR INSTITUT MAROCAIN DE NORMALISATION
INRA | INSTITUT NATIONAL DE LA RECHERCHE AGRONOMIQUE
INRH INSTITUT NATIONAL DE RECHERCHES HALIEUTIQUES
IPM INSTITUT PASTEUR DU MAROC
ISCAE GROUPE INSTITUT SUPERIEUR DE COMMERCE ET D'ADMINISTRATION DES ENTREPRISES
ITPSMGEA INSTITUT PRINCE SIDI MOHAMMED DES TECHNICIENS SPECIALISES EN GESTION ET COMMERCE AGRICOLE
MDA MAISON DE L'ARTISAN
oc OFFICE DES CHANGES
onco OFFICE DE DEVELOPPEMENT DE LA COOPERATION
OFPPT | OFFICE DE LA FORMATION PROFESSIONNELLE ET DE LA PROMOTION DU TRAVAIL

{*) Hors EEP en cours de liquidation



ANNEXE 12
LISTE DES ETABLISSEMENTS ET ENTREPRISES PUBLICS ET AUTRES ORGANISMES SOUMIS
AU CONTROLE FINANCIER DE L'ETAT CLASSES PAR TYPE DE CONTRÔLE (*)

CONTROLE PREALABLE - 198 - (3/3)

I- Etablissements Publics (suite et fin)

Raison sociale

OFFICE NATIONAL DU CONSEIL AGRICOLE

UNIVERSITES (13) UNIVERSITE

Il- Autres Organismes Publics

Raison sociale

AREP (12) AGENCE REGIONALE D'EXECUTION DES PROJETS

FSEC FONDS DE SOLIDARITE CONTRE LES EVENEMENTS CATASTROPHIQUES

(*) Hors EEP en cours de liquidation



RAPPOI UR LES ETABLISSEMENTS ET ENTREPRISES PUBLICS

ANNEXE 12
LISTE DES ETABLISSEMENTS ET ENTREPRISES PUBLICS SOUMIS
AU CONTROLE FINANCIER DE L'ETAT CLASSES PAR TYPE DE CONTRÔLE (*)
CONTROLE D'ACCOMPAGNEMENT - 31 -

|- Etablissements et Entreprises Publics

p e

AASLM AGENCE POUR L'AMENAGEMENT DU SITE DE LA LAGUNE MARCHICA
AAVBR AGENCE POUR L'AMENAGEMENT DE LA VALLEE DU BOU REGREG
ANCFCC AGENCE NATIONALE DE LA CONSERVATION FONCIERE, DU CADASTRE ET DE LA CARTOGRAPHIE
[7 ANP ; AGENCE NATIONALE DES PORTS |
| BAMSA BARID AL MAGHRIB SA
BIOPHARMA [ SOCIETE DE PRODUCTIONS BIOLOGIQUES ET PHARMACEUTIQUES VETERINAIRES
CMR CAISSE MAROCAINE DES RETRAITES
CNss CAISSE NATIONALE DE LA SECURITE SOCIALE
HAO HOLDING AL OMRANE |
ITHMAR ALMAWARID _ ITHMAR AL MAWARID
JZN JARDIN ZOOLOGIQUE NATIONAL SA
LOARC LABORATOIRE OFFICIEL D'ANALYSES ET DE RECHERCHES CHIMIQUES DE CASABLANCA
MAP AGENCE MAGHREB ARABE PRESSE
MASEN MOROCCAN AGENCY FOR SUSTAINABLE ENERGY
MDJs LA MAROCAINE DES JEUX ET DES SPORTS
OMPIC OFFICE MAROCAIN DE LA PROPRIETE INDUSTRIELLE ET COMMERCIALE
ONCF OFFICE NATIONAL DES CHEMINS DE FER
oNDA OFFICE NATIONAL DES AEROPORTS
ONEE OFFICE NATIONAL DE L'ELECTRICITE ET DE L'EAU POTABLE
CONHYM OFFICE NATIONAL DES HYDROCARBURES ET DES MINES
oNP OFFICE NATIONAL DES PECHES |
RADEEMA REGIE AUTONOME DE DISTRIBUTION D'EAU ET D'ELECTRICITE DE MARRAKECH
SsAPT SOCIETE D'AMENAGEMENT POUR LA RECONVERSION DE LA ZONE PORTUAIRE DE TANGER VILLE
ï SIE SOCIETE D'INGENIERIE ENERGETIQUE |
sMiT SOCIETE MAROCAINE D'INGÉNIERIE TOURISTIQUE :
SNRT SOCIETE NATIONALE DE LA RADIODIFFUSSION ET DE TELEVISION
SNTL SOCIETE NATIONALE DES TRANSPORTS ET DE LA LOGISTIQUE
sonacos SOCIETE NATIONALE DE COMMERCIALISATION DE SEMENCES
SONARGES SOCIETE NATIONALE DE REALISATION ET DE GESTION DES EQUIPEMENTS SPORTIFS
SRRA SOCIETE RABAT REGION AMENAGEMENT
TMSA AGENCE SPECIALE TANGER MEDITERRANEE

(*) Hors EEP en cours de liquidation



ANNEXE 12
LISTE DES ETABLISSEMENTS ET ENTREPRISES PUBLICS SOUMIS

AU CONTROLE FINANCIER DE L'ETAT CLASSES PAR TYPE DE CONTRÔLE (*)
CONTROLE CONVENTIONNEL - 29 -

Sigle Raison sociale

i ADER AGENCE POUR LE DEVELOPPEMENT ET LA REHABILITATION DE LA MEDINA DE FES
[ ADM SOCIETE NATIONALE DES AUTOROUTES DU MAROC
CASA AMENAGEMENT CASABLANCA AMENAGEMENT
CASA TRANSPORTS SOCIETE CASABLANCA TRANSPORTS SA
IDMAJ SAKAN CIE CASA ISKANE ET EQUIPEMENT
MARCHICA MED SOCIETE DE DEVELOPPEMENT DE LA LAGUNE DE MARCHICA MED
MASEN CAPITAL MASEN CAPITAL
NWM SOCIETE NADOR WEST MED
OcP OCPsA
PORTNET SOCIETE PORTNET SA
| RAM COMPAGNIE NATIONALE DE TRANSPORT AERIEN ROYAL AIR MAROC
| SAO ALJANOUB SOCIETE AL OMRANE AL JANOUB
i sAO BMK SOCIETE AL OMRANE BENI MELLAL KHENIFRA
[ saocs SOCIETE AL OMRANE CASABLANCA SETTAT
SsAO FM SOCIETE AL OMRANE FES-MEKNES
sAaoMs SOCIETE AL OMRANE MARRAKECH SAFI
saoo SOCIETE AL OMRANE DE LA REGION DE L'ORIENTALE
SAO RSK SOCIETE AL OMRANE RABAT SALE KENITRA
sAO sM SOCIETE AL OMRANE SOUSS MASSA
SAOTTH SOCIETE AL OMRANE TANGER TETOUAN AL HOCEIMA
| sac SOCIETE BOUREGREG CULTURE
sBM SOCIETE BOUREGREG MARINA
sGPTV [ SOCIETE DE GESTION DU PORT DE TANGER VILLE
SOREAD SOCIETE D'ETUDES ET DE REALISATIONS AUDIOVISUELLES "SOREAD" SA
SOREC SOCIETE ROYALE D'ENCOURAGEMENT DU CHEVAL
| sosiPo SOCIETE DES SILOS PORTUAIRES
| STAVOM SOCIETE D'AMENAGEMENT DE LA VALLEE DE OUED MARTIL
| RRM (ex. STRS) [ SOCIETE RABAT REGION MOBILITE
I- Entreprises relevant des colle s territoriales
Sigle Raison sociale
RRE (ex PIAJ) SOCIETE RABAT REGION EMERGENCE SA

(*) Hors EEP en cours de liquidation

A



ANNEXE 12
LISTE DES ETABLISSEMENTS ET ENTREPRISES PUBLICS ET AUTRES ORGANISMES SOUMIS
AU CONTROLE FINANCIER DE L'ETAT CLASSES PAR TYPE DE CONTRÔLE (*)
CONTROLE SPECIFIQUE - 40 -

|- Etablissements et Entreprises Publics

sigle Raison sociale
ADD AGENCE DE DEVELOPPEMENT DU DIGITAL
ADS AGENCE DE DEVELOPPEMENT SOCIAL
ALEM AGENCE DES LOGEMENTS ET D'EQUIPEMENTS MILITAIRES
AMDIE AGENCE MAROCAINE DE DEVELOPPEMENT DES INVESTISSEMENTS ET DES EXPORTATIONS
ANGSPE AGENCE NATIONALE DE GESTION STRATEGIQUE DES PARTICIPATIONS DE L'ETAT
ANPME AGENCE NATIONALE POUR LA PROMOTION DE LA PETITE ET MOYENNE ENTREPRISE
ANRE AUTORITE NATIONALE DE REGULATION DE L'ELECTRICITE
ANRT AGENCE NATIONALE DE REGLEMENTATION DES TELECOMMUNICATIONS
APDN AGENCE POUR LA PROMOTION ET LE DEVELOPPEMENT ECONOMIQUE ET SOCIAL DES PROVINCES DU NORD
APDSs AGENCE POUR LA PROMOTION ET LE DEVELOPPEMENT ECONOMIQUE ET SOCIAL DES PROVINCES DU SUD
CRI(12) CENTRE REGIONAL D'INVESTISSEMENT
FDSHIL FONDS HASSAN II POUR LE DEVELOPPEMENT ECONOMIQUE ET SOCIAL
FEC FONDS D'EQUIPEMENT COMMUNAL
FMVI FONDS MOHAMMED VI POUR L'INVESTISSEMENT

SNGFE (ex CCG) SOCIETE NATIONALE DE GARANTIE ET DE FINANCEMENT DE L'ENTREPRISE

Il- Autres Organismes Publics

sigle Raison sociale

ACAPS AUTORITE DE CONTROLE DES ASSURANCES ET DE LA PREVOYANCE SOCIALE

AMA AGENCE MAROCAINE ANTIDOPAGE

AMMC AUTORITÉ MAROCAINE DU MARCHÉ DES CAPITAUX

AMSUP AGENCE DE MUTUALISATION DES UNIVERSITES MAROCAINES DES ETABLISSEMENTS D'ENSEIGNEMENT SUPERIEUR,
DE RECHERCHE ET DE SUPPORT A L'ENSEIGNEMENT

PDAFOS POLE DIGITAL DE L'AGRICULTURE, DE LA FORET ET OBSERVATOIRE DE LA SECHERESSE

FMHC FONDATION DE LA MOSQUEE HASSAN II A CASABLANCA

FMVIESC FONDATION MOHAMMED VI POUR L'EDITION DU SAINT CORAN

FMVIOSEF FONDATION MOHAMMED VI POUR LA PROMOTION DES OEUVRES SOCIALES DE L'EDUCATION-FORMATION

FMVI PHAI FONDATION MOHAMMED VI DES ŒUVRES SOCIALES DU PERSONNEL DU MINISTERE DES HABOUS ET DES AFFAIRES
ISLAMIQUES

FMVIPR FONDATION MOHAMMED VI DES PREPOSES RELIGIEUX

HAs HAUTE AUTORITE DE SANTE

INCVT INSTITUT NATIONAL DES CONDITIONS DE VIE AU TRAVAIL

ISM INSTITUT SUPERIEUR DE LA MAGISTRATURE

IRCAM INSTITUT ROYAL DE LA CULTURE AMAZIGHE

({*) Hors EEP en cours de liquidation



ANNEXE 12
LISTE DES ENTREPRISES SOUMISES AU CONTROLE CONTRACTUEL - 3 -

Raison sociale

m SOCIETE AMENSOUSS






    


"""
    conversation_history = StreamlitChatMessageHistory()  # Créez l'instance pour l'historique

    st.header("PLF2025: Explorez le rapport sur les établissements et entreprises publics à travers notre chatbot 💬")
    
    # Load the document
    #docx = 'PLF2025-Rapport-FoncierPublic_Fr.docx'
    
    #if docx is not None:
        # Lire le texte du document
        #text = docx2txt.process(docx)
        #with open("so.txt", "w", encoding="utf-8") as fichier:
            #fichier.write(text)

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
        st.session_state.conversation_history.add_user_message(query) 
        if "Donnez-moi un résumé du rapport" in query:
            summary="""Le rapport sur les établissements et entreprises publics (EEP) pour le Projet de Loi de Finances 2025 présente un bilan détaillé des performances financières et opérationnelles des EEP au Maroc. Il couvre des indicateurs clés tels que le chiffre d'affaires, les charges d'exploitation, les investissements, et la dette de financement. Le secteur des EEP est dominé par des secteurs tels que l’énergie, les mines, l’eau et l’environnement, qui représentent une part importante du chiffre d'affaires et des investissements. En 2023, les EEP ont généré un chiffre d'affaires total de 332 milliards de dirhams, et leurs investissements ont augmenté de 6 % par rapport à l'année précédente. Le rapport met également en lumière les défis financiers, notamment des déficits dans certains secteurs et une diminution de la capacité d'autofinancement, nécessitant des transferts et subventions de l'État pour maintenir la viabilité des opérations."""
            st.session_state.conversation_history.add_ai_message(summary) 

        else:
            messages = [
                {
                    "role": "user",
                    "content": (
                        f"{query}. Répondre à la question d'apeés ce texte repondre justement à partir de texte ne donne pas des autre information voila le texte donnee des réponse significatif et bien formé essayer de ne pas dire que information nest pas mentionné dans le texte si tu ne trouve pas essayer de repondre dapres votre connaissance ms focaliser sur ce texte en premier: {text} "
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
           
                # Votre logique pour traiter les réponses
            #conversation_history.add_user_message(query)
            #conversation_history.add_ai_message(response)
            st.session_state.conversation_history.add_ai_message(summary)  # Ajouter à l'historique
            
            # Afficher la question et le résumé de l'assistant
            #conversation_history.add_user_message(query)
            #conversation_history.add_ai_message(summary)

            # Format et afficher les messages comme précédemment
                
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
