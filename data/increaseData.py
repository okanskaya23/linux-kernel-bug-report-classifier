import pandas as pd
import os
import time
import numpy as np
BREAK_COUNT = 8900
START_COUNT = 8800
start_time = time.time()
cwd = os.getcwd()
df = pd.read_csv(cwd+"/updatedData.csv")

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import types
dateArr = []
#descArr = []
importanceArr = []
count = 0
#df['Created'] = np.nan
#df['Importance'] = np.nan
#df['Description'] = np.nan
for index, row in df.iterrows():
    if count < START_COUNT:
        count += 1
        continue
    count += 1
    id = row['Bug ID']
    detailPage = requests.get(f'https://bugzilla.kernel.org/show_bug.cgi?id={id}')
    soup = BeautifulSoup(detailPage.text, features='html.parser')
    found = soup.find("th", string='\n      Reported:\n    ')
    dateFound = found.find_next_sibling("td")
    dateString = dateFound.contents[0]
    dateString = dateString[0: dateString.index('UTC')]
    dateString = dateString.replace('-', '/')
    dateString = dateString.strip()
    datetime_object = datetime.strptime(dateString, "%Y/%m/%d %H:%M")
    dateArr.append(datetime_object)
    df.loc[index,'Created'] = datetime_object
    importanteValue = soup.find("a", href="page.cgi?id=fields.html#importance").parent.parent.find_next_sibling("td").contents[0]
    importanteValue = " ".join(importanteValue.strip().split())
    importanceArr.append(importanteValue)
    df.loc[index,'Importance'] = importanteValue
    #descriptionElementParent = soup.find("div",attrs={"class":"bz_comment bz_first_comment"})
    #descriptionElement = [] if isinstance(descriptionElementParent, types.NoneType) else descriptionElementParent.findChild("pre")
    #description = descriptionElement.contents[0] if len(descriptionElement.contents) > 0 else ""
    #descArr.append(description)
    #df.loc[index,'Description'] = description
    if count % 100 == 0:
        print(count)
        if count == BREAK_COUNT:
            break
#df['Created'] = dateArr
#df['Importance'] = importanceArr
#df['Description'] = descArr
print(df.head())
df.to_csv('updatedData.csv')
print("--- %s seconds ---" % (time.time() - start_time))