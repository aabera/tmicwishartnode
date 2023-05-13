from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User


class News(models.Model):
    date = models.DateField(auto_now_add=True)
    description = models.CharField(max_length=5000)
    image = models.ImageField(upload_to="img")
    link = models.CharField(max_length=100, blank=True, null=True)

# class Blog(models.Model):
#     date = models.DateField(auto_now_add=True)
#     description = models.CharField(max_length=5000)
#     image = models.ImageField(upload_to="img")
#     link = models.CharField(max_length=100, blank=True, null=True)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100, blank=True, null=True)
    order_note = models.CharField(max_length=5000, blank=True, null=True)
    country = models.CharField(max_length=100)
    address = models.CharField(max_length=500)
    city = models.CharField(max_length=500)
    province = models.CharField(max_length=500)
    postal_code = models.CharField(max_length=500)
    phone = models.CharField(max_length=500)

class Item(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    max_price = models.FloatField()
    min_price = models.FloatField()
    image = models.ImageField(upload_to="images")
    cost_per_sample = models.CharField(max_length=1000)
    matrices = models.CharField(max_length=1000)
    vol_requirements = models.CharField(max_length=1000)
    species = models.CharField(max_length=1000)
    pathways = models.CharField(max_length=1000)
    compound_classes = models.CharField(max_length=1000)
    no_of_compounds = models.CharField(max_length=1000)
    quantitative = models.CharField(max_length=1000)
    compound_list = models.CharField(max_length=1000)
    validation = models.CharField(max_length=1000)
    slug = models.SlugField(blank=True, null=True)

    def __str__(self):
        return f'{self.title} {self.id}'

    def save(self, *args, **kwargs):
        self.slug = slugify(f'{self.title}-{self.id}')
        super(Item, self).save(*args, **kwargs)


class OrderItem(models.Model):
    id = models.AutoField(primary_key=True)
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    user = models.CharField(max_length=100)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    sub_total = models.FloatField()
    category = models.CharField(max_length=50)
    sample_type = models.CharField(max_length=50, blank=True, null=True)
    analysis_type = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

class Order(models.Model):
    id = models.AutoField(primary_key=True)
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    user = models.CharField(max_length=100)
    items = models.ManyToManyField(OrderItem)
    total = models.FloatField()
    ordered_date = models.DateTimeField(auto_now_add=True)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.id} {self.user}"


