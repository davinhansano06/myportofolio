from django.urls import path
from rest_framework.authtoken import views as authtoken_views

from main.api_views import (
    EducationListCreateAPIView,
    EducationDetailAPIView,
    EducationStarAPIView,
    experience_list_create,
    experience_detail,
    experience_star,
    ContactMessageListCreateAPIView,
    ContactMessageDetailAPIView,
    api_logout,
)

app_name = "api"

urlpatterns = [
    # Token Authentication
    path(
        "auth/token/",
        authtoken_views.obtain_auth_token,
        name="api_token_auth",
    ),
    path(
        "auth/logout/",
        api_logout,
        name="api_logout",
    ),
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
    
    # Experience API - IA6
    path(
        "experiences/",
        experience_list_create,
        name="experience_list_create",
    ),
    path(
        "experiences/<uuid:pk>/",
        experience_detail,
        name="experience_detail",
    ),
    path(
        "experiences/<uuid:pk>/star/",
        experience_star,
        name="experience_star",
    ),

    # Contact Inbox Messages API (DRF)
    path(
        "messages/",
        ContactMessageListCreateAPIView.as_view(),
        name="contact_message_list_create",
    ),
    path(
        "messages/<uuid:pk>/",
        ContactMessageDetailAPIView.as_view(),
        name="contact_message_detail",
    ),

]
