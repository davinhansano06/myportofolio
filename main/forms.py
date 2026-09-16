from django.forms import ModelForm, TextInput
from main.models import Education


class EducationForm(ModelForm):
    class Meta:
        model = Education
        fields = [
            "institution",
            "degree",
            "period",
            "location",
            "skills",
            "logo",
        ]

        labels = {
            "institution": "Nama Institusi",
            "degree": "Jenjang Pendidikan",
            "period": "Periode",
            "location": "Lokasi",
            "skills": "Skills",
            "logo": "Logo",
        }

        widgets = {
            "institution": TextInput(
                attrs={
                    "placeholder": "Universitas Indonesia",
                    "maxlength": 255,
                }
            ),
            "degree": TextInput(
                attrs={
                    "placeholder": "Undergraduate Student · Computer Science Major",
                    "maxlength": 255,
                }
            ),
            "period": TextInput(
                attrs={
                    "placeholder": "July 2025 - Juni 2029 · On Going",
                    "maxlength": 100,
                }
            ),
            "location": TextInput(
                attrs={
                    "placeholder": "Depok, West Java, Indonesia",
                    "maxlength": 255,
                }
            ),
            "skills": TextInput(
                attrs={
                    "placeholder": "Business Analysis, Computer Sciences & Data Analysis",
                    "maxlength": 255,
                }
            ),
            "logo": TextInput(
                attrs={
                    "placeholder": "img/uiputih.png",
                    "maxlength": 255,
                }
            ),
        }