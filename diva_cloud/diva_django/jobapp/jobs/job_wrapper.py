from jobapp.jobs.common import check_file, get_file_url
from django.conf import settings
from jobapp.serializers import JobSerializer
from fileapp.serializers import Serialize_a_File
from rest_framework.response import Response
import os

#################################### JOB WRAPPER #################################
#
# Copy and paste this file replacing "_wrapper" in the file name by the job name
#
# Replace all the <something> fields with job specifications
#
##################################################################################


from <import_job_sources>


class <name_of_job> ():

    # Job type: <name_of_job>
    # Description: <insert descritption>
    # Inputs:
    #   - <input1name> : 1 or X file | integer | [Required]/[Optionnal] | key = <fileTypeOfInput1>
    #   - <input2name>: 1 or X file | string | [Required]/[Optionnal] | key = <fileTypeOfInput2>
    # Parameters:
    #   - <parameter1name> : integer | [Required]/[Optionnal] default : x | key = <nameOfParameter1InDict>
    # Outputs:
    #   - <output1name> | key = <fileTypeOfOuyput1>

    <input1name>_id = False
    <input1name>_url = ""
    <input1name>_key = <fileTypeOfInput1>

    <input2name>_id = False
    <input2name>_url = ""
    <input2name>_key = <fileTypeOfInputZ>

    <parameter1name> = <defaultvalue>
    <parameter1name>_key = <nameOfParameter1InDict>

    <output1name>_url = ""
    <output1name>_key = <fileTypeOfOuyput1>

    def job_launcher(self, jobid, inputs_dict, parameters_dict, jobtype, myjob):

        # Get inputs id
        try:
            self.<input1name>_id = inputs_dict[self.<input1name>_key][0]
        except Exception:
            return Response("No " + self.<input1name>_key + " in job " + str(jobid), status=404)

        try:
            self.<input2name>_id = inputs_dict[self.<input2name>_key][0]
        except Exception: 
            print("No input <name_of_input>")  # (optionnal input)

        # Get parameters
        try:
            self.<parameter1name> = parameters_dict[self.<parameter1name>_key]
        except Exception: 
            print("No <name_of_parameter> parameter, default <default value>")  # (optionnal parameter)

        # Check file existence in db:
        finded, notfinded = check_file(self.<input1name>_id, jobid)
        if not finded:
            return notfinded
        else:
            self.features_url = os.path.join(settings.MEDIA_ROOT, get_file_url(self.<input1name>_id))

        if self.<input2name>_id:
            finded, notfinded = check_file(self.<input2name>_id, jobid)
            if not finded:
                return notfinded
            else:
                self.<input2name>_url = os.path.join(settings.MEDIA_ROOT, get_file_url(self.<input2name>_id))

        # Set the type to the job in db
        serializer = JobSerializer(myjob, data={'type': jobtype})
        if not serializer.is_valid():
            return serializer.errors

        # Launch the job
        self.<output1name>_url = self.launch()

        # Serialize output files and link to the job
        if not self.<output1name>_url:
            if serializer.is_valid():
                serializer.save(status="error")
            return "Problem in job: " + str(jobid)
        else:
            fpath = settings.BASE_DIR + self.<output1name>_url
            fid, error = Serialize_a_File(fpath, self.<output1name>_key, self.<output1name>_key, jobid)
            if error:
                return error

        # Serialize the Job with "done" status
        if serializer.is_valid():
            serializer.save(status="done")
            return None
        return serializer.errors

    def launch(self):
        #CODE TO WRITE TO REALIZE YOUR JOB:
        <<EXEMPLE OF JOB:>>
        <classification_strength = int(self.<parameter1name>)>
        <temp_filename = "files/classifier.pckl">
        <glob_class = combining_classifiers(self.<input1name>_url, self.<input2name>_url, classification_strength)>
        <glob_class.__prepare_data_for_training__()>
        <glob_class.__apply_multiple_classifier_to_features__()>
        <glob_class.__apply_main_classifier__()>
        <pickle.dump(glob_class.liste_learner, open(settings.MEDIA_ROOT + "/" + temp_filename, 'wb'))>
        <output = settings.MEDIA_URL + temp_filename>
        <return output>