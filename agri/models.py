from django.db import models
from django.contrib.auth.models import User
from base.models import BaseModel
from django.utils import timezone


class Account(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=100)
    image = models.ImageField(upload_to='account_images/', blank=True, null=True)
    def __str__(self):
        return str(self.user.first_name)
    

class AccountEmail(models.Model):
    email = models.EmailField(max_length=255)

    def __str__(self):
        return str(self.email)
    

class ResetPassword(models.Model):
    email = models.EmailField(max_length=255)
    code = models.CharField(max_length=6)
    expires = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.email)
    

class Employer(BaseModel):
    phone_number = models.CharField(max_length=25)
    company_name = models.CharField(max_length=1000)
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    # cv = models.FileField(upload_to="uploads/", null=True)

    def __str__(self):
        return str(self.user.first_name)


    

class Category(models.Model):
    CATEGORY = [
        ('farming', 'Farming'),
        ('livestock', 'Livestock'),
        ('agro_tourism', 'Agro Tourism')
    ]
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    category = models.CharField(choices=CATEGORY, max_length=255, null=True)
    image = models.ImageField(upload_to="category_images/", editable=True)
    
    def __str__(self) -> str:
        return str(self.name)
    

class Joblisting(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='jobs_images/', blank=True, editable=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.title)


    
class EducationalResources(BaseModel):
    # title = models.CharField(max_length=255)
    content = models.TextField(max_length=1000)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name)


class SkillAssessment(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField()
    date_taken = models.DateField(auto_now_add=True)
    category = models.ForeignKey(EducationalResources, on_delete=models.CASCADE, blank=True)

    def __str__(self):
        return str(self.name)
    

class SkillsAssessmentEmail(models.Model):
    email = models.EmailField(max_length=255)
    assessment = models.ForeignKey(SkillAssessment, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.email)