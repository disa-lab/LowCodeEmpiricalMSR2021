import pandas as pd

COLS = ['google-app-maker', 'appian', 'outsystems', 'zoho', 'mendix', 'powerapps',
        'quickbase', 'vinyl', 'salesforce-lightning', 'powerapps-formula', 'lwc', 'lightning',
        'powerapps-selected-items', 'powerapps-collection', 'salesforce-communities',
        'powerapps-canvas', 'salesforce-chatter', 'salesforce-service-cloud', 'aura-framework']
colsSet = set(COLS)
# df = pd.read_csv('Question_ver_1__Extracted_questions_by_taglist.csv')
df = pd.read_csv('output_1.csv')

print('REMOVE QUESTIONS WITH WRONG TAGS')
print('Before', len(df))
indicesToRemove = []
for i in range(len(df)):
    tags = df.iloc[i]['Tags'][1:-1].replace('><', ' ').split()
    f = True
    for tag in tags:
        if tag in colsSet:
            f = False
            break
    if f:
        indicesToRemove.append(i)
df = df.drop(index=indicesToRemove)
# df.to_csv('Ver2__Questions_removed_wrong_tags.csv', index=False)
print('After', len(df))

print('\nREMOVING DUPLICATE SCORES')
print('Before', len(df))
df.drop_duplicates('Id',inplace=True)
# df.to_csv('Ver_3__Questions_removed_duplicates.csv', index=False)
print('After', len(df))

print('\nREMOVING QUESTIONS WITH NEGATIVE SCORES')
print('Before', len(df))
df = df[df['Score'] >= 0]
df.to_csv('output_2.csv', index=False)
print('After', len(df))