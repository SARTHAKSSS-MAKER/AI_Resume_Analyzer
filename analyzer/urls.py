from django.urls import path
from . import views

urlpatterns = [
    path(
        '',
        views.home,
        name='home'
    ),

    path(
        'upload/',
        views.upload_resume,
        name='upload'
    ),

    path(
        'download-report/',
        views.download_report,
        name='download_report'
    ),
]