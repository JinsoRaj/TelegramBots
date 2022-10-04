import json

with open("data.json", "r") as myfile:
    json_data=json.load(myfile)

def get_question(entry_point):
    for i in json_data['data']:
        if entry_point in i['entry_points']: return i
    return None

def get_answered_question(choosen):
    for question in json_data['data']:
        for answer in question['a']:
            if answer['callback'] == choosen: return (question['q'], answer['text']) 
    return (None, None)