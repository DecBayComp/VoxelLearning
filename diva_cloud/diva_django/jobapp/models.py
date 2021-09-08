from django.db import models
from fileapp.models import File
from django.contrib.postgres.fields import JSONField


JOB_TYPE = (('test', 'Test'), ('train', 'train program by JBM'), ('infer', 'inference program by JBM'), ('stock', 'Stock files'), ('null', 'Nothing to do'),
            ('merge', 'Merge'), ('diva', 'Diva'), ('init', 'Initialization'), ('run', 'Run a job'), ('image', ('Temp: manage job on image')))
FILE_TYPES = (('input', 'Input'), ('output', 'Output'), ('classifier_in', 'Existing classifier'), ('features', 'features'), ('classifier_out', 'New classifier'), ('proba_out', 'Proba on classif'), ('packet_features', 'Features for one Packet'))
STATUS = (('initialization', 'Initialization'), ('file_updating', 'File updating'), ('job_launching', 'Job launching'),
          ('running', 'Running'), ('done', 'Done'), ('error', 'Error'), ('', 'None'),)


class JobType(models.Model):
    name = models.CharField(choices=JOB_TYPE, max_length=20, primary_key=True)
    description = models.CharField(default='', max_length=100)
    version = models.DecimalField(default=0.0, max_digits=3, decimal_places=2)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Type of job for the job manager"
        ordering = ['name']


class Job(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.ForeignKey(JobType, on_delete=models.CASCADE)
    status = models.CharField(
        choices=STATUS, default='initialization', max_length=100)
    taskid = models.CharField(max_length=100, default='')

    def __str__(self):
        return str(self.id)

    def gettaskid(self):
        return self.taskid

    class Meta:
        verbose_name = "Job management"
        ordering = ['id']

    def getfiles(self): #????
        return JobFiles.objects.filter(job=self.id).values_list('file', flat=True)
    def getspecificfiles(self,type): #????
        return JobFiles.objects.filter(job=self.id, type=type).values_list('file', flat=True)
    def countspecificfiles(self,type): #????
        return JobFiles.objects.filter(job=self.id, type=type).count()



class JobFiles(models.Model):
    id = models.AutoField(primary_key=True)
    file = models.ForeignKey(File, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    type = models.CharField(choices=FILE_TYPES, max_length=100)

    def getfid(self):
        return self.file.id

    def __str__(self):
        return str({"id": self.id, "file": self.file.id, "fname": self.file, "job": self.job.id, "type": self.type})
