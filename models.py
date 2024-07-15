from django.db import models
import datetime
from django.contrib.auth.models import User

class Product(models.Model):
    name=models.CharField(max_length=150,null=False,blank=False)
    image=models.ImageField(upload_to='',null=True,blank=True)
    vendor=models.CharField(max_length=150,null=False,blank=False)
    quantity=models.IntegerField(null=False,blank=False)
    original_price=models.FloatField(null=False,blank=False)
    selling_price=models.FloatField(null=False,blank=False)
    description=models.TextField(max_length=500,null=False,blank=False)
    status=models.BooleanField(default=False,help_text="0-show,1-Hidden")

    def __str__(self):
        return self.name

class Viewproduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name=models.CharField(max_length=150,null=False,blank=False)
    quantity = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
 
    def __str__(self):
        return self.name

class Cart(models.Model):
  user=models.ForeignKey(User,on_delete=models.CASCADE)
  product=models.ForeignKey(Product,on_delete=models.CASCADE)
  product_qty=models.IntegerField(null=False,blank=False)
  created_at=models.DateTimeField(auto_now_add=True)

  @property
  def total_cost(self):
    return self.product_qty*self.product.selling_price
