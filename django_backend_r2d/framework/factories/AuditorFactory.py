from framework.factories.interfaces.BaseAuditorFactory import BaseAuditorFactory

class AuditorFactory(BaseAuditorFactory):
    @staticmethod
    def get_auditor(auditor_name:str):
        return True