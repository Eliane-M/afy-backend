from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from agri.models import SkillAssessment
from agri.serializers import SkillAssessmentSerializer


@api_view(['GET'])
def skill_assessment_list(request):
    if request.method == 'GET':
        skill_assessments = SkillAssessment.objects.all()
        serializer = SkillAssessmentSerializer(skill_assessments, many=True)
        return Response({"assessment list":serializer.data}, status=status.HTTP_200_OK)
    

@api_view(['POST'])
@permission_classes([])
def new_skill_assessment(request):
    if request.method == 'POST':
        assessment_name = request.data.get('name')
        skill_level = request.data.get('level')
        assessment_category = request.data.get('category')

        try:
            assessment_category = SkillAssessment.obejct.get(category=assessment_category)
            skill_assessment = SkillAssessment.objects.create(
                name=assessment_name,
                level=skill_level,
                category=assessment_category
            )

            skill_assessment.save()
            assessment_serializer = SkillAssessmentSerializer(skill_assessment).data
            return Response({"assessment": assessment_serializer}, status=status.HTTP_201_CREATED)
        
        except SkillAssessment.DoesNotExist:
            return Response({"error": "Invalid assessment category."}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({"error": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    else:
        return Response({"error": "Only POST method is allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)