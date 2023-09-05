
import django_filters as dj_filters
from django.db import models as django_models
from django_filters import rest_framework as filters
from rest_framework import viewsets
from rest_framework import filters


class BaseDateFilter(dj_filters.FilterSet):
    class Meta:
        model = None
        fields = {
            # 'timestamp': ('lte', 'gte')
        }

    filter_overrides = {
        django_models.DateTimeField: {
            'filter_class': dj_filters.IsoDateTimeFilter
        },
    }
    

class CreatedAtBetweenDateFilterBackend(filters.BaseFilterBackend):
    """
    based on query params, filter queryset by a date range created_at__gte and created_at__lte
    """
    def filter_queryset(self, request, queryset, view):
        start_date = request.query_params.get('created_at__gte', None)
        end_date = request.query_params.get('created_at__lte', None)
        if start_date:
            queryset = queryset.filter(created_at__gte=start_date)
        if end_date:
            queryset = queryset.filter(created_at__lte=end_date)
        return queryset

class UpdatedAtBetweenDateFilterBackend(filters.BaseFilterBackend):
    """
    based on query params, filter queryset by a date range updated_at__gte and updated_at__lte
    """
    
    def filter_queryset(self, request, queryset, view):
        start_date = request.query_params.get('updated_at__gte', None)
        end_date = request.query_params.get('updated_at__lte', None)
        if start_date:
            queryset = queryset.filter(updated_at__gte=start_date)
        if end_date:
            queryset = queryset.filter(updated_at__lte=end_date)
        return queryset




def multiSelectFilterFactory(_base_filter_queryparam):
    """
    based on query params, filter queryset by a multi select
    """
    class MyMultiSelectFilter(filters.BaseFilterBackend):
        base_filter_queryparam = _base_filter_queryparam
        def filter_queryset(self, request, queryset, view):
            values = request.query_params.get(self.base_filter_queryparam, None)
            # split values by comma and convert to int
            values = [int(value) for value in values.split(',')] if values else None
            
            if values:
                kwargs = {
                    self.base_filter_queryparam: values
                }
                queryset = queryset.filter(**kwargs)
                # queryset = queryset.filter(client__in=values)
            
            return queryset
    return MyMultiSelectFilter


class MultiSelectFilter(filters.BaseFilterBackend):
    """
    based on query params, filter queryset by a multi select
    """
    base_filter_queryparam = None
    def filter_queryset(self, request, queryset, view):
        values = request.query_params.get(self.base_filter_queryparam, None)
        # split values by comma and convert to int
        values = [int(value) for value in values.split(',')] if values else None
        
        if values:
            kwargs = {
                self.base_filter_queryparam: values
            }
            queryset = queryset.filter(**kwargs)
            # queryset = queryset.filter(client__in=values)
        
        return queryset
    
class ClientMultiSelectFilter(MultiSelectFilter):
    """
    based on query params, filter queryset by a multi select
    """
    base_filter_queryparam = 'client__in'
    
class StatusMultiSelectFilter(MultiSelectFilter):
    """
    based on query params, filter queryset by a multi select
    """
    base_filter_queryparam = 'status__in'

class ReasonMultiSelectFilter(MultiSelectFilter):
    """
    based on query params, filter queryset by a multi select
    """
    base_filter_queryparam = 'reason__in'
    
class TypeMultiSlectFilter(MultiSelectFilter):
    """
    based on query params, filter queryset by a multi select
    """
    base_filter_queryparam = 'type__in'