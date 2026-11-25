
from django.db.models import Q
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from main.models import Education, Experience, ContactMessage
from main.serializers import (
    EducationSerializer,
    ExperienceSerializer,
    ContactMessageSerializer,
)
from main.permissions import IsPortfolioOwnerOrEditorOrReadOnly

from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
)
from rest_framework.authentication import SessionAuthentication
from main.models import Experience
from main.serializers import ExperienceSerializer

class EducationListCreateAPIView(APIView):
    permission_classes = [IsPortfolioOwnerOrEditorOrReadOnly]

    def get(self, request):
        educations = Education.objects.prefetch_related("starred_by").all()

        # Search menggunakan parameter ?q=
        query = request.GET.get("q", "").strip()

        if query:
            educations = educations.filter(
                Q(institution__icontains=query)
                | Q(degree__icontains=query)
                | Q(location__icontains=query)
                | Q(skills__icontains=query)
            )

        serializer = EducationSerializer(
            educations,
            many=True,
            context={"request": request}
        )

        return Response(serializer.data)

    def post(self, request):
        serializer = EducationSerializer(
            data=request.data,
            context={"request": request}
        )

        if serializer.is_valid():
            education = serializer.save()

            return Response(
                EducationSerializer(
                    education,
                    context={"request": request}
                ).data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class EducationDetailAPIView(APIView):
    permission_classes = [IsPortfolioOwnerOrEditorOrReadOnly]

    def get_object(self, pk):
        return get_object_or_404(
            Education.objects.prefetch_related("starred_by"),
            pk=pk
        )

    def get(self, request, pk):
        education = self.get_object(pk)

        serializer = EducationSerializer(
            education,
            context={"request": request}
        )

        return Response(serializer.data)

    def put(self, request, pk):
        education = self.get_object(pk)

        serializer = EducationSerializer(
            education,
            data=request.data,
            context={"request": request}
        )

        if serializer.is_valid():
            education = serializer.save()

            return Response(
                EducationSerializer(
                    education,
                    context={"request": request}
                ).data
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def patch(self, request, pk):
        education = self.get_object(pk)

        serializer = EducationSerializer(
            education,
            data=request.data,
            partial=True,
            context={"request": request}
        )

        if serializer.is_valid():
            education = serializer.save()

            return Response(
                EducationSerializer(
                    education,
                    context={"request": request}
                ).data
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, pk):
        education = self.get_object(pk)
        education.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class EducationStarAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        education = get_object_or_404(Education, pk=pk)

        if education.starred_by.filter(id=request.user.id).exists():
            education.starred_by.remove(request.user)
            is_starred = False
        else:
            education.starred_by.add(request.user)
            is_starred = True

        return Response({
            "is_starred": is_starred,
            "star_count": education.starred_by.count()
        })


@api_view(["GET", "POST"])
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
def experience_list_create(request):
    """
    GET: Menampilkan dan mencari Experience.
    POST: Membuat Experience (Owner only).
    """

    if request.method == "GET":
        experiences = Experience.objects.prefetch_related(
            "starred_by"
        ).all()

        query = request.query_params.get("q", "").strip()

        if query:
            experiences = experiences.filter(
                Q(title__icontains=query)
                | Q(institution__icontains=query)
                | Q(period__icontains=query)
                | Q(description__icontains=query)
            )

        serializer = ExperienceSerializer(
            experiences,
            many=True,
            context={"request": request}
        )

        return Response(serializer.data)

    serializer = ExperienceSerializer(
        data=request.data,
        context={"request": request}
    )

    if serializer.is_valid():
        experience = serializer.save()

        return Response(
            ExperienceSerializer(
                experience,
                context={"request": request}
            ).data,
            status=status.HTTP_201_CREATED
        )

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(["GET", "PUT", "PATCH", "DELETE"])
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
def experience_detail(request, pk):
    """
    GET: Detail Experience.
    PUT/PATCH: Mengubah Experience.
    DELETE: Menghapus Experience (Owner only).
    """

    experience = get_object_or_404(
        Experience.objects.prefetch_related("starred_by"),
        pk=pk
    )

    if request.method == "GET":
        serializer = ExperienceSerializer(
            experience,
            context={"request": request}
        )
        return Response(serializer.data)

    if request.method in ["PUT", "PATCH"]:
        serializer = ExperienceSerializer(
            experience,
            data=request.data,
            partial=request.method == "PATCH",
            context={"request": request}
        )

        if serializer.is_valid():
            experience = serializer.save()

            return Response(
                ExperienceSerializer(
                    experience,
                    context={"request": request}
                ).data
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    experience.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def experience_star(request, pk):
    """
    Toggle star Experience untuk pengguna yang login.
    """

    experience = get_object_or_404(
        Experience.objects.prefetch_related("starred_by"),
        pk=pk
    )

    if experience.starred_by.filter(
        id=request.user.id
    ).exists():
        experience.starred_by.remove(request.user)
        is_starred = False
    else:
        experience.starred_by.add(request.user)
        is_starred = True

    return Response({
        "is_starred": is_starred,
        "star_count": experience.starred_by.count()
    })


class ContactMessageListCreateAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        if not (request.user and request.user.is_authenticated and request.user.is_superuser):
            return Response(
                {"detail": "Hanya Owner portofolio yang dapat melihat inbox pesan."},
                status=status.HTTP_403_FORBIDDEN,
            )

        messages = ContactMessage.objects.all()
        serializer = ContactMessageSerializer(messages, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ContactMessageSerializer(data=request.data)
        if serializer.is_valid():
            msg = serializer.save()
            return Response(
                ContactMessageSerializer(msg).data,
                status=status.HTTP_201_CREATED,
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )


class ContactMessageDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def _check_owner(self, request):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.is_superuser
        )

    def patch(self, request, pk):
        if not self._check_owner(request):
            return Response(
                {"detail": "Hanya Owner portofolio yang dapat mengubah status pesan."},
                status=status.HTTP_403_FORBIDDEN,
            )
        msg = get_object_or_404(ContactMessage, pk=pk)
        serializer = ContactMessageSerializer(
            msg, data=request.data, partial=True
        )
        if serializer.is_valid():
            msg = serializer.save()
            return Response(ContactMessageSerializer(msg).data)
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, pk):
        if not self._check_owner(request):
            return Response(
                {"detail": "Hanya Owner portofolio yang dapat menghapus pesan."},
                status=status.HTTP_403_FORBIDDEN,
            )
        msg = get_object_or_404(ContactMessage, pk=pk)
        msg.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def api_logout(request):
    if request.auth is not None:
        request.auth.delete()

    return Response(status=status.HTTP_204_NO_CONTENT)