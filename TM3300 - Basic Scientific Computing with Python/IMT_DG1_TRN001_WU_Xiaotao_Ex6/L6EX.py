# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 14:09:00 2020

@author: icwhchoy
"""
# Module of the day
import pandas as pd
# TM3300 - L6 (Examples)
#%%
a=int(input('a='))	# ask user to input a number
result=a*a
print("a^2 ={}".format(result))

#%%
inFo = open("input.txt", "r")
outFo = open("result.txt","w")
for line in inFo:
    val=int(line)
    result="{}^2 = {}\n".format(val, val**2)
    outFo.write(result)
inFo.close()   
outFo.close()
# TM3300 - L6 (Examples)
#%%
list1 = [3,2,0,1]
list2 = [0,3,7,2]

# create series form lists
ser_apple = pd.Series(list1)	
ser_orange = pd.Series(list2)	
ser_orange2 = pd.Series(list1,index=['MK','KC','YL','ST'])

#%%
frame = { 'Apple': ser_apple, 'Orange': ser_orange } 
df_furit = pd.DataFrame(frame) 

#%%
frame = { 'Apple': ser_apple, 'Orange': ser_orange2 } 
df_furit = pd.DataFrame(frame) 
ser = pd.Series(list)	
print(ser)
# 0     Apple
# 1    Orange
# 2    Banana
# dtype: object


#%%
print(df_furit.columns)
print(df_furit.Apple)
print(df_furit.Orange)
#%%

staff = {'Name':['Alex', 'Bob', 'Calvin', 'David'],
	'Age':	[19, 22, 25, 32],
	'Qualification':	['UG', 'UG', 'MPhil', 'EngD']}

df = pd.DataFrame(staff)
#%%
df['Age']=df['Age']+4
df.assign(year_to_retirement=60-df['Age'])
#%%
print("iloc before re-index: {}".format(df.iloc[[1,2]]))
print("loc before re-index: {}".format(df.loc[[1,2]]))

df1=df.set_index([pd.Index(['a', 'b', 'c', 'd'])])
print("iloc after re-index: {}".format(df1.iloc[[1,2]]))
print("loc after re-index: {}".format(df1.loc[[1,2]]))
print("loc after re-index: {}".format(df1.loc[['b','c']]))
#%%
print(df.iloc[1:3,:])
print(df.iloc[:,-1])


#%%

print(df[df['Age']<30])
print(df[df['Name']=='Alex'])
print(df[df['Qualification']!='UG'])
#%%
#df[(df.Qualification == 'UG') & (df.Age> 20)]
df[(df["Qualification"] == 'UG') & (df["Age"]> 20)]
df[(df["Qualification"] == 'UG') | (df["Qualification"] == "MPhil")]
#%%
df.loc[4] = ['Edward',40,'MSc']	# Insert a new row to the DataFrame
print(df)
df.drop(4)
print(df)
df.drop(4,inplace=True)

#%%
df = pd.read_csv('dse2017.csv')
print(df)

# Use a specific column ‘Subject’ as index
df = pd.read_csv('dse2017.csv', index_col ='Subject')
print(df)
print(df.columns) 
col_list=['5**', '5*', '5+']
print(df[col_list])
print(df[col_list].sum(axis=1))

df['5PS']=df[col_list].sum(axis=1)/df['Attended']*100
print(df[col_list])
print(df[['5PS']])
#%%
df = pd.read_excel('Population 2016.xlsx')
print(df)
print(df.info())
print(df.dtypes)
print(df.describe())

print(df.to_string())
HKI=df.iloc[:,0:5]
KLN=df.iloc[:,[0]+list(range(5,10))]
NT=df.iloc[:,[0]+list(range(10,19))]
print(HKI.to_string())
print(KLN.to_string())
print(NT.to_string())

HKI.to_csv("HKI.csv")
KLN.to_csv("KLN.csv")
NT.to_csv("NT.csv")
