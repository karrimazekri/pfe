from rest_framework import serializers
from .models import  Cas, Patient , User , SharedCase

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','email']
class PatientSerializer(serializers.ModelSerializer):
    user=UserSerializer()
    class Meta:
        model = Patient
        fields = ['data','user','date_creation']
    # def create(self, validated_data):
    #     user_data = validated_data.pop('user')  
    #     user = User.objects.create(**user_data)

    #     patient = Patient.objects.create(user=user, **validated_data)

    #     return patient
class CasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cas
        fields ='__all__'

class CasReadSerializer(serializers.ModelSerializer):
    user=UserSerializer()
    patient=PatientSerializer()
    class Meta:
        model = Cas
        fields = ['id', 'user','image_avant','image_apres','patient','shared_with','created_at','updated_at']
class CasWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cas
        fields = '__all__'        

class SharedCaseSerializer(serializers.ModelSerializer):
    # cases = CasSerializer(many=True)

    # def create(self, validated_data):
    #     cases_data = validated_data.pop('cases')
    #     shared_case = SharedCase.objects.create(**validated_data)
    #     for case_data in cases_data:
    #         Cas.objects.create(shared_case=shared_case, **case_data)

    #     return shared_case
    shared_with=UserSerializer
    class Meta:
        model =  SharedCase
        fields = '__all__'
class SharedCaseReadSerializer (serializers.ModelSerializer):
    cas=CasReadSerializer
    class Meta:
        model =  SharedCase
        fields = ['id','shared_with','cas','end_date']
        depth =2
