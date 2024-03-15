import json
import os
from azure.storage.blob import BlobServiceClient,BlobSasPermissions,generate_blob_sas
from glob import glob
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

class retrieve_blob:

    def __init__(self,connection_string,container):
        self.connection_string=connection_string
        self.container=container


    def retrieve_file(self,filename=''):
        '''
        The function retrives the files from the given blob container
        Arguments:
        filename: If filename is blank, retrieve all the files in the given container
                  else, retrive the given file from the given container
        '''
    
        try:
            conn_str = self.connection_string
            cont_name = self.container
            
            blob_service = BlobServiceClient.from_connection_string(conn_str)
            container = blob_service.get_container_client(cont_name)
            blobs = container.list_blobs()


            if filename is not None:
                with open(filename, 'wb') as f:
                    data = container.get_blob_client(blob=filename).download_blob()
                    f.write(data.readall())
            else:

                for blob in blobs:
                    print(blob.name)
                    file = blob.name
                    file_path=glob(os.getenv('DataFolder')+file)
                    with open(file_path, 'wb') as f:
                        data = container.get_blob_client(blob.name).download_blob()
                        f.write(data.readall())

            print("files fetched successfully")
            return 1
        except:
            return None

class delete_blob:

    def __init__(self,connection_string,container):
        self.connection_string=connection_string
        self.container=container


    def del_file(self,filename=''):
        '''
        It deletes the given files or all the files
        Arguments:
        filename: If filename is blank, delete all the files in the given container
                  else, delete the given file from the given container
        '''
    
        try:
            conn_str = self.connection_string
            cont_name = self.container
            
            blob_service = BlobServiceClient.from_connection_string(conn_str)
            container = blob_service.get_container_client(cont_name)
            blobs = container.list_blobs()


            if filename:
                with open(filename, 'wb') as f:
                    blob_client = container.get_blob_client(blob=filename)
                    blob_client.delet_blob()
            else:

                for blob in blobs:
                
                    print(blob.name)
                    file_path = blob.name
                    with open(file_path, 'wb') as f:
                        blob_client= container.get_blob_client(blob.name)
                        blob_client.delete_blob()

            print("file deleted successfully")
            return 1
        except:
            return None


class upload_blob:

    def __init__(self,connection_string,container):
        self.connection_string=connection_string
        self.container=container


    def upload_file(self,filename=''):
        '''
        It uploads the given file
        Arguments:
        filename: If filename is blank, delete all the files in the given container
                  else, delete the given file from the given container
        '''
    
        try:
            conn_str = self.connection_string
            cont_name = self.container
            
            blob_service = BlobServiceClient.from_connection_string(conn_str)
            container = blob_service.get_container_client(cont_name)
            

            if filename:
                with open(filename, 'rb') as data:
                    blob_client = container.upload_blob(name=filename,data=data)
            else:

                print("Provide a file to be uploaded")
                return

            print("file uploaded successfully")
            return 1
        except:
            return None

class generate_sas_url():
    def __init__(self,accountName:str,accountKey:str,azureContainer:str):
        self.accountName = accountName
        self.accountKey = accountKey
        self.azureContainer = azureContainer
    
    def generate_sas_token(self,file_name:str)->str:
        account_name=self.accountName
        account_key=self.accountKey
        azure_container=self.azureContainer

        sas = generate_blob_sas(account_name=account_name,
                                account_key=account_key,
                                container_name=azure_container,
                                blob_name=file_name,
                                permission=BlobSasPermissions(read=True),
                                expiry=datetime.utcnow() + timedelta(hours=1))

        
        sas_url ='https://'+account_name+'.blob.core.windows.net/'+azure_container+'/'+file_name+'?'+sas
        return sas_url
