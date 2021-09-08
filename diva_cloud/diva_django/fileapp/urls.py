from django.urls import path
from fileapp.views import classifier_views, transfer_views, file_views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('jobs/<int:jobid>/files/', file_views.FileUploadView),
    path('train/<int:jobid>/files/', file_views.FileUploadView),
    path('jobs/<int:jobid>/files/<int:fid>', file_views.FileAccessView),
    path('train/<int:jobid>/files/<int:fid>', file_views.FileAccessView),
    path('files/', file_views.FilesView),
    path('files/<int:fid>', file_views.FileAccessView),
    path('classifier', classifier_views.classifierView),
    path('classifier/<int:id>', classifier_views.classifier_detailView),
    path('transfer', transfer_views.transferView),
    path('transfer/<int:fid>', transfer_views.transfer_detailView),
    path('jobs/<int:jobid>/features/', file_views.FeaturesUploadView),
]

urlpatterns = format_suffix_patterns(urlpatterns)
