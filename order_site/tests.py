# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase, Client
from django.contrib.auth.models import User

from django.test import TestCase


class AuthenticationTest(TestCase):

    def setUp(self):
        self.client = Client()
        User.objects.create_user(username="test", password="sdvor12345", email="test@sdvor.com")
        self.username = 'test'
        self.password = 'sdvor12345'

    def test_unauthenticated_access(self):
        response = self.client.get('/api/orders')
        self.assertEqual(response.status_code, 401)

    def test_authentication(self):
        # test login
        self.assertTrue(self.client.login(username=self.username, password=self.password))

        print(dir(self.client.session.session_key))
        # test logout
        self.assertTrue(self.client.logout())

