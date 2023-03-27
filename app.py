from flask import Flask, render_template, request, url_for
import pandas as pd
import pickle

app = Flask(__name__)

# Load the pickled model
with open('pipe.pkl', 'rb') as f:
   model = pickle.load(f)
with open('pipe2.pkl', 'rb') as f:
   model2 = pickle.load(f)
with open('pipe3.pkl', 'rb') as f:
   model3 = pickle.load(f)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/inn2', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Extract the form data
        form_data = request.form
        batting = form_data['batting']
        bowling = form_data['bowling']
        city = form_data['city']
        target = float(form_data['target'])
        score = float(form_data['score'])
        overs = float(form_data['overs'])
        wickets = float(form_data['wickets'])
        runs_left=target-score
        balls_left=120-6*overs
        crr=score/overs
        rrr=(runs_left/balls_left)*6
        if(wickets>10):
            error=1
        # Make the prediction
        see={'batting_team':[batting],'bowling_team':[bowling], 'city':[city],'runs_left':[runs_left], 'balls_left':[balls_left], 'wickets':[10-wickets], 'total_runs_x':[target], 'crr':[crr], 'rrr':[rrr]}
        df = pd.DataFrame(see)
        output=model.predict_proba(df)
        #prediction = model.predict([[batting, bowling, city, runs_left, balls_left, (1-wickets), target, crr, rrr]])
        return render_template('form.html', batting_team=batting ,message=round((1-output[0][0])*100,2), bowling_team=bowling, error=0)
    return render_template('form.html')

@app.route('/inn1', methods=['GET', 'POST'])
def inning():
        if request.method == 'POST':
            # Extract the form data
            form_data = request.form
            batting = form_data['batting']
            bowling = form_data['bowling']
            city = form_data['city']
            score = float(form_data['score'])
            overs = float(form_data['overs'])
            wickets = float(form_data['wickets'])
            crr=score/overs

            see={'batting_team':[batting],'bowling_team':[bowling], 'city':[city],'current_score':[score], 'ball':[6], 'over':[overs], 'wickets':[10-wickets], 'crr':[crr]}
            pf = pd.DataFrame(see)
            output=model2.predict_proba(pf)
            ans=round((1-output[0][0])*100,1)
            return render_template('form2.html', batting_team=batting ,message=ans, bowling_team=bowling, error=0)
        return render_template('form2.html')

@app.route('/prematch', methods=['GET', 'POST'])
def pre():
        if request.method == 'POST':
            # Extract the form data
            form_data = request.form
            batting = form_data['batting']
            bowling = form_data['bowling']
            city = form_data['city']

            see={'batting_team':[batting],'bowling_team':[bowling], 'city':[city]}
            kf = pd.DataFrame(see)
            output1=model3.predict_proba(kf)
            ans=round((1-output1[0][0])*100,2)
            return render_template('form3.html', batting_team=batting ,message=ans, bowling_team=bowling, error=0)
        return render_template('form3.html')

if __name__ == '__main__':
    app.run()