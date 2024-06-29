from framework.auditors.BaseAuditorFactory import BaseAuditorFactory

class AuditorFactory(BaseAuditorFactory):
    @staticmethod
    def get_auditor(auditor_name:str):
        if auditor_name == 'gpt_class_diagram_auditor':
            return "gpt Class Diagram auditor"
        else:
            raise ValueError(f"No valid audtior found for {auditor_name}")