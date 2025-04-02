from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # 자소서 작성자가 현재 로그인한 유저와 같은지 확인
        return obj.cover_letter.user == request.user
