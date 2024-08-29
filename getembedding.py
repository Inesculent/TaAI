#Changed from Bedrock to Ollama cause of some error, will have to figure out later
#from langchain_community.embeddings.ollama import OllamaEmbeddings
from langchain_community.embeddings.bedrock import BedrockEmbeddings
from langchain_openai.embeddings import OpenAIEmbeddings

def get_embedding_function():
    #embeddings = BedrockEmbeddings(client = any, credentials_profile_name="default", region_name="us-east-1")
    #embeddings = OllamaEmbeddings(model="nomic-embed-text")
    embeddings = OpenAIEmbeddings(openai_api_key='sk-3BxHhdzWnm_pT-jC_icP0616Mw7kNFUQQGC4a7PX51T3BlbkFJqQR00moyfRknwUhq1U4Rzcgdio3SZqqd6Cr4eZHzsA')
    return embeddings


