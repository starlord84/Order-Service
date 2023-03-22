from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Sum, Count, Min, Q, Subquery
from django.db.models.functions import TruncDate, TruncMonth
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from rest_framework import generics
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.response import Response
from collections import defaultdict
from .serializers import *
from user.models import User
from .models import *
from datetime import datetime, timezone
from django.utils import timezone
current_time = timezone.now()


class MenuList(ListAPIView):
    serializer_class = CategorySerializer

    def list(self, request, *args, **kwargs):
        current_day = datetime.isoweekday(datetime.now())
        categories = Category.objects.filter(
            Q(dish__menuitem__menu__day_of_the_week=current_day)
        ).distinct()

        serializer = self.serializer_class(categories, many=True)

        menu_items = MenuItem.objects.filter(menu__day_of_the_week=datetime.isoweekday(datetime.now()))
        menu_item_serializer = MenuItemSerializer(menu_items, many=True)

        response_data = {
            'current_date': datetime.today().strftime('%Y-%m-%d'),
            'menu_items': menu_item_serializer.data,
        }

        return Response(response_data)


class CreateOrderItemView(generics.CreateAPIView):
    serializer_class = CreateOrderItemSerializer


def organizations_list(request):
    organizations = Organization.objects.all()

    context = {
        'organizations': organizations,
        'orders': orders
    }
    return render(request, 'order/organizations.html', context=context)


def orders(request, org_id):
    try:
        org = Organization.objects.get(id=org_id)
        orders_by_date = Order.objects.filter(user__organization_id=org_id) \
            .annotate(date=TruncDate('order_datetime')) \
            .values('date',) \
            .annotate(min_order_id=Min('id')) \
            .order_by('-date')

        context = {
            'orders_by_date': orders_by_date,
            'org_id': org_id,
            'org': org
        }
        print(orders_by_date)
        return render(request, 'order/orders_org.html', context=context)
    except:
        raise ValueError('Организация с таким иденитификатором не сущеcтвует')


def order_item_by_day(request, order_id, org_id):
    try:
        order = Order.objects.get(id=order_id)
        order_items = OrderItems.objects.filter(order__order_datetime=order.order_datetime, order__user__organization_id=org_id)
        users = User.objects.filter(user__order_datetime=order.order_datetime, organization_id=org_id)

        user_order_items = {}
        for user in users:
            user_items = order_items.filter(order__user=user)
            total_price = sum(item.price*item.quantity for item in user_items)
            user_order_items[user] = {'items': user_items, 'total_price': total_price}
        print(order_items)
        order_total = sum(item.price*item.quantity for item in order_items)

        context = {
            'order': order,
            'user_order_items': user_order_items,
            'order_total': order_total

        }
        return render(request, 'order/order.html', context=context)
    except ObjectDoesNotExist:
        raise ValueError('Неверно указанные идентификаторы организации и/или заказа')


def choice(request, id):
    org = Organization.objects.get(id=id)
    context = {
        'id': id,
        'org': org
                }
    return render(request, 'order/option_choice.html', context=context)


def months_list(request, organization_id):
    try:
        organization = get_object_or_404(Organization, pk=organization_id)
        orders = Order.objects.filter(order_datetime__year=timezone.now().year, user__organization_id=organization_id)
        months_with_orders = orders.dates('order_datetime', 'month')
        months_with_orders_name = [month.strftime('%B') for month in months_with_orders]
        context = {
            'organization': organization,
            'months_with_orders_name': months_with_orders_name,
            'months_with_orders': months_with_orders,
            'org_id': organization_id
            }

        return render(request, 'order/months.html', context=context)
    except:
        raise ValueError('Организация с таким иденитификатором не сущеcтвует')


def list_by_month(request, year, month, org_id):
    try:
        org = Organization.objects.get(id=org_id)
        orders = Order.objects.filter(user__organization_id=org_id, order_datetime__month=month,
                                      order_datetime__year=year)

        user_date_totals = defaultdict(lambda: defaultdict(float))
        for order in orders:
            order_items = OrderItems.objects.filter(order=order)
            for order_item in order_items:
                user = order_item.order.user
                date = order_item.order.order_datetime
                user_date_totals[date][user] += order_item.total_price()

        users = list(set(user for date_totals in user_date_totals.values() for user in date_totals))
        dates = sorted(user_date_totals.keys())
        table_data = [[None for _ in range(len(users) + 2)] for _ in range(len(dates) + 2)]

        table_data[0][0] = 'Date'
        for i, user in enumerate(users):
            table_data[0][i+1] = user.username

        table_data[0][-1] = 'Total / day'
        table_data[-1][0] = 'Total / user'

        daily_totals = [0] * len(dates)
        for i, date in enumerate(dates):
            table_data[i+1][0] = date.strftime('%Y-%m-%d')
            date_totals = user_date_totals[date]
            daily_total = 0
            for j, user in enumerate(users):
                if user in date_totals:
                    total = date_totals[user]
                    table_data[i+1][j+1] = total
                    daily_total += total
            daily_totals[i] = daily_total
            table_data[i+1][-1] = daily_total

        user_totals = defaultdict(float)
        for date_totals in user_date_totals.values():
            for user, total in date_totals.items():
                user_totals[user] += total

        for i, user in enumerate(users):
            table_data[-1][i+1] = user_totals[user]
        table_data[-1][-1] = sum(daily_totals)

        context = {
            'table_data': table_data,
            'daily_totals': daily_totals,
            'org': org,
            'y': year,
            'm': month
        }

        return render(request, 'order/test.html', context=context)
    except ObjectDoesNotExist:
        raise ValueError('Организация с таким иденитификатором не сущеcтвует')
