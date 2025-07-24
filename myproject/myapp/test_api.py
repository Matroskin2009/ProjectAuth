import pytest
from django.urls import reverse
from myapp.models import User, InviteActivation


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()


@pytest.fixture
def test_user(db):
    return User.objects.create_user(
        username="test_user",
        password="testpass123",
        number_phone="+79991112233",
        ref_code="INVITE1"
    )


@pytest.mark.django_db
class TestAuthAPI:
    def test_registration(self, api_client):
        url = reverse('unified_auth')
        data = {
            'username': 'new_user',
            'password': 'newpass123',
            'number_phone': '+79998887766',
            'user_key': '1234',
            'right_key': '1234'
        }
        response = api_client.post(url, data)
        assert response.status_code == 200
        assert User.objects.filter(username='new_user').exists()

    def test_login(self, api_client, test_user):
        url = reverse('unified_auth')
        data = {
            'username': 'test_user',
            'password': 'testpass123',
            'number_phone': '+79991112233',
            'user_key': '1234',
            'right_key': '1234'
        }
        response = api_client.post(url, data)
        assert response.status_code == 200
        assert 'sessionid' in api_client.cookies


@pytest.mark.django_db
class TestInviteAPI:
    def test_activate_invite(self, api_client, test_user):
        # Аутентификация
        api_client.login(username='test_user', password='testpass123')

        # Создаем инвайтера
        inviter = User.objects.create_user(
            username="inviter",
            password="inviterpass",
            number_phone="+79990001122",
            ref_code="INVITER1"
        )

        url = reverse('add_inviter')
        data = {'inviter': 'INVITER1'}
        response = api_client.post(url, data)

        assert response.status_code == 200
        assert InviteActivation.objects.filter(
            inviter=inviter,
            invited=test_user
        ).exists()

    def test_invite_validation(self, api_client, test_user):
        api_client.login(username='test_user', password='testpass123')

        url = reverse('add_inviter')
        data = {'inviter': 'INVALID_CODE'}
        response = api_client.post(url, data)

        assert response.status_code == 404
        assert 'Инвайт-код не найден' in str(response.content)


@pytest.mark.django_db
class TestProfileAPI:
    def test_get_profile(self, api_client, test_user):
        api_client.login(username='test_user', password='testpass123')
        url = reverse('profile_page')
        response = api_client.get(url)

        assert response.status_code == 200
        assert test_user.number_phone in str(response.content)
        assert test_user.ref_code in str(response.content)