import json
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Order, OrderedItem


class ApiTestCase(TestCase):

    fixtures = ['fixtures/items.json']
    # We take items from fixtures
    # Price for item 1 = 359
    # Price for item 2 = 10

    def setUp(self):
        # Every test needs a client
        self.client = Client()
        self.user = User.objects.create_user(username="test", password="sdvor12345", email="test@sdvor.com")
        self.client.force_login(self.user)

    def test_get_items(self):
        # Check getting items list from API
        response = self.client.get('/api/items')
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.content), 0)

    def test_create_new_order(self):
        # Creating new order and testing the results via API
        response = self.client.post('/api/orders', {
                'full_name': 'Andrey Gaichikov',
                'address': 'Izhevsk, Udmurtskaya str',
                'phone': '89501655098',
                'email': 'gaichikov@gmail.com',
                'items': json.dumps([{"quantity":1,"item":{"id":5}},{"quantity":1,"item":{"id":4}}])
                })

        self.assertEqual(response.status_code, 201)

        # Check created order
        response = self.client.get('/api/orders/1/')
        self.assertEqual(response.status_code, 200)
        response_json = response.json()
        total_sum = response_json['results']['total_sum']
        self.assertEqual(total_sum, 369)

        # Increase amount of one of the items, and check if total sum changed
        ordered_item = OrderedItem.objects.get(pk=1)
        ordered_item.quantity = 5
        ordered_item.save()
        response = self.client.get('/api/orders/1/')
        response_json = response.json()
        total_sum = response_json['results']['total_sum']
        self.assertEqual(total_sum, 1805)
