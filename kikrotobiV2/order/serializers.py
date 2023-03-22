from datetime import datetime, date

from user.models import User
from .models import *
from rest_framework import serializers


class MenuSerializer(serializers.ModelSerializer):
    day_of_the_week_name = serializers.CharField(source='get_day_of_the_week_display')

    class Meta:
        model = Menu
        fields = 'day_of_the_week_name'.split()


class DishSerializer2(serializers.ModelSerializer):

    class Meta:
        model = Dish
        fields = 'title'.split()


class MenuItemSerializer(serializers.ModelSerializer):
    menu = MenuSerializer()
    dish = DishSerializer2()

    class Meta:
        model = MenuItem
        fields = 'id menu dish price'.split()


class DishSerializer(serializers.ModelSerializer):
    menu_items = MenuItemSerializer(many=True, read_only=True, source='menuitem_set')

    class Meta:
        model = Dish
        fields = 'title menu_items'.split()


class CategorySerializer(serializers.ModelSerializer):
    dish = DishSerializer(many=True, read_only=True, source='category')

    class Meta:
        model = Category
        fields = 'name dish'.split()


class MenuWithDateSerializer(serializers.Serializer):
    current_date = serializers.DateField(default=date.today())
    menu_items = MenuItemSerializer(many=True)


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'contact_phone')


class CreateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('id',)


class CreateOrderItemSerializer(serializers.ModelSerializer):
    user_phone = serializers.CharField(write_only=True)

    class Meta:
        model = OrderItems
        fields = ('id', 'quantity', 'menu_item', 'user_phone')

    def validate_user_phone(self, value):
        try:
            user = User.objects.get(contact_phone=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("User does not exist with this phone number.")
        return user

    def create(self, validated_data):
        user = validated_data.pop('user_phone')
        order = Order.objects.create(user=user)
        order_item = OrderItems.objects.create(order=order, **validated_data)
        return order_item
