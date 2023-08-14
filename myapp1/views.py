from django.shortcuts import render
from rest_framework.generics import  CreateAPIView
from rest_framework.generics import DestroyAPIView
from rest_framework import generics
from django.shortcuts import render
from django.core.mail import send_mail
from rest_framework.decorators import api_view
from rest_framework import viewsets , permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .models import Cas, Patient , User , SharedCase ,Notification
from .serializers import CasReadSerializer,CasWriteSerializer,  PatientSerializer , UserSerializer, SharedCaseSerializer,SharedCaseReadSerializer,CasSerializer
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework import status
import requests
from django.utils.timezone import now
from rest_framework import status
from rest_framework.decorators import api_view


def get_token(request):
    data = {"username": "karima", "password": "karima_cns_2023"}
    headers = {}
    response = requests.post("http://curvesnsmiles.com/api/token/", data=data, headers=headers)
    resp = response.json()
    return JsonResponse({'ret': resp}, safe=False)

def index(request):
    return render(request, "index.html")









class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    
class CasViewSet(viewsets.ModelViewSet):
    serializer_class = CasSerializer
    parser_classes = [MultiPartParser, FormParser]
    queryset = Cas.objects.all()
def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
class SharedCasViewSet(viewsets.ModelViewSet):
    queryset = SharedCase.objects.all()
    serializer_class = SharedCaseSerializer
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_id = self.request.user.id
        user = get_object_or_404(User, id=user_id)
        print(str(user))
       
        shared_cases = SharedCase.objects.filter(shared_with=user_id)
       
        print(shared_cases)
        cas_queryset = Cas.objects.filter(user__id=user_id)
        
        cas_serializer = CasSerializer(cas_queryset, many=True)
        shared_case_serializer = SharedCaseSerializer(shared_cases, many=True)
        return shared_cases
    
    def create(self, request, *args, **kwargs):
        data = request.data
        cas_id = data['cas']
        email_user = data['shared_with']
        try:
            user = User.objects.get(email=email_user)  
            case = Cas.objects.get(id=cas_id)  
        
        except User.DoesNotExist:
            return Response({"message": "L'utilisateur n'a pas été trouvé."}, status=status.HTTP_404_NOT_FOUND)
        except Cas.DoesNotExist:
            return Response({"message": "Le cas n'a pas été trouvé."}, status=status.HTTP_404_NOT_FOUND)
        
        new_sharedcase = SharedCase.objects.create(shared_with=user, cas=case)
        # notification_message = f"Le cas de Digital Smile Design a été partagé avec vous."
        # notification = Notification.objects.create(user=user, message=notification_message)
        # new_sharedcase.notification = notification
        new_sharedcase.save()
        serializer = SharedCaseSerializer(new_sharedcase)
        return Response(serializer.data)
def create_notification(request):
    cas_id = request.POST.get('casId')
    recipient_email = request.POST.get('recipientEmail')
    notification_message = f"Le cas {cas_id} a été partagé avec vous."
    new_notification = Notification.objects.create(
        user=User.objects.filter(email=recipient_email).first(),
        message=notification_message
    )

    response_data = {'message': 'Notification created successfully'}
    return JsonResponse(response_data)
     
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
class CasListView(generics.ListAPIView):
    queryset = Cas.objects.all()
    serializer_class = CasReadSerializer      
class CasCreateView(CreateAPIView):
    queryset = Cas.objects.all()
    serializer_class = CasWriteSerializer
class SharedCasListView(generics.ListAPIView):
    queryset = SharedCase.objects.all()
    serializer_class = SharedCaseReadSerializer


