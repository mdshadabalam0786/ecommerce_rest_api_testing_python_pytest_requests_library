import pytest
from requests import Session
url = "https://www.shoppersstack.com/shopping/users/login"

"""Positive test case"""
"""test with valid credential"""
def test_shopperlogin_valid_credential():
    session = Session()
    session.headers.update({"content-type": "application/json"})

    payload = {
        "email": "alamsahdab786@gmail.com",
        "password": "Nagma@123",
        "role": "SHOPPER"
    }
    response = session.post(url, json=payload)
    session.close() # Ensure the session is closed after the request
    assert response.status_code == 200, f"Expected status code 200 but got {response.status_code}"  # Assert status code
    assert response.ok, f"Expected response to be OK but got {response.ok}"# Assert response is OK
    assert response.elapsed.total_seconds() <= 3, f"Response time exceeded: {response.elapsed.total_seconds()} seconds" # Assert response time
    header = response.headers # Assert response headers
    assert header['Content-Type'] == "application/json", f"Expected Content-Type 'application/json' but got {header['Content-Type']}"
    r = response.json()# Assert response body
    assert 'data' in r, f"Response JSON does not contain 'data' key"
    assert r['data']['email'] == payload['email'], f"Expected email {payload['email']} but got {r['data']['email']}"
    assert r['data']['role'] == payload['role'], f"Expected role {payload['role']} but got {r['data']['role']}"
    # Optional additional checks
    assert 'jwtToken' in r['data'], "Response JSON does not contain 'token' key"
    assert isinstance(r['data']['jwtToken'], str), f"Expected 'token' to be a string but got {type(r['data']['token'])}"

header="username,password"
data=[("alamsahdab786@gmail.com","Nagma@123"),("sandeepsandy580023@gmail.com","Password@123"),
("syedmaheen687@gmail.com","1Cd19ec14$"),("sumanbss21@gmail.com","Saibaba@1528"),("richashrivastava401@gmail.com","Richa@401")]
@pytest.mark.parametrize(header,data)
def test_shopperlogin_with_five_different_valid_credential(username,password):
    session = Session()
    session.headers.update({"content-type": "application/json"})

    payload = {
        "email": username,
        "password": password,
        "role": "SHOPPER"
    }
    response = session.post(url, json=payload)
    session.close()  # Ensure the session is closed after the request
    assert response.status_code == 200, f"Expected status code 200 but got {response.status_code}"  # Assert status code
    assert response.ok, f"Expected response to be OK but got {response.ok}"  # Assert response is OK
    assert response.elapsed.total_seconds() <= 3, f"Response time exceeded: {response.elapsed.total_seconds()} seconds"  # Assert response time
    header = response.headers  # Assert response headers
    assert header['Content-Type'] == "application/json", f"Expected Content-Type 'application/json' but got {header['Content-Type']}"
    r = response.json()  # Assert response body
    assert 'data' in r, f"Response JSON does not contain 'data' key"
    assert r['data']['email'] == payload['email'], f"Expected email {payload['email']} but got {r['data']['email']}"
    assert r['data']['role'] == payload['role'], f"Expected role {payload['role']} but got {r['data']['role']}"
    # Optional additional checks
    assert 'jwtToken' in r['data'], "Response JSON does not contain 'token' key"
    assert isinstance(r['data']['jwtToken'], str), f"Expected 'token' to be a string but got {type(r['data']['token'])}"


"""Negative test case"""
"""test with invalid credential"""
def test_shopper_invalid_credential():
    session=Session()
    session.headers.update({"content-type":"application/json"})
    payload=payload = {
                    "email": "alamsahdab111786@gmail.com",
                    "password": "Nagma@123",
                    "role": "SHOPPER"
                       }
    response=session.post(url,json=payload)
    session.close()
    assert response.status_code==401,f"expected status code 401 but we got {response.status_code}"
    assert response.elapsed.total_seconds()<=3,f"expected response in 2 second but getting from server {response.elapsed.total_seconds()}"
    assert not response.ok, f"Expected response not to be OK but got {response.ok}"
    r=response.json()
    assert r['data']=="Given user ID or password is wrong",f"expecting Given user ID or password is wrong but got it from server {r['data']}"
    assert r['message']=="UNAUTHORIZED",f"Expecting UNAUTHORIZED but got it from server {r['message']}"

def test_shopper_login_with_boundary_limit():
    session=Session()
    session.headers.update({"content-type":"application/json"})
    payload={
              "email":"alamsahdab786111111111111111111111wsdd@gmail.com",
              "password":"Nagma@123sdddddddddddddddddddddddddddddd",
              "role":"SHOPPER"
            }
    response=session.post(url,json=payload)
    session.close()
    assert response.status_code in [401,200],f"unexpected status {response.status_code}"

"""testing rate limiting/brute force protection"""
def test_shopper_login_rate_limiting():
    session=Session()
    session.headers.update({"content-type":"application/json"})
    payload={
              "email":"alamsahdab786@gmail.com",
              "password":"Nagma@1234", #invalid password
              "role":"SHOPPER"
            }
    for i in range(5): # Simulate multiple invalid login attempts
        response = session.post(url, json=payload)
        assert response.status_code in [200,400],f"expected 400 but got it {response.status_code}"
    session.close()
    # Check if rate limiting or account lockout occurs
    response = session.post(url, json=payload)
    assert response.status_code in [429, 400], f"expected 400 but got it {response.status_code}"

"""testing with empty body or without json"""
def test_shopper_login_empty_json():
    session=Session()
    session.headers.update({"content-type":"application/json"})
    payload={}
    response=session.post(url,json=payload)
    assert response.status_code==401,f"expected this from server {response.status_code}"
    assert not response.ok, f"expected is {response.ok}"
    assert response.elapsed.total_seconds() <= 3, f"expected time is 2 sec but we got it {response.elapsed.total_seconds()}"


"""tesing with casesensitive or special character"""
def test_shopper_login_case_sensitive():
    session=Session()
    session.headers.update({"content-type":"application/json"})
    payload={
              "email":"ALAMSAHDAB786@GMAIL.COM",#email is valid but value given in uppercase format
              "password":"Nagma@123",
              "role":"SHOPPER"
            }
    response=session.post(url,json=payload)
    assert response.status_code==401,f"expected is {response.status_code}"
    assert not response.ok,f"expected is {response.ok}"
    assert response.elapsed.total_seconds()<=3,f"expected time is 2 sec but we got it {response.elapsed.total_seconds()}"

"""====================="""