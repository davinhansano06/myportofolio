
from django.utils.html import strip_tags
from rest_framework import serializers

from main.models import Education, Experience, ContactMessage


class EducationSerializer(serializers.ModelSerializer):
    star_count = serializers.SerializerMethodField()
    is_starred = serializers.SerializerMethodField()
    starred_by_names = serializers.SerializerMethodField()

    class Meta:
        model = Education
        fields = [
            "id",
            "institution",
            "degree",
            "period",
            "location",
            "skills",
            "is_current",
            "logo",
            "star_count",
            "is_starred",
            "starred_by_names",
        ]
        read_only_fields = [
            "id",
            "star_count",
            "is_starred",
            "starred_by_names",
        ]

    def validate_institution(self, value):
        value = strip_tags(value).strip()
        if not value:
            raise serializers.ValidationError(
                "Institution cannot be empty."
            )
        return value

    def validate_degree(self, value):
        return strip_tags(value).strip()

    def validate_period(self, value):
        return strip_tags(value).strip()

    def validate_location(self, value):
        return strip_tags(value).strip()

    def validate_skills(self, value):
        return strip_tags(value).strip()

    def validate_logo(self, value):
        return strip_tags(value).strip()

    def get_star_count(self, obj):
        return obj.starred_by.count()

    def get_is_starred(self, obj):
        request = self.context.get("request")

        if request is None or not request.user.is_authenticated:
            return False

        return obj.starred_by.filter(
            id=request.user.id
        ).exists()

    def get_starred_by_names(self, obj):
        return ", ".join(
            user.username for user in obj.starred_by.all()
        )


class ExperienceSerializer(serializers.ModelSerializer):
    star_count = serializers.SerializerMethodField()
    is_starred = serializers.SerializerMethodField()

    class Meta:
        model = Experience
        fields = [
            "id",
            "title",
            "institution",
            "period",
            "description",
            "image",
            "star_count",
            "is_starred",
        ]
        read_only_fields = [
            "id",
            "star_count",
            "is_starred",
        ]

    def validate_title(self, value):
        value = strip_tags(value).strip()
        if not value:
            raise serializers.ValidationError(
                "Title cannot be empty."
            )
        return value

    def validate_institution(self, value):
        return strip_tags(value).strip()

    def validate_period(self, value):
        return strip_tags(value).strip()

    def validate_description(self, value):
        value = strip_tags(value).strip()
        if not value:
            raise serializers.ValidationError(
                "Description cannot be empty."
            )
        return value

    def validate_image(self, value):
        return strip_tags(value).strip()

    def get_star_count(self, obj):
        return obj.starred_by.count()

    def get_is_starred(self, obj):
        request = self.context.get("request")

        if request is None or not request.user.is_authenticated:
            return False

        return obj.starred_by.filter(
            id=request.user.id
        ).exists()


class ContactMessageSerializer(serializers.ModelSerializer):
    created_at_display = serializers.SerializerMethodField()

    class Meta:
        model = ContactMessage
        fields = [
            "id",
            "sender_name",
            "sender_org",
            "sender_contact",
            "topic",
            "message",
            "is_read",
            "created_at",
            "created_at_display",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "created_at_display",
        ]

    def validate_sender_name(self, value):
        value = strip_tags(value).strip()
        if not value:
            raise serializers.ValidationError("Nama tidak boleh kosong.")
        return value

    def validate_sender_org(self, value):
        return strip_tags(value or "").strip()

    def validate_sender_contact(self, value):
        value = strip_tags(value).strip()
        if not value:
            raise serializers.ValidationError(
                "Kontak (WhatsApp / Email) tidak boleh kosong."
            )
        return value

    def validate_topic(self, value):
        value = strip_tags(value or "Kolaborasi Proyek").strip()
        return value or "Kolaborasi Proyek"

    def validate_message(self, value):
        value = strip_tags(value).strip()
        if not value:
            raise serializers.ValidationError("Pesan tidak boleh kosong.")
        return value

    def get_created_at_display(self, obj):
        if not obj.created_at:
            return ""
        return obj.created_at.strftime("%d %b %Y · %H:%M")

