from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from main.models import Experience, Education
from main.forms import EducationForm, ExperienceForm




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
    json_response = get_experience_json(request)

    experience_list = list(
        serializers.deserialize(
            "json",
            json_response.content.decode("utf-8")
        )
    )

    experience_list = [
        item.object for item in experience_list
    ]

    context = {
        "name": "Davin Tristan Hansano",
        "experience_list": experience_list,
    }

    return render(request, "experience.html", context)

def get_experience_json(request):
    experience = Experience.objects.all()

    experience_json = serializers.serialize(
        "json",
        experience
    )

    return HttpResponse(
        experience_json,
        content_type="application/json"
    )

def show_education(request):
    json_response = get_education_json(request)

    education_list = list(
        serializers.deserialize(
            "json",
            json_response.content.decode("utf-8")
        )
    )

    education_list = [item.object for item in education_list]

    context = {
        "name": "Davin Tristan Hansano",
        "education_list": education_list,
        "institution_query": request.GET.get("institution", ""),
    }

    return render(request, "education.html", context)

def get_education_json(request):
    institution_query = request.GET.get("institution", "")

    education = Education.objects.all()

    if institution_query:
        education = education.filter(
            institution__icontains=institution_query
        )

    education_json = serializers.serialize("json", education)

    return HttpResponse(
        education_json,
        content_type="application/json"
    )

def create_education(request):
    form = EducationForm(request.POST or None)

    if form.is_valid():
        form.save()
        messages.success(request, "Education berhasil ditambahkan!")
        return redirect("main:show_education")
    context = {
        "form": form,
        "name": "Davin Tristan Hansano",
    }

    return render(request, "create_education.html", context)

def create_experience(request):
    form = ExperienceForm(request.POST or None)

    if form.is_valid():
        form.save()
        messages.success(request, "Experience berhasil ditambahkan!")
        return redirect("main:show_experience")

    context = {
        "form": form,
        "name": "Davin Tristan Hansano",
    }

    return render(request, "create_experience.html", context)

def update_education(request, id):
    education = get_object_or_404(Education, id=id)

    form = EducationForm(
        request.POST or None,
        instance=education
    )

    if form.is_valid():
        form.save()
        messages.success(request, "Education berhasil diperbarui!")
        return redirect("main:show_education")

    context = {
        "form": form,
        "name": "Davin Tristan Hansano",
        "education": education,
    }

    return render(request, "update_education.html", context)

def update_experience(request, id):
    experience = get_object_or_404(Experience, id=id)

    form = ExperienceForm(
        request.POST or None,
        instance=experience
    )

    if form.is_valid():
        form.save()
        messages.success(request, "Experience berhasil diperbarui!")
        return redirect("main:show_experience")

    context = {
        "form": form,
        "name": "Davin Tristan Hansano",
        "experience": experience,
    }

    return render(request, "update_experience.html", context)

def delete_education(request, id):
    education = get_object_or_404(Education, id=id)
    education.delete()
    return redirect("main:show_education")

def delete_experience(request, id):
    experience = get_object_or_404(Experience, id=id)
    experience.delete()
    return redirect("main:show_experience")