# -*- coding: utf-8 -*-
"""
Created on Tue Jun  7 08:35:37 2022
Student name: WU Xiaotao
Student number: 21097724D
"""
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits import mplot3d

#Question1
plt.figure()
x1=np.linspace(-2,5,100)
x2=np.linspace(-2*np.pi,2*np.pi,100)
y1=3*x1**4-16*x1**3+6*x1**2+24*x1+1
y2=np.sin(2*x2-1)
plt.subplots_adjust(hspace=1)
#1
plt.subplot(2,1,1)
plt.plot(x1,y1)
plt.title(r'$3x^{4}4-16x^{3}+6x^{2}+24x+1$')
plt.xlabel('x')
plt.ylabel('y')
#2
plt.subplot(2,1,2)
plt.plot(x2,y2)
plt.title('y=sin(2x-1)')
plt.xlabel('x')
plt.ylabel('y')
plt.show()


#Question2
plt.figure()
month=['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC']
tem=[15,13,20,23,25,27,29,31,31,28,24,20]
index=np.arange(12)
p=plt.bar(index,tem,width=0.3)
plt.title('Average temperature of a city in 2010')
plt.xlabel('Month')
plt.ylabel('Temperature(°C) ')
plt.xticks(index,month)
plt.show()


#Question3
x=np.linspace(-50,50,101)
y=np.linspace(-50,50,101)
XX,YY=np.meshgrid(x,y)
X,Y=np.meshgrid(x,y)
ax=plt.axes(projection="3d")
R=(X**2+Y**2)**(1/3)
Z=2*R**2*np.cos(R)
ax.plot_surface(X,Y,Z,cmap=plt.cm.YlGnBu_r)
plt.title(r'$Z=2R^{2}cos(R)$')