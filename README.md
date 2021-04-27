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



# API specifications (Live Server)
## Host = https://flaskapp.osc-fr1.scalingo.io
## Version = api/v1
##
##Login
#### [POST] /api/v1/login (https://flaskapp.osc-fr1.scalingo.io/api/v1/login)
#### sample request 
    {
        "username": "noel",
        "password": "1234"
    }
#### sample response
    {
        "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2MTE4MDQ4ODYsIm5iZiI6MTYxMTgwNDg4NiwianRpIjoiOGJkZDk0MDItYmFlZi00YTQ0LThmNWYtYTBhNTBiMTJlMTJkIiwiaWRlbnRpdHkiOjIsImZyZXNoIjp0cnVlLCJ0eXBlIjoiYWNjZXNzIn0.w8GMwm0e-aqCuUI5YgKnAdN-MVtSzLhh9s4w9BIUj_Q",
        "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2MTE4MDQ4ODYsIm5iZiI6MTYxMTgwNDg4NiwianRpIjoiOTI4ZmFiZDAtMGJhMS00NDE1LTkyZjEtNGYyY2Q5OTQ1MWI1IiwiZXhwIjoxNjE0Mzk2ODg2LCJpZGVudGl0eSI6MiwidHlwZSI6InJlZnJlc2gifQ.kW9s7l-zCg18kgX4QH6ZixvohUEz4q5i5y3IjlIQ7U0"
    }
#### for log-in required end-points, add header
    Authorization: "Bearer {access_token}"
##
## /item
#### [GET] /api/v1/item?name={name} 
#### Query params: 
    ?name={name}
    ?id={id}
#### sample response 
    {
        "item": {
            "id": 4,
            "name": "dog",
            "price": 333.99,
            "create_time": 1611647715
        }
    }

#### [POST] /api/v1/item  (login required)
#### sample request 
    {
        "name": "dog",
        "price": 333.99
    }
#### sample response 
    {
        "id": 4,
        "name": "dog",
        "price": 333.99,
        "create_time": 1611647715
    }

#### [DELETE] api/v1/item?name={name}(login required)
#### Query params:
    ?name={name}
    ?id={id}
#### sample response
    {
        "items": [
            {
                "id": 1,
                "name": "apple",
                "price": 3.99,
                "create_time": 1611647703
            },
            {
                "id": 3,
                "name": "cat",
                "price": 333.99,
                "create_time": 1611647712
            },
            {
                "id": 4,
                "name": "dog",
                "price": 333.99,
                "create_time": 1611647715
            }
        ]
    }

##
## /items
#### [GET] api/v1/items
#### required param: ?sort={sort}
0: create_time desc, 1: create_time asc, 2: price desc, 3: price asc
#### sample response, ?sort=3
    {
        "count": 5,
        "items": [
            {
                "create_time": 1619506998,
                "id": 3,
                "name": "pencil",
                "price": 0.2
            },
            {
                "create_time": 1619506959,
                "id": 1,
                "name": "orange",
                "price": 0.5
            },
            {
                "create_time": 1619508095,
                "id": 5,
                "name": "apple",
                "price": 0.99
            },
            {
                "create_time": 1619507580,
                "id": 4,
                "name": "grape",
                "price": 1.99
            },
            {
                "create_time": 1619508104,
                "id": 6,
                "name": "pen",
                "price": 2.99
            }
        ]
    }