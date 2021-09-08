from fileapp.models import File
from jobapp.models import JobFiles

def get_file_url(fid):
    return str(File.objects.get(id=fid))

def check_file(fid, jobid):
    try:
        JobFiles.objects.get(job=jobid, file=fid)
        return True, ""
    except Exception:
        return False, "No file with id " + str(fid) + " in job " + str(jobid)