from app import app
from model.user_model import user_model
from model.auth_model import auth_model
from flask import request, send_file
from datetime import datetime

obj=user_model()
auth=auth_model()

@app.route("/user/signup",methods=["POST"])
@auth.token_auth()
def user_signup_controller():
    return obj.user_signup_model(request.form)

@app.route("/user/updateuser",methods=["PUT"])
def user_update_controller():
    return obj.user_update_model(request.form)

@app.route("/user/deleteuser/<id>",methods=["DELETE"])
def user_delete_controller(id):
    return obj.user_delete_model(id)
 
@app.route("/user/getall")
@auth.token_auth()
def user_getall_controller():
    return obj.user_getall_model()

@app.route("/user/getall/limit/<limit>/page/<pno>",methods=["GET"])
def user_pagination_controller(limit,pno):
    return obj.user_pagination_model(limit,pno)

@app.route("/user/patch/<id>", methods=["PATCH"])
def user_patch_controller(id):
    return obj.user_patch_model(id,request.form)

@app.route("/user/<uid>/upload/avatar", methods=['PUT'])
def user_upload_avatar_controller(uid):
    file = request.files['avatar']
    uniqueFileName = str(datetime.now().timestamp()).replace(".", "")
    fileNameSplit = str(file.filename).split(".");
    extension = fileNameSplit[len(fileNameSplit)-1]
    finalFileNameWithPath=f"uploads/{uniqueFileName}.{extension}"
    file.save(finalFileNameWithPath)
    return obj.user_upload_avatar_model(uid,finalFileNameWithPath)

@app.route("/uploads/<filename>")
def user_get_avatar_controller(filename):
    return send_file(f"uploads/{filename}")

@app.route("/user/login",methods=['POST'])
def user_login_controller():
    return obj.user_login_model(request.form)


