from rest_framework.decorators import api_view
from fileapp.serializers import TransferFunctionSerializer
from fileapp.models import Transfer_function
from rest_framework.response import Response
import json

@api_view(['GET', 'POST'])
def transferView(request):
    if request.method == 'GET':
        files = Transfer_function.objects.all()
        serializer = TransferFunctionSerializer(files, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':

        # if request.data.get('id'):
        #     file_id = request.data.get('id')
        #     my_file = JSON_fntransfer.objects.get(id=file_id)
        #     if not my_file:
        #         return Response("No file with id " + str(file_id), status=404)
        #     file_serializer = TransferFunctionSerializer(data={'file': my_file.file})
        # elif request.data.get('file'):
        file = request.data['file']
        my_json = file.read()
        my_json = my_json.decode('utf8').replace("'", '"')
        data = {}
        data['content'] = json.loads(my_json)
        json_serializer = TransferFunctionSerializer(data=data)
        # else:
        #     return Response("Missing a file or a file id to your request", status=404)

        if json_serializer.is_valid():
            json_serializer.save()
        else:
            return Response(json_serializer.errors, status=400)
        return Response(json_serializer.data, status=201)


@api_view(['GET', 'DELETE'])
def transfer_detailView(request, fid, format=None):
    try:
        my_json = Transfer_function.objects.get(pk=fid)
    except Transfer_function.DoesNotExist:
        return Response("No transfer function file with id " + str(fid), status=404)

    if request.method == 'GET':
        accept = ""
        if request.META.get('HTTP_ACCEPT'):
            accept = request.META.get('HTTP_ACCEPT')
        if "application/json" in accept or format == "json":
            serializer = TransferFunctionSerializer(my_json)
            return Response(serializer.data['content'], status=200)
        else:
            serializer = TransferFunctionSerializer(my_json)
            return Response(serializer.data, status=200)

    elif request.method == 'DELETE':
        default_storage.delete(str(my_file))
        my_file.delete()
        return Response("Transfer function file deleted", status=204)
