from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class AuthFlowTests(TestCase):
    def test_register_get(self):
        r = self.client.get(reverse('register'))
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, '<form')

    def test_login_get(self):
        r = self.client.get(reverse('login'))
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, '<form')

    def test_profile_requires_login(self):
        r = self.client.get(reverse('profile'))
        self.assertEqual(r.status_code, 302)  # redirect to login

    def test_profile_update_post(self):
        user = User.objects.create_user(username='u1', email='u1@x.com', password='pass12345')
        self.client.login(username='u1', password='pass12345')
        r = self.client.post(reverse('profile'), {
            'username': 'u1_new',
            'email': 'new@x.com',
            'bio': 'hello there'
        })
        self.assertEqual(r.status_code, 302)  # PRG redirect
        user.refresh_from_db()
        self.assertEqual(user.username, 'u1_new')
        self.assertEqual(user.email, 'new@x.com')
