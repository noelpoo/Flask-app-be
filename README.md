# Requirements
### python3.7 or above

## Libraries
#### Flask==1.1.2
#### Flask-JWT==0.3.2
#### Flask-RESTful==0.3.8
#### Werkzeug==1.0.1
#### requests==2.25.1
#### shortuuid==1.0.1
#### PyJWT==1.4.2
#### flasgger==0.9.5

## To install Libs
pip3 install -r requirements.txt

## To install Libs and run on python venv
./run.sh



# API specifications
## Local host = http://127.0.0.1:5000/ 
## /auth (login module)
#### sample request 
    {
        "username": "noel",
        "password": "1234"
    }
#### sample response
    {
        "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2MTE1NTQ4MDMsImlhdCI6MTYxMTU1NDUwMywibmJmIjoxNjExNTU0NTAzLCJpZGVudGl0eSI6Mn0.Z9pJB8wWdSJWXD5uO_MjDPuRZnozTG2jL7ZfjftcEuQ"
    }
#### for log-in required modules, add header
    Authorization: "JWT {access_token}"
## /item
#### [GET] /item/{item_name}
#### sample response 
    {
    "item": {
        "id": 1,
        "name": "orange",
        "price": 1.99
        }
    }

#### [POST] /item/{item_name}  (login required)
#### sample request 
    {
        "name": "apple",
        "price": 2.99
    }
#### sample response 
    {
    "item": {
        "id": 1,
        "name": "apple",
        "price": 2.99
        }
    }

#### [DELETE] /item/{item_name} (login required)
#### sample response
    {
        "items": [
            {
                "id": 1,
                "name": "orange",
                "price": 1.99
            },
            {
                "id": 3,
                "name": "grape",
                "price": 1.99
            }
        ]
    }

## /items
#### [GET] /items
#### sample response
    {
        "items": [
            {
                "id": 1,
                "name": "grape",
                "price": 1.99
            },
            {
                "id": 2,
                "name": "pencil",
                "price": 12.99
            },
            {
                "id": 3,
                "name": "phone",
                "price": 15.99
            }
        ]
    }
