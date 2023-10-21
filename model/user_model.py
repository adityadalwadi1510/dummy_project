import mysql.connector,json
from flask import make_response
from datetime import datetime,timedelta
import jwt
from config.config import dbconfig

class user_model():
    def __init__(self):
        try:
            self.con=mysql.connector.connect(host=dbconfig['hostname'],user=dbconfig['username'],password=dbconfig['password'],database=dbconfig['database'])
            self.cur=self.con.cursor(dictionary=True)
            self.con.autocommit=True
            print("Connection successful")
        except:
            print("Some error")


    def user_signup_model(self,data):
        self.cur.execute(f"INSERT INTO users(name, email, phone, password) values('{data['name']}', '{data['email']}', '{data['phone']}', '{data['password']}')")
        return make_response({"message":"User created successfully"},201)
    
    def user_update_model(self,data):
        self.cur.execute(f"UPDATE users SET name='{data['name']}', email='{data['email']}', phone='{data['phone']}', password='{data['password']}', role='{data['role']}' WHERE id={data['id']}")
        if self.cur.rowcount>0:
            return make_response({"message":"User Updated successfully"},201)
        else:
            return make_response({"message":"Nothing to update"},202)
        
    def user_delete_model(self,id):
        self.cur.execute(f"DELETE from users WHERE id={id}")
        if self.cur.rowcount>0:
            return make_response({"message":"User deleted successfully"},200)
        else:
            return make_response({"message":"Nothing to delete"},202)
        
    def user_patch_model(self, id, data):
        qry="UPDATE users SET " 
        for key in data:
            qry+=f"{key}='{data[key]}', "
        qry=qry[:-2]+f" WHERE id={id}"

        self.cur.execute(qry)
        if self.cur.rowcount>0:
            return make_response({"message":"User Updated successfully"},201)
        else:
            return make_response({"message":"Nothing to update"},202)

    def user_getall_model(self):
        self.cur.execute("SELECT * from users")
        result=self.cur.fetchall()
        if len(result)>0:
            return make_response({"message":result}, 200)
        else:
            return make_response({"message":"Data not found"}, 204)
    
    def user_pagination_model(self,limit,pno):
        limit=int(limit)
        pno=int(pno)
        start=(limit*pno)-limit
        qry=f"SELECT * FROM users LIMIT {start}, {limit}"  
        self.cur.execute(qry)
        result=self.cur.fetchall()
        if len(result)>0:
            return make_response({"message":result,"page_no":pno,"limit":len(result)}, 200)
        else:
            return make_response({"message":"Data not found"}, 204)
    
    def user_upload_avatar_model(self,uid,filename):
        self.cur.execute(f"UPDATE users SET avatar='{filename}' WHERE id={uid}")
        if self.cur.rowcount>0:
            return make_response({"message":"File uploaded successfully"},201)
        else:
            return make_response({"message":"Nothing to update"},202)
        
    def user_login_model(self,data):
        str=f"SELECT id, name, email, phone, avatar, role_id"
        str+= " FROM users "
        str+= f"WHERE email = '{data['email']}' and password = '{data['password']}'"
        self.cur.execute(str)
        result=self.cur.fetchall()
        if len(result) == 1:
            userdata = result[0]
            exp_time = datetime.now() + timedelta(minutes=15)
            exp_epoch_time = int(exp_time.timestamp())
            payload={
                "payload":userdata,
                "exp":exp_epoch_time
            }
            token = jwt.encode(payload,"aditya",algorithm="HS256")
            return make_response({"toker":token},200)
        else:
            return make_response({"message":"USER NOT FOUND"},204)