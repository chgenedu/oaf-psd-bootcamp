# Calvin Hsieh chgenedu@gmail.com
# oa-professional-software-development-bootcamp
# Week 2
# Nov 5, 2023
#
# animal.py

from abc import abstractmethod

class Animal:
	def __init__(self, name, age):
		self.__name = name
		self.__age = age
	def get_name(self):
		return(self.__name)
	def get_age(self):
		return(self.__age)
	
	@abstractmethod
	def speak(self):
		pass

class Cat(Animal):
	def speak(self):
		print(f"\t{self.get_name()} (age {self.get_age()}) is ~meowing~.")

class Dog(Animal):
	def speak(self):
		print(f"\t{self.get_name()} (age {self.get_age()}) is !!barking!!")