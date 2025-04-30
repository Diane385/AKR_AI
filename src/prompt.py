from AKProvider.akkodis_llm_langchain import AkkodisAPIProvider
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import ChatPromptTemplate
from utils.files import append_file
import sys
import os


# Initialisation de la mémoire
memory = ConversationBufferMemory()

# Création d'un modèle de langage
deployment_id = "models-gpt-4o-mini"
api_version = "2024-08-01-preview"
akkodis_provider = AkkodisAPIProvider(deployment_id=deployment_id, api_version=api_version)

prompt_template = ChatPromptTemplate([
    ("system", "{conversation_history}"),
    ("user", "{user_message}")
])

# Fonction pour exécuter la chaîne
def generer_reponse(conversation_history, user_message):
    prompt = prompt_template.invoke({"conversation_history":conversation_history, "user_message":user_message})
    response = akkodis_provider.invoke(prompt)
    return response

# Fonction pour interagir avec l'utilisateur
def interagir_avec_utilisateur():
    conversation_history = ""
    while True:
        user_input = input("Vous : ")
        if user_input.lower() in ["exit", "quitter"]:
            print("Fin de la conversation.")
            break
        
        # Générer la réponse
        response = generer_reponse(conversation_history, user_input)
        print(f"Bot : {response}")

        # Mettre à jour l'historique de la conversation
        conversation_history += f"Utilisateur : {user_input}\n\nBot : {response}\n"
        raw_path = sys.argv[1]
        normalized_path = os.path.normpath(raw_path)
        append_file(normalized_path, f"{response}\n")

# Lancer l'interaction
interagir_avec_utilisateur()