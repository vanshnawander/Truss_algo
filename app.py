from flask import *
import sqlite3
from algo_part2 import mlalgo
from flask_session import Session
from flask_socketio import *
import subprocess as sp
from flask import request, redirect
from flask import render_template
import pymysql

app = Flask(__name__)

try:
    connection=pymysql.connect(host="truss.clwk1t6znrss.ap-south-1.rds.amazonaws.com",user='admin',password='axtrixninjastar321',db='truss', autocommit=True)
    cursor=connection.cursor()
except Exception as e:
    print("database conn failed")
# this is the entry point
application = app
#app.config["SESSION_PERMANENT"] = False
app.debug = True
app.config['SECRET_KEY'] = 'secret'	
app.config['SESSION_TYPE'] = 'filesystem'

Session(app)

socketio = SocketIO(app, manage_session=False)

# Sign In Page
@app.route('/')
def home():
	return render_template('index.html')

@app.route('/example')
def example():
	out=sp.run(["../php/form.php"], stdout=sp.PIPE)
	return out.stdout




#Sign In Page
@app.route('/signin',methods = ['POST', 'GET'])
def login():
	if request.method == 'POST':
		username = request.form['mail']
		password = request.form['passWord']
		session['email'] = username
		return redirect(url_for('dashboard'))
	else:
		return render_template('signin.html')
	
#After login for now
@app.route('/dashboard', methods=["POST", "GET"])
def dashboard():
	# LoginData = request.form['result']
	# print(data)
	# return render_template('afterLogIn.html',data=data)  , data=data
	print(session['email'])
	users=mlalgo(session['email'])
	users = [d for d in users if d.get('email') != session['email']]
	ans = cursor.execute(f"select * from truss_data where email!='{session['email']}' LIMIT 20")
	data2 = cursor.fetchall()
	print(session['email'])
	return render_template('finder.html', data=users,data2=data2)

@app.route('/profile', methods=["POST", "GET"])
def profile():
	profileData=request.form['result']
	print(profileData)
	data=cursor.execute(f"select * from truss_data where email='{profileData}'")
	data=cursor.fetchone()
	return render_template('otherProfile.html')

@app.route('/profile1', methods=["POST", "GET"])
def profile1():
	profileData=request.form['result1']
	print(profileData)
	data=cursor.execute(f"select * from truss_data where email='{profileData}'")
	data=cursor.fetchone()
	print(data)
	return render_template('otherProfile.html',data=data)

#Sign Up Page
@app.route('/signup1')
def signup1():
    # if request.method=='POST':
    #     email=request.form.get('emailAddress')
    #     return redirect(url_for('signup2',email=email))
    return render_template('signup.html')
    
@app.route('/signup2')
def signup2():
    # email=request.args.get('email',None)       
	return render_template('setpass.html')

#add signup2 to database
@app.route('/signup2_add',methods = ['POST', 'GET'])
def signup2_add():
	if request.method == 'POST':
		pass1 = request.form['pass']
		pass2 = request.form['pass2']
		if pass1==pass2:
			try:
				con = sqlite3.connect("MVP.sqlite3")
				cur = con.cursor()
				cur.execute("UPDATE user SET password = (?) WHERE user.id = (?);",(pass1, addedUserId))
				con.commit()
				return redirect(url_for('signup3'))
			except:
				con.rollback()
				error = "error!"
				return render_template('setpass.html',error = error)
		else:
			error="Password Does Not Match"
			return render_template('setpass.html',error = error)


#done with upload
@app.route('/upload')
def upload():
	return render_template('upload.html')
	
#Input Instituon
@app.route('/signup3')
def signup3():
	return render_template('instituion.html')

#add signup3 to database
@app.route('/signup3_add',methods = ['POST', 'GET'])
def signup3_add():
	if request.method == 'POST':
		institutionName = request.form['institutionName']
		course = request.form['course']
		year = request.form['year']
		try:
			con = sqlite3.connect("MVP.sqlite3")
			cur = con.cursor()
			cur.execute("UPDATE user SET institutionName = (?), course = (?), year = (?) WHERE user.id = (?);",(institutionName, course, year, addedUserId))
			con.commit()
			return redirect(url_for('signup4'))
		except:
			con.rollback()
			error = "error!"
			return render_template('instituion.html',error = error)
		


#Input Founder or Co-Founder
@app.route('/signup4')
def signup4():
	return render_template('forcof1.html')

#If Founder
@app.route('/signupIfFounder1')
def signupIfFounder1():
	role="founder"
	try:
		con = sqlite3.connect("MVP.sqlite3")
		cur = con.cursor()
		cur.execute("UPDATE user SET role = (?) WHERE user.id = (?);",(role, addedUserId))
		con.commit()
		return redirect(url_for('signup5F'))
	except:
		con.rollback()
		return redirect(url_for('signup1'))

#If CoFounder
@app.route('/signupIfCoFounder1')
def signupIfCoFounder1():
	role="Cofounder"
	try:
		con = sqlite3.connect("MVP.sqlite3")
		cur = con.cursor()
		cur.execute("UPDATE user SET role = (?) WHERE user.id = (?);",(role, addedUserId))
		con.commit()
		return redirect(url_for('signup5CF'))
	except:
		con.rollback()
		return redirect(url_for('signup1'))

#Input Founder Data
@app.route('/signup5F')
def signup5F():
	return render_template('founder.html')
	
#Input Founder skill Data
@app.route('/signup5F2')
def signup5F2():
	return render_template('founderSkill.html')



#Input CoFounder Data
@app.route('/signup5CF')
def signup5CF():
	return render_template('cofounder.html')
	
#Input CoFounder skill Data
@app.route('/signup5CF2')
def signup5CF2():
	return render_template('cofounderSkill.html')


#done with signup
@app.route('/thankyou')
def thankyou():
	return render_template('thankyou.html')


	
#under develoupment
@app.route('/ud')
def ud():
	return render_template('ud.html')

#other peoples profile



#Finder Page
@app.route('/finder',methods = ['POST', 'GET'])
# @app.route('/finder')
def finder():
    # data = request.form
    # data = "Hi Prasanna!"
	return render_template('finder.html')

#Finder Page


#CreateFriendRequest
@app.route('/send_friend_request', methods=['POST'])
def send_friend_request():
    sender_id = 91
    recipient_id = 92 
    request = FriendRequest(sender_id=sender_id, recipient_id=recipient_id, status='pending')
    db.session.add(request)
    db.session.commit()
    return render_template('requestSent.html')
    
    
#acceptFriendRequest
@app.route('/view_friend_requests')
def view_friend_requests():
    # user_id = session['user_id']
    user_id = 92
    requests = FriendRequest.query.filter_by(recipient_id=user_id, status='pending').all()
    return render_template('notifications.html', requests=requests)
    
    
    
@app.route('/chat')
def chat():
	return render_template('chatsystem.html')

#Finder Page
# @app.route('/chat',methods = ['POST', 'GET'])
# def chat():
# 		userid=session["SignedInUserId"]
# 		con = sqlite3.connect("MVP.sqlite3")
# 		cur = con.cursor()
# 		cur.execute("SELECT firstName FROM user WHERE user.id=(?)",(userid,))
# 		account=cur.fetchone()
# 		username=account[0]
# 		room=1
# 		session["username"]=username
# 		session["room"]=room
# 		return render_template('chatsystem.html',session=session)


# @socketio.on('join', namespace='/chat')
# def join(message) :
# 	room = session.get('room')
# 	join_room(room)
# 	emit ('status', {'msg': session.get('username') + ' has entered the room.'}, room=room)

# @socketio.on('text', namespace='/chat')
# def text(message):
#     room = session.get('room')
#     emit('message', {'msg': session.get('username') + ' : ' + message['msg']}, room=room)

# @socketio.on('left', namespace='/chat')
# def left(message):
#     room = session.get('room')
#     username = session.get('username')
#     leave_room(room)
#     emit('status', {'msg': username + ' has left the room.'}, room=room)

if __name__ == '__main__':
	#app.run(debug=True)
	socketio.run(app)

