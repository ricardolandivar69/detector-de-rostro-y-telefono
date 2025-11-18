from django.test import Client
import pytest

@pytest.mark.django_db
def test_main_routes():
    client = Client()
    response = client.get('/')
    assert response.status_code == 200

    response = client.get('/some-other-route/')
    assert response.status_code == 200

    response = client.get('/another-route/')
    assert response.status_code == 200