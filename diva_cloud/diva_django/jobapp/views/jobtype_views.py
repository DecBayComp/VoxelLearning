from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from jobapp.serializers import JobTypeSerializer, JobTypeSerializerWithouNname
from jobapp.models import JobType

@api_view(['GET', 'POST'])
@renderer_classes([JSONRenderer])
def jobtype_list(request):
    """
    List all jobType, or create a new jobType.
    """
    if request.method == 'GET':
        jobtypes = JobType.objects.all()
        serializer = JobTypeSerializer(jobtypes, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = JobTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@api_view(['GET', 'PATCH', 'PUT', 'DELETE'])
@renderer_classes([JSONRenderer])
def jobtype_detail(request, name):
    """
    Retrieve, update or delete a jobType.
    """
    try:
        jobtype = JobType.objects.get(pk=name)
    except JobType.DoesNotExist:
        return Response(status=404)

    if request.method == 'GET':
        serializer = JobTypeSerializer(jobtype)
        return Response(serializer.data)
    elif request.method in ['PATCH', 'PUT']:
        serializer = JobTypeSerializerWithouNname(jobtype, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    elif request.method == 'DELETE':
        jobtype.delete()
        return Response(status=204)
    else:
        return

