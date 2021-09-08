from django.test import TestCase

from jobapp.models import Job, JobType, JobFiles
from fileapp.models import File


class JobTestCase(TestCase):
    def setUp(self):
        self.testtype = JobType.objects.create(name="test")
        self.job = Job.objects.create(id=1, type=self.testtype)

    def test_jobtype_init(self):
        jt1 = self.testtype
        self.assertEqual(jt1.name, 'test')
        self.assertEqual(jt1.description, '')
        self.assertEqual(jt1.version, 0.0)

    def test_job_init(self):
        j1 = self.job
        self.assertEqual(j1.id, 1)
        self.assertEqual(j1.status, 'initialization')


class JobFilesTestCase(TestCase):
    def setUp(self):
        testtype = JobType.objects.create(name="test")
        self.job = Job.objects.create(id=1, type=testtype)
        self.file = File.objects.create(id=1, file="/home/user/toto.txt")
        self.jobFile = JobFiles.objects.create(id=1, file=self.file, job=self.job, type="input")

    def test_job_add_file(self):
        jf1 = self.jobFile
        self.assertEqual(jf1.id, 1)
        self.assertEqual(jf1.file, self.file)
        self.assertEqual(jf1.file.id, 1)
        self.assertEqual(jf1.job, self.job)
        self.assertEqual(jf1.job.id, 1)
        self.assertEqual(jf1.type, "input")
