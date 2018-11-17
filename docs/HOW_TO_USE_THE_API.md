# How to use the AUCR API



## How to get an Authorization token using http
Example API calls to generate an auth token and using it to query data using http 0.9.9

    http --auth admin:admin POST http://0.0.0.0:5000/auth/tokens
    HTTP/1.1 200 OK
    Connection: keep-alive
    Content-Length: 106
    Content-Type: application/json
    Date: Sun, 19 Aug 2018 21:12:36 GMT
    
    {
        "token": "ikQnNEIieS535ArsMyz8uJMZCJGDsaATLl+QzOtxCzRCNK+Y+dDFft8s9Ovh0CdehkbTi1Z8iVQTgNPTVKCUSg=="
    }


## How to get group information using the id with http.
    
    http GET http://0.0.0.0:5000/api/groups/1 "Authorization:Bearer ikQnNEIieS535ArsMyz8uJMZCJGDsaATLl+QzOtxCzRCNK+Y+dDFft8s9Ovh0CdehkbTi1Z8iVQTgNPTVKCUSg=="
    HTTP/1.1 200 OK
    Connection: keep-alive
    Content-Length: 95
    Content-Type: application/json
    Date: Sun, 19 Aug 2018 21:15:03 GMT
    
    {
        "groups_id": 1,
        "id": 1,
        "time_stamp": "2018-08-16T22:06:40Z",
        "username_id": 1
    }


## How to get an Authorization token using python3

    import ujson
    import requests
    API_URL = 'http://0.0.0.0:5000/auth/tokens'
    response = requests.post(API_URL, auth=('admin', 'admin'))
    test = ujson.loads(response.text)
    
    print(ujson.dumps(test, indent=4, sort_keys=True))

# Python 3 Examples

## Get Group Information
    
    import ujson
    import requests
    API_URL = 'http://0.0.0.0:5000'
    API_KEY = 'QeboqPEom18c9SjwvWjin7c77pZbyIsYCXvbIaRClMnji+QYZyU/nOYmFDYRInN03YnJP9Up3lEEBCG2n8Eazg=='
    headers = {'Authorization': 'Bearer ' + API_KEY}
    response = requests.get('{}/api/groups/1'.format(API_URL), headers=headers)
    test = ujson.loads(response.text)
    print(ujson.dumps(test, indent=4, sort_keys=True))


## Create new group

    import ujson
    import requests
    API_URL = 'http://0.0.0.0:5000'
    API_KEY = 'QeboqPEom18c9SjwvWjin7c77pZbyIsYCXvbIaRClMnji+QYZyU/nOYmFDYRInN03YnJP9Up3lEEBCG2n8Eazg=='
    headers = {'Authorization': 'Bearer ' + API_KEY}
    response = requests.post('{}/api/groups'.format(API_URL), headers=headers, json={'group_name': 'testapi'})
    test = ujson.loads(response.text)
    print(ujson.dumps(test, indent=4, sort_keys=True))
    
## Create new user

    import ujson
    import requests
    API_URL = 'http://0.0.0.0:5000'
    API_KEY = 'QeboqPEom18c9SjwvWjin7c77pZbyIsYCXvbIaRClMnji+QYZyU/nOYmFDYRInN03YnJP9Up3lEEBCG2n8Eazg=='
    headers = {'Authorization': 'Bearer ' + API_KEY}
    response = requests.post('{}/api/users'.format(API_URL), headers=headers, json={'username': 'testapi', 'password': 'testing',
                                                                'email': 'test@localhost.local'})
    test = ujson.loads(response.text)
    print(ujson.dumps(test, indent=4, sort_keys=True))