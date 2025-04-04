from django.db import models
from vendor.models import Vendor
# Create your models here.
class Category(models.Model):
    vendor=models.ForeignKey(Vendor, on_delete=models.CASCADE)
    category_name=models.CharField(max_length=50)
    slug=models.SlugField(max_length=100,unique=True) #nothing but url for category
    description=models.TextField(max_length=250,blank=True)
    created_at=models.DateTimeField(auto_now=False, auto_now_add=True)
    modified_at=models.DateTimeField(auto_now=True, auto_now_add=False)

    class Meta:
        verbose_name='category'
        verbose_name_plural='categories'

    def __str__(self):
        return f"{self.category_name}"

    def clean(self):
        self.category_name=self.category_name.capitalize()

class FoodItem(models.Model):
    vendor=models.ForeignKey(Vendor, on_delete=models.CASCADE)
    category=models.ForeignKey(Category,on_delete=models.CASCADE,related_name='fooditems')
    food_title=models.CharField(max_length=50)
    slug=models.SlugField(max_length=100,unique=True)
    description=models.TextField(max_length=250,blank=True)
    price=models.DecimalField(max_digits=10, decimal_places=2)
    image=models.ImageField(upload_to='foodimages')
    is_available=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now=False, auto_now_add=True)
    modified_at=models.DateTimeField(auto_now=True, auto_now_add=False)


    def __str__(self):
        return f"{self.food_title}"

    def clean(self):
        self.food_title=self.food_title.capitalize()