from AKProvider.helper import HttpRequest, Endpoint
from AKProvider.requests_config import request_config

request_config = request_config("models-gpt-4o-mini", "2024-08-01-preview")

url = "https://cld.akkodis.com/api/openai/deployments/{deployment-id}/chat/completions?api-version={api-version}"
param = {
        "deployment-id": "models-gpt-4o-mini",
        "api-version": "2024-08-01-preview",
    }

class_A = Endpoint(url, **param)
Endpoint_instance = HttpRequest(url, **param)

class_A.show()

user_prompt = "introduction to langchain" 

messages = [
    {"role": "system", "content": user_prompt},
    {"role": "user", "content": user_prompt},
]

response = request_config.send_message(messages)
print("AI Response:", response)