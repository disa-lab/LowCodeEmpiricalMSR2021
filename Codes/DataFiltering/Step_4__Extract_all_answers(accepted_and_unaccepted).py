import xml.etree.ElementTree as ET
import pandas as pd
import csv
import traceback
import sys


FILE = 'Posts.xml'
# SO_V6 = 'Ver_4__Questions_removed_duplicates.csv'
# SO_V6 = 'Ver_6__extracted_questions_with_accepted_answers_time.csv'
SO_V6 = 'output_3.csv'

TAGS = ['google-app-maker', 'appian', 'outsystems', 'zoho', 'mendix', 'powerapps', 'quickbase', 'vinyl', 'salesforce-lightning', 'powerapps-formula', 'lwc', 'lightning',
        'powerapps-selected-items', 'powerapps-collection', 'salesforce-communities', 'powerapps-canvas', 'salesforce-chatter', 'salesforce-service-cloud', 'aura-framework']
COLS = ["Id", "PostTypeId", "AcceptedAnswerId", "ParentId", "CreationDate", "DeletionDate", "Score", "ViewCount", "Body", "OwnerUserId", "OwnerDisplayName", "LastEditorUserId",
        "LastEditorDisplayName", "LastEditDate", "LastActivityDate", "Title", "Tags", "AnswerCount", "CommentCount", "FavoriteCount", "ClosedDate", "CommunityOwnedDate", "ContentLicense"]


df = pd.read_csv(SO_V6)
questionIdDict = {}
for index, row in df.iterrows():
    temp = row['Id']
    if not (temp != temp):
        questionIdDict[int(temp)] = index
print(len(questionIdDict))


context = ET.iterparse(FILE, events=("start", "end"),
                       parser=ET.XMLParser(encoding='utf-8'))


with open('AllAnswers__' + SO_V6, 'w', newline='', encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(COLS)
    _, root = next(context)
    for event, elem in context:
        if event == "end" and elem.tag == "row":
            parentId = int(elem.attrib.get('ParentId', '0'))
            if parentId in questionIdDict:
                data = []
                for col in COLS:
                    data.append(elem.attrib.get(col, ''))
                csvwriter.writerow(data)
                continue
            # progress
            if int(elem.attrib['Id']) % 100000 == 0:
                print('done', elem.attrib['Id'])
            elem.clear()
            root.clear()
 
