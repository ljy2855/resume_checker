from django.urls import path
from . import views

urlpatterns = [
    path("", views.submit_resume, name="submit_resume"),
    path("resume/<int:resume_id>/", views.view_resume, name="view_resume"),
    path("evaluate/<int:resume_id>", views.evaluate_resume, name="evaluate_resume"),
]
