from django.test import TestCase, Client
from django.urls import reverse
from http import HTTPStatus

from users.models import User
from users.factories import UserFactory


class UserTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.url_registration = reverse('users:registration')
        self.url_login = reverse('users:login')

        self.user_data = {
            'first_name': 'Иван', 'last_name': 'Иванов',
            'username': 'ivan', 'email': 'ivan@mail.ru',
            'password1': '12345678pP', 'password2': '12345678pP',
        }

    def test_user_registration_GET(self):
        response = self.client.get(self.url_registration)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/registration.html')

    def test_user_registration_POST(self):
        response = self.client.post(self.url_registration, self.user_data)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, self.url_login)
        self.assertTrue(User.objects.filter(username=self.user_data['username']).exists())

    def test_user_registration_POST_already_exists(self):
        user = UserFactory(username='already_exists_user')
        self.user_data.update({'username': user.username})
        response = self.client.post(self.url_registration, self.user_data)

        response_form = response.context['form']
        self.assertFalse(response_form.is_valid())
        self.assertEqual(response_form.errors['username'][0], 'Пользователь с таким именем уже существует.')
        self.assertEqual(User.objects.count(), 1)

    def test_user_login_GET(self):
        response = self.client.get(self.url_login)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/login.html')

    def test_user_login_POST(self):
        user = UserFactory(username='test-user')
        data = {'username': user.username, 'password': '12345678pP'}
        response = self.client.post(self.url_login, data=data)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('index'))

    def test_user_login_POST_with_wrong_data(self):
        user = UserFactory(username='test-user')
        data = {'username': user.username, 'password': '123'}
        response = self.client.post(self.url_login, data=data)

        error_msg = 'Пожалуйста, введите правильные имя пользователя и пароль. ' \
                    'Оба поля могут быть чувствительны к регистру.'
        form_response = response.context['form']
        self.assertEqual(form_response.errors['__all__'][0], error_msg)
