from django.db import models




    
class Child(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    description = models.TextField()
    is_adopted = models.BooleanField(default=False)
    gender = models.CharField(max_length=10 , null= True)
    photo = models.ImageField(upload_to='children_photos/' , null= True)

    def __str__(self):
        return self.name
