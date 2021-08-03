from django_filters import FilterSet, CharFilter, DateFilter
from django.forms import DateInput
from django.utils.translation import gettext as _


class PostFilter(FilterSet):
    title = CharFilter(field_name='title', lookup_expr='icontains', label=_('Title'))
    author = CharFilter(field_name='author_id__user_id__username', lookup_expr='icontains', label=_('Author'))
    datetime = DateFilter(field_name='created_at', widget=DateInput(attrs={'type': 'date'}), lookup_expr='gt', label=_('Start date'))
