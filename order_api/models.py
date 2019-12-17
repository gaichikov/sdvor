from datetime import date, datetime
from django.db import models
from django.db.models import Sum
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


class Item(models.Model):
    name = models.CharField(max_length=1000)
    price = models.FloatField(default=0, verbose_name="Item price")
    description = models.TextField(blank=True, null=True, verbose_name="Item description")

    class Meta:
        db_table = 'items'
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return self.name



class Contact(models.Model):
    # order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='order')
    phone = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=1000, blank=True, null=True)
    full_name = models.CharField(max_length=1000, blank=True, null=True)
    email = models.EmailField(max_length=1000, validators=[validate_email])

    def __str__(self):
        return self.full_name

    class Meta:
        db_table = 'contacts'
        verbose_name = "Контакт"
        verbose_name_plural = "Контакты"


class OrderedItem(models.Model):
    ''' Store here every position of order with quantity parameter '''

    # order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)

    class Meta:
        db_table = 'ordered_items'
        verbose_name = "Заказанный товар"
        verbose_name_plural = "Заказанные товары"


    def __str__(self):
        return self.item.name

    @property
    def sum(self):
        return self.item.price * self.quantity


class Order(models.Model):

    order_uid = models.CharField(max_length=100, verbose_name="unique order id")
    date = models.DateField(auto_now=True, verbose_name="creation date")
    ts = models.DateTimeField(auto_now=True, verbose_name="creation datetime")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user', verbose_name="order creator")
    contact = models.OneToOneField(Contact, on_delete=models.CASCADE, related_name='contact', blank=True, null=True)
    items = models.ManyToManyField(OrderedItem)

    class Meta:
        db_table = 'orders'
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return self.order_uid

    def save(self, *args, **kwargs):
        # Sets order_uid from current date and current day`s order increment
        today = date.today()
        orders_count = Order.objects.filter(date=today).count()
        self.order_uid = '%s-%s' % (today.strftime('%d%m%Y'), orders_count)
        return super().save(*args, **kwargs)

    @property
    def total_sum(self):
        # return self.items.aggregate(Sum('sum'))
        # Aggregation doesn`t work on computed properties, so we have to iterate through items
        # https://stackoverflow.com/questions/3066491/django-can-you-use-property-as-the-field-in-an-aggregation-function
        return sum([item.sum for item in self.items.all()])

