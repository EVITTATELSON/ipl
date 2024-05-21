from flask import Flask, render_template, request, url_for, redirect ,session
import pickle
import numpy as np

app = Flask(__name__)
app.secret_key = 'your_secret_key'
with open('model.pkl', 'rb') as file:
    model = pickle.load(file)

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

client = MongoClient("mongodb+srv://admin:mongo@cluster0.imbdhgi.mongodb.net/",server_api=ServerApi('1'))
mongo = client["myDatabase"]
users_collection = mongo['users']

@app.route("/")
def home():
    return render_template("homepage.html")


@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        # Get form data
        first_name = request.form['fname']
        last_name = request.form['lname']
        username = request.form['uname']
        email = request.form['email']
        password = request.form['password']
        
       
        
        # Insert user data into MongoDB
        user_data = {
            'first_name': first_name,
            'last_name': last_name,
            'username': username,
            'email': email,
            'password': password
        }
        users_collection.insert_one(user_data)
        
        # Redirect to login page
        return redirect(url_for('login'))
    else:
        return render_template('createpage.html')

# Route for user login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get form data
        username = request.form['username']
        password = request.form['password']

        # Validate user credentials against MongoDB
        user = users_collection.find_one({'username': username, 'password': password})
        if user:
            session['username'] = username
            # Authentication successful, redirect to home page
            return redirect(url_for('match'))
        else:
            # Authentication failed, redirect back to login page with error message
            return render_template('loginpage.html', error='Invalid username or password')
    else:
        return render_template('loginpage.html')

# Route for the match page
@app.route('/match')
def match():
    if 'username' not in session:  # Check if user is logged in
        return redirect(url_for('login'))
    return render_template("matchpage.html")

#LOGOUT
@app.route('/logout')
def logout():
    session.pop('username', None)  # Remove username from session
    return redirect(url_for('home'))

#model function
def score_predict(venue,innings,ball,batting_team, bowling_team,runs,cruns,cwicket):
  bat=[]
  bowl=[]
  stadium=[]
  #venue
  if venue == 'Arun Jaitley Stadium':
    stadium=[1,0,0,0,0,0,0,0,0,0,0]
  elif venue == 'Dr. Y.S. Rajasekhara Reddy ACA-VDCA Cricket Stadium':
    stadium=[0,1,0,0,0,0,0,0,0,0,0]
  elif venue == 'Eden Gardens':
    stadium=[0,0,1,0,0,0,0,0,0,0,0]
  elif venue == 'Himachal Pradesh Cricket Association Stadium':
    stadium=[0,0,0,1,0,0,0,0,0,0,0]
  elif venue == 'M. A. Chidambaram Stadium':
    stadium=[0,0,0,0,0,1,0,0,0,0,0]
  elif venue == 'M. Chinnaswamy Stadium':
    stadium=[0,0,0,0,1,0,0,0,0,0,0]
  elif venue == 'Narendra Modi Stadium':
    stadium=[0,0,0,0,0,0,1,0,0,0,0]
  elif venue == 'Punjab Cricket Association IS Bindra Stadium':
    stadium=[0,0,0,0,0,0,0,1,0,0,0]
  elif venue == 'Rajiv Gandhi International Stadium':
     stadium=[0,0,0,0,0,0,0,0,1,0,0]
  elif venue == 'Sawai Mansingh Stadium':
     stadium=[0,0,0,0,0,0,0,0,0,1,0]
  elif venue == 'Wankhede Stadium':
    stadium=[0,0,0,0,0,0,0,0,0,0,1]
      
  # Batting Team
  if batting_team == 'Chennai Super Kings':
    bat=[1,0,0,0,0,0,0,0,0,0]
  elif batting_team == 'Delhi Capitals':
    bat=[0,1,0,0,0,0,0,0,0,0]
  elif batting_team == 'Gujarat Titans':
    bat= [0,0,1,0,0,0,0,0,0,0]
  elif batting_team == 'Kolkata Knight Riders':
    bat=[0,0,0,1,0,0,0,0,0,0]
  elif batting_team == 'Lucknow Super Giants':
    bat=[0,0,0,0,1,0,0,0,0,0]
  elif batting_team == 'Mumbai Indians':
    bat=[0,0,0,0,0,1,0,0,0,0]
  elif batting_team == 'Punjab Kings':
    bat= [0,0,0,0,0,0,1,0,0,0]
  elif batting_team == 'Rajasthan Royals':
    bat= [0,0,0,0,0,0,0,1,0,0]
  elif batting_team == 'Royal Challengers Bengaluru':
    bat=[0,0,0,0,0,0,0,0,1,0]
  elif batting_team == 'Sunrisers Hyderabad':
    bat=[0,0,0,0,0,0,0,0,0,1]
      
  # Bowling Team
  if bowling_team == 'Chennai Super Kings':
    bowl=[1,0,0,0,0,0,0,0,0,0]
  elif bowling_team == 'Delhi Capitals':
    bowl=[0,1,0,0,0,0,0,0,0,0]
  elif bowling_team == 'Gujarat Titans':
    bowl= [0,0,1,0,0,0,0,0,0,0]
  elif bowling_team == 'Kolkata Knight Riders':
    bowl=[0,0,0,1,0,0,0,0,0,0]
  elif bowling_team == 'Lucknow Super Giants':
    bowl=[0,0,0,0,1,0,0,0,0,0]
  elif bowling_team == 'Mumbai Indians':
    bowl=[0,0,0,0,0,1,0,0,0,0]
  elif bowling_team == 'Punjab Kings':
    bowl= [0,0,0,0,0,0,1,0,0,0]
  elif bowling_team == 'Rajasthan Royals':
    bowl= [0,0,0,0,0,0,0,1,0,0]
  elif bowling_team == 'Royal Challengers Bengaluru':
    bowl=[0,0,0,0,0,0,0,0,1,0]
  elif bowling_team == 'Sunrisers Hyderabad':
    bowl=[0,0,0,0,0,0,0,0,0,1]

  array=stadium+[innings,ball]+bat+bowl+[runs,cruns,cwicket]  
  prediction_array = np.array([array]) 
  print(prediction_array)
  pred = model.predict(prediction_array)
  return int(round(pred[0]))
  

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        venue=request.form['stadium']
        inn=int(request.form['Innings'])
        ball=float(request.form['currentBall'])
        batting=request.form['battingTeam']
        bowling=request.form['bowlingTeam']
        runs=int(request.form['currentRuns'])
        cruns=int(request.form['currentScore'])
        cwicket=int(request.form['currentWickets'])
        print("\nst:",venue,"\ninn:",inn,"\nball:",ball,"\nbat:",batting,"\nbowl:",bowling,"\nruns:",runs,"\ncruns:",cruns,"\ncwick:",cwicket)
        output=score_predict(venue,inn,ball,batting, bowling,runs,cruns,cwicket)
        print(output)
        # data = {
        #     'venue': [int(request.form['stadium'])],
        #     'innings': [1],
        #     'ball': [float(request.form['currentBall'])],
        #     'batting_team': [request.form['battingteam']],
        #     'bowling_team': [request.form['bowlingteam']],
        #     'runs': [float(request.form['currentScore'])],
        #     'current_r]uns': [float(request.form['currentScore'])],
        #     'wicket': [0],
        #     'current_wickets': [int(request.form['currentWickets'])]
        # }
        # input_data = pd.DataFrame(data)
        # print(input_data)
        # prediction = model.predict(input_data)
        # output = prediction[0]
        return render_template('predictpage.html', score=output)
if __name__ == "__main__":
    app.run(debug=True) 