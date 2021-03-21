import pandas as pd
import numpy as np

df = pd.read_csv("so_data_with_acceptedanswers.csv")
answers_df = df.copy()
answers_df = answers_df[['Id', 'AcceptedAnswer']]
answers_df = answers_df.dropna()
answers_df.columns = ['id', 'raw']
answers_df.insert(1, 'qa', 'a')
answers_df.id = answers_df.id.apply(np.int64)
print(answers_df.head())
print(len(answers_df))

questions_df = df.copy()
questions_df = questions_df[['Id', 'Body', 'Title']]
questions_df['titlePlusQuestion'] = questions_df[['Title', 'Body']].apply(lambda x: ' '.join(x), axis=1)
questions_df = questions_df.drop(['Title', 'Body'], axis=1)
questions_df.columns = ['id', 'raw']
questions_df.insert(1, 'qa', 'q')
print(questions_df.head())
print(len(questions_df))

df = pd.concat([questions_df,answers_df])
print(len(df))
df.to_csv('so_body.csv', index=False)