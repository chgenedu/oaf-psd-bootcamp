# Calvin Hsieh chgenedu@gmail.com
# oa-professional-software-development-bootcamp
# Week 2
# Nov 5, 2023
#
# main.py

'''
Write abstract class Animal with two implementations Cat & Dog
	Share private attributes: name, age
	Abstract method: speak() -> prints individual message
Implement class Zoo
	Attribute: list of Animal objects
	Method: speak_all() (calls speak method for each animal in the current instance)
Implement class ZooKeeper
	Attribute: single Zoo instance
	Method: add_animal(animal: Animal) (adds an animal to the assigned zoo)
At each step, add print statements to showcase behavior
Run your code by creating instances of all classes, calling all methods at least once
'''

from animal import Cat, Dog
from zoo import Zoo, ZooKeeper


def main():
	print("[Begin program execution]")
	
	print("Create a cat and make it speak.")
	catherine = Cat("Catherine", 3)
	catherine.speak()

	print("Create a dog and make it speak.")
	douglas = Dog("Douglas", 5)
	douglas.speak()

	print("Create an empty zoo.")
	zoo = Zoo()
	print("Assign the zoo to a zookeeper.")
	zookeeper = ZooKeeper(zoo)
	print("All animals in the zoo speak:")
	zoo.speak_all()

	print("The zookeeper adds a cat to the zoo.")
	zookeeper.add_animal(catherine)
	print("All animals in the zoo speak:")
	zoo.speak_all()

	print("The zookeeper adds a dog to the zoo.")
	zookeeper.add_animal(douglas)
	print("All animals in the zoo speak:")
	zoo.speak_all()

	print("Extra: Create a second zoo and initialize it with 5 animals.")
	print("(This shows that you can initialize a new zoo with an arbitrary number of animals.)")
	cat1 = Cat("Cat1", 4)
	cat2 = Cat("Cat2", 5)
	cat3 = Cat("Cat3", 6)
	dog1 = Dog("Dog1", 2)
	dog2 = Dog("Dog2", 3)
	zoo2 = Zoo(cat1, cat2, dog1, dog2, cat3)
	print("All animals in the second zoo speak:")
	zoo2.speak_all()

	print("[End program execution]")

if __name__ == "__main__":
	main()


