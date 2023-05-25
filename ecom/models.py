from django.db import models
import uuid
# Create your models here.
from base.utils import Base_content
from django.contrib.auth import get_user_model


class Product(Base_content):
    '''
    model for the product
    '''

    product_name = models.CharField(max_length=300)
    price = models.DecimalField(null=True,default=0.000,decimal_places=3,max_digits=100000)
    description = models.CharField(max_length=300,null=True)
    image = models.ImageField(upload_to='product')
    created_by = models.ForeignKey(get_user_model(),on_delete=models.CASCADE)
    slug_field = models.SlugField(unique=True,null=True,blank=True)

    def save(self,*args,**kwargs):
        if not self.slug_field :
            uuid_str = str(uuid.uuid4())[:10]
            self.slug_field = uuid_str
        return super().save(*args,**kwargs)
        

    def __str__(self):
        return self.product_name
    
    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ['-created_on']



class Cart(Base_content):
    '''
    cart model
    '''
    product_name = models.ForeignKey(Product,on_delete=models.CASCADE,null=True)
    quantity = models.IntegerField(null=True,default=0)
    created_by = models.ForeignKey(get_user_model(),on_delete=models.CASCADE,null=True)
    price = models.DecimalField(default=0.00,max_digits=10000,null=True,decimal_places=2)
    
    def __str__(self):
        return str(self.product_name)
    

    def get_total_quantity(self):
        return self.quantity
    
