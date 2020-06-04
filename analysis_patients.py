
from sklearn.pipeline import make_pipeline
from sklearn.svm import SVC 
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import SelectKBest, f_classif

#################################### PREPROCESSING ######################################

# Fonction d'encodage 
def encodage(df):
    code = {'positive':1, 'negative':0, 'detected':1, 'not_detected':0}
    for col in df.select_dtypes('object').columns:
        df.loc[:,col] = df[col].map(code)
    return df 

# Fonction Imputation 
def imputation(df):
    df = df.dropna(axis=0)
    return df

def final_preprocessing(df):
    df = encodage(df)
    df = imputation(df)
    
    features = ['Patient age quantile', 'Hemoglobin', 'Platelets', 'Leukocytes', 'Eosinophils', 'Monocytes', 'Rhinovirus/Enterovirus']
    X = df[features]
    y = df['SARS-Cov-2 exam result']
    
    return X,y

##################################### PREDICTION ########################################

def model_prediction(X_patient,X,y):
    final_model = make_pipeline(SelectKBest(f_classif, k=7), StandardScaler(), SVC(random_state=0))
    final_model.fit(X, y)
    return final_model.predict(X_patient)


##################################### COVID RESULT ######################################

def covid_prediction(X_patient,df):
    ### preprocessing 
    X, y = final_preprocessing(df)
    
    ### fit 
    model_prediction(X_patient,X, y)

    ### prediction
    return int(model_prediction(X_patient,X,y))




##################################### FINAL ANSWER ######################################

def answer(X_input,data,patient): 
    '''
    prediction = True : covid positif 
    prediction = False : covid negative
    patient = 1 : patient 
    patient = 0 : praticien  
    '''
    if (covid_prediction(X_input,data) == 1 and patient == 1): 
        return "Il y a de fortes chances que vous ayez contracté le Covid-19. Veuillez contactez votre médecin au plus vite."
    if (covid_prediction(X_input,data) == 1 and patient == 0): 
        return "Il y a de fortes chances que le patient ait contracté le Covid-19."
    elif(covid_prediction(X_input,data) == 0 and patient == 1):
        return "Il semblerait que vous n'ayez pas contracté le Covid-19. Attendez quelques jours avant de vous présenter au service de santé le plus proche."
    elif(covid_prediction(X_input,data) == 0 and patient == 0):
        return "Il semblerait que le patient n'ait pas contracté le Covid-19."