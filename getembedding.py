#Changed from Bedrock to Ollama cause of some error, will have to figure out later
#from langchain_community.embeddings.ollama import OllamaEmbeddings
from langchain_community.embeddings.bedrock import BedrockEmbeddings
from langchain_openai.embeddings import OpenAIEmbeddings

def get_embedding_function():
    #embeddings = BedrockEmbeddings(client = any, credentials_profile_name="default", region_name="us-east-1")
    #embeddings = OllamaEmbeddings(model="nomic-embed-text")
    embeddings = OpenAIEmbeddings(openai_api_key='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')
    return embeddings


