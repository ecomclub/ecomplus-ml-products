import pandas as pd
import csv
import time
import sys
from datetime import datetime
import sys

# -- open csv for analyse

df= pd.read_csv('profile.csv',encoding='iso-8859-1')

df.head()

# -- convert gender

def convert_gender(gender):
    if gender =='m':
        return 0
    if gender =='f':
        return 1
    
    
# -- categorization of data

def age_convert(s):
    if s <= 14:
        return 1
    elif s >= 15 and s<=18:
        return 2
    elif s >=19 and s<=21:
        return 3
    elif s >= 15 and s<=18:
        return 4
    elif s >=22 and s<=26:
        return 5
    elif s >=31 and s<=35:
        return 6
    elif s >=36 and s<=40:
        return 7
    elif s >=41 and s<=50:
        return 8
    elif s >=50 and s<=60:
        return 9
    elif s >=61 and s<=80:
        return 10
    elif s >=81:
        return 11
    
# -- treating date of birth information
now = datetime.now()
birth_date_year=sys.argv[1]
age=now.year-birth_date_year
age_convert = age_convert(age)
age_convert=str(age_convert)

# -- treating information of the gendere
gender_convert = convert_gender(sys.argv[2])
gender_convert=str(gender_convert)

# -- treating information of the province
province_code=sys.argv[3]
province_code=str(province_code)
      
# -- create the query of result

df.query( 'age_range == '+age_convert+' and gender == '+gender_convert+' and region =="'+province_code+'" ', inplace = True) 
vetor = df.values
result=str(vetor)[2:-10]

print(result)
