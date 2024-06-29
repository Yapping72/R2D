from django.db import models
from framework.factories.BaseModelFactory import BaseModelFactory

class ModelFactory(BaseModelFactory):
    @staticmethod
    def get_model(model_name:str):
        if model_name == 'gpt_class_diagram':
            return "Class Diagram Model"
        elif model_name == 'gpt_sequence_diagram':
            return "Sequence Diagram Model"
        else:
            raise ValueError(f"No valid model found for {model_name}")