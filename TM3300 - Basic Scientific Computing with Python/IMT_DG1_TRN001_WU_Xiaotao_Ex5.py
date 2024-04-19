# -*- coding: utf-8 -*-
"""
Created on Tue Jun  7 13:16:58 2022
student name: WU Xiaotao
student number: 21097724D
"""
import numpy as np
import random

#Question1
#a
for i in np.arange(10):
    if i==0:
        y=np.array([random.randint(1,10) ])
    if i!=0:
        y=np.append(y,[random.randint(1,10) ])
print('array y:',y)
#b
b=[]
for i in y:
    if i<5:
        b=np.append(b,i)
    else:
        continue
print('elements<5',b)
#c
c=[]
for j in y:
    if (j<=3 or j>8):
        c=np.append(c,j)
    else:
        continue
print('elements  smaller than or equal to 3 or larger than 8.',c)
    
    
    
#Question2
for x in np.arange(181):
    print("sin({})=".format(x),np.sin(np.deg2rad(x)))
    
#Question3
a=1
while a!=0:
    a=int(input('input='))
    print ('inputr should be 0')
    if a==0:
        print('input is 0, the loop ends')
        
#Question4
target=random.randint(1,100)
time=0
a=-1
min1=1
max1=100
a=int(input('Guess a number from 1 to 100:'))
while a!=target:
    if a<target:
        min1=a
        a=int(input('Guess a number from {} to {}:'.format(min1,max1)))
        time=time+1
    elif a>target:
        max1=a
        a=int(input('Guess a number from {} to {}:'.format(min1,max1)))
        time=time+1
if a==target:
    print('The guess is correct!')
    print('The answer is ',target)
    print('You made ',time,"guesses")

