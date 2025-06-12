from rest_framework.viewsets import ReadOnlyModelViewSet
from ..models import Category
from ..serializers.category_serializer import CategorySerializer


class CategoryViewSet(ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

