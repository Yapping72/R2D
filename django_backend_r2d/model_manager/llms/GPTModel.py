from langchain_openai import ChatOpenAI
from model_manager.interfaces.BaseModel import BaseModel
from model_manager.constants import OpenAIModels  
from model_manager.interfaces.BasePromptTemplate import BasePromptTemplate
from model_manager.services.ModelExceptions import *

class GPTModel(BaseModel):
    def __init__(self, openai_api_key: str, model_name: OpenAIModels, **kwargs):
        """
        GPTModel that can be used to perform text generation or embeddings.
        The list of supported models are defined in the ModelName enum (constants.py).
        openai_api_key: str
        model_name: OpenAIModels, when initializing the model, the model_name.value will be used to get the model name.
        **kwargs: Additional keyword arguments - temperature, max_tokens, timeout, max_retries.
        """
        if not openai_api_key:
            raise ModelAPIKeyError("OpenAI API key is required.")
        self.llm = ChatOpenAI(openai_api_key=openai_api_key, model_name=model_name.value, **kwargs)

    def analyze(self, prompt:str) -> str:
        pass 
    
