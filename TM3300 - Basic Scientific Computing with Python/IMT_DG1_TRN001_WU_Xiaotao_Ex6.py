# -*- coding: utf-8 -*-
"""
Created on Wed Jun  8 10:12:53 2022
student name: WU Xiaotao
student number: 21097724D
"""
import pandas as pd
import matplotlib.pyplot as plt

#Question1
df=pd.read_excel('TM33xx_marks.xlsx')
df=df.drop(columns=['Unnamed: 4'])
#a
print('a:',df[df['Assignment_1']<40])
#b
print('b:',df[(df['Assignment_1']>=80)&(df['Assignment_2']>=80)])
#c
df['Final']=df['Assignment_1']*0.3+df['Assignment_2']*0.3+df['Quiz']*0.4
print('c:',df)
#d
print('d:',df[df['Final']>80])
#e
df.to_csv('TM3300_Final.csv')


#Question2
df2=pd.read_csv('HK_max_temp.csv')
#a
df2_a=df2.groupby(['Year'])['Value'].max()
print('df2_a:')
print(df2_a)
#b
df2_b=df2.groupby(['Year'])['Value'].min()
print('df2_b:')
print(df2_b)
#c
df2_c=df2.groupby(['Year'])['Value'].mean()
print('df2_c:')
print(df2_c)
#d
plt.figure()
plt.plot(df2_c)
plt.legend(['HongKong'])
plt.xlabel('Year')
plt.ylabel('Temperature')
plt.title('Year vs Average Temperature')
plt.show()

#Question3
df3=pd.read_csv('Sales_2019_JAN.csv')
print(df3)
#a
#df3=df3.astype[{'Quantity Ordered':'int64','Price Each':'float64'}]
df3['Sales']=df3['Quantity Ordered']*df3['Price Each']
print(df3)
#b
df3_b=df3.groupby('Product')[['Sales']].sum()
print('df3_b:')
print(df3_b)
#c
plt.figure()
plt.plot(df3_b)
plt.legend(['Jan 2019'])
plt.xlabel('Product')
plt.ylabel('Sales')

plt.xticks(rotation='vertical')

plt.title('Product vs Sales')
plt.show()


