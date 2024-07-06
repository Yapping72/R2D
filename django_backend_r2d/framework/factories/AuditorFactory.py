import os
from framework.factories.interfaces.BaseAuditorFactory import BaseAuditorFactory
from model_manager.constants import ModelProvider, OpenAIModels
from model_manager.auditors.GPTAuditor import GPTAuditor
from model_manager.services.ModelExceptions import *
import logging
from enum import Enum

# R2D Logger module
logger = logging.getLogger('application_logging')

class AuditorFactory(BaseAuditorFactory):
    @staticmethod
    def get_auditor(provider: ModelProvider, model_name: Enum):
        """
        Returns a model instance based on the provider and model name.
        @params: provider: ModelProvider
        @params: model_name: OpenAIModels
        Raises AuditorInitializationError if the model cannot be initialized.
        """
        try:
            # Check if the model provider is OpenAI and the model name is valid (part of OpenAIModels enum)
            if provider == ModelProvider.OPEN_AI and model_name in [model for model in OpenAIModels]:
                logger.debug(f"Initializing auditor {model_name} from OpenAI.")    
                model_api_key = AuditorFactory._get_api_key("R2D_OPENAI_API_TOKEN")
                # Create the gpt model using the OpenAI API key and the model name
                max_tokens = 4096 # Default max tokens
                return GPTAuditor(openai_api_key=model_api_key, model_name=model_name, temperature=0.5, max_tokens=max_tokens, timeout=30, max_retries=3)
            else:
                raise ModelNotFoundException(f"No valid model found for {model_name}.")
        except (ModelAPIKeyError, ModelNotFoundException, ModelProviderNotFoundException) as e:
            raise AuditorInitializationError(f"Model cannot be initialized to audit results: {e}")
        
    @staticmethod
    def _get_api_key(api_key_id:str):
        """Retrieve the API key from the environment variables."""
        api_key = os.getenv(api_key_id)
        if api_key is None:
            raise ModelAPIKeyError(f"API key {api_key_id} not found.")
        return api_key