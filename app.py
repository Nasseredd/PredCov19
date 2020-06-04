#! usr/bin/python
# -*- coding: utf-8 -*- 

from flask import Flask, request, render_template
import analysis_patients as ap 
import pandas as pd 

from sklearn.pipeline import make_pipeline
from sklearn.svm import SVC 
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import SelectKBest, f_classif

app = Flask(__name__)

############################# HOME ###########################

# Root view 
@app.route('/')
def default():
    return render_template('index.html')

###################### Praticien - Data ######################

file = 'data_analyse/data/dataset.xlsx'
raw_data = pd.read_excel(file)
df = raw_data.copy()

# missing rate 
mr = df.isna().sum()/df.shape[0]

blood_columns = list(df.columns[(mr < 0.9) & (mr > 0.88)])
viral_columns = list(df.columns[(mr < 0.80) & (mr > 0.75)])
add_colomns = ['Patient age quantile', 'SARS-Cov-2 exam result']

praticien_df = df[add_colomns + blood_columns + viral_columns]

########################### PATIENTS #########################

# patients path 
@app.route('/patients.html')
def patients():
    return render_template('patients.html')

# Form view 
@app.route('/send', methods=['GET','POST'])
def send():
    if request.method == 'POST': 

        #features_list = ['gender','fever','tiredness','dry_cough','nasal_congestion','runny_nose','diarhea','contact']
        
        # Features Extraction
        #liste = []
        #i = 0 
        #for i in range(len(features_list)):
        #    liste.append(request.form[features_list[i]])

        #Create a dataframe 
        #df = pd.DataFrame(liste).transpose()

        # Extract a simple answer 
        #age = float(request.form[0])

        # Extract answer from a radio button 
        #option = request.form['example']

        # Create a dataframe from answers 
        


        return render_template('answer-patients.html')#, answer=ap.answer(df,1), test=liste[2]) 
    else:
        return render_template('patients.html')

########################## Praticiens ########################

@app.route('/praticiens.html')
def praticiens():
    return render_template('praticiens.html')

# Form view 
@app.route('/send_praticiens', methods=['GET','POST'])
def send_praticiens():
    if request.method == 'POST': 
        # Extract a simple answer 
        #age = float(request.form['age'])

        # Extract answer from a radio button 
        #option = request.form['example']

        # positive example  
        # 14,1.042812,-1.245998,-1.085284,-0.835508,-0.745508,0

        # negative example 
        # 

        # Create a dataframe from answers 
        columns = ['Patient age quantile', 'Hemoglobin', 'Platelets', 'Leukocytes','Eosinophils', 'Monocytes', 'Rhinovirus/Enterovirus']
        names = ['age', 'Hemoglobin', 'Platelets', 'Leukocytes','Eosinophils', 'Monocytes']
        values = []
        for item in names:
            values.append(float(request.form[item]))
        values.append(request.form['Rhino'])

        X_input = pd.DataFrame(values).transpose()
        X_input.columns = columns

        return render_template("answer-praticiens.html", answer=ap.answer(X_input,praticien_df,0)) 
    else:
        return render_template('praticiens.html')

############################# ABOUT ############################

@app.route('/about.html')
def about():
    return render_template('about.html')

############################ CONTACT ###########################

@app.route('/contact.html')
def contact():
    return render_template('contact.html')

















if __name__ == "__main__":
    app.run(debug=True)