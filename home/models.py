from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=50)
    password = models.CharField(max_length=255)
    created_date = models.DateTimeField(auto_now_add=True)
    # img = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.name

class Person(models.Model):
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    

class Note(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Each note is associated with a user
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title