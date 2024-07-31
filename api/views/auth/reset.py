from django.utils import timezone
import random
import string
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password

from agri.models import ResetPassword
from base.emails.emails import reset_email_password

@api_view(["POST"])
def password_reset_request(request):
    if request.method =="POST":
        email = request.data.get("email")
        if not email:
            return Response({"error":"Email is required"}, status=status.HTTP_400_BAD_REQUEST)
    
        try:
            user = User.objects.get(email=email)
            print(user)
            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            ResetPassword.objects.create(
                email=email,
                code=code,
                expires=timezone.now() + timezone.timedelta(minutes=5),
            )
            # Send the email with the code to the user's email address
            reset_email_password(email, user.first_name, code)
            return Response({"message": "Password reset instructions sent to email"}, status=status.HTTP_200_OK)
        
        except User.DoesNotExist:
            return Response({"error":"User with that email does not exist"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error":f" There was an error {str(e)}" }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response({"error":"Method is not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)



@api_view(["POST"])
def password_reset_confirm(request):
    token = request.data.get("token")
    uid = request.data.get("uid")
    new_password = request.data.get("new_password")

    if not token or not uid or not new_password:
        return Response({"error": "Token, UID, and new password are required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(pk=uid)
        if default_token_generator.check_token(user, token):
            user.password = make_password(new_password)
            user.save()
            return Response({"message": "Password has been reset successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid token or user ID"}, status=status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        return Response({"error": "Invalid user ID"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": f"There was an error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)