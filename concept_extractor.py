import json
from models.program_builder import program 
from models.prompt_builder import promptcreator
from models.response_builder import responseModel,response
from models.pat_pro_model import PatientModel,ProviderModel
from models.concept_summary_model import ConceptSummaryModel
from utilities.azure import retrieve_blob,generate_sas_url
from llm_response.qna import ExlAI, QnA
from dotenv import load_dotenv
import os
import uuid
from datetime import datetime
import getpass as gt
from dboperations.db_utility import DB
from utilities.datetime_utilities import file_creation_date

load_dotenv()

username = gt.getuser()

def retreive_auth_requests(filename:str=None):
    '''Retreives the prior authorization requests from the designated azure blob'''
    
    connection_string=os.getenv('AzureConnectionString')
    container=os.getenv('container_name')
    retrieve_file=retrieve_blob(connection_string=connection_string,
                            container=container
                            )

    retrieve_file.retrieve_file(filename=filename)

retreive_auth_requests()

with open('concepts.json','r') as concept_file:
    concepts:dict=json.loads(concept_file.read())

PromptPath=os.getenv('PromptPath')
prior_auth_locations=os.getenv('DataFolder')


PatientPromptPath:str = os.getenv('PatientPromptPath')
ProviderPromptPath:str = os.getenv('ProviderPromptPath')
conceptSummarizePromptPath:str = os.getenv('conceptSummaryPromptPath')


#Initiate the generate_sas_url object
PdfContainerAccountName:str = os.getenv('PdfArchiveAccountName')
PdfContainerAccountKey:str = os.getenv('PdfArchiveAccountKey')
PdfContainer:str = os.getenv('PdfArchiveAccountContainer')
generateSasUrlObj:generate_sas_url = generate_sas_url(PdfContainerAccountName,PdfContainerAccountKey,PdfContainer)

db_object=DB()

for filename in os.listdir(prior_auth_locations):
   document_id = str(uuid.uuid4())
   Doc_sas_path:str =  generateSasUrlObj.generate_sas_token(filename)
   creation_datetime =file_creation_date(os.path.join(prior_auth_locations, filename))
   cd_data = {
            'Identifier':document_id,
            'Document_Name': filename,
            'Document_Path':Doc_sas_path,
            'Document_Review_Status':"Not Started",
            'Prior_Auth_Description':'',
            'Patient_Document_id':document_id,
            'Provider_Document_id':document_id,
            'Document_Receive_dts': creation_datetime,
            'Document_Evaluation_dts': creation_datetime,
            'Last_Updated_dts': creation_datetime,
            'User_Name':username
            }
   cds_data= {
    'All_Evidence_Feedback':'',
    'All_Evidence_Summary':'',
    'CDS_Identifier':'',
    'Identifier':document_id,
    'Concept_Name': '',
    'User_Notes':'',
    'Concept_Review_Status': 'Not-Started',
    'Creation_Date': '2024-02-20',
    'Last_Updated_Dts': '2024-02-20',
    'User_Name':username
            }
   
   ces_data= {
    'CES_Identifier':'',
    'CDS_Identifier':'',
    'Concept_LLM_Summary':'Concept_Summary',
    'Reference_Text':'disease_reference',
    'Response_Attribute':'response_text',
    'User_Feedback':'7',
    'Document_Page_Number': '21',
    'Creation_Date': '2024-02-27',
    'Last_Updated_Dts': '2024-02-27',
    'User_Name': username
            }
   
   db_object.posttocd(cd_data)

   #Patient and Provider details are still to be fetched from their DB
   #These details later need to be updated to the patient and provider databases

   
   with open(os.path.join(prior_auth_locations, filename), 'r') as f: # open in readonly mode
        medical_record:dict=json.loads(f.read())
    
    # Get the prompts for the patient and provider details
    FirstPageOfMedicalRecord:str = medical_record['1']
    Patient_Promp_Creator_Obj = promptcreator(PatientPromptPath,FirstPageOfMedicalRecord)
    Provider_Promp_Creator_Obj = promptcreator(ProviderPromptPath,FirstPageOfMedicalRecord)
    Patient_Prompt = Patient_Promp_Creator_Obj.promptbuilder()
    Provider_Prompt = Patient_Promp_Creator_Obj.promptbuilder()
    
    

   customllm=ExlAI()
   qna=QnA()
   program_object:program = program(responseModel,customllm)
   
   # Patient program to get the patient Details
   patientProgram:program = program(PatientModel,customllm)
   patientDetailsRespond = patientProgram.programrespond(Patient_Prompt)
   patientDetails:PatientModel = patientDetailsRespond()

   # Provider program to get the provider details
   providerProgram:program = program(ProviderModel,customllm)
   providerDetailsRespond = providerProgram.programrespond(Provider_Prompt)
   providerDetails:ProviderModel = providerDetailsRespond()

   #Patient and Provider Details
   patientDetailsDict:dict = {
    "Document_Identifier": document_id,
    "Patient_Id":document_id,
    "Patient_Name": patientDetails.Patient_Name,
    "Patient_Gender": patientDetails.Patient_Gender,
    "Patient_DoB": str(patientDetails.Patient_DoB),
    "Patient_Address_line":patientDetails.Patient_Address_line,
    "Patient_State": patientDetails.Patient_State,
    "Patient_Contact": patientDetails.Patient_Contact
    }

    providerDetailsDict:dict = {
    "Document_Identifier": document_id,
    "Provider_Id": document_id,
    "Provider_Name": providerDetails.Provider_Name,
    "Provider_Address_line": providerDetails.Provider_Address_line,
    "Provider_State":providerDetails.Provider_State,
    "Provider_Contact":providerDetails.Provider_Contact
    }

    # Update the database with the patient and provider details
    postToPatientdb(patientDetailsDict)
    postToProviderdb(providerDetailsDict)

    response_object:response= response(PromptPath, program_object,medical_record)
    concept_evidence:dict[str,dict] = response_object.generateResponse(concepts)

    for conceptid in concept_evidence:
        cds_id = str(uuid.uuid4())
        conceptevidences:str = ""
        cds_data['CDS_Identifier'] = cds_id
        ces_data['CDS_Identifier'] = cds_id
        
        cds_data['Concept_Name'] = concepts[conceptid]

        now = datetime.now()
        formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
        cds_data['Creation_Date'] = formatted_date
        cds_data['Last_Updated_Dts'] = formatted_date


        for page in concept_evidence[conceptid]:
            now = datetime.now()
            formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
            
            ces_data['Creation_Date'] = formatted_date
            ces_data['Last_Updated_Dts'] = formatted_date
            ces_data['CES_Identifier'] = str(uuid.uuid4())
            ces_data['Reference_Text'] = concept_evidence[conceptid][page].reference_text
            ces_data['Concept_LLM_Summary'] = concept_evidence[conceptid][page].generated_text
            attributes = concept_evidence[conceptid][page].attributes
            ces_data['Response_Attribute'] = str(attributes)
            
            cds_data['Document_Page_Number'] = str(page)
            DB.posttoces(ces_data)

            conceptevidences += "Evidence Text from LLM: "+(concept_evidence[conceptid][page].generated_text)
            conceptevidences += " Reference Text from Medical Record: " + (concept_evidence[conceptid][page].reference_text)
            conceptevidences += " Page Number of Medical Record: " + (page)
            conceptevidences += "\n"
        Summarize_Concept_PromptCreator_Obj = promptcreator(conceptSummarizePromptPath,conceptevidences)
        Summarize_Concept_Prompt:str = Summarize_Concept_PromptCreator_Obj.promptbuilder()
        SummarizeConceptProgram:program = program(ConceptSummaryModel,customllm)
        SummarizeConceptRespond = SummarizeConceptProgram.programrespond(Summarize_Concept_Prompt)
        ConceptSummary:ConceptSummaryModel = SummarizeConceptRespond()
        
        cds_data['All_Evidence_Feedback'] = ConceptSummary.AllEvidenceFeedback
        cds_data['All_Evidence_Summary'] = ConceptSummary.AllEvidenceSummary
        DB.posttocds(cds_data)
            
        
    



    

    


    

    













