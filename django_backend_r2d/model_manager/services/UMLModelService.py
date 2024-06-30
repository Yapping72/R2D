from model_manager.interfaces.BaseModelService import BaseModelService
from model_manager.interfaces.BaseModel import BaseModel
from model_manager.interfaces.BaseAuditor import BaseAuditor  
from model_manager.constants import OpenAIModels
from framework.factories.ModelFactory import ModelFactory
from framework.factories.AuditorFactory import AuditorFactory   

class UMLModelService(BaseModelService):
    """
    Service that instantiates the LangChain compatible models and uses them to generate UML diagrams.
    """
    def __init__(self, model_factory:ModelFactory, auditor_factory:AuditorFactory):
        self.model_factory = ModelFactory()
        #self.auditor_factory = AuditorFactory()

    def _start_generate_and_audit_chain(self, model:BaseModel, auditor:BaseAuditor, prompt:str):
        """
        Start the model chain with the model name and prompt.
        This method will generate the output from the model and then audit the output.
        """
        return model.analyze(prompt)
    
    def generate_user_stories(self,model_name:str, auditor_name:str, job_id:str):
        """
        Generate user stories based on the model name and prompt.
        """
        model = self.model_factory.create_model(model_name)
        #auditor = self.auditor_factory.create_auditor(auditor_name)
        logger.debug(f"Generating user stories for job_id: {job_id}")
        
        return self._start_generate_and_audit_chain(model, None, prompt)