# Calvin Hsieh chgenedu@gmail.com
# oa-professional-software-development-bootcamp
# Week 2
# Nov 5, 2023
#
# zoo.py

class Zoo():
	def __init__(self, *animals):
		self.animals = []
		for animal in animals:
			self.add_animal(animal)
	def add_animal(self, animal):
		self.animals.append(animal)
	def speak_all(self):
		if len(self.animals) == 0:
			print("\t~~ silence ~~ (No animal in zoo.)")
		else:
			for animal in self.animals:
				animal.speak()

class ZooKeeper:
	def __init__(self, zoo):
		self.zoo = zoo
	def add_animal(self, animal):
		self.zoo.add_animal(animal)
