from django.test import TestCase
from django.contrib.auth.models import User
from django.test import Client

# Create your tests here.
class TestUser(TestCase):
    def test_signup(self):
        u = User.objects.create(username="test1", email="test1@mail.com")
        self.assertTrue(isinstance(u, User))

    def test_successful_login(self):
        user = User.objects.create(username='test2', email="test2@mail.com")
        user.set_password('pass123')
        user.save()

        c = Client()
        logged_in = c.login(username='test2', password='pass123')
        self.assertTrue(logged_in)

    def test_unsuccessful_login(self):
        user = User.objects.create(username='test3', email="test3@mail.com")
        user.set_password('pass123')
        user.save()

        c = Client()
        logged_in = c.login(username='test3', password='pass456')
        self.assertFalse(logged_in)
