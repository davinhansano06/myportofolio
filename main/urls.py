from django.urls import path
from main.views import (
    show_main,
    show_experience,
    show_education,
    create_education,
    update_education,
    delete_education,
    get_education_json,
    get_experience_json,
    create_experience,
    update_experience,
    delete_experience
)
app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("experience/", show_experience, name="show_experience"),
    path("education/", show_education, name="show_education"),
    path("education/create/", create_education, name="create_education"),
    path("education/delete/<uuid:id>/", delete_education, name="delete_education"),
    path("api/education/", get_education_json, name="get_education_json"),
    path("api/experience/", get_experience_json, name="get_experience_json"),
    path("education/update/<uuid:id>/", update_education, name="update_education"),
    path("experience/create/", create_experience, name="create_experience"),
    path("experience/update/<uuid:id>/", update_experience, name="update_experience"),
    path("experience/delete/<uuid:id>/", delete_experience, name="delete_experience"),
]