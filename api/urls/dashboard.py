from django.urls import path
from api.views.resources.resources import educational_resources_list, new_educational_resource
from api.views.category.category import category_list, new_category
from api.views.jobs.jobs import joblisting_list, joblisting_detail, jobs_viewed_api
from api.views.skills.skills import new_skill_assessment, skill_assessment_list


urlpatterns = [
    path('educational_resources/', educational_resources_list, name='educational_resources_list'),
    path('new_resource/', new_educational_resource, name='new_educational_resource'),
    path('category/', category_list, name='category_list'),
    path('new_category/', new_category, name='new_category'),
    path('joblisting/', joblisting_list, name='joblisting_list'),
    path('job_history/', jobs_viewed_api, name='jobs_viewed_api'),
    path('new_job/', joblisting_detail, name='joblisting_detail'),
    path('assessments/', skill_assessment_list, name='skill_assessment_list'),
    path('new_assessment/', new_skill_assessment, name='new_skill_assessment'),
]