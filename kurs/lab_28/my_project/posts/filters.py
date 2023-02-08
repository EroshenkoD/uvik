from django_filters import rest_framework as rf_filters

from .models import Posts


class PostsFilter(rf_filters.FilterSet):
    min_likes = rf_filters.NumberFilter(field_name="likes", lookup_expr='gte')
    max_likes = rf_filters.NumberFilter(field_name="likes", lookup_expr='lte')

    class Meta:
        model = Posts
        fields = ['title']