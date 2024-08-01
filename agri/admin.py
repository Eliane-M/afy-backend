from django.contrib import admin
from agri.models import SkillAssessment, Category, EducationalResources, Joblisting, Employer


admin.site.register(SkillAssessment)
admin.site.register(Joblisting)
admin.site.register(Category)
admin.site.register(EducationalResources)
admin.site.register(Employer)