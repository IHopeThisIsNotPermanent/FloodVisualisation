import sqlite3
import random
import string
import json
from flask import Flask, request
from flask_cors import *
from flask import make_response

app=Flask(__name__)
CORS(app, resources=r'/*', supports_credentials=True)


#this is the front page
@app.route("/")
@cross_origin()
def deal_nothing():
    return "hello this is the front page '/'"

#this is the page to send comment, useless but I still leave it here
@app.route("/commentSend")
@cross_origin()
def deal_commentSend_request():
    temp_dict=request.values

    #The format of the json data from front end  to back end is the dicitionary. (key and value, and use "get" to catch the value)
    #Below is the examples.
    #receiver_temp = temp_dict.get("receiver")
    #comment_temp = temp_dict.get("comment")
    #user_current_cookie=request.cookies.get("user_token")
    #sender_temp=request.cookies.get("user")
    
    if cookie_dictionary[sender_temp] == user_current_cookie:
        conn = sqlite3.connect('password_name.db')
        print("Opened database successfully");

        conn.execute("INSERT INTO COMMENT (SENDER,RECEIVER,COMMENT) VALUES ('" + sender_temp + "','" + receiver_temp + "','" + comment_temp + "')")
        
        conn.commit()
        conn.close()
        print("Operation done successfully")
        return "message send!"
    return "Wrong cookie, get out!"
    
@app.route("/checkComment")
@cross_origin()
def deal_checkComment_request():
    temp_dict=request.values
    
    user_current_cookie=request.cookies.get("user_token")
    sender_temp=request.cookies.get("user")
    
    global cookie_dictionary
    if cookie_dictionary[sender_temp] == user_current_cookie:
        conn = sqlite3.connect('password_name.db')
        cursor = conn.execute("SELECT comment from COMMENT WHERE receiver='" + sender_temp + "'")
        temp_data={}
        i=1
        for row in cursor:
            temp_data.update({i:row[0]})
            i=i+1
        return json.dumps(temp_data)


@app.route("/login")
@cross_origin()
def deal_login_request():
    temp_dict=request.values
    password_temp = temp_dict.get("password")
    name_temp = temp_dict.get("name")
    comments = []
    conn = sqlite3.connect('password_name.db')
    print("Opened database successfully");

    cursor = conn.execute("SELECT id from COMPANY WHERE name='" + name_temp + "' and password='" + password_temp+"'")
    
    for row in cursor:
            
    
        temp_cookie_token=name_temp+name_temp+name_temp#''.join(random.sample(string.printable,20)).encode('latin_1')
        global cookie_dictionary
        cookie_dictionary.update({name_temp: temp_cookie_token})
        
        resp=make_response("ok")
        resp.set_cookie("user", name_temp)
        resp.set_cookie("user_token", temp_cookie_token)
        
        conn.close()
        resp.headers['Access-Control-Allow-Credentials'] = 'true'
        resp.headers['Access-Control-Allow-Origin'] = "http://127.0.0.1:5000"
        return resp
    conn.close()
    return "no such he/she/they"

    print("Operation done successfully");
    
    

@app.route("/register")
@cross_origin()
def deal_register_request():
    #print(request.values)
    temp_dict=request.values
    password_temp = temp_dict.get("password")
    name_temp = temp_dict.get("name")
    
       
    conn = sqlite3.connect('password_name.db')
    print("Opened database successfully")
    global seqid
    seqid=seqid+1
    sqlstr="INSERT INTO COMPANY (ID,name,password) VALUES (" + str(seqid) + ",'" + name_temp + "','" + password_temp + "')"
    #print(sqlstr)
    conn.execute(sqlstr)
    
    conn.commit()
    print("Records created successfully")
    conn.close()
    return "this is register page"
    
    
app.run()

#-------------------------------------------------

