from django.db import models


class Organization(models.Model):
    class Meta:
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'

    title = models.CharField('Название', max_length=255)
    address = models.CharField('Адрес', max_length=255)
    contact_phone = models.CharField('Контакный номер телефона', max_length=255)
    contact_name = models.CharField('Контактное имя', max_length=255)

    def __str__(self):
        return self.title


class Order(models.Model):
    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    user = models.ForeignKey('user.User', on_delete=models.DO_NOTHING, verbose_name='Клиент', related_name='user')
    order_datetime = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} {self.pk}'


class Category(models.Model):
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    name = models.CharField('Категория', max_length=255)

    def __str__(self):
        return self.name


class Dish(models.Model):
    class Meta:
        verbose_name = 'Блюдо'
        verbose_name_plural = 'Блюда'

    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, verbose_name='Категория')
    title = models.CharField('Название', max_length=255)
    weight = models.FloatField('Вес')

    def __str__(self):
        return self.title


class Menu(models.Model):
    DAYS_OF_THE_WEEK = (
        ('1', 'Понедельник'),
        ('2', 'Вторник'),
        ('3', 'Среда'),
        ('4', 'Четверг'),
        ('5', 'Пятница'),
        ('6', 'Суббота'),
        ('7', 'Воскресенье'),
    )

    class Meta:
        verbose_name = 'Меню'
        verbose_name_plural = 'Меню'

    date_from = models.DateField('Дата начала актуальности меню')
    date_to = models.DateField('Дата окончания актуальности меню')
    day_of_the_week = models.CharField('День недели в которые действует меню', max_length=255, choices=DAYS_OF_THE_WEEK)

    def __str__(self):
        return self.day_of_the_week


class MenuItem(models.Model):
    class Meta:
        verbose_name = 'Предмет меню'
        verbose_name_plural = 'Предметы меню'

    menu = models.ForeignKey(Menu, on_delete=models.DO_NOTHING, verbose_name='Меню')
    dish = models.ForeignKey(Dish, on_delete=models.DO_NOTHING, verbose_name='Блюдо')
    price = models.FloatField('Цена')

    def __str__(self):
        return f'{self.dish}'


class OrderItems(models.Model):
    class Meta:
        verbose_name = 'Заказ блюда'
        verbose_name_plural = 'Заказы блюда'

    order = models.ForeignKey(Order, on_delete=models.DO_NOTHING, verbose_name='Заказ', related_name='order')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.DO_NOTHING, verbose_name='Предмет меню')
    quantity = models.PositiveSmallIntegerField('Количество')
    price = models.FloatField('Цена', null=True)

    def __str__(self):
        return f'{self.order}'

    def total_price(self):
        return self.quantity * self.price
