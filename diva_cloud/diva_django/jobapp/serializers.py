from rest_framework import serializers
from .models import Job, JobType, JobFiles
from fileapp.models import File


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ('id', 'status', 'type')
        read_only_fields = ('id', 'status', 'taskid')
        extra_kwargs = {
            'security_question': {'write_only': True},
            'security_question_answer': {'write_only': True},
            'password': {'write_only': True}
        }


# Serialize only for job initialization. To return aslo the taskid when we create a new job
class JobNewSerializer(serializers.ModelSerializer):  
    class Meta:
        model = Job
        fields = "__all__"
        read_only_fields = ('id', 'status')
        extra_kwargs = {
            'security_question': {'write_only': True},
            'security_question_answer': {'write_only': True},
            'password': {'write_only': True}
        }


class JobTrainSerializer(serializers.ModelSerializer):  # useless?
    class Meta:
        model = Job
        fields = ('id', 'status')
        read_only_fields = ('id', 'status')
        extra_kwargs = {
            'security_question': {'write_only': True},
            'security_question_answer': {'write_only': True},
            'password': {'write_only': True}
        }


class JobTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobType
        fields = "__all__"


class JobTypeSerializerWithouNname(serializers.ModelSerializer):
    class Meta:
        model = JobType
        fields = "__all__"
        read_only_fields = ('name',)


class JobFilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobFiles
        fields = "__all__"
        read_only_fields = ('id',)


class FilelinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ('id', 'file',)


class JobFilesPlusSerializer(serializers.ModelSerializer):
    file = FilelinkSerializer()

    class Meta:
        model = JobFiles
        fields = ('file', "type")
