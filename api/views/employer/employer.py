from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from agri.models import Employer
from agri.serializers import EmployerSerializer


@api_view(['GET'])
def employer_list(request):
    if request.method == 'GET':
        employers = Employer.objects.all()
        serializer = EmployerSerializer(employers, many=True)
        return Response({"employers": serializer.data}, status=status.HTTP_200_OK)
    else: 
        return Response({"error": "Invalid request method"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

   
@api_view(['POST'])
@permission_classes([])
def new_employer(request):
    if request.method == 'POST':
        name = request.data.get('name')
        address = request.data.get('address')
        contact_number = request.data.get('contact_number')
        email = request.data.get('email')
        website = request.data.get('website')


        try:
            employer = Employer.objects.create(
                name=name,
                address=address,
                contact_number=contact_number,
                email=email,
                website=website,
            )
            serializer = EmployerSerializer(employer)
            return Response({"employer": serializer.data}, status=status.HTTP_201_CREATED)
        
        except name is None or contact_number is None or email is None:
            return Response({"error": "name, contact_number, and email are required."}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"error": str(e.message)}, status=status.HTTP_400_BAD_REQUEST)