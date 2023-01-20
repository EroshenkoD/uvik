from rest_framework import status, viewsets, generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import filters
from django_filters import rest_framework as rf_filters

from .models import Posts
from .serializers import PostsSerializer


class PostsFilter(rf_filters.FilterSet):
    min_likes = rf_filters.NumberFilter(field_name="likes", lookup_expr='gte')
    max_likes = rf_filters.NumberFilter(field_name="likes", lookup_expr='lte')

    class Meta:
        model = Posts
        fields = ['title']


class PostsViewSet(viewsets.ModelViewSet, generics.ListAPIView):
    queryset = Posts.objects.all()
    serializer_class = PostsSerializer
    filter_backends = (rf_filters.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filterset_class = PostsFilter
    search_fields = ['title', 'likes']
    ordering_fields = ['title', 'likes']
    ordering = ['likes']


class PostsList(APIView, LimitOffsetPagination):

    def get(self, request, likes=None):
        if likes:
            posts = Posts.objects.filter(likes__gte=likes)
        else:
            posts = Posts.objects.all()
        posts = self.paginate_queryset(posts, request, view=self)
        serializer = PostsSerializer(posts, many=True)
        return self.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = PostsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def post_detail(request, pk):

    try:
        posts = Posts.objects.get(pk=pk)
    except Posts.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PostsSerializer(posts)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = PostsSerializer(posts, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        posts.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
