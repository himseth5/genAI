import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()

class DB:

    def __init__(self)->None:
        cds_endpoint=os.getenv('PostToCDSEndPoint')
        ces_endpoint=os.getenv('PostToCESEndPoint')
        cd_endpoint=os.getenv('PostToCDEndpoint')
        pat_endpoint=os.getenv('PostToPatientEndpoint')
        provider_endpoint=os.getenv('PostToProviderEndPoint')
    
    def posttocds(self,cdsdict:dict)->None:
        url=self.cds_endpoint
        headers = {'Accept-Charset': 'utf-8','Accept':'application/json','accept-encoding' : 'gzip','Content-Type':'application/json'}
        put_cl_data =json.dumps(cdsdict)

        response = requests.post(url, data=put_cl_data, headers=headers)
        print(response.text)

    def posttoces(self,cesdict:dict)->None:
        url = self.ces_endpoint
        headers = {'Accept-Charset': 'utf-8','Accept':'application/json','accept-encoding' : 'gzip','Content-Type':'application/json'}
        put_cl_data =json.dumps(cesdict)

        response = requests.post(url, data=put_cl_data, headers=headers)
        print(response.text)
    
    def posttocd(self,cdDic:dict):
        url = self.cd_endpoint
        headers = {'Accept-Charset': 'utf-8','Accept':'application/json','accept-encoding' : 'gzip','Content-Type':'application/json'}
        data1 =json.dumps(cdDic)
        response = requests.post(url, data=data1, headers=headers)
        print(response.text)

    def postToPatientdb(self,patDict:dict):
        url = self.pat_endpoint
        headers = {'Accept-Charset': 'utf-8','Accept':'application/json','accept-encoding' : 'gzip','Content-Type':'application/json'}
        data1 =json.dumps(patDict)
        response = requests.post(url, data=data1, headers=headers)
        print(response.text)

    def postToProviderdb(self,proDict:dict):
        url = self.provider_endpoint
        headers = {'Accept-Charset': 'utf-8','Accept':'application/json','accept-encoding' : 'gzip','Content-Type':'application/json'}
        data1 =json.dumps(proDict)
        response = requests.post(url, data=data1, headers=headers)
        print(response.text)