import requests

class ApiCall:
    basepath: str = 'http://web.notewave.test/api/'
    
    def __init__(self, path: str, data: dict):
        url = self.basepath + path
        request = requests.post(url, params='', json=data)

        self.response = request.json()
        
    
    