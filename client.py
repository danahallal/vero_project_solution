import pandas
from flask_restful import Resource
from datetime import  date
import json
import csv
import openpyxl
from openpyxl.styles import PatternFill

#read data from vehicles.csv
csv_path="vehicles.csv"
with open("vehicles.csv") as data_file:
    data = pandas.read_csv(data_file,sep=";")
    API_REQUESTS = data.to_string()
#transmit the data in vehicles.csv to the api adresse :
class transmit_csv(Resource):
    def get(self):
        return f'{API_REQUESTS}'



#transfer the json data to csv:
with open('web_data.json') as json_file:
    jsondata = json.load(json_file)
    df = pandas.read_json(r'web_data.json')
    df.to_csv(r'web_data.csv', index=None)

#merge the 2 csv in one file:
desired_columns = ['rnr', 'gruppe', 'kurzname', 'langtext', 'info', 'sort', 'lagerort', 'lteartikel',
                       'businessUnit', 'vondat', 'bisdat', 'hu', 'asu', 'createdOn', 'editedOn', 'fuelConsumption',
                       'priceInformation', 'safetyCheckDate', 'tachographTestDate', 'gb1', 'ownerId', 'userId',
                       'externalId', 'vin', 'labelIds', 'bleGroupEnum', 'profilePictureUrl', 'thumbPathUrl']

desired_rows = []


def fill_desired_rows(filename, delimiter_value):
        with open(filename, 'r') as f:
             reader = csv.DictReader(f, delimiter=delimiter_value)
             for row in reader:
                row_info = {}
                for column in desired_columns:
                    if column in row:
                        row_info[column] = row[column]
                    else:
                        row_info[column] = None
                desired_rows.append(row_info)


fill_desired_rows("vehicles.csv", ';');
fill_desired_rows("web_data.csv", ',');

with open('output.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=desired_columns)
        writer.writeheader()
        writer.writerows(desired_rows)


#convert the merged csv file  to excel file:
default=True
k=input(str("enter your keyword-k/--keys:"))
c=input("enter True or False if you want the data colored:" or default).lower().capitalize()

def convert_to_excel(keys,colored):
        #set today's date":
        today_date=date.today()
        #set my xlsx file name :
        excel_file_name=f"vehicles_{today_date}.xlsx"
        #convert data to excel:
        with open("output.csv") as data_file:
            data = pandas.read_csv(data_file, sep=',')
            excel_writer=pandas.ExcelWriter(excel_file_name)
            DATA=data.to_excel(excel_writer,index=None,header=True)
            excel_writer.close()


#
# Rows are sorted by response field gruppe
# Columns always contain rnr field
# Only keys that match the input arguments are considered as additional columns (i.e. when the script is invoked with kurzname and info, print two extra columns)
# If labelIds are given and at least one colorCode could be resolved, use the first colorCode to tint the cell's text (if labelIds is given in -k)
# If the -c flag is True, color each row depending on the following logic:
# If hu is not older than 3 months --> green (#007500)
# If hu is not older than 12 months --> orange (#FFA500)
# If hu is older than 12 months --> red (#b30000)





transmit_csv()
convert_to_excel(k,c)
