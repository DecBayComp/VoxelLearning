from rest_framework import serializers
from .models import File, File_classifier, Transfer_function
from jobapp.serializers import JobFilesSerializer
from django.core.files.uploadedfile import InMemoryUploadedFile
import os
from jobapp.models import JobFiles


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = "__all__"


class FileClassifierSerializer(serializers.ModelSerializer):
    class Meta:
        model = File_classifier
        fields = "__all__"


class TransferFunctionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transfer_function
        fields = "__all__"


def Serialize_a_File(fpath, fname, ftype, jobid):
    with open(fpath, 'rb') as f:
        fdata = InMemoryUploadedFile(
            f, 'file', fname, None, os.path.getsize(fpath), None)
        file_serializer = FileSerializer(data={'file': fdata})
        if file_serializer.is_valid():
            file_serializer.save()
            if ftype in ["output", "classifier_out"]:  # Try to serialize a file without copying it and deleting source
                os.remove(fpath)
            fid = str(file_serializer.data.get('id', None))
            data = {"file": fid, "job": jobid, "type": ftype}
            JobFiles_serializer = JobFilesSerializer(data=data)
            if JobFiles_serializer.is_valid():
                JobFiles_serializer.save()
            else:
                return 0, JobFiles_serializer.errors
        else:
            return 0, file_serializer.errors

    f.close()
    return fid, False