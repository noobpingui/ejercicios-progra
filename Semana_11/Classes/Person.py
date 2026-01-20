
class Person():
	
	def __init__(self):
		self.name = input("What is the name of this passenger? ")

	def __str__(self):
		
		return(
			f"Name: {self.name}"
		)