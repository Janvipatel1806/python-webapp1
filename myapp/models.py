from django.db import models

# Create your models here.
class User(models.Model):
	fname=models.CharField(max_length=100)
	lname=models.CharField(max_length=100)
	email=models.EmailField()
	mobile=models.PositiveIntegerField()
	password=models.CharField(max_length=100)

	def __str__(self):
		return self.fname+" "+self.lname

class SUser(models.Model):
	fname=models.CharField(max_length=100)
	lname=models.CharField(max_length=100)
	email=models.EmailField()
	mobile=models.PositiveIntegerField()
	password=models.CharField(max_length=100)

	def __str__(self):
		return self.fname+" "+self.lname


class Additem(models.Model):
	seller=models.ForeignKey(SUser,on_delete=models.CASCADE)
	price=models.CharField(max_length=100)
	brand=(
		("PUMA","PUMA"),
		("ADIDAS","ADIDAS"),
		("BATA","BATA"),
		("CAMPUS","CAMPUS"),
		)
	brand=models.CharField(max_length=100,choices=brand)
	size=(
		("8","8"),
		("9","9"),
		("10","10"),
		("11","11"),
		)
	size=models.CharField(max_length=100,choices=size)
	pic=models.ImageField(upload_to="profile_pic/")

	def __str__(self):
		return self.seller.fname
class Wishlist(models.Model):
	user=models.ForeignKey(User,on_delete=models.CASCADE)
	product=models.ForeignKey(Additem,on_delete=models.CASCADE)

	def __str__(self):
		return self.user.fname+' '+self.product.brand

class Cart(models.Model):
	user=models.ForeignKey(User,on_delete=models.CASCADE)
	product=models.ForeignKey(Additem,on_delete=models.CASCADE)
	price=models.PositiveIntegerField()
	qty=models.PositiveIntegerField()
	total=models.PositiveIntegerField()
	pstatus=models.BooleanField(default=False)

	def __str__(self):
		return self.user.fname+' '+self.product.brand
