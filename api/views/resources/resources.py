import datetime
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from agri.models import EducationalResources
from agri.serializers import EducationalResourcesSerializer


@api_view(['GET'])
def educational_resources_list(request):
    if request.method == 'GET':
        educational_resources = EducationalResources.objects.all()
        serializer = EducationalResourcesSerializer(educational_resources, many=True)
        return Response({"educational_resources": serializer.data}, status=status.HTTP_200_OK)
    else:
        return Response({"error": "Only GET method is allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@api_view(['POST'])
@permission_classes([])
def new_educational_resource(request):
    if request.method == 'POST':
        name = request.data.get('name')
        description = request.data.get('description')
        content = request.data.get('content')

        try: 
            educational_resource = EducationalResources.objects.create(
                name=name,
                description=description,
                content=content,
                created_by=request.user.id,
                updated_by=request.user.id,
                created_at=datetime.now(),
                updated_at=datetime.now()
            )

            educational_resource.save()

            educational_resource_serializer = EducationalResourcesSerializer(educational_resource).data
            return Response({"resource": educational_resource_serializer}, status=status.HTTP_201_CREATED)

        except name is None and description is None and content is None:
            return Response({"error": "name, description, and content are required."}, status=status.HTTP_400_BAD_REQUEST) 
        except Exception as e:
            return Response({"error": f"There was an error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response({"error": "Only POST method is allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)