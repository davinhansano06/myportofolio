from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from main.models import Experience, Education
from main.forms import EducationForm, ExperienceForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
import datetime



def show_main(request):
    last_login = request.COOKIES.get(
        "last_login",
        "Belum ada sesi login / Cookie tidak ditemukan"
    )
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

def register(request):
    form = UserCreationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Akun berhasil dibuat. Silakan login.")
        return redirect("main:login")

    context = {
        "name": "Davin Tristan Hansano",
        "form": form,
    }

    return render(request, "register.html", context)


def login_user(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)

        response = redirect("main:show_main")

        response.set_cookie(
            "last_login",
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )

        return response

    context = {
        "name": "Davin Tristan Hansano",
        "form": form,
    }

    return render(request, "login.html", context)


def logout_user(request):
    logout(request)

    response = redirect("main:show_main")
    response.delete_cookie("last_login")

    return response

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

@login_required
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

@login_required
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

@login_required
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

@login_required
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

@login_required
def delete_education(request, id):
    education = get_object_or_404(Education, id=id)
    education.delete()
    return redirect("main:show_education")

@login_required
def delete_experience(request, id):
    experience = get_object_or_404(Experience, id=id)
    experience.delete()
    return redirect("main:show_experience")

def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Akun berhasil dibuat!")
            return redirect("main:login")

    context = {
        "form": form,
        "name": "Davin Tristan Hansano",
    }

    return render(request, "register.html", context)