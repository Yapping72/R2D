from typing import Optional, Union, Type
from pydantic import BaseModel as PydanticModel
from langchain.output_parsers import PydanticOutputParser

from langchain_openai import ChatOpenAI
from model_manager.interfaces.BaseModel import BaseModel
from model_manager.constants import OpenAIModels  
from model_manager.interfaces.BasePromptTemplate import BasePromptTemplate
from model_manager.services.ModelExceptions import *

import logging 
# Initialize the logger
logger = logging.getLogger('application_logging')

class GPTModel(BaseModel):
    def __init__(self, openai_api_key: str, model_name: OpenAIModels, **kwargs):
        """
        GPTModel that can be used to perform text generation or embeddings.
        The list of supported models are defined in constants.py
        args:
            openai_api_key: str
            model_name: OpenAIModels (Enum), when initializing the model, the model_name.value will be used to get the model name.
            **kwargs: Additional keyword arguments - temperature, max_tokens, timeout, max_retries.
        Raises:
            ModelAPIKeyError if no valid api key is provided
            InvalidModelType if the model_name is not an instance of OpenAIModels enum
        """
        if not openai_api_key:
            raise ModelAPIKeyError("OpenAI API key is required.")
        if not isinstance(model_name, OpenAIModels):
            raise InvalidModelType("model_name should be an instance of OpenAIModels enum")
        
        super().__init__(model_name=model_name.value)
        self.llm = ChatOpenAI(openai_api_key=openai_api_key, model_name=model_name.value, **kwargs)
        
    def analyze(self, prompt: str, response_schema:(Optional[Union[Type[PydanticModel], dict]]) = None) -> str:
        """
        Performs LLM analysis on the given prompt.
        Args:
            prompt (str): The prompt to be used for the analysis, retrieved from concrete BasePromptTemplate classes.
            response_schema (Optional[Type[PydanticModel], dict]): Optional schema for structured response, either a valid Pydantic model or None.
            The response_schema will be used to parse the output of the LLM.
        Returns:
            str: The response from the LLM, potentially parsed by a Pydantic model.
        Raises:
            ModelAnalysisError: If there is an error in analyzing the prompt.
        """
        try:
            if response_schema and isinstance(response_schema, PydanticModel):
                logger.debug(f"Using Pydantic model for structured response")
                # If a Pydantic model is defined, use it to parse the output
                parser = PydanticOutputParser(pydantic_object=response_schema)
                response = self.llm.invoke({"role": "user", "content": prompt}, output_parser=parser)
            elif response_schema:
                logger.debug(f"Using JSON schema for structured response")
                # If a JSON schema is defined, use it to parse the output
                structured_llm = self.llm.with_structured_output(response_schema)
                response = structured_llm.invoke([{"role": "user", "content": prompt}])
            else:
                logger.debug("No default schema provided, returning the entire response.")
                response = self.llm.invoke([{"role": "user", "content": prompt}])
        except Exception as e:
            raise ModelAnalysisError(f"Error analyzing the prompt: {str(e)}")
        
        return response  # Return the entire response