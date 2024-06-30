import os
from django.db import models
from framework.factories.interfaces.BaseModelFactory import BaseModelFactory
from model_manager.constants import ModelProvider, OpenAIModels
from model_manager.llms.GPTModel import GPTModel
from model_manager.services.ModelExceptions import *
import logging

# R2D Logger module
logger = logging.getLogger('application_logging')

class ModelFactory(BaseModelFactory):
    @staticmethod
    def get_model(provider: ModelProvider, model_name: OpenAIModels):
        """
        Returns a model instance based on the provider and model name.
        @params: provider: ModelProvider
        @params: model_name: OpenAIModels
        Raises ModelInitializiationError if the model cannot be initialized.
        """
        try:
            # Check if the model provider is OpenAI and the model name is valid (part of OpenAIModels enum)
            if provider == ModelProvider.OPEN_AI and model_name in [model for model in OpenAIModels]:
                logger.debug(f"Initializing model {model_name} from OpenAI.")    
                model_api_key = ModelFactory._get_api_key("R2D_OPENAI_API_TOKEN")
                # Create the gpt model using the OpenAI API key and the model name
                return GPTModel(openai_api_key=model_api_key, model_name=model_name, temperature=0.5, max_tokens=4096, timeout=30, max_retries=3)
            else:
                raise ModelNotFoundException(f"No valid model found for {model_name}.")
        except (ModelAPIKeyError, ModelNotFoundException, ModelProviderNotFoundException) as e:
            raise ModelInitializationError(f"Model could not be initialized. {e}")
        
    @staticmethod
    def _get_api_key(api_key_id:str):
        """Retrieve the API key from the environment variables."""
        api_key = os.getenv(api_key_id)
        if api_key is None:
            raise ModelAPIKeyError(f"API key {api_key_id} not found.")
        return api_key