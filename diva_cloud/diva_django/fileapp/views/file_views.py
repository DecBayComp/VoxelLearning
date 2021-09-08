from rest_framework.response import Response
from django.http import FileResponse
from rest_framework.decorators import api_view, renderer_classes
from fileapp.serializers import FileSerializer
from fileapp.models import File
from fileapp.renderer import DIVARenderer
from jobapp.models import Job, JobFiles, FILE_TYPES
from jobapp.serializers import JobFilesSerializer, JobFilesPlusSerializer
from rest_framework.renderers import JSONRenderer
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile

import base64
import pandas as pd
import os
import json


@api_view(['POST', 'GET'])
@renderer_classes([JSONRenderer])
def FilesView(request, format=None):
    """
    List all files or create a new one.
    """
    if request.method == 'GET':
        files = File.objects.all()
        serializer = FileSerializer(files, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        if request.data.get('type'):
            input_type = request.data['type']
        else:
            return Response("You need to specify file type with the 'type' key (" + ", ".join(str(x) + "(" + str(y) + ")" for x, y in FILE_TYPES) + ")", status=404)

        file_serializer = FileSerializer(data=request.data)
        if file_serializer.is_valid():
            file_serializer.save()
        else:
            return Response(file_serializer.errors, status=400)
        return Response(file_serializer.data, status=201)


@api_view(['POST', 'GET'])
@renderer_classes([JSONRenderer])
def FileUploadView(request, jobid, format=None):
    """
    List all files link to a job, or create a new file in a job.
    """
    if request.method == 'GET':
        try:
            jobfiles = JobFiles.objects.filter(job=jobid).select_related('file')
            jobfiles[0]
        except IndexError:
            return Response("No file in job " + str(jobid), status=404)

        serializer = JobFilesPlusSerializer(jobfiles, many=True)
        return Response(serializer.data)


    elif request.method == 'POST':
        try:
            job_caller = Job.objects.get(pk=jobid)
        except Job.DoesNotExist:
            return Response("No job with id " + str(jobid), status=404)
        # IF JOB has already be done
        if job_caller.status == "done":
            return Response("Jobs has already been done", status=400)

        job_caller.status = "file_updating"

        # If we send bytes
        if request.data.get('Bytestring64'):
            bytes_df = []
            fname = 'features.csv'
            fpath = '' + fname

            for val_bytestring64 in request.data['Bytestring64']:
                val_byte = base64.b64decode(val_bytestring64)
                val_bytelist = list(val_byte)
                bytes_df.append(val_bytelist)
            pddf = pd.DataFrame(bytes_df).transpose()
            pddf.to_csv(fpath, index=False)

            with open(fpath, 'rb') as fcsv:
                fdata = InMemoryUploadedFile(fcsv, 'file', fname, None, os.path.getsize(fpath), None)
                file_serializer = FileSerializer(data={'file': fdata})
                if file_serializer.is_valid():
                    file_serializer.save()
                    fid = file_serializer.data.get('id', None)
                    input_type = "features"    #VAL TEMP need to manage it on the request
                else:
                    return Response(file_serializer.errors, status=400)
            fcsv.close()

        # If we send file
        else:
            if request.data.get('type'):
                input_type = request.data['type']
            else:
                return Response("You need to specify file type with the 'type' key (" + ", ".join(str(x) + "(" + str(y) + ")" for x, y in FILE_TYPES) + ")", status=404)

            # If we point an id of file
            if request.data.get('id'):
                fid = request.data.get('id')
                try:
                    my_file = File.objects.get(pk=fid)
                except File.DoesNotExist:
                    return Response("No file with id " + str(fid), status=404)

                file_serializer = FileSerializer(my_file)
            # If we send a file
            else:
                file_serializer = FileSerializer(data=request.data)
                if file_serializer.is_valid():
                    file_serializer.save()
                    fid = file_serializer.data.get('id', None)
                else:
                    return Response(file_serializer.errors, status=400)

        data = {"file": fid, "job": jobid, "type": input_type}
        JobFiles_serializer = JobFilesSerializer(data=data)
        if JobFiles_serializer.is_valid():
            JobFiles_serializer.save()
        else:
            return Response(JobFiles_serializer.errors, status=400)

        job_caller.save()
        return Response(file_serializer.data, status=201)




@api_view(['POST', 'GET'])
@renderer_classes([JSONRenderer])
def FeaturesUploadView(request, jobid, format=None):
    """
    List all files link to a job, or create a new file in a job.
    """
    if request.method == 'GET':
       try:
           jobfiles = JobFiles.objects.filter(job=jobid).select_related('file').filter(type="packet_features")
           jobfiles[0]
       except IndexError:
           return Response("No packet features file in job " + str(jobid), status=404)

       serializer = JobFilesPlusSerializer(jobfiles, many=True)
       return Response(serializer.data)

    elif request.method == 'POST':
        try:
            job_caller = Job.objects.get(pk=jobid)
        except Job.DoesNotExist:
            return Response("No job with id " + str(jobid), status=404)
        if job_caller.status == "done":
            return Response("Jobs has already been done", status=400)

        job_caller.status = "file_updating"

        # If we send features
        fname = "packet.json"
        fpath = "" + fname
        with open(fpath, 'w') as jsonpacket:
            json.dump(request.data, jsonpacket)

        with open(fpath, 'rb') as f:
            fdata = InMemoryUploadedFile(f, 'file', fname, None, os.path.getsize(fpath), None)
            file_serializer = FileSerializer(data={'file': fdata})
            if file_serializer.is_valid():
                file_serializer.save()
                fid = file_serializer.data.get('id', None)
                input_type = "packet_features"
            else:
                return Response(file_serializer.errors, status=400)
        f.close() 
        #os.remove(fpath)

        data = {"file": fid, "job": jobid, "type": input_type}
        JobFiles_serializer = JobFilesSerializer(data=data)
        if JobFiles_serializer.is_valid():
            JobFiles_serializer.save()
        else:
            return Response(JobFiles_serializer.errors, status=400)

        job_caller.save()
        return Response(file_serializer.data, status=201)


@api_view(['GET', 'DELETE'])
@renderer_classes([JSONRenderer, DIVARenderer])
def FileAccessView(request, fid, format=None, jobid=None,):
    """
    Retrieve or delete a specific file.
    """
    try:
        my_file = File.objects.get(pk=fid)
        if(jobid):
            try:
                JobFiles.objects.get(job=jobid, file=fid)
            except Exception:
                return Response("No file with id " + str(fid) + " in job " + str(jobid), status=404)
    except File.DoesNotExist:
        return Response("No file with id " + str(fid), status=404)

    if request.method == 'GET':
        accept = ""
        if request.META.get('HTTP_ACCEPT'):
            accept = request.META.get('HTTP_ACCEPT')
        if "application/json" in accept or format == "json":
            serializer = FileSerializer(my_file)
            return Response(serializer.data, status=200)
        else:
            file_handle = my_file.file.open()
            response = FileResponse(file_handle, status=200)
            response['Content-Length'] = my_file.file.size
            response['Content-Disposition'] = 'attachment; filename="%s"' % my_file.file.name
            return response

    elif request.method == 'DELETE':
        try:
            default_storage.delete(str(my_file))
            my_file.delete()
        except Exception:
            return Response("File " + str(my_file) + " not deleted", status=404)
        return Response("File entry deleted", status=200)

