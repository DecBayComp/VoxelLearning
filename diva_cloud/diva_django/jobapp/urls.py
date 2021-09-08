from django.urls import path
from jobapp.views import jobtype_views, job_views

urlpatterns = [
    path('jobs/', job_views.job_list),
    path('jobs/<int:jobid>', job_views.job_detail),
    path('learning/<int:jobid>', job_views.job_detail),
    path('jobtype/', jobtype_views.jobtype_list),
    path('jobtype/<str:name>', jobtype_views.jobtype_detail),
    path('train/', job_views.train_list),
    path('infer/', job_views.infer_list),

]
