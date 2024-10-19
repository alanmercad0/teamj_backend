import os
from dotenv import load_dotenv
from musicai_sdk import MusicAiClient
import json

from tools import download_youtube_video_as_mp3,json_response

from moviepy.editor import AudioFileClip

load_dotenv()

MUSICAI_API_KEY = os.getenv('MUSICAI_API_KEY')
WORKFLOW_ID = os.getenv('WORKFLOW_ID')



class MusicAIClass:
    def __init__(self) -> None:
        self.api_key = MUSICAI_API_KEY
        self.workflow_id = WORKFLOW_ID
        self.client = MusicAiClient(api_key=MUSICAI_API_KEY)
    def get_job(self,job_id):
        job_info = self.client.get_job(job_id=job_id)
        return job_info
    def get_all_jobs(self):
        jobs = self.client.get_jobs()
        return jobs
    async def create_job(self,job_name,mp3):
        file_url = self.client.upload_file(file_path=mp3)
        workflow_params = {
            'inputUrl': file_url
        }
        print(f"workflow_id",self.workflow_id)
        try:
            print("Trying")
            create_job_info = self.client.create_job(job_name=job_name,workflow_id=self.workflow_id,params=workflow_params)
            job_id = create_job_info['id']
            # Wait for job to complete
            job_info = self.client.wait_for_job_completion(job_id)
            print('Job Status:', job_info['status'])
            print('Job Result:', type(job_info['result']))
            if job_info['status'] == 'FAILED':
                raise Exception('Something went wrong!')        
        except:
            return json_response(500,'internal error: failed to create job')
        
        print(job_info['result'].keys())
        return json_response(200,f'success: job created... job id={job_id}'), job_info['result']
    
    def delete_job(self,job_id):
        try:
            self.client.delete_job(job_id=job_id)
        except:
            return json_response(500,'internal error: failed to delete job')
        return json_response(200,'success: job deleted')
    


        
