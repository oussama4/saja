from django.db import models


from ../users import user 
# Create your models here.


class Cart(models.model):

    user_id = models.ForeignKey(user,related_name="+",
