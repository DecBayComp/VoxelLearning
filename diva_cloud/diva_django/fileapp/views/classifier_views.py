from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from fileapp.renderer import DIVARenderer
from fileapp.serializers import FileClassifierSerializer
from fileapp.models import File_classifier
from rest_framework.response import Response
from django.http import FileResponse


@api_view(['GET', 'POST'])
def classifierView(request):
    if request.method == 'GET':
        files = File_classifier.objects.all()
        serializer = FileClassifierSerializer(files, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        file_id = request.data.get('fid')
        if not file_id:
            return Response("No file with id " + str(file_id), status=404)
        file_serializer = FileClassifierSerializer(data={"fid": file_id})
        if file_serializer.is_valid():
            file_serializer.save()
        else:
            return Response(file_serializer.errors, status=400)

        return Response(file_serializer.data, status=201)


@api_view(['GET', 'DELETE'])
@renderer_classes([JSONRenderer, DIVARenderer])
def classifier_detailView(request, id, format=None):
    try:
        my_file = File_classifier.objects.get(pk=id)
    except File_classifier.DoesNotExist:
        return Response("No classifier file with id " + str(id), status=404)

    if request.method == 'GET':
        accept = ""
        if request.META.get('HTTP_ACCEPT'):
            accept = request.META.get('HTTP_ACCEPT')
        if "application/json" in accept or format == "json":
            serializer = FileClassifierSerializer(my_file)
            return Response(serializer.data, status=200)
        else:
            file_handle = my_file.fid.file.open()
            response = FileResponse(file_handle, status=200)
            response['Content-Length'] = my_file.fid.file.size
            response['Content-Disposition'] = 'attachment; filename="%s"' % my_file.fid.file.name
            return response

    elif request.method == 'DELETE':
        default_storage.delete(str(my_file))
        my_file.delete()
        return Response("Classifier file deleted", status=204)
