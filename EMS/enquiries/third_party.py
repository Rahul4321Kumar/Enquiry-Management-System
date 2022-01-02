import requests

BASE_URL = "https://jsonplaceholder.typicode.com/"

class Users:
    def list_user(self):
        import pdb;pdb.set_trace()
        response = requests.get(BASE_URL + "users")
        return response