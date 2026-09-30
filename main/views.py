from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse,JsonResponse
from main.models import Experience, Education
from main.forms import EducationForm, ExperienceForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.core.exceptions import PermissionDenied
from django.views.decorators.http import require_POST
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
        "last_login": last_login,
        "education_list": Education.objects.all(),
        "experience_list": Experience.objects.all(),
        "form": ExperienceForm(),
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
    context = {
        "name": "Davin Tristan Hansano",
        "form": ExperienceForm(),
    }
    return render(request, "experience.html", context)

def get_experience_json(request):
    search_query = request.GET.get("title", "")

    experience_list = Experience.objects.prefetch_related(
        "starred_by"
    ).filter(
        title__icontains=search_query
    )
    data = []

    for experience in experience_list:
        starred_users = experience.starred_by.all()

        is_starred = (
            request.user in starred_users
            if request.user.is_authenticated
            else False
        )

        starred_by_names = ", ".join(
            [user.username for user in starred_users]
        )

        data.append({
            "pk": str(experience.id),
            "fields": {
                "title": experience.title,
                "institution": experience.institution,
                "period": experience.period,
                "description": experience.description,
                "image": experience.image,
                "star_count": starred_users.count(),
                "is_starred": is_starred,
                "starred_by_names": starred_by_names,
            }
        })

    return JsonResponse(data, safe=False)

def show_education(request):
    institution_query = request.GET.get("institution", "")

    education_list = Education.objects.all()

    if institution_query:
        education_list = education_list.filter(
            institution__icontains=institution_query
        )

    context = {
        "name": "Davin Tristan Hansano",
        "education_list": education_list,
        "institution_query": institution_query,
        "form": EducationForm(),
    }

    return render(request, "education.html", context)

def get_education_json(request):
    institution_query = request.GET.get("institution", "")

    education_list = Education.objects.prefetch_related(
        "starred_by"
    )

    if institution_query:
        education_list = education_list.filter(
            institution__icontains=institution_query
        )

    data = []

    for education in education_list:
        starred_users = education.starred_by.all()

        is_starred = (
            request.user in starred_users
            if request.user.is_authenticated
            else False
        )

        data.append({
            "pk": str(education.id),
            "fields": {
                "institution": education.institution,
                "degree": education.degree,
                "period": education.period,
                "location": education.location,
                "skills": education.skills,
                "is_current": education.is_current,
                "logo": education.logo,
                "star_count": starred_users.count(),
                "is_starred": is_starred,
            }
        })

    return JsonResponse(data, safe=False)

def is_editor(user):
    return user.groups.filter(name="Editor").exists()

@login_required
def create_education(request):
    if not request.user.is_superuser:
        raise PermissionDenied

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

@require_POST
def create_education_ajax(request):
    if not request.user.is_superuser:
        return JsonResponse(
            {
                "message": "Kamu tidak memiliki izin untuk menambahkan education."
            },
            status=403,
        )

    form = EducationForm(request.POST)

    if form.is_valid():
        education = form.save()

        return JsonResponse(
            {
                "message": "Education berhasil ditambahkan!",
                "pk": str(education.id),
            },
            status=201,
        )

    errors = {}

    for field, field_errors in form.errors.items():
        errors[field] = [
            {"message": error}
            for error in field_errors
        ]

    return JsonResponse(
        {
            "errors": errors
        },
        status=400,
    )

@login_required
def create_experience(request):
    if not request.user.is_superuser:
        raise PermissionDenied
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
    if not request.user.is_superuser and not is_editor(request.user):
        raise PermissionDenied

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
    if not request.user.is_superuser and not is_editor(request.user):
        raise PermissionDenied
    
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
    if not request.user.is_superuser:
        raise PermissionDenied
    education = get_object_or_404(Education, id=id)
    education.delete()
    return redirect("main:show_education")

@login_required
def delete_experience(request, id):
    if not request.user.is_superuser:
        raise PermissionDenied
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

@login_required
@require_POST
def toggle_star(request, model, id):
    if model == "education":
        item = get_object_or_404(Education, id=id)
    elif model == "experience":
        item = get_object_or_404(Experience, id=id)
    else:
        raise PermissionDenied

    if request.user in item.starred_by.all():
        item.starred_by.remove(request.user)
    else:
        item.starred_by.add(request.user)

    return redirect(request.META.get("HTTP_REFERER", "/"))


@require_POST
def create_experience_ajax(request):
    if not request.user.is_superuser:
        return JsonResponse(
            {
                "message": "Kamu tidak memiliki izin untuk menambahkan experience."
            },
            status=403,
        )

    form = ExperienceForm(request.POST)

    if form.is_valid():
        experience = form.save()

        return JsonResponse(
            {
                "message": "Experience berhasil ditambahkan!",
                "pk": str(experience.id),
            },
            status=201,
        )

    errors = {}

    for field, field_errors in form.errors.items():
        errors[field] = [
            {"message": error}
            for error in field_errors
        ]

    return JsonResponse(
        {
            "errors": errors
        },
        status=400,
    )