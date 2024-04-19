# -*- coding: utf-8 -*-
"""
Created on Mon Jun  6 13:26:26 2022
student name: WU Xiaotao
student number: 21097724D
"""
#Question1
import numpy as np
#a
totalCost=3000+12000/(3*2)
print("totalCost",totalCost)
#b
y1=5**3+4*np.sin(np.pi/4)
print("y1",y1)
#c
y2=10*np.cos(np.deg2rad(135))**2+2*np.sin(np.deg2rad(45))**2
print("y2",y2)


#Question2
#a
a2=np.arange(31,52,2)
print("a2",a2)
#b
b2=np.linspace(np.pi,2*np.pi,30)
print("b2",b2)


#Question3
Numbers=np.arange(12)
Numbers=Numbers*2+33
print(sum(Numbers))


#Question4
t=np.arange(1,3.1,0.2)
print("t:",t)
#a
a4=np.logspace(1.0,3.0,11,base=np.e)
print("a4:",a4)
#b
#e**a is the same to exp(a)
b4=np.e**t*(1+np.cos(3*t))
print("b4:",b4)
#c
c4=np.tan(t)*(180/np.pi)
print("c4:",c4)


#Question5
a5=np.array(([1,9,6,8],[2,2,7,3],[6,1,3,5]))
#a
print(a5[0,1])
#b
print(a5[0])
#c
print(a5[:,2])


#Question6
x = [1, 3, 5, 7, 9, 11]
y = [2, 4, 6, 8, 10, 12]
x6=np.array(x)
y6=np.array(y)
z=x6*y6
print("z:",z)