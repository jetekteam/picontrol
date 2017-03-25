#!/usr/bin/python 
#user.py

from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)

class User():
    username = ''
    password = ''

    def generate_auth_token(self, key, expiration = 172800):
        s = Serializer(key, expires_in = expiration)
        return s.dumps({'id': self.username})

    @staticmethod
    def verify_auth_token(token, key):
        s = Serializer(key)
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None
        except BadSignature:
            return None
        
        sessionUser = User()
        sessionUser.username = data['id']
        return sessionUser
        

    