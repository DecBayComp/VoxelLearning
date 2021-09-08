from django.conf import settings
from jobapp.models import Job

from rest_framework.response import Response
from jobapp.jobs.job_train import Train
from jobapp.jobs.job_infer import Infer 
#TO PARAMETER : from jobapp.jobs.job_<X> import <X>

class Jobstype:
    type_dict = {"train": "train", "infer": "infer"} #TO PARAMETER : {..., "<X>": <X>}

def job_launcher(jobid, inputs_dict, parameters_dict, jobtype): 
    job_objects = Job.objects.get(pk=jobid)
    if job_objects.status == "done":
        return "Jobs has already been done"

    job = ""
    if jobtype == Jobstype.type_dict["train"]:
        job = Train()
    elif jobtype == Jobstype.type_dict["infer"]:
        job = Infer()
    else:
        return Response("jobtype error", status=404)
	#elif jobtype == Jobstype.type_dict["<job>"]:
    #    job = <job>()

    return job.job_launcher(jobid, inputs_dict, parameters_dict, jobtype, job_objects)