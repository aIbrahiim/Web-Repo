from django.apps import AppConfig
from pickle import load
import os
import numpy as np
import pandas as pd

class ChatbotConfig(AppConfig):
    name = 'chatbot'

    #modelPath = os.path.join(projectPath,'finalized_model.sav')
    model = load(open("finalized_model.sav", "rb"))
    data_set = pd.read_pickle("main_data_frame.pkl")
    disease_indexed_data_frame = data_set.set_index('prognosis').drop('Sum', axis=1)

    feature_importance = model.feature_importances_
    indices = np.argsort(feature_importance)[::-1]
    features = data_set.columns.drop(['prognosis', 'Sum'])

    features_dict = {}
    for i,f in enumerate(features):
        features_dict[f] = i

    ASKING_LIMIT = 8
    
    # Create a DataFrame that hase the features in the index, and the importance as the data
    feature_importance_df = pd.concat([ pd.DataFrame(data=features, columns=['symptom']),
                                        pd.DataFrame(data=model.feature_importances_, 
                                        columns=['importance'])]
                                        , axis=1)

    feature_importance_df.set_index('symptom', inplace=True)

    # Sort the feature_importance_df by importance 
    sorted_feature_importance_df = feature_importance_df.sort_values('importance', ascending=False)

    # The top symptoms to be used to ask the user for input, iterating 4 times, and using 5 symptoms at a time.
    top_symptoms = sorted_feature_importance_df.iloc[:20].index.values
    




    def symptoms_of(disease):
        df = ChatbotConfig.disease_indexed_data_frame.loc[[disease], :]
        return df[df.columns[(df==1).any()]].columns

    def find_most_common_symptom(feature_importance_df, df=None, list_of_symptoms=None):
        if df is not None and list_of_symptoms is None:
            list_of_symptoms = ChatbotConfig.symptoms_in_dataframe(df)
        elif (df is None and list_of_symptoms is None) and (df is not None and list_of_symptoms is not None): 
            raise Exception("Must use either df OR a list of symptoms")
        
        highset_importance = 0.0
        highest_symptom = ''
        for symptom in list_of_symptoms:
            current_importance = feature_importance_df.loc[symptom].values[0]
            if current_importance > highset_importance:
                highset_importance = current_importance
                highest_symptom = symptom
        return highest_symptom

    def update_dataframe_with_symptom(df, symptom, has_symptom = False):
        if has_symptom:
            return df[df[symptom] > 0].drop(symptom, axis=1)
        else:
            return df[df[symptom] == 0].drop(symptom, axis=1)
    
    def find_top_n_common_symptom(df, n):
        common_symptoms = []
        list_of_symptoms = symptoms_in_dataframe(df)
        for i in range(n):
            common_symptom = find_most_common_symptom(feature_importance_df, list_of_symptoms=list_of_symptoms)
            common_symptoms.append(common_symptom)
            list_of_symptoms.remove(common_symptom)
        return common_symptoms

    
    

    def remaning_symptoms_of_possible_disease(possible_disease, already_asked):
        symptoms_of_possible_disease = list(ChatbotConfig.symptoms_of(possible_disease[0]))
        for symptom in already_asked.keys():
            if symptom in symptoms_of_possible_disease:
                symptoms_of_possible_disease.remove(symptom)
        return symptoms_of_possible_disease


    def symptoms_in_dataframe(df):
        """
        A method used to get the symptoms exists in a dataframe
        Input: df, the data frame we want to get the symptoms in it.
        Output: a list of the symptoms exist in the dataframe df.
        """
        symptoms_dict = {}
        for index, row in df.iterrows():
            row = row.dropna()
            disease_symptoms = row.index.tolist()
            for symptom in disease_symptoms:
                symptoms_dict[symptom] = 1
        return list(symptoms_dict.keys())