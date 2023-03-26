from Helpers.Connection import *
import time
import datetime
import requests
import os

class User:
    def __init__(self, id, name, email, created_at, updated_at):
        self.id = id
        self.name = name
        self.email = email
        self.created_at = created_at
        self.updated_at = updated_at
        
    @staticmethod
    def exists(email: str, password: str):
        url = 'http://web.notewave.test/api/authenticate'
        
        data = {
            "email":email,
            "password":password,
        }
        
        r = requests.post(url, params='', json=data)

        return r.json()
    
    @staticmethod
    def get(email: str):
        query = 'SELECT * FROM users WHERE email = %s'
        values = (email,)
        
        cursor.execute(query, values)
        
        user = cursor.fetchone()
        
        return User(
            user['id'],
            user['name'],
            user['email'],
            user['created_at'],
            user['updated_at'],
        )
        
    @staticmethod
    def serialize(user):
        return {
            "id": user.id,
            "name": user.name,
            "email": user.email
        }
        
    @staticmethod
    def isAuthenticated():
        if os.path.exists('assets/user.json'):
            return True
        else:
            return False