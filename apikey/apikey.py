import json

def getlist():
    with open('./apikey/apikey.json', 'r', encoding="cp949") as file:
        json_data = json.load(file)
    return json_data

def getapi(name):
    json_data = getlist()
    if name not in json_data.keys():
        print("사전에 수강하시겠다고 응답하신 분들에게만 api key가 발급됩니다. OpenAI 홈페이지에 가서 키를 발급받아주세요")
        return 0
    else:
        print("api key 발급성공")
        return json_data[name]