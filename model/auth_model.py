from functools import wraps
import mysql.connector,json
from flask import make_response,request
import jwt
import re
from config.config import dbconfig

class auth_model():
    def __init__(self):
        try:
            self.con=mysql.connector.connect(host=dbconfig['hostname'],user=dbconfig['username'],password=dbconfig['password'],database=dbconfig['database'])
            self.cur=self.con.cursor(dictionary=True)
            self.con.autocommit=True
            print("Connection successful")
        except:
            print("Some error")

    def token_auth(self,endpoint=""):
        def inner1(func):
            @wraps(func)
            def inner2(*args):
                    endpoint=request.url_rule
                    print(endpoint)
                    authorization = request.headers.get("Authorization")
                    if re.match("^Bearer *([^ ]+) *",authorization,flags=0):
                        token = authorization.split(" ")[1]
                        try:
                            jwt_decoded = jwt.decode(token,"aditya",algorithms="HS256")
                        except jwt.ExpiredSignatureError:
                             return make_response({"ERROR":"TOKEN_EXPIRED"},401)
                        role_id = jwt_decoded['payload']['role_id']
                        str = f"SELECT roles FROM accessibilty_view WHERE endpoints = '{endpoint}'"
                        self.cur.execute(str)
                        result=self.cur.fetchall()
                        if(len(result)>0):
                            allowed_role=json.loads(result[0]['roles'])
                            if(role_id in allowed_role): 
                                return func(*args)
                            else:
                                return make_response({"ERROR":"Invalid_REQUEST"},401)       
                    else:
                         return make_response({"ERROR":"Invalid_Token"},401)
            return inner2
        return inner1