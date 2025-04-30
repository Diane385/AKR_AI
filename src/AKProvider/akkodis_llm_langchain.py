import requests
from langchain.llms import BaseLLM
from langchain.schema import LLMResult
from langchain_core.outputs import GenerationChunk
from pydantic import BaseModel, Field
import os
import yaml

# TODO : create try except request error

class AkkodisAPIProvider(BaseLLM, BaseModel):
    deployment_id: str = Field(..., description="ID du déploiement OpenAI")
    api_version: str = Field(..., description="Version de l'API Akkodis")

    def _generate(self, prompts, **kwargs) -> LLMResult:
        """Effectue un appel à l'API Akkodis pour générer du texte."""
        url = f"https://cld.akkodis.com/api/openai/deployments/{self.deployment_id}/chat/completions?api-version={self.api_version}"
        Dirname = os.path.dirname(__file__) # current directory
        Filename = os.path.join(Dirname, '../config/config.yml') # relative path to config file
        with open(Filename, 'r') as file:
            config = yaml.safe_load(file)

        api_key = config['api']['key']
        headers = {
            "Content-Type": "application/json",
            "Cache-Control": "no-cache",
            "api-key": "{}".format(api_key, api_key),

        }

        # Préparer les messages pour l'API
        messages = [{"role": "user", "content": prompt} for prompt in prompts]
        data = {
            "messages": messages
        }

        try:
            response = requests.post(url, json=data, headers=headers)
            # response.raise_for_status()  # Raises an HTTPError for bad responses
            result = response.json()      # Parse the JSON response
        
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")  # Handle HTTP errors
        except requests.exceptions.ConnectionError as conn_err:
            print(f"Connection error occurred: {conn_err}")  # Handle connection errors
        except requests.exceptions.Timeout as timeout_err:
            print(f"Timeout error occurred: {timeout_err}")  # Handle timeout errors
        except requests.exceptions.RequestException as req_err:
            print(f"An error occurred: {req_err}")  # Handle any other request-related errors
        except ValueError as json_err:
            print(f"JSON decode error: {json_err}")  # Handle JSON decoding errors
        
        try:
            generations = [
            [GenerationChunk(text=choice['message']['content']) for choice in result['choices']]
        ]
            # print(result['choices'][0]['message']['content'])
        except:
            generations = [
            [GenerationChunk(text=error[0]) for error in result['error']]
        ]
            print(result['error'])
        # Créer une instance de LLMResult avec le texte généré
        return LLMResult(generations=generations)

    @property
    def _llm_type(self):
        """Retourne le type de modèle de langage."""
        return "akkodis"
