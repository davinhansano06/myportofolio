
from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsPortfolioOwnerOrEditorOrReadOnly(BasePermission):
    """
    Semua orang boleh membaca Education.
    Owner boleh melakukan semua perubahan.
    Editor hanya boleh melakukan PUT dan PATCH.
    """

    def has_permission(self, request, view):
        # GET, HEAD, OPTIONS boleh dilakukan siapa saja.
        if request.method in SAFE_METHODS:
            return True

        # Perubahan membutuhkan pengguna yang login.
        if not request.user.is_authenticated:
            return False

        # Owner memiliki akses penuh.
        if request.user.is_superuser:
            return True

        # Editor hanya boleh mengubah data.
        return (
            request.method in ("PUT", "PATCH")
            and request.user.groups.filter(name="Editor").exists()
        )
