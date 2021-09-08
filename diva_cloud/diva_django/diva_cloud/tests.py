import re
import shutil
import json
from django.test import TestCase, SimpleTestCase, override_settings
from django.test import Client
from diva_cloud import settings
from jobapp.models import JobType, Job, JobFiles
from django.contrib.auth.models import User
from fileapp.models import File, File_classifier, Transfer_function
from fileapp.serializers import Serialize_a_File


###########################################################################################
class JobTypeTestCase(TestCase):
    c = Client()

    def setUp(self):
        # [Prepare] Create a user and login
        self.user = User.objects.create_user(
            username='testuserjobtype', password='12345')
        login = self.c.login(username='testuserjobtype', password='12345')
        # [Check] Log in worked
        self.assertTrue(login)
        # [Prepare] Create a 'init' jobtype
        JobType.objects.create(name="init")

    # /JOBTYPE/ [POST] (V) ################################################################
    def test_postJobtype_ok(self):
        # [TEST PURPOSE] Post a 'test' jobtype
        response = self.c.post('/jobtype/', {"name": "test"})
        # [Check] Response status : 201
        self.assertEqual(response.status_code, 201, "{Status code: " + str(
            response.status_code) + "; Response: " + str(response.content) + "}")
        # [Check] It return the jobtype
        self.assertTrue(re.match('b\'{"name":"test","description":"","version":"0.00"}\'', str(
            response.content)), "{Response:" + str(response.content) + "}")

    # /JOBTYPE/ [POST] (X) ################################################################
    def test_postJobtype_nok(self):
        # [TEST PURPOSE] Post a 'test' without 'name' field
        response = self.c.post('/jobtype/')
        # [Check] Response status : 400
        self.assertEqual(response.status_code, 400, "{Status code: " + str(
            response.status_code) + "; Response: " + str(response.content) + "}")
        # [Check] It detect the empty field
        self.assertTrue(re.match('b\'{"name":\["This field is required."\]}\'', str(
            response.content)), "{Response:" + str(response.content) + "}")

    # /JOBTYPE/ [POST] (X) ################################################################
    def test_postJobtype2_nok(self):
        # [TEST PURPOSE] Post a 'toto666' jobtype (not acceptable)
        response = self.c.post('/jobtype/', {"name": "toto666"})
        # [Check] Response status : 400
        self.assertEqual(response.status_code, 400, "{Status code: " + str(
            response.status_code) + "; Response: " + str(response.content) + "}")
        # [Check] It detect the bad choice
        self.assertTrue(re.match('b\'{"name":\[.* is not a valid choice."\]}\'', str(
            response.content)), "{Response:" + str(response.content) + "}")

    # /JOBTYPE/x [GET] (V) ###################################################################
    def test_getJobtype_ok(self):
        # [TEST PURPOSE] Get the 'init' jobtype
        response = self.c.get('/jobtype/init', content_type='application/json')
        # [Check] Response status : 200
        self.assertEqual(response.status_code, 200, "{Status code: " + str(
            response.status_code) + "; Response: " + str(response.content) + "}")
        # [Check] It return the jobtype
        self.assertTrue(re.match('b\'{"name":"init","description":"","version":"0.00"}\'', str(
            response.content)), "{Response:" + str(response.content) + "}")

    # /JOBTYPE/x [GET] (X) ###################################################################
    def test_getJobtype_nok(self):
        # [TEST PURPOSE] Get the (not existing) 'toto' jobtype
        response = self.c.get('/jobtype/toto', content_type='application/json')
        # [Check] Response status : 404
        self.assertEqual(response.status_code, 404, "{Status code: " + str(
            response.status_code) + "; Response: " + str(response.content) + "}")
        # [Check] It return nothing
        self.assertTrue(re.match('b\'\'', str(response.content)), "{Response:" + str(response.content) + "}")

    # /JOBTYPE/x [PUT] (V) ###################################################################
    def test_putJobtype_ok(self):
        # [TEST PURPOSE] Put request on 'version' and 'description' of jobtype
        response = self.c.put('/jobtype/init', {"version": "1.0", "description": "Use this type to initialize a new job"}, content_type='application/json')
        # [Check] Response status : 200
        self.assertEqual(response.status_code, 200, "{Status code: " + str(
            response.status_code) + "; Response: " + str(response.content) + "}")
        # [Check] It return the jobtype updated
        self.assertTrue(re.match('b\'{"name":"init","description":"Use this type to initialize a new job","version":"1.00"}\'', str(
            response.content)), "{Response:" + str(response.content) + "}")

    # /JOBTYPE/x [PUT] (V) ###################################################################
    def test_putJobtype2_ok(self):
        # [TEST PURPOSE] Put request on 'version', 'description' and 'name' of jobtype
        response = self.c.put('/jobtype/init', {"name": "new_name_even_if_its_a_primary_key", "version": "1.0",
                                                "description": "Use this type to initialize a new job"}, content_type='application/json')
        # [Check] Response status : 200
        self.assertEqual(response.status_code, 200, "{Status code: " + str(
            response.status_code) + "; Response: " + str(response.content) + "}")
        # [Check] It return the jobtype updated but not the name because its a primary key
        self.assertTrue(re.match('b\'{"name":"init","description":"Use this type to initialize a new job","version":"1.00"}\'', str(
            response.content)), "{Response:" + str(response.content) + "}")

    # /JOBTYPE/x [PUT] (V) ###################################################################
    def test_putJobtype_nok(self):
        # [TEST PURPOSE] Put request on jobtype that not exist
        response = self.c.put(
            '/jobtype/toto666', {"version": "1.0", "description": "Use this type to initialize a new job"}, content_type='application/json')
        # [Check] Response status : 404
        self.assertEqual(response.status_code, 404, "{Status code: " + str(
            response.status_code) + "; Response: " + str(response.content) + "}")
        # [Check] It return nothing
        self.assertTrue(re.match('b\'\'', str(response.content)), "{Response:" + str(response.content) + "}")

    # /JOBTYPE/x [PATCH] (V) #################################################################
    def test_patchJobtype_ok(self):
        # [TEST PURPOSE] Patch request on 'version' and 'description' of jobtype
        response = self.c.patch(
            '/jobtype/init', {"version": "2.0", "description": "Use this type to initialize a new job"}, content_type='application/json')
        # [Check] Response status : 200
        self.assertEqual(response.status_code, 200, "{Status code: " + str(
            response.status_code) + "; Response: " + str(response.content) + "}")
        # [Check] It return the jobtype updated
        self.assertTrue(re.match('b\'{"name":"init","description":"Use this type to initialize a new job","version":"2.00"}\'', str(
            response.content)), "{Response:" + str(response.content) + "}")

    # /JOBTYPE [GET] (V) ###################################################################
    def test_getAllJobtype_ok(self):
        # [TEST PURPOSE] Get all jobtypes
        response = self.c.get('/jobtype/', content_type='application/json')
        # [Check] Response status : 200
        self.assertEqual(response.status_code, 200, "{Status code: " + str(
            response.status_code) + "; Response: " + str(response.content) + "}")
        # [Check] It return a table of jobtypes
        self.assertTrue(re.match('b\'\[{"name":"init","description":"","version":"0.00"}\]\'', str(
            response.content)), "{Response:" + str(response.content) + "}")


###########################################################################################
class JobTestCase(TestCase):
    c = Client()

    def setUp(self):
        # [Prepare] Create a user and login
        self.user = User.objects.create_user(
            username='testuserjob', password='12345')
        login = self.c.login(username='testuserjob', password='12345')
        self.assertTrue(login)
        # [Prepare] Create a 'init' jobtype
        self.jt_init = JobType.objects.create(name="init")
        # [Prepare] Init a job
        job = Job.objects.create(type=self.jt_init)
        self.jobid = str(getattr(job, 'id'))

    # /JOBS/ [POST] (V) ###################################################################
    def test_postJobs_ok(self):
        # [TEST PURPOSE] Initialize a job with a type init
        response = self.c.post('/jobs/', {'type': 'init'})
        # [Check] Response status : 201
        self.assertEqual(response.status_code, 201, "{Status code: " + str(
            response.status_code) + "; Response: " + str(response.content) + "}")
        self.jobid = str(response.json()['id'])
        # [Check] It return a the new job
        self.assertEqual(
            str(response.content), 'b\'{"id":' + self.jobid + ',"status":"initialization","taskid":"","type":"init"}\'', "{Response:" + str(response.content) + "}")

    # TO DELETE, no more post jobs #37
    # /JOBS/ [POST] (X) ###################################################################
    # def test_postJobsrun_nok(self):
    #     # [Prepare] Create a 'run' jobtype
    #     response = self.c.post('/jobtype', {'name': 'run'})
    #     # [TEST PURPOSE] Create a job with a type not managed
    #     response = self.c.post('/jobs/', {'type': 'run'})
    #     # [Check] Response status : 400
    #     self.assertEqual(response.status_code, 400, "{Status code: " + str(
    #         response.status_code) + "; Response: " + str(response.content) + "}")
    #     # [Check] The job is not submitted
    #     self.assertEqual(response.content, b'"No job submitted (type unavailable)"',
    #                      "{Response:" + str(response.content) + "}")

    # /JOBS/ [GET] (V) ####################################################################
    def test_getAllJobs_ok(self):
        # [TEST PURPOSE] Get all jobs
        response = self.c.get('/jobs/')
        # [Check] Response status : 200
        self.assertEqual(response.status_code, 200, "{Status code: " + str(
            response.status_code) + "; Response: " + str(response.content) + "}")
        # [Check] It return a table of jobs
        self.assertEqual(
            str(response.content), 'b\'[{"id":' + self.jobid + ',"status":"initialization","type":"init"}]\'', "{Response:" + str(response.content) + "}")

    # /JOBS/x [GET] (V) ###################################################################
    def test_getJobX_ok(self):
        # [TEST PURPOSE] Get a specific job
        response = self.c.get('/jobs/' + self.jobid)
        # [Check] Response status : 200
        self.assertEqual(response.status_code, 200, "{Status code: " + str(
            response.status_code) + "; Response: " + str(response.content) + "}")
        # [Check] It return the job
        self.assertEqual(
            str(response.content), 'b\'{"id":' + self.jobid + ',"status":"initialization","type":"init"}\'', "{Response:" + str(response.content) + "}")

    # /JOBS/x [GET] (X) ###################################################################
    def test_getJob666_nok(self):
        # [TEST PURPOSE] Get a nonexistent job
        response = self.c.get('/jobs/666')
        # [Check] Response status : 404
        self.assertEqual(response.status_code, 404, "{Status code: " + str(
            response.status_code) + "; Response: " + str(response.content) + "}")
        # [Check] It return an error
        self.assertEqual('b\'"No job with id 666"\'', str(response.content), "{Response:" + str(response.content) + "}")

    # /JOBS/x [DELETE] (V) ################################################################
    def test_deleteJob_ok(self):
        # [Prepare] Init a job
        job = Job.objects.create(type=self.jt_init)
        jobid2 = str(getattr(job, 'id'))
        # [TEST PURPOSE] Delete a specific job
        response = self.c.delete('/jobs/' + jobid2)
        # [Check] Response status : 200
        self.assertEqual(response.status_code, 200, "{Status code: " + str(
            response.status_code) + "; Response: " + str(response.content) + "}")
        # [Check] It return a confirmation message
        self.assertEqual('b\'"Job entry deleted"\'', str(response.content), "{Response:" + str(response.content) + "}")
        # [Check] the job has been deleted
        try:
            jf = JobFiles.objects.get(jobid=jobid2)
        except Exception:
            jf = False
        self.assertFalse(jf, "{JobFiles:" + str(jf) + "}")

    # /JOBS/x [DELETE] (V) #############################################################
    @override_settings(MEDIA_ROOT=settings.TEST_ROOT, MEDIA_URL=settings.TEST_URL)
    def test_deleteJobsInFiles_ok(self):
        # [Prepare] Init a job
        job = Job.objects.create(type=self.jt_init)
        jobid2 = str(getattr(job, 'id'))
        # [Prepare] Create a file in a specific job
        fpath = settings.TEST_ROOT + "/test"
        fid, error = Serialize_a_File(fpath, "test", "input", jobid2)
        self.assertTrue(not error, "Error:" + str(error))
        # [TEST PURPOSE] Delete this specific job
        response = self.c.delete('/jobs/' + jobid2)
        # [Check] Response status : 200
        self.assertEqual(response.status_code, 200, "{Status code: " + str(
            response.status_code) + "; Response: " + str(response.content) + "}")
        # [Check] It return a confirmation message
        self.assertEqual('b\'"Job entry deleted"\'', str(response.content), "{Response:" + str(response.content) + "}")
        # [Check] the jobfiles link to this job has been deleted
        try:
            jf = JobFiles.objects.get(jobid=jobid2)
        except Exception:
            jf = False
        self.assertFalse(jf, "{JobFiles:" + str(jf) + "}")

###########################################################################################
@override_settings(MEDIA_ROOT=settings.TEST_ROOT, MEDIA_URL=settings.TEST_URL)
class FileTestCase(TestCase):
    c = Client()

    def setUp(self):
        # [Prepare] Create a user and login
        self.user = User.objects.create_user(
            username='testuserfile', password='12345')
        login = self.c.login(username='testuserfile', password='12345')
        self.assertTrue(login)
        # [Prepare] Create a 'init' jobtype
        self.jt_init = JobType.objects.create(name="init")
        # [Prepare] Init a job
        job = Job.objects.create(type=self.jt_init)
        self.jobid = str(getattr(job, 'id'))
        # [Prepare] Create a file
        fpath = settings.TEST_ROOT + "/test"
        self.fid, error = Serialize_a_File(fpath, "test", "input", self.jobid)
        self.assertTrue(not error, "Error:" + str(error))
 
    # /FILES/ [GET] (V) ###################################################################
    def test_getAllFiles_ok(self):
        # [Show] there is only one file in "files" tab
        files_count = File.objects.all().count()
        self.assertTrue(files_count == 1, "{Files:" + str(files_count) + "}")
        # [Prepare] Create a second file
        fpath = settings.TEST_ROOT + "/test"
        fid2, error = Serialize_a_File(fpath, "test", "input", self.jobid)
        self.assertTrue(not error, "Error:" + str(error))
        # [Show] there is now two files in "files" tab
        files_count = File.objects.all().count()
        self.assertTrue(files_count == 2, "{Files:" + str(files_count) + "}")
        # [TEST PURPOSE] Get all files
        response = self.c.get('/files/')
        # [Check] Response status : 200
        self.assertEqual(response.status_code, 200, "{Status code: " + str(
            response.status_code) + "; Response: " + str(response.content) + "}")
        # [Check] if two files are returned by the query
        self.assertTrue(re.match('b\'\[{"id":' + self.fid + ',"file":"\/test\/files\/test_?.*"},{"id":' + fid2 + ',"file":"\/test\/files\/test_?.*"}\]\'', str(
            response.content)), "{Response:" + str(response.content) + "}")

    # /FILES/x [GET] (V) ##################################################################
    def test_getFile_ok(self):
        # [TEST PURPOSE] Get a specific file
        response = self.c.get('/files/' + self.fid, HTTP_ACCEPT='application/json')
        # [Check] It return the file
        self.assertTrue(re.match('b\'{"id":' + self.fid + ',"file":"\/test\/files\/test_?.*"}\'', str(
            response.content)), "{Response:" + str(response.content) + "}")
        # [Check] Response status : 200
        self.assertEqual(response.status_code, 200, "{Status code: " + str(
            response.status_code) + "; Response: " + str(response.content) + "}")

    # /FILES/x [GET] (X) ##################################################################
    def test_getFile666_nok(self):
        # [TEST PURPOSE] Get a nonexistent file
        response = self.c.get('/files/666', HTTP_ACCEPT='application/json')
        # [Check] Response status : 404
        self.assertEqual(response.status_code, 404, "{Status code: " + str(
            response.status_code) + "; Response: " + str(response.content) + "}")
        # [Check] It return an error
        self.assertTrue(re.match('.*No file with id 666.*',
                                 str(response.content)), "{Response:" + str(response.content) + "}")

    # /FILES/x [DELETE] (V) ###############################################################
    def test_deleteFile_ok(self):
        # [TEST PURPOSE] Delete a specific file
        response = self.c.delete('/files/' + self.fid)
        # [Check] Response status : 200
        self.assertEqual(response.status_code, 200, "{Status code: " + str(
            response.status_code) + "; Response: " + str(response.content) + "}")
        # [Check] It return a confirmation message
        self.assertTrue(re.match('.*File entry deleted.*',
                                 str(response.content)), "{Response:" + str(response.content) + "}")
        # [Check] the jobfiles link to this file has been deleted
        try:
            jf = JobFiles.objects.get(fid=self.fid)
        except Exception:
            jf = False
        self.assertFalse(jf, "{JobFiles:" + str(jf) + "}")

    # /FILES/x [DELETE] (X) ###############################################################
    def test_deleteFile_nok(self):
        # [TEST PURPOSE] Delete a nonexistent file
        response = self.c.delete('/files/666')
        # [Check] Response status : 404
        self.assertEqual(response.status_code, 404, "{Status code: " + str(
            response.status_code) + "; Response: " + str(response.content) + "}")
        # [Check] It return an error
        self.assertTrue(re.match('.*No file with id 666.*',
                                 str(response.content)), "{Response:" + str(response.content) + "}")


    # /JOBS/x/FILES [POST] (V) ############################################################
    def test_postFile_ok(self):
        # [TEST PURPOSE] Create a new file
        with open(settings.TEST_ROOT + "/test") as fp:
            response = self.c.post(
                '/jobs/' + self.jobid + '/files/', {'name': 'file', 'filename': 'test', 'file': fp, 'type': 'input'})
        fp.close()
        # [Check] Response status : 201
        self.assertEqual(response.status_code, 201, "{Status code: " + str(
            response.status_code) + "; Response: " + str(response.content) + "}")
        # [Check] Files has been created
        self.fid = str(response.json()['id'])
        self.assertTrue(re.match('b\'{"id":' + self.fid + ',"file":"\/test\/files\/test_?.*"}\'', str(
            response.content)), "{Response:" + str(response.content) + "}")


    # /JOBS/x/FILES [POST] (V) ############################################################
    def test_postJobFile_ok(self):
        # [TEST PURPOSE] Create a new file
        with open(settings.TEST_ROOT + "/test") as fp:
            response = self.c.post(
                '/files/', {'name': 'file', 'filename': 'test', 'file': fp, 'type': 'input'})
        fp.close()
        # [Check] Response status : 201
        self.assertEqual(response.status_code, 201, "{Status code: " + str(
            response.status_code) + "; Response: " + str(response.content) + "}")
        # [Check] Files has been created
        self.fid = str(response.json()['id'])
        self.assertTrue(re.match('b\'{"id":' + self.fid + ',"file":"\/test\/files\/test_?.*"}\'', str(
            response.content)), "{Response:" + str(response.content) + "}")


    # /JOBS/x/FILES [POST] (V) ############################################################
    def test_postJobFileBytestring64_ok(self):
        # [TEST PURPOSE] Create a new file from Bytestring64
        with open(settings.TEST_ROOT + "/Bytestring64.txt", "rb") as json_byte:
            data = json.load(json_byte)
            response = self.c.post('/jobs/' + self.jobid + '/files/',
                                json.dumps(data),
                                content_type="application/json")


        # [Check] Response status : 201
        self.assertEqual(response.status_code, 201, "{Status code: " + str(
            response.status_code) + "; Response: " + str(response.content) + "}")
        # [Check] Files has been created
        self.fid = str(response.json()['id'])
        self.assertTrue(re.match('b\'{"id":' + self.fid + ',"file":"\/test\/files\/features_?.*"}\'', str(
            response.content)), "{Response:" + str(response.content) + "}")

    # /JOBS/x/FILES [POST] (X) ############################################################
    def test_postJobFiles_nok(self):
        # [TEST PURPOSE] Create a new file with bad request
        with open(settings.TEST_ROOT + "/test") as fp:
            response = self.c.post('/jobs/' + self.jobid + '/test/', {'name': 'file', 'filename': 'toto', 'file': fp, 'type': 'input'})
        fp.close()
        # [Check] Response status : 404
        self.assertEqual(response.status_code, 404, "{Status code: " + str(
            response.status_code) + "; Response: " + str(response.content) + "}")
        # [Check] It return an error
        self.assertTrue(re.match('.*The requested resource was not found on this server.*',
                                 str(response.content)), "{Response:" + str(response.content) + "}")

    # /JOBS/x/FILES [POST] (V) ############################################################
    def test_postJobFileId_ok(self):
        # [Prepare] Init a job
        job = Job.objects.create(type=self.jt_init)
        jobid = str(getattr(job, 'id'))
        # [TEST PURPOSE] Add a file in the new job through a file id:
        response = self.c.post('/jobs/' + jobid + '/files/', {'id': self.fid, 'type': 'input'})
        # [Check] Response status : 201
        self.assertEqual(response.status_code, 201, "{Status code: " + str(
            response.status_code) + "; Response: " + str(response.content) + "}")
        # [Check] The file as been found, register and returned
        self.assertTrue(re.match('b\'{"id":' + self.fid + ',"file":"/test/files/test_?.*"}\'', str(
            response.content)), "{Response:" + str(response.content) + "}")
        # [Check] The status of the job has been updated
        j = Job.objects.get(id=jobid)
        self.assertTrue(j.status == "file_updating", "{Job__status:" + str(j.status) + "}")
        # [Check] The file is well linked to the job
        jf = JobFiles.objects.get(job=self.jobid, file=self.fid)
        self.assertTrue(re.match('{\'id\': .*, \'file\': ' + self.fid + ', \'fname\': .*test.*, \'job\': ' + self.jobid + ', \'type\': \'input\'}', str(jf)), "{JobFiles:" + str(jf) + "}")

    # /JOBS/x/FILES [POST] (V) ############################################################
    def test_post2JobFile_ok(self):
        # [Prepare] Init a second job
        job = Job.objects.create(type=self.jt_init)
        jobid2 = str(getattr(job, 'id'))
        # [TEST PURPOSE] Post a file in a second job
        response = self.c.post('/jobs/' + jobid2 + '/files/', {'id': self.fid, 'type': 'input'})
        # [Check] Response status : 201
        self.assertEqual(response.status_code, 201)
        # [Check] The file is link to two jobs
        jobs_link_to_file = JobFiles.objects.filter(file=self.fid)
        self.assertTrue(jobs_link_to_file.count() == 2)
        # [Check] The file is link to jobs 1 and 2
        jobids = jobs_link_to_file.values_list('job', flat=True)
        self.assertTrue(re.match('.*\[' + self.jobid + ', ' + jobid2 + '\].*', str(jobids)), "{JobFiles_jobids:" + str(jobids) + "}")

    # /JOBS/x/FILES [POST] (V) ############################################################
    def test_postJob2File_ok(self):
        # [TEST PURPOSE] Create a second file in the same job
        with open(settings.TEST_ROOT + "/test") as fp:
            response = self.c.post(
                '/jobs/' + self.jobid + '/files/', {'name': 'file', 'filename': 'test', 'file': fp, 'type': 'input'})
        # [Check] Response status : 201
        self.assertEqual(response.status_code, 201, "{Status code: " + str(
            response.status_code) + "; Response: " + str(response.content) + "}")
        fp.close()
        fid2 = str(response.json()['id'])
        # [Check] The job is now link to two files
        files_link_to_job = JobFiles.objects.filter(job=self.jobid)
        self.assertTrue(files_link_to_job.count() == 2)
        # [Check] The job is link to files 1 and 2
        fids = files_link_to_job.values_list('file', flat=True)
        self.assertTrue(re.match('.*\[' + self.fid + ', ' + fid2 + '\].*', str(fids)), "{JobFiles_fids:" + str(fids) + "}")

    # /JOBS/x/FILES [POST] (X) ############################################################
    def test_postJobFileId_nok(self):
        # [TEST PURPOSE] Add a file in the new job through a nonexistent file id
        response = self.c.post('/jobs/' + self.jobid + '/files/', {'id': 666, 'type': 'input'})
        # [Check] Response status : 404
        self.assertEqual(response.status_code, 404, "{Status code: " + str(
            response.status_code) + "; Response: " + str(response.content) + "}")
        # [Check] It return an error
        self.assertTrue(re.match('.*No file with id 666.*',
                                 str(response.content)), "{Response:" + str(response.content) + "}")

    # /JOBS/x/FILES [GET] (V) #############################################################
    def test_getJobFiles_ok(self):
        # [Prepare] Create a second file
        fpath = settings.TEST_ROOT + "/test"
        fid2, error = Serialize_a_File(fpath, "test", "input", self.jobid)
        self.assertTrue(not error, "Error:" + str(error))
        # [TEST PURPOSE] get all file link to a job:
        response = self.c.get('/jobs/' + self.jobid + '/files/') 
        # [Check] Response status : 200
        self.assertEqual(response.status_code, 200, "{Status code: " + str(
            response.status_code) + "; Response: " + str(response.content) + "}")
        # [Check] it return the two files linked to the job
        self.assertTrue(re.match('b\'\[{"file":{"id":' + self.fid + ',"file":"\/test\/files\/test_?.*"},"type":"input"},{"file":{"id":' + fid2 + ',"file":"\/test\/files\/test_?.*"},"type":"input"}\]\'', str(response.content)), "{Response:" + str(response.content) + "}")

    # /JOBS/x/FILES [GET] (X) #############################################################
    def test_getJobFiles_nok(self):
        # [TEST PURPOSE] get all file link to a nonexistent job
        response = self.c.get('/jobs/666/files/')
        # [Check] Response status : 404
        self.assertEqual(response.status_code, 404, "{Status code: " + str(
            response.status_code) + "; Response: " + str(response.content) + "}")
        # [Check] It return an error
        self.assertTrue(re.match('.*No file in job 666.*',
                                 str(response.content)), "{Response:" + str(response.content) + "}")

    # /JOBS/x/FILES/x [GET] () ###########################################################
    def test_getJobFileXnoheader_ok(self):
        # [TEST PURPOSE] get a specific file in a job (With no 'HTTP_ACCEPT' header)
        response = self.c.get('/jobs/' + self.jobid + '/files/' + self.fid)
        # [Check] Response status : 200
        self.assertEqual(response.status_code, 200,
                         "{Status code: " + str(response.status_code) + "}")
        # [Check] It return the file
        self.assertTrue(re.match('attachment; filename="files/test_?.*', response.get(
            'Content-Disposition')), "{Content-Disposition:" + response.get('Content-Disposition') + "}")

    # /JOBS/x/FILES/x [GET] (V) ###########################################################
    def test_getJobFileX_ok(self):
        # [TEST PURPOSE] get a specific file in a job (With the 'application/diva' accept header)
        response = self.c.get(
            '/jobs/' + self.jobid + '/files/' + self.fid, HTTP_ACCEPT='application/diva')
        # [Check] Response status : 200
        self.assertEqual(response.status_code, 200,
                         "{Status code: " + str(response.status_code) + "}")
        # [Check] It return the file
        self.assertTrue(re.match('attachment; filename="files/test_?.*', response.get(
            'Content-Disposition')), "{Content-Disposition:" + response.get('Content-Disposition') + "}")

    # /JOBS/x/FILES/x [GET] (V) ###########################################################
    def test_getJobFileXjson_ok(self):
        # [TEST PURPOSE] get a specific file in a job (With the 'application/json' accept header)
        response = self.c.get(
            '/jobs/' + self.jobid + '/files/' + self.fid, HTTP_ACCEPT='application/json')
        # [Check] Response status : 200
        self.assertEqual(response.status_code, 200, "{Status code: " + str(
            response.status_code) + "; Response: " + str(response.content) + "}")
        # [Check] It return the file metadatas
        self.assertTrue(re.match('b\'{"id":' + self.fid + ',"file":"\/test\/files\/test_?.*"}\'', str(
            response.content)), "{Response:" + str(response.content) + "}")

    # /JOBS/x/FILES/x [GET] (V) ###########################################################
    def test_getJobFileXjson2_ok(self): 
        # [TEST PURPOSE] get a specific file in a job (With the .json extension)
        response = self.c.get('/jobs/' + self.jobid + '/files/' + self.fid + '.json')
        # [Check] Response status : 200
        self.assertEqual(response.status_code, 200, "{Status code: " + str(
            response.status_code) + "; Response: " + str(response.content) + "}")
        # [Check] It return the file metadatas
        self.assertTrue(re.match('b\'{"id":' + self.fid + ',"file":"\/test\/files\/test_?.*"}\'', str(
            response.content)), "{Response:" + str(response.content) + "}")

    # /JOBS/x/FILES/x [GET] (X) ###########################################################
    def test_getJobFileXheader_nok(self): 
        # [TEST PURPOSE] get a specific file in a job (With an nonexistent 'application/toto' accept header):
        response = self.c.get(
            '/jobs/' + self.jobid + '/files/' + self.fid, HTTP_ACCEPT='application/toto')
        # [Check] Response status : 406 'Not Acceptable'
        self.assertEqual(response.status_code, 406, "{Status code: " + str(
            response.status_code) + "; Response: " + str(response.content) + "}")

    # /JOBS/x/FILES/x [GET] (X) ###########################################################
    def test_getJobFileX_nok(self): 
        # [TEST PURPOSE] get a specific file in a job (With the nonexistent .toto extension):
        response = self.c.get('/jobs/' + self.jobid + '/files/' + self.fid + '.toto')
        # [Check] Response status : 404
        self.assertEqual(response.status_code, 404, "{Status code: " + str(
            response.status_code) + "; Response: " + str(response.content) + "}")

    # /JOBS/x/FILES/x [GET] (X) ###########################################################
    def test_getJobFile666_nok(self): 
        # [TEST PURPOSE] get a specific nonexistent file in a job 
        response = self.c.get('/jobs/' + self.jobid + '/files/666')
        # [Check] Response status : 404
        self.assertEqual(response.status_code, 404, "{Status code: " + str(
            response.status_code) + "; Response: " + str(response.content) + "}")
        # [Check] It return an error
        self.assertTrue(re.match('.*No file with id 666.*',
                                 str(response.content)), "{Response:" + str(response.content) + "}")

    # /JOBS/x/FILES/x [DELETE] (V) ########################################################
    def test_deleteFileInJobs_ok(self):
        # [TEST PURPOSE] Delete a specific file in a job
        response = self.c.delete('/jobs/' + self.jobid + '/files/' + self.fid)
        # [Check] Response status : 200
        self.assertEqual(response.status_code, 200, "{Status code: " + str(
            response.status_code) + "; Response: " + str(response.content) + "}")
        # [Check] It return a confirmation message
        self.assertTrue(re.match('.*File entry deleted.*',
                                 str(response.content)), "{Response:" + str(response.content) + "}")
        # [Check] the jobfiles link to this file has been deleted
        try:
            jf = JobFiles.objects.get(fid=self.fid)
        except Exception:
            jf = False
        self.assertFalse(jf, "{JobFiles:" + str(jf) + "}")


###########################################################################################
@override_settings(MEDIA_ROOT=settings.TEST_ROOT, MEDIA_URL=settings.TEST_URL)
class LaunchTestCase(TestCase):
    c = Client()  # replace c by factory

    def setUp(self):
        # [Prepare] Create a user and login
        self.user = User.objects.create_user(
            username='testuserlaunch', password='12345')
        login = self.c.login(username='testuserlaunch', password='12345')
        self.assertTrue(login)
        # [Prepare] Create a 'init' jobtype
        jt_init = JobType.objects.create(name="init")
        # [Prepare] Create a 'test' jobtype
        self.jt_test = JobType.objects.create(name="test")
        # [Prepare] Create a 'train' jobtype
        self.jt_train = JobType.objects.create(name="train")
        # [Prepare] Init a job
        job = Job.objects.create(type=jt_init)
        self.jobid = str(getattr(job, 'id'))
        # [Prepare] Create a csv features file
        fpath = settings.TEST_ROOT + "/test_features.csv"
        self.fid, error = Serialize_a_File(fpath, "test", "input", self.jobid)
        self.assertTrue(not error, "Error:" + str(error))

    # /JOBS/x [PUT] (V) ################################################################### TODO: MANAGE OTHER JOBS?
    # def test_putJob_ok(self):
    #    # [Prepare] create an input request
    #    req = {"inputs_files": [self.fid]}
    #    # [TEST PURPOSE] Launch a test
    #    response = self.c.put(
    #        '/jobs/' + self.jobid, {'type': 'test', 'inputs': req}, content_type='application/json')
    #    # [Check] Response status : 200
    #    self.assertEqual(response.status_code, 200, "{Status code: " + str(
    #        response.status_code) + "; Response: " + str(response.content) + "}")
    #    # [Check] Return a 'done' job
    #    self.assertTrue(re.match('b\'{"id":' + self.jobid + ',"status":"done","type":"test"}\'', str(
    #        response.content)), "{Response:" + str(response.content) + "}")
    #    # [Check] the output is link to the job by the jobfiles table
    #    try:
    #        jf = JobFiles.objects.get(type="output", job=self.jobid)  # Change type
    #    except JobFiles.DoesNotExist:
    #        jf = JobFiles.DoesNotExist
    #    self.assertTrue(re.match('{\'id\': .*, \'file\': .*, \'fname\': .*output.*, \'job\': ' + self.jobid + ', \'type\': \'output\'}', str(jf)), "{JobFiles:" + str(jf) + "}")

    # /JOBS/x [PUT] (X) ###################################################################
    def test_putJob666_nok(self):
        # [TEST PURPOSE] Launch a test on an nonexistent job
        response = self.c.put(
            '/jobs/666', {'type': 'test'}, content_type='application/json')
        # [Check] Response status : 404
        self.assertEqual(response.status_code, 404, "{Status code: " + str(
            response.status_code) + "; Response: " + str(response.content) + "}")
        # [Check] It return an error
        self.assertTrue(re.match('.*No test job with id 666.*',
                                 str(response.content)), "{Response:" + str(response.content) + "}")

   # /JOBS/x [PUT] (X) ###################################################################
    def test_putJobnull_nok(self):
        # [TEST PURPOSE] Launch a test with an non managed jobtype
        response = self.c.put(
            '/jobs/' + self.jobid, {'type': 'null', 'strength': 5}, content_type='application/json')
        # [Check] Response status : 400
        self.assertEqual(response.status_code, 404, "{Status code: " + str(
            response.status_code) + "; Response: " + str(response.content) + "}")
        # [Check] It return an error
        self.assertTrue(re.match('.*Only .*train.*infer.* jobs are curently available.*',
                                 str(response.content)), "{Response:" + str(response.content) + "}")

    # TEST ON REAL JOB ('TRAIN' by JBM)
    # /LEARNING/x [PUT] (V) ###################################################################
    def test_putJobTrain_ok(self):
        # [Prepare] Add features
        with open(settings.TEST_ROOT + "/Bytestring64.txt", "rb") as json_byte:
            data = json.load(json_byte)
            response = self.c.post('/jobs/' + self.jobid + '/files/',
                                json.dumps(data),
                                content_type="application/json")

        # [TEST PURPOSE] Launch a 'train' test 
        response = self.c.put(
           '/learning/' + self.jobid, {'type': 'train', 'strength': 5}, content_type='application/json')
        # [Check] Response status : 200
        self.assertEqual(response.status_code, 201, "{Status code: " + str(
           response.status_code) + "; Response: " + str(response.content) + "}")
        # [Check] Return a 'running' job
        self.assertTrue(re.match('b\'{"id":' + self.jobid + ',"status":"running","type":"train"}\'', str(
           response.content)), "{Response:" + str(response.content) + "}")
        # [Check] The output is link to the job by the jobfiles table 
        # [NO OUTPUT, job is running]
        # try:
        #    jf = JobFiles.objects.get(type="classifier_out", job=self.jobid)
        # except JobFiles.DoesNotExist:
        #    jf = JobFiles.DoesNotExist
        # self.assertTrue(re.match('{\'id\': .*, \'file\': .*, \'fname\': .*output.*, \'job\': ' + self.jobid + ', \'type\': \'classifier_out\'}', str(jf)), "{JobFiles:" + str(jf) + "}")

   # /LEARNING/x [PUT] (X) ###################################################################
    # def test_putJobTrain_nok(self):
    #    # [TEST PURPOSE] Launch a 'train' test with no features
    #    response = self.c.put(
    #        '/learning/' + self.jobid, {'type': 'train', 'strength': 5}, content_type='application/json')
    #    # [Check] Response status : 404
    #    self.assertEqual(response.status_code, 404, "{Status code: " + str(
    #        response.status_code) + "; Response: " + str(response.content) + "}")
    #    # [Check] It return an error
    #    self.assertTrue(re.match('.*No features in train job ' + self.jobid,
    #                             str(response.content)), "{Response:" + str(response.content) + "}")
    # ==> Not possible anymore, at this time

   # /LEARNING/x [PUT] (X) ###################################################################  # Need to manage input_classifier
    def test_putJobTrainWithClassifier_ok(self):
        # [Prepare] Add features
        with open(settings.TEST_ROOT + "/Bytestring64.txt", "rb") as json_byte:
            data = json.load(json_byte)
            response = self.c.post('/jobs/' + self.jobid + '/files/', json.dumps(data),content_type="application/json")
        json_byte.close()
        # [Prepare] Create the classifier file
        with open(settings.TEST_ROOT + "/test") as classifier:
            response = self.c.post(
                '/jobs/' + self.jobid + '/files/', {'name': 'file', 'filename': 'test', 'file': classifier, 'type': 'classifier_in'})
        classifier.close()
        # [TEST PURPOSE] Launch a 'train' test with a classifier
        response = self.c.put(
           '/learning/' + self.jobid, {'type': 'train', 'strength': 5}, content_type='application/json')
        # [Check] Response status : 404
        self.assertEqual(response.status_code, 201, "{Status code: " + str(response.status_code) + "; Response: " + str(response.content) + "}")
        # [Check] It return an error
        self.assertTrue(re.match('b\'{"id":' + self.jobid + ',"status":"running","type":"train"}\'', str(response.content)), "{Response:" + str(response.content) + "}")
       

@override_settings(MEDIA_ROOT=settings.TEST_ROOT, MEDIA_URL=settings.TEST_URL)
class TrainTestCase(TestCase):
    c = Client()

    def setUp(self):
        # [Prepare] Create a user and login
        self.user = User.objects.create_user(
            username='testusertrain', password='12345')
        login = self.c.login(username='testusertrain', password='12345')
        self.assertTrue(login)
        # [Prepare] Create a 'train' jobtype
        self.jt_train = JobType.objects.create(name="train")

# /TRAIN/ (X) #########################################################################
    def test_createTrain_ok(self):
        # [Prepare] Init a job
        self.job = Job.objects.create(type=self.jt_train)
        self.jobid = str(getattr(self.job, 'id'))
        # [Prepare] Create a csv features file
        fpath = settings.TEST_ROOT + "/test_features.csv"
        self.fid, error = Serialize_a_File(fpath, "test", "input", self.jobid)
        self.assertTrue(not error, "Error:" + str(error))
        # [TEST PURPOSE] Launch asynchronous default train
        from celery_tasks import launch_asynchron
        strength = 1
        res = launch_asynchron.apply(args=(int(self.jobid), {"features": [int(self.fid)]}, False, "train"))
        response = self.c.get('/jobs/' + self.jobid)
        # [Check] Train is accessible
        self.assertTrue(re.match('b\'{"id":' + self.jobid + ',"status":"done","type":"train"}\'', str(response.content)), "{Response:" + str(response.content) + "}")
        # [Check] Train_asynchron job suceed
        self.assertEqual(res.state, "SUCCESS", "{state: " + str(res.state) + ",res: " + str(res.get(timeout=1)) + "}")
        rst = res.get()
        # [Check] Train_asynchron result is "None" ==> All is ok
        self.assertEqual(rst, None, "{res: " + str(rst) + "}")
        # [Check] Train_asynchron output file has been created
        self.assertEqual(self.job.countspecificfiles("classifier_out"), 1, "{Number of \"classifier_out\" files: " + str(self.job.countspecificfiles("classifier_out")) + "}")
        # [Check] Train_asynchron input and output files
        response = self.c.get('/jobs/' + self.jobid + '/files/')
        self.assertTrue(re.match('b\'\[{"file":{"id":.*,"file":".*"},"type":"input"},{"file":{"id":.*,"file":".*"},"type":"classifier_out"}\]\'', str(response.content)), "{Response:" + str(response.content) + "}")

    # /TRAIN/ (X) #########################################################################
    def test_createTrain_s1_ok(self):
        # [Prepare] Init a job
        self.job = Job.objects.create(type=self.jt_train)
        self.jobid = str(getattr(self.job, 'id'))
        # [Prepare] Create a csv features file
        fpath = settings.TEST_ROOT + "/test_features.csv"
        self.fid, error = Serialize_a_File(fpath, "test", "input", self.jobid)
        self.assertTrue(not error, "Error:" + str(error))
        # [TEST PURPOSE] Launch asynchronous train with strength = 1
        from celery_tasks import launch_asynchron
        strength = 1
        res = launch_asynchron.apply(args=(int(self.jobid), {"features": [int(self.fid)]}, {"strength": strength}, "train"))
        response = self.c.get('/jobs/' + self.jobid)
        # [Check] Train is accessible
        self.assertTrue(re.match('b\'{"id":' + self.jobid + ',"status":"done","type":"train"}\'', str(response.content)), "{Response:" + str(response.content) + "}")
        # [Check] Train_asynchron job suceed
        self.assertEqual(res.state, "SUCCESS", "{state: " + str(res.state) + ",res: " + str(res.get(timeout=1)) + "}")
        rst = res.get()
        # [Check] Train_asynchron result is "None" ==> All is ok
        self.assertEqual(rst, None, "{res: " + str(rst) + "}")
        # [Check] Train_asynchron output file has been created
        self.assertEqual(self.job.countspecificfiles("classifier_out"), 1, "{Number of \"classifier_out\" files: " + str(self.job.countspecificfiles("classifier_out")) + "}")
        # [Check] Train_asynchron input and output files
        response = self.c.get('/jobs/' + self.jobid + '/files/')
        self.assertTrue(re.match('b\'\[{"file":{"id":.*,"file":".*"},"type":"input"},{"file":{"id":.*,"file":".*"},"type":"classifier_out"}\]\'', str(response.content)), "{Response:" + str(response.content) + "}")


    # /TRAIN/ (X) #########################################################################
    def test_createTrain_s5_ok(self):
        # [Prepare] Init a job
        self.job = Job.objects.create(type=self.jt_train)
        self.jobid = str(getattr(self.job, 'id'))
        # [Prepare] Create a csv features file
        fpath = settings.TEST_ROOT + "/test_features.csv"
        self.fid, error = Serialize_a_File(fpath, "test", "input", self.jobid)
        self.assertTrue(not error, "Error:" + str(error))
        # [TEST PURPOSE] Launch asynchronous train with strength = 5
        from celery_tasks import launch_asynchron
        strength = 5
        res = launch_asynchron.apply(args=(int(self.jobid), {"features": [int(self.fid)]}, {"strength": strength}, "train"))
        response = self.c.get('/jobs/' + self.jobid)
        # [Check] Train is accessible
        self.assertTrue(re.match('b\'{"id":' + self.jobid + ',"status":"done","type":"train"}\'', str(response.content)), "{Response:" + str(response.content) + "}")
        # [Check] Train_asynchron job suceed
        self.assertEqual(res.state, "SUCCESS", "{state: " + str(res.state) + ",res: " + str(res.get(timeout=1)) + "}")
        rst = res.get()
        # [Check] Train_asynchron result is "None" ==> All is ok
        self.assertEqual(rst, None, "{res: " + str(rst) + "}")
        # [Check] Train_asynchron output file has been created
        self.assertEqual(self.job.countspecificfiles("classifier_out"), 1, "{Number of \"classifier_out\" files: " + str(self.job.countspecificfiles("classifier_out")) + "}")
        # [Check] Train_asynchron input and output files
        response = self.c.get('/jobs/' + self.jobid + '/files/')
        self.assertTrue(re.match('b\'\[{"file":{"id":.*,"file":".*"},"type":"input"},{"file":{"id":.*,"file":".*"},"type":"classifier_out"}\]\'', str(response.content)), "{Response:" + str(response.content) + "}")
        

    # def test_createTrain_s10_ok(self):   #Not working? The requested resource was not found on this server
    #     # [Prepare] Init a job
    #     self.job = Job.objects.create(type=self.jt_train)
    #     self.jobid = str(getattr(self.job, 'id'))
    #     # [Prepare] Create a csv features file
    #     fpath = settings.TEST_ROOT + "/test_features.csv"
    #     self.fid, error = Serialize_a_File(fpath, "test", "input", self.jobid)
    #     self.assertTrue(not error, "Error:" + str(error))
    #     # [TEST PURPOSE] Launch asynchronous train with strength = 10
    #     from celery_tasks import launch_asynchron
    #     strength = 10
    #  res = launch_asynchron.apply(args=(int(self.jobid), {"features": list(int(self.fid))}, False, "train"))
    #     response = self.c.get('/train/' + self.jobid)
    #     # [Check] Train is accessible
    #     self.assertTrue(re.match('b\'{"id":' + self.jobid + ',"status":"initialization","type":"train"}\'', str(response.content)), "{Response:" + str(response.content) + "}")
    #     # [Check] Train_asynchron job suceed
    #     self.assertEqual(res.state, "SUCCESS", "{state: " + str(res.state) + ",res: " + str(res.get(timeout=1)) + "}")
    #     rst = res.get()
    #     # [Check] Train_asynchron result is "None" ==> All is ok
    #     self.assertEqual(rst, None, "{res: " + str(rst) + "}")
    #     # [Check] Train_asynchron output file has been created
    #     self.assertEqual(self.job.countspecificfiles("classifier_out"), 1, "{Number of \"classifier_out\" files: " + str(self.job.countspecificfiles("classifier_out")) + "}")
    #     # [Check] Train_asynchron input and output files
    #     response = self.c.get('/jobs/' + self.jobid + '/files/')
    #     self.assertTrue(re.match('b\'\[{"file":{"id":.*,"file":".*"},"type":"input"},{"file":{"id":.*,"file":".*"},"type":"classifier_out"}\]\'', str(response.content)), "{Response:" + str(response.content) + "}")
        
# /TRAIN/ (X) #########################################################################
    #def test_createTrain_classifier_ok(self):
    #TODO
    # [TEST PURPOSE] Launch asynchronous train with a classifier

@override_settings(MEDIA_ROOT=settings.TEST_ROOT, MEDIA_URL=settings.TEST_URL)
class InferTestCase(TestCase):
    c = Client()

    def setUp(self):
        # [Prepare] Create a user and login
        self.user = User.objects.create_user(
            username='testuserinfer', password='12345')
        login = self.c.login(username='testuserinfer', password='12345')
        self.assertTrue(login)
        # [Prepare] Create a 'train' jobtype
        self.jt_infer = JobType.objects.create(name="infer")

###########################################################################################
@override_settings(MEDIA_ROOT=settings.TEST_ROOT, MEDIA_URL=settings.TEST_URL)
class ClassifiersTestCase(TestCase):
    c = Client()

    def setUp(self):
        # [Prepare] Create a user and login
        self.user = User.objects.create_user(
            username='testuserclassifier', password='12345')
        login = self.c.login(username='testuserclassifier', password='12345')
        self.assertTrue(login)
        # [Prepare] Create a 'init' jobtype
        jt_init = JobType.objects.create(name="init")
        # [Prepare] Init a job
        job = Job.objects.create(type=jt_init)
        self.jobid = str(getattr(job, 'id'))
        # [Prepare] Create a file
        fpath = settings.TEST_ROOT + "/test"
        self.fid, error = Serialize_a_File(fpath, "test", "input", self.jobid)
        self.assertTrue(not error, "Error:" + str(error))
        # [Prepare] Create a classifier
        file = File.objects.get(id=self.fid)
        classifier = File_classifier.objects.create(fid=file)
        self.id = str(getattr(classifier, 'id'))

    # /CLASSIFIER [POST] (V) ##############################################################
    def test_postClassifier_ok(self):
        # [TEST PURPOSE] Add a file in the classifier table trough a file id
        response = self.c.post('/classifier', {'fid': self.fid})
        # [Check] Response status : 201
        self.assertEqual(response.status_code, 201, "{Status code: " + str(response.status_code) + "; Response: " + str(response.content) + "}")
        # [Check] The file as been found, register and returned
        self.id = str(response.json()['id'])
        self.assertTrue(re.match('b\'{"id":' + self.id + ',"fid":' + self.fid + '}\'', str(
            response.content)), "{Response:" + str(response.content) + "}")

    # /CLASSIFIER [GET] (V) ###############################################################
    def test_getClassifier_ok(self):
        # [TEST PURPOSE] Get a file from the classifier table
        response = self.c.get('/classifier')
        # [Check] Response status : 200
        self.assertEqual(response.status_code, 200, "{Status code: " + str(
            response.status_code) + "; Response: " + str(response.content) + "}")
        # [Check] It return the file metadatas
        self.assertTrue(re.match('b\'\[{"id":' + self.id + ',"fid":' + self.fid + '}\]\'', str(
            response.content)), "{Response:" + str(response.content) + "}")

    # /CLASSIFIER/x [GET] (V) #############################################################
    def test_getClassifier1json_ok(self):
        # [TEST PURPOSE] Get a file from the classifier table (With the 'application/json' accept header)
        response = self.c.get(
            '/classifier/' + self.fid, HTTP_ACCEPT='application/json')
        # [Check] Response status : 200
        self.assertEqual(response.status_code, 200, "{Status code: " + str(
            response.status_code) + "; Response: " + str(response.content) + "}")
        # [Check] It return the file metadatas
        self.assertTrue(re.match('b\'{"id":' + self.id + ',"fid":' + self.fid + '}\'', str(
            response.content)), "{Response:" + str(response.content) + "}")

    # /CLASSIFIER/x [GET] (V) #############################################################
    def test_getClassifier1_ok(self):
        # [TEST PURPOSE] Get a file from the classifier table (With the 'application/diva' accept header)
        response = self.c.get(
            '/classifier/' + self.fid, HTTP_ACCEPT='application/diva')
        # [Check] Response status : 200
        self.assertEqual(response.status_code, 200, "{Status code: " + str(
            response.status_code) + "}")
        # [Check] It return the file content
        self.assertTrue(re.match('attachment; filename="files/test_?.*', response.get(
            'Content-Disposition')), "{Content-Disposition:" + response.get('Content-Disposition') + "}")


###########################################################################################
@override_settings(MEDIA_ROOT=settings.TEST_ROOT, MEDIA_URL=settings.TEST_URL)
class TransferFunctionTestCase(TestCase):
    c = Client()

    def setUp(self):
        # [Prepare] Create a user and login
        self.user = User.objects.create_user(
            username='testusertransfer', password='12345')
        login = self.c.login(username='testusertransfer', password='12345')
        self.assertTrue(login)
        # [Prepare] Create json entry
        with open(settings.TEST_ROOT + "/test_transfer_function.json") as file:
            json_string = file.read().replace("'", '"')
            my_json = json_string.replace("'", '"')
            file = Transfer_function.objects.create(content=json.loads(my_json))
            self.fid = str(getattr(file, 'id'))

    # /FNTRANSFER [POST] (V) ##############################################################
    def test_postTransferFunctions_ok(self):
        # [TEST PURPOSE] Create a jsonfile on transferfunction table
        with open(settings.TEST_ROOT + "/test_transfer_function.json") as fp:
            response = self.c.post(
                '/transfer', {'name': 'file', 'filename': 'test', 'file': fp})
        # [Check] Response status : 201
        self.assertEqual(response.status_code, 201, "{Status code: " + str(
                response.status_code) + "; Response: " + str(response.content) + "}")
        fp.close()
        # [Check] It return the json metadatas
        fid = str(response.json()['id'])
        self.assertTrue(re.match('b\'{"id":' + fid + ',"content":{"tfs":.*}}\'', str(
            response.content)), "{Response:" + str(response.content) + "}")

    # /FNTRANSFER [GET] (V) ###############################################################
    def test_getTransferFunctions_ok(self):
        # [TEST PURPOSE] Get all jsonfiles off the transferfunction table
        response = self.c.get('/transfer')
        # [Check] Response status : 200
        self.assertEqual(response.status_code, 200, "{Status code: " + str(
            response.status_code) + "; Response: " + str(response.content) + "}")
        # [Check] It return a table of jsons metadatas
        self.assertTrue(re.match('b\'\[{"id":' + self.fid + ',"content":{"tfs":.*}}\]\'', str(
            response.content)), "{Response:" + str(response.content) + "}")

    # /FNTRANSFER/x [GET] (V) #############################################################
    def test_getTransferFunction1json_ok(self):
        # [TEST PURPOSE] Get a transfer function (With the 'application/json' accept header)
        response = self.c.get(
            '/transfer/' + self.fid, HTTP_ACCEPT='application/json')
        # [Check] Response status : 200
        self.assertEqual(response.status_code, 200, "{Status code: " + str(
            response.status_code) + "; Response: " + str(response.content) + "}")
        # [Check] It return the json content
        self.assertTrue(re.match('b\'{"tfs":.*}\'', str(
            response.content)), "{Response:" + str(response.content) + "}")

    # /FNTRANSFER/x [GET] (V) #############################################################
    def test_getTransferFunction1_ok(self):
        # [TEST PURPOSE] Get a transfer function (With no accept header)
        response = self.c.get(
            '/transfer/' + self.fid)
        # [Check] Response status : 200
        self.assertEqual(response.status_code, 200, "{Status code: " + str(
            response.status_code) + "; Response: " + str(response.content) + "}")
        # [Check] It return the json metadatas
        self.assertTrue(re.match('b\'{"id":' + self.fid + ',"content":{"tfs":.*}}\'', str(
            response.content)), "{Response:" + str(response.content) + "}")


###########################################################################################
# Comment to not clean
class CleanTestCase(SimpleTestCase):
    # [PURPOSE] Clean de repository files wich contain all the test files
    def test_clean(self):
        shutil.rmtree(settings.TEST_ROOT + '/files')
