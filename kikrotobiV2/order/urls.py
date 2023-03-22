from django.urls import path
from .views import *


urlpatterns = [
    path('menu/', MenuList.as_view()),
    path('order/', CreateOrderItemView.as_view()),

    path('', organizations_list, name='orgs'),
    path('organizations/<int:org_id>/', orders, name='org-orders'),
    path('order/<int:order_id>/<int:org_id>', order_item_by_day, name='order'),
    path('organizations/option_choice/<int:id>/', choice, name='choice'),
    path('months/<int:organization_id>/', months_list, name='months'),
    path('order/<int:year>/<int:month>/<int:org_id>', list_by_month, name='test')
]
