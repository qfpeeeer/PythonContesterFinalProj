from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from contester.models import Notification
from contester.serializers import NotificationSerializer


class NotificationView(APIView):

    def get(self, request):
        user = request.user
        notification = Notification.objects.filter(user_id=user.id)
        serializer = NotificationSerializer(notification, many=True)
        return Response({"notifications": serializer.data})

    def post(self, request):
        notification = request.data.get("notification")
        serializer = NotificationSerializer(notification, many=True)
        if serializer.is_valid(raise_exception=True):
            notification_saved = serializer.save()
            return Response({"success": "Notification '{}' created successfully".format(notification_saved.title)})

    def put(self, request, pk):
        saved_article = get_object_or_404(Notification.objects.all(), pk=pk)
        data = request.data.get('notification')
        serializer = NotificationSerializer(instance=saved_article, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            notification_saved = serializer.save()
            return Response({
                "success": "Notification '{}' updated successfully".format(notification_saved.title)
            })

    def delete(self, request):
        user = request.user
        notification = get_object_or_404(Notification.objects.all(), user_id=user.id)
        notification.delete()
        return Response({
            "message": "Notification with id {} has been deleted.".format(user.id)
        }, status=204)