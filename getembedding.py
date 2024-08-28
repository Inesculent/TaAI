#Changed from Bedrock to Ollama cause of some error, will have to figure out later
#from langchain_community.embeddings.ollama import OllamaEmbeddings
from langchain_community.embeddings.bedrock import BedrockEmbeddings
from langchain_openai.embeddings import OpenAIEmbeddings

def get_embedding_function():
    #embeddings = BedrockEmbeddings(client = any, credentials_profile_name="default", region_name="us-east-1")
    #embeddings = OllamaEmbeddings(model="nomic-embed-text")
    embeddings = OpenAIEmbeddings(openai_api_key='sk-hAsV9Zqp7EQVY3KW-hb0ll6KGypZxouf4x08qTaIr4T3BlbkFJgOulnwUGR6wQDM3n_hVp1NrmuN04GLtIvfkEtVeesA')
    return embeddings


