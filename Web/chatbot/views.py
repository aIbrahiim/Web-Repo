from django.shortcuts import render
from rest_framework.views import APIView
from django.http import HttpResponse, JsonResponse
from rest_framework import permissions
from .apps import ChatbotConfig
import json
import numpy as np
import codecs, json 
import pandas as pd
import pickle

# Create your views here.
class call_model(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, format=None):
        #GET request will reset and start new Conversion
        username = request.user.username
        lis = listMaker()
        session  = {'cnt':0,
                    'already_asked':{},
                    'symptoms_indicies_list': listMaker(),
                    'features_dict' : ChatbotConfig.features_dict,
                    'most_common_symptom': '',
                    'possible_disease':None,
                    'data' : "",
                    'dataShape' : 0,
                    'inLoop':"true",
                    'ynq':"false",
                    'solved':True,
                    'prev_asked_diseases' : []
                    }
        
        request.session[username] = session

        data =  primitive_asking_FirstPart(prev_asked_diseases=None,already_asked=None,data=ChatbotConfig.data_set)
        #print(data)
        q = primitive_asking_SecondPart(data,0)
        request.session[username]['cnt'] = 1
        
        #Create new temp pkl file to every user
        path = 'tempPkl/'+username+'.pkl'
        newFile = open(path,'wb')
        pickle.dump(data, newFile)
        newFile.close()
        session['dataShape'] = data.shape[0]
        session['data'] = path
        session['most_common_symptom'] = q

        return JsonResponse({'question':"Do you have "+q+"?"}, safe=False)

    def post(self, request, format=None):
        request.session.modified = True
        username = request.user.username
        #print(username)
        session = request.session[username]
                
        #get answer from json file
        body_unicode = request.body.decode('utf-8')
        body_data = json.loads(body_unicode)
        ans = str(body_data['ans'])

        if session['inLoop'] == "true":
            if session['dataShape'] > 0 and  session['cnt'] < ChatbotConfig.ASKING_LIMIT:
                primitive_asking_ThirdPart(
                    answer = ans,
                    already_asked = session['already_asked'],
                    dataPath = session['data'],
                    symptoms_indicies_list= session['symptoms_indicies_list'],
                    most_common_symptom = session['most_common_symptom'],
                    features_dict = session['features_dict']
                )
                
                data = pd.read_pickle(session['data'])
                session['dataShape'] = data.shape[0]

                request.session[username]['cnt']+=1
                q = primitive_asking_SecondPart(data,request.session[username]['cnt'])
                
                request.session[username]['most_common_symptom'] = q
                #print(request.session[username]['most_common_symptom'])

                print("in First")
                if q != "":
                    return JsonResponse({'question':"Do you have "+q+"?"}, safe=False)
                    
                else :
                    print("else Mode")
                    possible_disease = primitive_asking_ForthPart(session['symptoms_indicies_list'])
                    session['possible_disease'] = possible_disease[0]
                    session['prev_asked_diseases'].append(possible_disease[0])
                    session['inLoop'] = "False";
                    session['ynq'] = "true";
                    session['symptoms_of_possible_disease'] = ChatbotConfig.remaning_symptoms_of_possible_disease(possible_disease,session['already_asked'])
                    if session['cnt'] == ChatbotConfig.ASKING_LIMIT: session['cnt'] = 0
                        
                    # Ensuring asking
                    session['ys'] = 0
                    session['ns'] = 0
                    session['i'] = 0
                    session['range'] = len(range(int(len(session['symptoms_of_possible_disease'])*0.6//1)))
                    return JsonResponse( {'question':"Do you have "+session['symptoms_of_possible_disease'][session['i']]+"?"},safe=False)

  
        if session['ynq'] == "true":
            if session['i'] < session['range']:
                session['cnt'] +=1
                if session['cnt'] < ChatbotConfig.ASKING_LIMIT:
                    if ans == 'y':
                        session['already_asked'][session['symptoms_of_possible_disease'][session['i']]] = 1
                        session['ys'] +=1
                        print("yes")
                    else :
                        session['already_asked'][session['symptoms_of_possible_disease'][session['i']]] = 0
                        session['ns'] +=1
                        print("no")
                    
                    session['i'] +=1
                else :
                    session['cnt'] = 0
                
                if session['ys'] > session['ns']:
                    return JsonResponse({"disease":"It is likely you have :"+session['possible_disease']},safe=False)
                else :
                    session['solved'] = False
                    session['newItrate'] = False
                    
        

            if session['solved'] == False:    
                if session['newItrate'] == False:
                    data =  primitive_asking_FirstPart(
                                prev_asked_diseases = None,
                                already_asked=session['already_asked'],
                                
                                data = pd.read_pickle(session['data']),
                                )
                    q = primitive_asking_SecondPart(data,session['cnt']) 
                    session['cnt'] +=1
                    path = 'tempPkl/'+username+'.pkl'
                    newFile = open(path,'wb')
                    pickle.dump(data, newFile)
                    newFile.close()
                    session['dataShape'] = data.shape[0]
                    session['most_common_symptom'] = q
                    session['newItrate'] = True
                    session['inLoop2'] = True
                    return JsonResponse({'question':"Do you have "+q+"?"},safe=False)


                if session['dataShape'] > 0 and  session['cnt'] < ChatbotConfig.ASKING_LIMIT and session['inLoop2'] : 
                    primitive_asking_ThirdPart(
                        answer = ans,
                        already_asked = session['already_asked'],
                        dataPath = session['data'],
                        symptoms_indicies_list= session['symptoms_indicies_list'],
                        most_common_symptom = session['most_common_symptom'],
                        features_dict = session['features_dict']
                    )
                    data = pd.read_pickle(session['data'])
                    session['dataShape'] = data.shape[0]

                   
                    q = primitive_asking_SecondPart(data,session['cnt'])
                    session['cnt']+=1
                    session['most_common_symptom'] = q
                    if q != "" :
                        return JsonResponse({'question':"Do you have "+q+"?"},safe=False)
                    else:
                        possible_disease = primitive_asking_ForthPart(session['symptoms_indicies_list'])
                        session['prev_asked_diseases'].append(possible_disease[0])
                        session['symptoms_of_possible_disease'] = ChatbotConfig.remaning_symptoms_of_possible_disease(possible_disease, session['already_asked'])
                        if session['cnt'] == ChatbotConfig.ASKING_LIMIT: session['cnt'] = 0
                        # Ensuring asking
                        session['ys'] = 0
                        session['ns'] = 0
                        session['i'] = 0
                        session['inLoop2'] = False
                        session['range'] = len(range(int(len(session['symptoms_of_possible_disease'])*0.6//1)))
                        return JsonResponse({'question':"Do you have "+session['symptoms_of_possible_disease'][session['i']]+"?"},safe=False)

                if session['ynq'] == "true":
                    if session['i'] < session['range']:
                        session['cnt'] +=1
                        if session['cnt'] < ChatbotConfig.ASKING_LIMIT:
                            if ans == 'y':
                                session['already_asked'][session['symptoms_of_possible_disease'][session['i']]] = 1
                                session['ys'] +=1
                                print("yes")
                            else :
                                session['already_asked'][session['symptoms_of_possible_disease'][session['i']]] = 0
                                session['ns'] +=1
                                print("no")
                    
                    session['i'] +=1
                else :
                    session['cnt'] = 0
                
                if session['ys'] > session['ns']:
                    return JsonResponse({"disease":"It is likely you have :"+session['possible_disease']},safe=False)
                else :
                    data =  primitive_asking_FirstPart(
                                already_asked=session['already_asked'],
                                data = pd.read_pickle(session['data']))
                    q = primitive_asking_SecondPart(data,session['cnt']) 
                    session['cnt'] +=1
                    path = 'tempPkl/'+username+'.pkl'
                    newFile = open(path,'wb')
                    pickle.dump(data, newFile)
                    newFile.close()
                    session['dataShape'] = data.shape[0]
                    session['most_common_symptom'] = q
                    session['newItrate'] = True
                    session['inLoop2'] = True
                    return JsonResponse({'question':"Do you have "+session['symptoms_of_possible_disease'][session['i']]+"?"},safe=False)
                    
        return JsonResponse("error",safe=False)
        
 
        


def listMaker():
    lis = []
    lis = list(range(132))
    for i in range(132):
            lis[i]=0
    return lis

def setElement(elements,set):
    for e in elements:
        set[int(e)] = 1



def get_list_of_query(query):
    result = []
    for c in query:
        if c == 0 or c == 1:
            result.append(int(c))
    result = np.array(result)
    return result


def primitive_asking_FirstPart(prev_asked_diseases,data,already_asked):
    data = None
    if prev_asked_diseases is None:  #imp
        data = ChatbotConfig.data_set.copy().set_index('prognosis').drop('Sum', axis=1)
    else:
        data = ChatbotConfig.data_set.copy().set_index('prognosis').drop('Sum', axis=1).drop(prev_asked_diseases, axis=0)

    if already_asked is None:
        already_asked = {}

    try:
        # for symptom in already_asked.keys():
        # data.drop(symptom, axis=1, inplace=True)    
        for symptom, value in already_asked.items():
            if value == 1:
                data = ChatbotConfig.update_dataframe_with_symptom(data, symptom, has_symptom = True)
            else:
                data = ChatbotConfig.update_dataframe_with_symptom(data, symptom, has_symptom = False)
    except:
        pass

    #print("Testing droping diseases: " + str(data.shape[0]))

    return data


def primitive_asking_SecondPart(data,cnt):
    most_common_symptom = ""
    
    if data.shape[0] > 0 and cnt < ChatbotConfig.ASKING_LIMIT:  #--
        most_common_symptom = ChatbotConfig.find_most_common_symptom(ChatbotConfig.feature_importance_df, data)
        #print("The most common symptom: " + most_common_symptom)
    
    return most_common_symptom    


def primitive_asking_ThirdPart(answer,already_asked,dataPath,symptoms_indicies_list,most_common_symptom,features_dict):
    data = pd.read_pickle(dataPath)
    #print(data)
    if answer == 'y':
        already_asked[most_common_symptom] = 1
        
        #print("You have/feel " + most_common_symptom)
        
        data = ChatbotConfig.update_dataframe_with_symptom(data, most_common_symptom, has_symptom=True)
        
        #print("The new dataset shape: " + str(data.shape))
        symptoms_indicies_list[features_dict[most_common_symptom] ] += 1
        
        #print("The updated symptoms_idicies_list: \n" + str(symptoms_indicies_list))
        
    else:
        already_asked[most_common_symptom] = 0
        #data.drop(most_common_symptom, axis=1, inplace=True)
        data = ChatbotConfig.update_dataframe_with_symptom(data, most_common_symptom, has_symptom=False)
        #print("The new dataset shape: " + str(data.shape))

    newFile = open(dataPath,'wb')
    pickle.dump(data, newFile)
    newFile.close()

def primitive_asking_ForthPart(symptoms_indicies_list):
    
    symptoms_indicies_list_Np = get_list_of_query(symptoms_indicies_list)
    possible_disease = ChatbotConfig.model.predict(symptoms_indicies_list_Np.reshape(1, -1))
    return possible_disease


