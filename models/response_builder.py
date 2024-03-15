from pydantic import BaseModel, ValidationError
from .prompt_builder import promptcreator
from .program_builder import program
from llm_response.qna import QnA

class responseModel(BaseModel):
    """Data model for the LLM Response"""
    generated_text: str
    reference_text: str
    attributes: dict[str,str]


class response():
   
    def __init__(self,PromptPath:str,
                 MedicalRecord:dict,
                 program:program)-> None:
        
        self.Promptpath=PromptPath
        self.program = program
        self.MedicalRecord=MedicalRecord
    

    
    def generateResponse(self, concepts:dict)->dict:
        response_dict = {}
        
        for conceptid in concepts:
            PromptFile = self.PromptPath+concepts[conceptid]+".txt"
            page_evidence = {}
            for page in self.MedicalRecord:
                prompt_builder=promptcreator(PromptFile,self.MedicalRecord[page])
                prompt = prompt_builder.promptbuilder()
                
                respond = self.program.programrespond(prompt)
                response = respond()
                
                
                
                page_evidence[page] = response
            response_dict[conceptid]=page_evidence
        return response_dict

