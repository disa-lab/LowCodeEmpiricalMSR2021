import xml.etree.ElementTree as ET
import pandas as pd
import csv
import traceback
import sys


FILE = 'Posts.xml'
EXTRACTEDFILE = 'output_2.csv'
output_file_name = "output_2.csv"

TAGS = ['google-app-maker', 'appian', 'outsystems', 'zoho', 'mendix', 'powerapps', 'quickbase', 'vinyl', 'salesforce-lightning', 'powerapps-formula', 'lwc', 'lightning',
        'powerapps-selected-items', 'powerapps-collection', 'salesforce-communities', 'powerapps-canvas', 'salesforce-chatter', 'salesforce-service-cloud', 'aura-framework']
COLS = ["Id", "PostTypeId", "AcceptedAnswerId", "ParentId", "CreationDate", "DeletionDate", "Score", "ViewCount", "Body", "OwnerUserId", "OwnerDisplayName", "LastEditorUserId",
        "LastEditorDisplayName", "LastEditDate", "LastActivityDate", "Title", "Tags", "AnswerCount", "CommentCount", "FavoriteCount", "ClosedDate", "CommunityOwnedDate", "ContentLicense", "AcceptedAnswer"]
        
def updater(header, data, filename):
    with open(filename, "w", newline="", encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=header)
        writer.writeheader()
        writer.writerows(data)


df = pd.read_csv(EXTRACTEDFILE)
answerIdDict = {}
for index, row in df.iterrows():
    # access data using column names
    temp = row['AcceptedAnswerId']
    # collect only not nan vlues with indexes
    if not (temp != temp):
        answerIdDict[int(temp)] = index
print(len(answerIdDict))


context = ET.iterparse(FILE, events=("start", "end"),
                       parser=ET.XMLParser(encoding='utf-8'))


with open(output_file_name, newline='', encoding='utf-8') as file:
    readData = [row for row in csv.DictReader(file)]
    _, root = next(context)
    for event, elem in context:
        if event == "end" and elem.tag == "row":
            ansId = int(elem.attrib.get('Id', 'None'))
            if ansId in answerIdDict:
                index = answerIdDict[ansId]
                readData[index]['AcceptedAnswer'] = elem.attrib.get("Body", '')
                readData[index]['AcceptedAnswerCreationDate'] = elem.attrib.get('CreationDate', '')
                readHeader = readData[index].keys()
                updater(readHeader, readData, output_file_name)
            # progress
            if int(elem.attrib['Id']) % 100000 == 0:
                print('done', elem.attrib['Id'])
            elem.clear()
            root.clear()

        
 
