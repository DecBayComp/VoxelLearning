from jobapp.jobs.common import check_file, get_file_url
from django.conf import settings
from jobapp.serializers import JobSerializer
from fileapp.serializers import Serialize_a_File
from rest_framework.response import Response

import json
import os
import numpy as np
import pandas as pd
import base64

from diva_python_scripts.train import combining_classifiers

class Infer():

    # Job type: infer
    # Description: Infer on 3D image features from a classifier, return probabilities
    # Inputs:
    #   - packet_features : 1 file | id (integer) | [Required] | key = packet_features
    #   - classifier: 1 file | id (integer) | [Required] | key = classifier_in
    # Parameters:
    #   - strength : integer | [Optionnal] default : 5 | key = strength
    # Outputs:
    #   - proba | key = proba

    packet_features_fileid = False
    packet_features_url = False
    packet_features_key = "packet_features"

    classifier_input_fileid = False
    classifier_input_url = False
    classifier_input_key = "classifier_in"

    strength = 5
    strength_key = "strength"

    proba_url = False
    proba_key = "proba_out"

    def job_launcher(self, jobid, inputs_dict, parameters_dict, jobtype, myjob):

        # Get inputs id
        try:
            self.packet_features_fileid = inputs_dict[self.packet_features_key][0]
        except Exception:
            return Response("No " + self.packet_features_key + " in job " + str(jobid), status=404)
        try:
            self.classifier_input_fileid = inputs_dict[self.classifier_input_key][0]
        except Exception:
            return Response("No " + self.classifier_input_key + " in job " + str(jobid), status=404)

        # Get parameters
        try:
            self.strength = parameters_dict[self.strength_key]
        except Exception: 
            print("No strength parameter, default 5")  # (optionnal parameter)

        # Check file existence in db
        finded, notfinded = check_file(self.packet_features_fileid, jobid)
        if not finded:
            return notfinded
        else:
            self.packet_features_url = os.path.join(settings.MEDIA_ROOT, get_file_url(self.packet_features_fileid))

        finded, notfinded = check_file(self.classifier_input_fileid, jobid)
        if not finded:
            return notfinded
        else:
            self.classifier_input_url = os.path.join(settings.MEDIA_ROOT, get_file_url(self.classifier_input_fileid))

        # Set the type to the job in db
        serializer = JobSerializer(myjob, data={'type': jobtype})
        if not serializer.is_valid():
            return serializer.errors

        # Launch the job
        self.proba_url = self.launch()

        # Serialize output files and link to the job
        if not self.proba_url:
            if serializer.is_valid():
                serializer.save(status="error")
            return "Problem in job: " + str(jobid)
        else:
            fpath = settings.BASE_DIR + self.proba_url
            fid, error = Serialize_a_File(fpath, self.proba_key, self.proba_key, jobid)
            if error:
                return error

        # Serialize the Jobwith "done" status
        if serializer.is_valid():
            serializer.save(status="done")
            return None
        return serializer.errors

    def launch(self):      # Add classifier output in parameters

        classification_strength = int(self.strength)
        temp_filename = "files/proba.bytes"

        input_features_file = os.path.join(settings.MEDIA_ROOT, self.packet_features_url)
        with open(input_features_file, "r") as file:
            json_data = json.load(file)

        image_features = {}

        for label_data, feature_data_str in json_data.items():
            feature_data_str_ascii = feature_data_str.encode("ascii")
            feature_data = base64.b64decode(feature_data_str_ascii)
            image_features[label_data] = np.frombuffer(feature_data, dtype=np.uint8).astype(np.float)

        # diva-python # diva-python # diva-python # diva-python # diva-python # diva-python # diva-python #
        glob_class = combining_classifiers(pd.DataFrame({str(label): image_features[label] for label in image_features}), self.classifier_input_url, classification_strength)
        glob_class.__prepare_data_for_inference__()
        proba = glob_class.__predict_proba__()
        proba = (1 - proba) * 255
        proba_uint8 = proba.astype(np.uint8)
        proba_uint8bytes = proba_uint8.tobytes()

        f = open(settings.MEDIA_ROOT + "/" + temp_filename, "wb")
        f.write(proba_uint8bytes)
        f.close()
        # diva-python # diva-python # diva-python # diva-python # diva-python # diva-python # diva-python #

        output = settings.MEDIA_URL + temp_filename
        return output