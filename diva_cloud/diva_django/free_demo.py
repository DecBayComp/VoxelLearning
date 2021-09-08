from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from diva_cloud import settings
from jobapp.models import JobType
from jobapp.models import Job
from fileapp.serializers import Serialize_a_File
import json

class Free_demo(TestCase):

    c = Client()
    def setUp(self):
        # [Prepare] Create a user and login
        self.user = User.objects.create_user(
            username='demouser', password='12345')
        login = self.c.login(username='demouser', password='12345')
        # [Check] Log in worked
        self.assertTrue(login)
        # [Prepare] Create a 'init' jobtype
        jt_init = JobType.objects.create(name="init", version=1.0, description="Init a job")
        JobType.objects.create(name="train", version=1.0, description="Training job by Jean-Baptiste M.")
        # [Prepare] Init a job
        job = Job.objects.create(type=jt_init)
        self.jobid = str(getattr(job, 'id'))
        # [Prepare] Create a test file
        fpath = settings.TEST_ROOT + "/test"
        self.fid1, error = Serialize_a_File(fpath, "test", "input", self.jobid)
        self.assertTrue(not error, "Error:" + str(error))
        # [Prepare] Create a csv features file
        fpath = settings.TEST_ROOT + "/test_features.csv"
        self.fid2, error = Serialize_a_File(fpath, "test", "input", self.jobid)
        self.assertTrue(not error, "Error:" + str(error))

    def test(self):

        while(True):
            print("Possible Requests:")
            print("------------------")
            print("​​/jobtype GET POST")
            print("​/jobtype​/{name} GET PUT PATCH DELETE")
            print("/jobs​/ GET POST")
            print("​/jobs​/{jobid} GET PUT DELETE")
            print("/jobs​/{jobid}​/files​/ GET POST ")
            print("​/jobs​/{jobid}​/files​/{fid} GET DELETE")
            print("​/files​/ GET")
            print("​/files​/{fid} GET DELETE")
            print("​/classifier GET POST")
            print("​/classifier​/{id} GET DELETE")
            print("​/transfer GET POST")
            print("​/transfer​/{fid} GET DELETE")
            print()
            req_type = input("Request type (GET/PUT/POST/DELETE) : ") or "Null"
            req_url = input("Request url (/xxx/xxx) : ") or None
            req_json = {}

            if req_type == "GET":
                print('===request===')
                print("GET ==> http://127.0.0.1:8000" + req_url)
                response = self.c.get(req_url, HTTP_ACCEPT='application/json')
                print('---response---')
                print(response.content)
                print("--------------")
            elif req_type == "PUT":
                req_json = input("Request json (ex: {'label':'info'}) : ") or {}
                req_json = req_json.replace("'", '"')
                req_json = json.loads(req_json)
                print('===request===')
                print("PUT " + str(req_json) + "==> http://127.0.0.1:8000" + req_url)
                response = self.c.put(req_url, req_json, content_type='application/json')
                print('---response---')
                print(response.content)
                print("--------------")
            elif req_type == "POST":
                req_json = input("Request json (ex: {'label':'info'}) : ") or {}
                req_json = req_json.replace("'", '"')
                req_json = json.loads(req_json)
                print('===request===')
                print("POST " + str(req_json) + " ==> http://127.0.0.1:8000" + req_url)
                response = self.c.post(req_url, req_json, content_type='application/json')
                print('---response---')
                print(response.json())
                print("--------------")
            elif req_type == "DELETE":
                print('===request===')
                print("DELETE ==> http://127.0.0.1:8000" + req_url)
                response = self.c.delete(req_url)
                print('---response---')
                print(response.content)
                print("--------------")
            else:
                print("\n/!\ This request '" + req_type + "' is not available /!\ \n")
                response = False
                
            bool_continue = input("Continue? (Y/n)") or "Y"
            if (bool_continue == "n"):
                return
            print("--------------")
