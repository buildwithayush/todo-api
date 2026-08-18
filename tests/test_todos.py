def test_create_todo_authenticated(client):
    login_res = client.post('/api/v1/auth/login',json = {
        "email": "tester@example.com",
        "password": "strongpassword123"
    })

    token = login_res.json()['access_token']

    headers = {
        "Authorization": f"Bearer {token}"
    }

    todo_payload = {
        "title": "Study PyTest",
        "description": "Write automated tests for FastAPI",
    }

    response = client.post('/api/v1/todos/' , json=todo_payload , headers=headers)

    
    assert response.status_code == 201
    data = response.json()
    assert data['title'] == "Study PyTest"
    assert data['completed'] is False

def test_get_todos_unauthorized(client):

       response = client.get('/api/v1/todos/',)

       assert response.status_code == 401
       
       

