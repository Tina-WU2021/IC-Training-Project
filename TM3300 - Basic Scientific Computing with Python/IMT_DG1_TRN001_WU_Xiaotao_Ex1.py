# -*- coding: utf-8 -*-
"""
Student name: WU Xiaotao
Student ID: 21097724D
"""
#Question1
pet_list = ["dog", "bird", "rabbit", "fish", "cat"]
print(pet_list[0])
print(pet_list[4])


#Question2
print("The prices of 3 cars are: {:0.2f}, {:06d}, {:.2f}".format(2690, 1593, 7420.5))


#Question3
employeeSalary={'John': 7500, 'Mary': 8000, 'Peter': 6500, 'Candy': 7000}
#a
print("Mary's salary:{Mary:d}".format(**employeeSalary))
#b
employeeSalary["Candy"]=9000
#c
employeeSalary["David"]=5000
#d
employeeSalary.pop("Peter")


#Question4
staffInfo = [["Betty","Amy","Peter","Alex","Eric","Lisa","John","Crystal"],
             ['python', 'java', 'C', 'C', 'java', 'python', 'ruby', 'python']]

print(list(set(staffInfo[1])))
