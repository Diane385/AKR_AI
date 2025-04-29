from AKProvider.akkodis_llm_langchain import AkkodisAPIProvider

def test_llmchain():
    deployment_id = "models-gpt-4o-mini"
    api_version = "2024-08-01-preview"
    akkodis_provider = AkkodisAPIProvider(deployment_id=deployment_id, api_version=api_version)

    prompts = ["c'est quoi le biomimétisme avec le maximum des détails"]

    result = akkodis_provider.invoke(prompts)  # Utiliser invoke pour plusieurs prompts
    #result_generate = akkodis_provider._generate(prompts)
    print(result)
    #for i, generation in enumerate(result_generate.generations):
    #    print(f"Réponse {i + 1} : {generation[i].text}")

