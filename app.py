from flask import Flask,render_template,request,session,redirect,url_for
from flask_socketio import SocketIO,leave_room,join_room,send
import random
from config import settings
from string import ascii_uppercase

app = Flask(__name__)
app.config["SECRET_KEY"] = settings.SECRET_KEY
socketio = SocketIO(app)

rooms = {}

def generate_room_code(length):
  while True:
    code = ""
    for _ in range(length):
      code += random.choice(ascii_uppercase)
    if code not in rooms:
      break
  return code

@app.route("/", methods=["POST","GET"])
def home():
  session.clear()
  if request.method == "POST":
    name = request.form.get("name")
    room = request.form.get("room-id")
    #passkey = request.form.get("passkey")
    join = request.form.get("join",False)
    create = request.form.get("create",False)

    if not name:
      return render_template('home.html',error=["pick a username"],name=name,code=room)

    if join != False and not room:
      return render_template('home.html',error=["please specify room code"],name=name,code=room)

    room_code = room

    if create != False:
      room_code = generate_room_code(4)
      admin = name
      rooms[room_code] = {
        "admin":admin,
        "members":0,
        "messages":[]
      }
      session["admin"] = admin

    elif room_code not in rooms:
      return render_template("home.html",error=["Room does not exist"],name=name,code=room)
     
    session["name"] = name
    session["room"] = room_code
    
    
    return redirect(url_for("room"))


  return render_template("home.html")


@app.route("/room",methods=["POST","GET"])
def room():
  room = session.get('room')
  admin = session.get('admin')

  print(admin)
  if room is None or session.get('name') is None or room not in rooms:
    return redirect(url_for("home"))

  return render_template("room.html",room=room) 

@socketio.on("connect")
def connect(auth):
  room = session.get('room')
  name = session.get('name')
  admin = session.get("admin")

  if not name or not room:
    return
  
  if room not in rooms:
    leave_room(room)
    return

  origin:str = "same-origin"
  join_room(room)
  send({"name":name,"message":"has entered the room","origin":origin},to=room)
  rooms[room]["members"] += 1
  print(f"{name} has joined the room")

@socketio.on("disconnect")
def disconnect():
  room = session.get('room')
  name = session.get('name')

  if room in rooms:
    rooms[room]["members"] -= 1
    if rooms[room]["members"] <= 0:
      del rooms[room]
  
  origin:str = "same-origin"
  
  send({"name":name,"message":"has left the room","origin":origin},to=room)
  print(f"{name} has left room {room}")

@socketio.on("message")
def incoming_msg(data:dict):
  name = session.get('name')
  room = session.get('room')
  admin = session.get('admin')

  if room not in rooms:
    return

  origin = "diff-origin"

  content = {
    "name":session.get('name'),
    "message":data.get('data'),
    "origin": origin
  }
  send(content,to=room)
  rooms[room]["messages"].append(content)

if __name__ == "__main__":
  socketio.run(app,debug=True,port=5590,host="0.0.0.0")