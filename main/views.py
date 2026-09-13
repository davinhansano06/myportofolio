from django.shortcuts import render

from main.models import Experience, Education


def show_main(request):
    context = {
        "name": "Davin Tristan Hansano",
        "npm": "2506620513",
        "study_program": "S1 Information System",
        "bio": (
            "Mahasiswa Ilmu Komputer Universitas Indonesia yang tertarik "
            "pada pengembangan perangkat lunak dan pendidikan."
        ),
        "education_list": Education.objects.all(),
        "experience_list": Experience.objects.all(),
    }
    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "name": "Davin Tristan Hansano",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)

def show_education(request):
    context = {
        "name": "Davin Tristan Hansano",
        "education_list": Education.objects.all(),
    }
    return render(request, "education.html", context)