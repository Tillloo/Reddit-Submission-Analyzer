import pandas as pd

#hacky conversion to csv, works for a one time use though
data = pd.read_json('data/1/text/part-00000-ab7a075c-1d24-4d61-9a7e-7329edef3e7b-c000.json.gz', lines=True)
path = ''
for i in range(1,3296):

    if i < 10:
        path = 'data/1/text/part-0000' + str(i) + '-ab7a075c-1d24-4d61-9a7e-7329edef3e7b-c000.json.gz'
    elif i < 100:
        path = 'data/1/text/part-000' + str(i) + '-ab7a075c-1d24-4d61-9a7e-7329edef3e7b-c000.json.gz'
    elif i < 1000:
        path = 'data/1/text/part-00' + str(i) + '-ab7a075c-1d24-4d61-9a7e-7329edef3e7b-c000.json.gz'
    elif i < 10000:
        path = 'data/1/text/part-0' + str(i) + '-ab7a075c-1d24-4d61-9a7e-7329edef3e7b-c000.json.gz'
    temp = pd.read_json(path, lines=True)
    data = pd.concat([data, temp])


data.to_csv('news.csv', index=False)

data1 = pd.read_json('data/2/text/part-00000-0c140639-9d83-4301-b4bf-c1e49af3407a-c000.json.gz', lines=True)
path = ''
for i in range(1,3296):

    if i < 10:
        path = 'data/2/text/part-0000' + str(i) + '-0c140639-9d83-4301-b4bf-c1e49af3407a-c000.json.gz'
    elif i < 100:
        path = 'data/2/text/part-000' + str(i) + '-0c140639-9d83-4301-b4bf-c1e49af3407a-c000.json.gz'
    elif i < 1000:
        path = 'data/2/text/part-00' + str(i) + '-0c140639-9d83-4301-b4bf-c1e49af3407a-c000.json.gz'
    elif i < 10000:
        path = 'data/2/text/part-0' + str(i) + '-0c140639-9d83-4301-b4bf-c1e49af3407a-c000.json.gz'
    temp = pd.read_json(path, lines=True)
    data1 = pd.concat([data1, temp])


data1.to_csv('story.csv', index=False)