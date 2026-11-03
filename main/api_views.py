
from django.db.models import Q
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from main.models import Education
from main.serializers import EducationSerializer
from main.permissions import IsPortfolioOwnerOrEditorOrReadOnly


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
