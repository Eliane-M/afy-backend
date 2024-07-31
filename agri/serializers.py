from rest_framework import serializers
from django.contrib.auth.models import User
from agri.models import Account, EducationalResources, Employer, SkillAssessment, Joblisting, Category


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        
class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = "__all__"

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

class SkillAssessmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SkillAssessment
        fields = "__all__"

class EducationalResourcesSerializer(serializers.ModelSerializer):
    class Meta:
        model = EducationalResources
        fields = "__all__"

class EmployerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employer
        fields = "__all__"

class JoblistingSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    class Meta:
        model = Joblisting
        fields = "__all__"