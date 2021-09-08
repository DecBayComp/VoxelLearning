from jobapp.jobs.common import check_file, get_file_url
from django.conf import settings
from jobapp.serializers import JobSerializer
from fileapp.serializers import Serialize_a_File
from rest_framework.response import Response

import os
import pickle

from diva_python_scripts.train import combining_classifiers

class Train():

    # Job type: train
    # Description: Train a classifier from features of tags of a precise object on a 3D image (it can also take in input a previously made classifier)
    # Inputs:
    #   - features : 1 file | id (integer) | [Required] | key = features
    #   - classifier: 1 file | id (integer) | [Optionnal] | key = classifier_in
    # Parameters:
    #   - strength : integer | [Optionnal] default : 5 | key = strength
    # Outputs:
    #   - classifier | key = classifier_out

    features_fileid = False
    features_url = ""
    features_key = "features"

    classifier_input_fileid = False
    classifier_input_url = ""
    classifier_input_key = "classifier_in"

    strength = 5
    strength_key = "strength"

    classifier_output_url = ""
    classifier_output_key = "classifier_out"

    def job_launcher(self, jobid, inputs_dict, parameters_dict, jobtype, myjob):

        # Get inputs id
        try:
            self.features_fileid = inputs_dict[self.features_key][0]
        except Exception:
            return Response("No " + self.features_key + " in job " + str(jobid), status=404)

        try:
            self.classifier_input_fileid = inputs_dict[self.classifier_input_key][0]
        except Exception: 
            print("No input classifier")  # (optionnal input)

        # Get parameters
        try:
            self.strength = parameters_dict[self.strength_key]
        except Exception: 
            print("No strength parameter, default 5")  # (optionnal parameter)

        # Check file existence in db:
        finded, notfinded = check_file(self.features_fileid, jobid)
        if not finded:
            return notfinded
        else:
            self.features_url = os.path.join(settings.MEDIA_ROOT, get_file_url(self.features_fileid))

        if self.classifier_input_fileid:
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
        self.classifier_output_url = self.launch()

        # Serialize output files and link to the job
        if not self.classifier_output_url:
            if serializer.is_valid():
                serializer.save(status="error")
            return "Problem in job: " + str(jobid)
        else:
            fpath = settings.BASE_DIR + self.classifier_output_url
            fid, error = Serialize_a_File(fpath, self.classifier_output_key, self.classifier_output_key, jobid)
            if error:
                return error

        # Serialize the Jobwith "done" status
        if serializer.is_valid():
            serializer.save(status="done")
            return None
        return serializer.errors

    def launch(self):

        classification_strength = int(self.strength)
        temp_filename = "files/classifier.pckl"

        # diva-python # diva-python # diva-python # diva-python # diva-python # diva-python # diva-python #
        glob_class = combining_classifiers(self.features_url, self.classifier_input_url, classification_strength)
        glob_class.__prepare_data_for_training__()
        glob_class.__apply_multiple_classifier_to_features__()
        glob_class.__apply_main_classifier__()
        pickle.dump(glob_class.liste_learner, open(settings.MEDIA_ROOT + "/" + temp_filename, 'wb'))
        # diva-python # diva-python # diva-python # diva-python # diva-python # diva-python # diva-python #

        output = settings.MEDIA_URL + temp_filename
        return output