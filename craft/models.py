from django.db import models

# Create your models here.

class Product(models.Model):
    
    product_id=models.AutoField
    product_name=models.CharField(max_length=50)
    price=models.IntegerField(default=0)
    category=models.CharField(max_length=50,default="")
    subcategory=models.CharField(max_length=50,default="")
    image=models.ImageField(upload_to="craft/images",default="")
    
    def __str__(self):
        return self.product_name
    
# class Orders(models.Model):
#     order_id=models.AutoField(primary_key=True)
#     items_json=models.CharField(max_length=120)
#     amount=models.IntegerField(default=0)
#     name=models.CharField(max_length=122)
#     email=models.CharField(max_length=122,default="")
#     address=models.CharField(max_length=122,default="")
#     city=models.CharField(max_length=1000,default="")
#     state=models.CharField(max_length=1000,default="")
#     zip_code=models.CharField(max_length=1000,default="")
#     phone=models.CharField(max_length=122,default="")

class Orders(models.Model):
    order_id = models.AutoField(primary_key=True)
    items_json =  models.CharField(max_length=5000)
    amount = models.IntegerField(default=0)
    name = models.CharField(max_length=90)
    email = models.CharField(max_length=90,default="")
    address1 = models.CharField(max_length=200,default="")
    address2 = models.CharField(max_length=200,default="")
    city = models.CharField(max_length=100,default="")
    state = models.CharField(max_length=100,default="")
    zip_code = models.CharField(max_length=100,default="")    
    oid=models.CharField(max_length=150,blank=True)
    amountpaid=models.CharField(max_length=500,blank=True,null=True)
    paymentstatus=models.CharField(max_length=20,blank=True)
    phone = models.CharField(max_length=100,default="")
    def _str_(self):
        self.save
        return self.name
        


class OrderUpdate(models.Model):
    update_id = models.AutoField(primary_key=True)
    order_id = models.IntegerField(default="")
    update_desc = models.CharField(max_length=5000)
    delivered=models.BooleanField(default=False,null=True,blank=True)
    timestamp = models.DateField(auto_now_add=True)

    def _str_(self):
        return self.update_desc[0:7] + "..."
    
    
class Contact(models.Model):
    msg_id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=122)
    email=models.CharField(max_length=122,default="")
    phone=models.CharField(max_length=122,default="")
    desc=models.CharField(max_length=1000,default="")
    
    
    def __str__(self):
        return self.name

    
    







