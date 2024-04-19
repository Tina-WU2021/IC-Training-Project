# -*- coding: utf-8 -*-
"""
Created on Mon Jun  6 15:15:04 2022

student name: WU Xiaotao
Student number: 21097724D
"""
import numpy as np

#1
A=np.array(([-1,4,0],[3,4,-4],[-10,-12,5]))
B=np.array(([-72],[-4],[-50]))
invA=np.linalg.inv(A)
X=np.matmul(invA,B)
print("1:",X)


#2
#a
from numpy.polynomial import polynomial as P
f=P.Polynomial([48,-14,1])
print("a.f",f.roots())

g=P.Polynomial([-102,31,18,-9,1])
print("a.g",g.roots())

#b
f=[48,-14,1]
g=[-102,31,18,-9,1]
q,r=P.polydiv(g,f)
print("b.q",q)
print("b.r",r)
print("x",P.polyadd(P.polymul(f,q),r))


#c
c=P.polymul(f,g)
print("c",c)
