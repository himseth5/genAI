import requests
from llama_index.core.callbacks import CallbackManager
from llama_index.core.llms import (
    CustomLLM,
    CompletionResponse,
    CompletionResponseGen,
    LLMMetadata,
)
from dotenv import load_dotenv
import os

load_dotenv()

class QnA():
    def __init__(self)->None:
        self.url=os.environ["LLMEndPoint"] 
    
    def responseFromLLM(self, prompt)->str:
        # url = ''
        data = {'prompt':prompt}
        response = requests.post(self.url,json = data)
        return response.json()['response']
    
    # def seturl(self,url3):
    #     self.url = url3


class ExlAI(CustomLLM, QnA):
    context_window: int = 3900
    num_output: int = 256
    model_name: str = "custom"
    
    def __init__(self)->None:
         super().__init__()
                
    @property
    def metadata(self) -> LLMMetadata:
        """Get LLM Metadata"""
        return LLMMetadata(
            context_window = self.context_window,
            num_output = self.num_output,
            model_name = self.model_name,
        )
    
    # @llm_completion_callback()
    def complete(self, prompt:str,**kwargs: any)->CompletionResponse:
        return CompletionResponse(text=self.responseFromLLM(prompt))

        
    # @llm_completion_callback()
    def stream_complete(self, prompt:str,**kwargs: any) -> CompletionResponseGen:
        response = ""
        for token in self.responseFromLLM(prompt):
            response += token
            yield CompletionResponse(text = response,delta=token)
            
