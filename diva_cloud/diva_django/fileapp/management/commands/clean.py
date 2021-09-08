from diva_cloud import settings
from django.core.management.base import BaseCommand, CommandError
from jobapp.models import JobFiles
from fileapp.models import File
import glob
import os.path
from os import path


class Command(BaseCommand):
    help = 'Clean all file entry with non existing files'

    def add_arguments(self, parser):
        parser.add_argument('-p', '--print', type=int, help='Verbose (0 or 1)')
        #parser.add_argument('-c', '--confirm', type=str, help='Confirm to delete (y or n')

    def handle(self, *args, **options):
        print("____________________\n")
        action.delete_file_entry(options['print'])
        print("____________________\n")
        action.delete_file_in_filesystem(options['print'])
        print("____________________\n")




class action():

    def delete_file_entry(verbose):
        print("Deleting File entry with file not found on filesystem")
        deleted = 0
        files = File.objects.all()
        for f in files:
            exist = path.exists(f.path())
            if (verbose == 1):
                if(exist):
                    print("[V] " + f.path())
                if(not exist):
                    print("[X] " + f.path())
            if(not exist):
                File.objects.filter(id=f.id).delete()
                JobFiles.objects.filter(file=f.id).delete()
                deleted+=1
                print("\t[/!\\] Deleted file n°" + str(f.id) + " (" + str(f.file) + " not found).")
        print("\n" + str(deleted) + "/" + str(len(files)) +" file(s) deleted.")



    def delete_file_in_filesystem(verbose):
        print("Deleting files on fylesystem not found on file database")
        deleted = 0
        files_in_dir = glob.glob(os.path.join(settings.MEDIA_ROOT, settings.FILES_URL) + "*")
        for f_in_dir in files_in_dir:
            path = settings.FILES_URL + os.path.basename(f_in_dir)
            try: 
                filesfound=File.objects.get(file=path)
                if (verbose == 1):
                    print("[V] " + f_in_dir)
            except File.DoesNotExist:
                os.remove(f_in_dir)
                if (verbose == 1):
                    print("[X] " + f_in_dir)
                print("\t[/!\\] Deleted file " + os.path.basename(f_in_dir) + " (not found in database).")
                deleted+=1
        print("\n" + str(deleted) + "/" + str(len(files_in_dir)) +" file(s) deleted.")
