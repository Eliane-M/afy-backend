from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from agri.models import *
from agri.serializers import *
from api.authentication.auth import verify_user
from authentication.permissions.permission import IsEmployer



@api_view(['GET'])
def joblisting_list(request):
    if request.method == 'GET':
        joblistings = Joblisting.objects.all()
        serializer = JoblistingSerializer(joblistings, many=True)
        return Response({"job listing": serializer.data}, status=status.HTTP_200_OK)
    else:
        return Response({"error": "Invalid request method"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def jobs_viewed_api(request):
    if request.method == 'GET':
        access_token = request.headers.get("Authorization")
        user, message = verify_user(access_token)

        if user is None:
            return Response({'Message': message}, status=status.HTTP_401_UNAUTHORIZED)
        
        
        jobs_list = Joblisting.objects.filter(client=user)
        print(f"Jobs found: {jobs_list.count()}")

        history_serializer = JoblistingSerializer(jobs_list, many=True).data
        return Response({'History': history_serializer}, status=status.HTTP_200_OK)
    else:
        return Response({"error": "Invalid request method"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    

@api_view(['POST'])
@permission_classes([IsEmployer, IsAuthenticated])
def joblisting_detail(request):
    if request.method == 'POST':
        title = request.data.get('title')
        description = request.data.get('description')
        skills = request.data.get('skills')

        category = request.data.get('category')
        try:
            category = Category.objects.get(name__iexact=category)
        except Category.DoesNotExist:
            return Response({'error': 'Category not found. Choose between Farming, Livestock, or Agro-Tourism'}, status=status.HTTP_400_BAD_REQUEST)

        try: 
            joblisting = Joblisting.objects.create(
                title=title,
                description=description,
                skills=skills,
                category=category
            )
            serializer = JoblistingSerializer(joblisting).data
            return Response({"job listing": serializer}, status=status.HTTP_201_CREATED)
        
        except title is None:
            return Response({"message": "title is required"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    else:
        return Response({"error": "Invalid request method"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)