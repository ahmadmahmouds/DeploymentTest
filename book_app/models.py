from django.db import models
class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Book(models.Model):
    title=models.CharField(max_length=255)
    description=models.TextField()
    uploaded_By=models.ForeignKey(User,related_name="book_uploaded",on_delete=models.CASCADE)
    user_who_like=models.ManyToManyField(User,related_name='liked_book')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)









def insert_new_user(fname,lname,email,passwd):
    user=User.objects.create(first_name=fname,last_name=lname,email=email,password=passwd)
    return user
def is_duplicate_email(email):
    users = User.objects.filter(email=email).values()
    if len(users):
        return True
    return False
    return users[0]


def get_userByEmail(email):
    users = User.objects.filter(email=email)
    if users:
        return users[0]
    return None
# Create your models here.
