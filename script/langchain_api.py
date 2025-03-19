import requests
from langchain.llms import BaseLLM
from langchain.schema import LLMResult
from langchain_core.outputs import Generation
from pydantic import BaseModel, Field
import os
from langchain_core.prompts import ChatPromptTemplate


class AkkodisAPIProvider(BaseLLM, BaseModel):
    api_key: str = Field(..., description="Clé API pour l'authentification")
    deployment_id: str = Field(..., description="ID du déploiement OpenAI")
    api_version: str = Field(..., description="Version de l'API Akkodis")
    
    def _generate(self, prompts, **kwargs) -> LLMResult:
        """Effectue un appel à l'API Akkodis pour générer du texte."""
        url = f"https://cld.akkodis.com/api/openai/deployments/{self.deployment_id}/chat/completions?api-version={self.api_version}"
        headers = {
            "Content-Type": "application/json",
            "Cache-Control": "no-cache",
            "api-key": open(os.path.join(os.path.expanduser('.'), ".akr_key.txt"), 'r').read().strip()
        }
        
        # Préparer les messages pour l'API
        messages = [{"role": "user", "content": prompt} for prompt in prompts]
        data = {
            "messages": messages
        }
        
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()  # Lève une exception pour les codes d'erreur HTTP
        
        result = response.json()
        # Créer une instance de LLMResult avec le texte généré
        generations = [
            [Generation(text=choice['message']['content']) for choice in result['choices']]
        ]
        return LLMResult(generations=generations)

    @property
    def _llm_type(self):
        """Retourne le type de modèle de langage."""
        return "akkodis"

# Exemple d'utilisation
if __name__ == "__main__":
    # Remplacez par vos informations
    api_key = open(os.path.join(os.path.expanduser('.'), ".akr_key.txt"), 'r').read().strip()
    deployment_id = "models-gpt-4o-mini"
    api_version = "2024-08-01-preview"

    akkodis_provider = AkkodisAPIProvider(api_key=api_key, deployment_id=deployment_id, api_version=api_version)
    
    prompts = ["c'est quoi python", "introduction biomimitesme"]
    #result = akkodis_provider._generate(prompts)  # Utiliser invoke pour plusieurs prompts
    #print(result, type(result))

    prompt_template = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant"),
    ("user", "Tell me a joke about {topic}")
    ])

    print(prompt_template.invoke({"topic": "cats"}))
    #result = akkodis_provider._generate(prompt_template.invoke({"topic": "cats"}))
    #print(result)

    invoke_result = akkodis_provider.invoke(prompts) # Utiliser invoke pour plusieurs prompts
    print(invoke_result)
    
    #for i, generation in enumerate(result.generations):
    #    print(f"Réponse {i + 1} : {generation[0].text}")