from rest_framework import generics, viewsets
from .models import MenuItem, Category
from rest_framework.response import Response
from rest_framework.decorators import api_view,renderer_classes,permission_classes, throttle_classes
from .serializers import MenuItemSerializer, CategorySerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from .throttles import TenCallsPerMinute
from django.shortcuts import get_object_or_404

from django.contrib.auth.models import User, Group

class CategoriesView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class MenuItemsView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    ordering_fields = ['price', 'inventory']
    filterset_fields = ['price', 'inventory']
    search_fields = ['title']


class MenuItemsViewSet(viewsets.ModelViewSet):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    
    def get_throttles(self):
        if self.action == 'create':
            throttle_classes = [UserRateThrottle]
        else:
            throttle_classes = []
        return [throttle() for throttle in throttle_classes]

# creating a protected api endpoint
@api_view()
@permission_classes([IsAuthenticated])
def secret(request):
    return Response({"message":"some secret message"})


@api_view(['POST'])
@permission_classes([IsAdminUser])
def managers(request):
    username = request.data['username']
    if username:
        user = get_object_or_404(User, username=username)
        managers = Group.objects.get(name="Manager")
        if request.method == 'POST':
            managers.user_set.add(user)
        elif request.method == 'DELETE':
            managers.user_set.remove(user)
        return Response({"message":"ok"})
    
    return Response({"message":"error"}, status.HTTP_400_BAD_REQUEST)

# # creating manager view
# @api_view()
# @permission_classes([IsAuthenticated])
# def manager_view(request):
#     if request.user.groups.filter(name='Manager').exists():
#         return Response({"message":"Only manager should see this"})
#     else:
#         return Response({"message":"You are not authorised"}, 403)
    
    
# @api_view()
# @throttle_classes([AnonRateThrottle])
# def throttle_check(request):
#     return Response({"message":"successful"})


# @api_view()
# @permission_classes([IsAuthenticated])
# @throttle_classes([TenCallsPerMinute])
# def throttle_check_auth(request):
#     return Response({"message":"message for the logged in users only"})