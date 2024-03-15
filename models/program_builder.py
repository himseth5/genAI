from llama_index.core.program import LLMTextCompletionProgram

class program:
    def __init__(self,outputclass,llm)->None:
        self.outputclass = outputclass
        self.llm = llm
    
    def programrespond(self,prompt)->LLMTextCompletionProgram:
        program = LLMTextCompletionProgram.from_defaults(
            output_cls = self.outputclass,
            llm = self.llm,
            prompt_template_str = prompt,
            verbose = True
            )
        return program
