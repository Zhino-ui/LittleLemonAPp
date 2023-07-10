from rest_framework import generics
from .models import MenuItem, Category
from rest_framework.response import Response
from rest_framework.decorators import api_view,renderer_classes
from .serializers import MenuItemSerializer, CategorySerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes

class CategoriesView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class MenuItemsView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    ordering_fields = ['price', 'inventory']
    filterset_fields = ['price', 'inventory']
    search_fields = ['title']


# creating a protected api endpoint
@api_view()
@permission_classes([IsAuthenticated])
def secret(request):
    return Response({"message":"some secret message"})

# creating manager view
@api_view()
@permission_classes([IsAuthenticated])
def manager_view(request):
    if request.user.groups.filter(name='Manager').exists():
        return Response({"message":"Only manager should see this"})
    else:
        return Response({"message":"You are not authorised"}, 403)