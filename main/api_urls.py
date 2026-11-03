
from django.urls import path

from main.api_views import (
    EducationListCreateAPIView,
    EducationDetailAPIView,
    EducationStarAPIView,
)

app_name = "api"

urlpatterns = [
    # Daftar dan tambah Education
    path(
        "educations/",
        EducationListCreateAPIView.as_view(),
        name="education_list_create",
    ),

    # Detail, ubah, dan hapus Education
    path(
        "educations/<uuid:pk>/",
        EducationDetailAPIView.as_view(),
        name="education_detail",
    ),

    # Star dan unstar Education
    path(
        "educations/<uuid:pk>/star/",
        EducationStarAPIView.as_view(),
        name="education_star",
    ),
]
