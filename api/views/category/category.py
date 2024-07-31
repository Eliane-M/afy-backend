from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from agri.models import Category
from agri.serializers import CategorySerializer
from authentication.permissions.permissions import IsEmployer


@api_view(['GET'])
# @permission_classes[(IsAuthenticated)]
def category_list(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response({"categories": serializer.data}, status=status.HTTP_200_OK)
    


@api_view(['POST'])
@permission_classes([IsEmployer, IsAuthenticated])
def new_category(request):
    if request.method == 'POST':
        name = request.data.get('name')
        description = request.data.get('description')

        try:
            category = Category.objects.create(
                name=name, 
                description=description
            )
            category.save()
            category_serializer = CategorySerializer(category).data
            return Response({"category": category_serializer.data}, status=status.HTTP_201_CREATED)
        
        except name is None:
            return Response({"error": "name is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    else:
        return Response({"error": "Only POST method is allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)