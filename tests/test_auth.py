def test_signup_success(client):
    #  API Call
    payload = {
        "email": "tester@example.com",
        "password": "strongpassword123"
    }
    response = client.post("/api/v1/auth/signup", json=payload)
    
    #  Assertions 
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "tester@example.com"
    assert "id" in data
    assert "password" not in data  

def test_signup_duplicate_email(client):
    
    payload = {
        "email": "tester@example.com",
        "password": "strongpassword123"
    }
    response = client.post("/api/v1/auth/signup", json=payload)
    assert response.status_code == 400
    assert response.json()["detail"] == 'Email Already Registered'

def test_login_wrong_password(client):
    payload ={
        'email' :'tester@example.com',
        'password':'strongpassword12'
    }
    response = client.post('/api/v1/auth/login',json=payload)
    assert response.status_code == 401
    assert response.json()['detail'] == 'Invalid Credentials'

def test_login_sucess(client):
    payload = {
           "email": "tester@example.com",
           "password": "strongpassword123"
       }  
    response = client.post('api/v1/auth/login' , json =payload)

    assert response.status_code == 200

    data = response.json()

    assert 'access_token' in data
    assert data['token_type'] == 'bearer'  