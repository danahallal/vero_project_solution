import pandas
from flask_restful import Api
from flask import Flask
from client import transmit_csv
import requests
import json
url = "https://api.baubuddy.de/index.php/login/"
all_data_end_point= "https://api.baubuddy.de/dev/index.php/v1/vehicles/select/active"
label_ID_end_point="https://api.baubuddy.de/dev/index.php/v1/labels/{labelIds}"
payload = {
    "username": "365",
    "password": "1"
}
headers = {
    "Authorization":"Basic QVBJX0V4cGxvcmVyOjEyMzQ1NmlzQUxhbWVQYXNz",
    "Content-Type": "application/json",

}
#creat my rest api using flask
app=Flask(__name__)
api=Api(app)
transmit_csv()
api.add_resource(transmit_csv, "/csv")

#acess the access_token value from the url data :
response =requests.post( url,json=payload, headers=headers)
data=response.json()
access_token=data["oauth"]["access_token"]
#creat a new header with to change to set access token as value for "Authorization" key :
header_2={"Authorization":f"Bearer {access_token}",
    "Content-Type": "application/json",

}


#get the necessary data from the end point
response_1 = requests.request("GET", all_data_end_point, json=payload, headers=header_2)
Dataset=response_1.text
DATA=json.loads(Dataset)


#filtering hu with null values :
for data in DATA:
    for keys ,values in list(data.items()):
        if(data[keys]==None and keys=='hu'):
                   del data[keys]



#tried to reach the data to fix labelID but it's not workking
response_2=requests.request("GET",label_ID_end_point,json=payload,headers=header_2)


#return data sturcutre to json format:
FILTERED_DATA=json.dumps(DATA)


with open('web_data.json') as json_file:
   jsondata = json.load(json_file)
df = pandas.read_json (r'web_data.json')
df.to_csv(r'web_data.csv', index = None)





if __name__=="__main__":
    app.run(debug=True)
