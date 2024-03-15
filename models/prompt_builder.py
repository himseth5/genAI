

class promptcreator():

    def __init__(self,PromptFile:str,medicalrecord:str)->None:
        self.PromptFile=PromptFile
        self.medicalrecord=medicalrecord
    
    def promptbuilder(self)->str:
        pretext = "\nMedical Record: \n"
        with open(self.PromptFile,'r') as f:
            MedicalContext=f.read()
        
        promptWithoutMR = MedicalContext
        promptWithMR = promptWithoutMR+pretext+self.medicalrecord
        return promptWithMR