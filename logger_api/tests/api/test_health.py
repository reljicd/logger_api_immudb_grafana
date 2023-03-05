def test_health_check(client):
    expected_message = 'OK'
    expected_status_code = 200

    response = client.get('/health/')
    assert response.status_code == expected_status_code
    assert response.text == expected_message

