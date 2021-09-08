from rest_framework.response import Response
from jobapp.models import Job, JobFiles
from fileapp.models import File
from fileapp.serializers import FileSerializer
from jobapp.serializers import JobFilesSerializer, JobNewSerializer
from jobapp.serializers import JobSerializer
from rest_framework.decorators import api_view, renderer_classes, parser_classes
from rest_framework.renderers import JSONRenderer
from celery_tasks import launch_asynchron#train_asynchron, infer_asynchron
from celery.result import AsyncResult
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from jobapp.joblauncher import Jobstype

import base64
import pandas as pd
import os

@api_view(['GET', 'POST'])
@renderer_classes([JSONRenderer])
def job_list(request):
    """
    List all job, or create a new job.
    """
    if request.method == 'GET':
        jobs = Job.objects.all()
        serializer = JobSerializer(jobs, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':

        if request.data["type"] == "init":
            serializer = JobNewSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=201)
            return Response(serializer.errors, status=400)
        else:
            return Response("POST type need to be 'init'", status=400)

@api_view(['GET', 'PUT', 'DELETE'])
@renderer_classes([JSONRenderer])
def job_detail(request, jobid):
    """
    Get, delete or launch a job.
    """
    try:
        myjob = Job.objects.get(pk=jobid)
    except Job.DoesNotExist:    
        if request.data.get('type'):
            return Response("No " + request.data['type'] + " job with id " + str(jobid), status=404)
        else:
            return Response("No job with id " + str(jobid), status=404)

    if request.method == 'GET':
        serializer = JobSerializer(myjob)
        return Response(serializer.data)

    elif request.method == 'PUT':
        return put_job(request, jobid, myjob)

    elif request.method == 'DELETE':
        myjob.delete()
        return Response("Job entry deleted", status=200)

def put_job(request, jobid, myjob):

    ######################################
    # Get learning job type
    if not request.data.get('type'):
        return Response("You need to specify job type", status=404)
    myjobtype = request.data['type']
    myjobtype_dict = Jobstype.type_dict
    if myjobtype not in myjobtype_dict:
        return Response("Only " + str(list(myjobtype_dict.values())) + " jobs are curently available", status=404)

    ######################################
    # JOBS PARAMETERS
    if myjobtype == myjobtype_dict["train"]:              
        parameters_tab = ["strength"]
        inputs_tab = ["classifier_in","features"]
        return launch_job(request, jobid, myjob, myjobtype, parameters_tab, inputs_tab)
    elif myjobtype == myjobtype_dict["infer"]:              
        parameters_tab = ["strength"]
        inputs_tab = ["classifier_in","packet_features"]
        return launch_job(request, jobid, myjob, myjobtype, parameters_tab, inputs_tab)
	#elif myjobtype == myjobtype_dict["<name_of_job>"]:              
    #    parameters_tab = ["<parameter1name>"]
    #    inputs_tab = ["<input1name>","<input2name>"]
    #    return launch_job(request, jobid, myjob, myjobtype, parameters_tab, inputs_tab)

def launch_job(request, jobid, myjob, myjobtype, parameters_tab, inputs_tab):

    ######################################
    # PARAMETERS
    parameters_dict = {}

    for p in parameters_tab:
        if request.data.get(p):
            parameters_dict[p] = request.data[p]
    ######################################
    # INPUT
    inputs_dict = {}
    for i in inputs_tab:
        try:
            inputs_dict[i] = list(JobFiles.objects.filter(job=jobid, type=i).values_list('file', flat=True))  # /!\ it's a table
        except IndexError:
            inputs_dict[i] = False

    ######################################
    # LAUNCH
    res = launch_asynchron.delay(jobid, inputs_dict, parameters_dict, myjobtype)
    taskid = res.id


    Jobserializer = JobSerializer(myjob, data={'type': myjobtype})
    if Jobserializer.is_valid():
        Jobserializer.save(status="running", taskid=taskid)
    else:
        return Response(Jobserializer.errors, status=400)
    return Response(Jobserializer.data, status=201)
    ######################################

@api_view(['GET'])
@renderer_classes([JSONRenderer])
#@parser_classes([ByteParser, MultiPartParser])
def train_list(request):
    """
    Get all train jobs
    """
    if request.method == 'GET':
        trainjobs = Job.objects.filter(type="train")
        serializer = JobSerializer(trainjobs, many=True)
        return Response(serializer.data)

@api_view(['GET'])
@renderer_classes([JSONRenderer])
#@parser_classes([ByteParser, MultiPartParser])
def infer_list(request):
    """
    Get all inference jobs
    """
    if request.method == 'GET':
        inferjobs = Job.objects.filter(type="infer")
        serializer = JobSerializer(inferjobs, many=True)
        return Response(serializer.data)
