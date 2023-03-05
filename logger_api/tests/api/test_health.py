def test_health_check(client):
    expected_message = 'OK'
    expected_status_code = 200

    response = client.get('/health/')
    assert response.status_code == expected_status_code
    assert response.text == expected_message


def test_health_check_with_auth(client, user):
    expected_message = f'OK {user.username}'
    expected_status_code = 200

    response = client.get('/health/auth',
                          headers={'api-key': user.api_key})
    assert response.status_code == expected_status_code
    assert response.text == expected_message
