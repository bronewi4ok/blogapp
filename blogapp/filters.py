from users.models import CustomUser
import django_filters

class UserFilter(django_filters.FilterSet):
    first_name = django_filters.CharFilter(lookup_expr='icontains')
    year_joined = django_filters.NumberFilter(field_name='date_joined', lookup_expr='month')
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'year_joined' ]