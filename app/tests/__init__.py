
import json


def create_login_user(_object):
    # create a user
        data = json.dumps(_object.sample_user)
        _object.test_client.post('/auth/signup', data=data,
                              headers=_object.json_headers)
        # login user
        login_data = json.dumps(_object.sample_login)
        
        login_response = _object.test_client.post(
            '/auth/login', data=login_data, headers=_object.json_headers)

        token = json.loads(login_response.data.decode())['token']
        return {'token': token}
