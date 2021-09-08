from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import JSONField
# import time


def repository_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/<filename>
    return 'files/{0}'.format(filename)


class File(models.Model):
    id = models.AutoField(primary_key=True)
    file = models.FileField(blank=False, null=False, upload_to=repository_path)

    def __str__(self):
        return self.file.name

    def path(self):
        return settings.MEDIA_ROOT + "/" + self.file.name

    def assoc_array(self):
        return {str(self.id): self.path()}


class File_classifier(models.Model):
    id = models.AutoField(primary_key=True)
    fid = models.ForeignKey(File, on_delete=models.CASCADE)


class Transfer_function(models.Model):
    id = models.AutoField(primary_key=True)
    content = JSONField(default=dict)