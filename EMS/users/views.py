from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .JWTTokens import *
from .JWTTokenAuthentication import JWTAuthentication
from .permissions import companyPermission,employerPermission
from .backend  import MyAuthentication
from .models import employers,employer_profile,companies,company_profile
from  .serializer import companySerializer,employerSerializer,company_profileSerializer, employer_profileSerializer,employer_profileSerializer

class newuser(APIView):
   def post(self,request):
        serializer=companySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'registered'})
            
        return Response(serializer.errors)
class gettoken(APIView):
    def post(self,request):
        email=request.data.get('email')
        password=request.data.get('password')
        user=MyAuthentication.authenticate(request,email=email,password=password)
        print(user)
        if user is not None:
            
            access=access_token(user)
            refresh=refresh_token(user)
            MyAuthentication.login(request,user.email)
            if MyAuthentication.isemployee(user.email):
                role="employee"
                id=user.emp_id
            else:
                role="company"
                id=user.company_id

        return Response({'user':id,'access':access,'refresh':refresh,'role':role})

class company_register(APIView):
    authentication_classes=[JWTAuthentication]
    permission_classes=[companyPermission]
    def post(self,request):
        serializer=companySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'registered'})
        return Response(serializer.errors)  
    def get(self,request):
        company_id=request.session['company_id']
        data=companies.objects.get(company_id=company_id)  
        serializer=companySerializer(data)
        return Response(serializer.data) 
class company_pofile(APIView):
    authentication_classes=[JWTAuthentication]
    permission_classes=[companyPermission]
    def get(self,request):
        id=request.session['company_id']
        data=company_profile.objects.get(company_id=id) 
       
        serializer=company_profileSerializer(data)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def post(self,request):
        serializer=company_profileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'saves successfully'})
        return Response(serializer.errors) 

    def put(self, request):
        id = request.session['company_id']
        company = company_profile.objects.get(company_id=id)
        serializer = company_profileSerializer(company, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'Data Updated'})
        return Response(serializer.errors)

    def patch(self, request):
        id = request.session['company_id']
        print(id)
        company = company_profile.objects.get(company_id=id)
        serializer = company_profileSerializer(company, data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'partial Data Updated'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class employer_register(APIView):
    authentication_classes=[JWTAuthentication]
    permission_classes=[companyPermission]
    def get(self,request,pk=None):
        id=pk
        company_id=request.session['company_id']
        if id is None:
            
            data=employers.objects.filter(company_id=company_id)  
            serializer=employerSerializer(data,many=True)
            return Response(serializer.data) 
        employer=employers.objects.get(emp_id=id,company_id=company_id) 
        serializer=employerSerializer(employer)  
        return Response(serializer.data) 
    def post(self,request):
        
        data={

	"email":request.data.get('email'),
	"name":request.data.get('name'),
	"password":request.data.get('password'),
	"company_id":request.session['company_id']
        }
        serializer=employerSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'registered successfully'})
        else:    
            msg={'message':'not registered something wrong wit data',
                     'msg':serializer.errors}
            return Response(msg)

    
    def delete(self, request, pk, format=None):
        company_id=request.session['company_id']
        id = pk
        stu = employers.objects.get(emp_id=id,company_id=company_id)
        stu.delete()
        return Response({'message':'Data Deleted'})   
    def patch(self, request,pk,format=None):
        emp_id=pk
        company_id = request.session['company_id']
        data={
            'name':request.data.get('name'),
            'company_id':company_id,
            'password':request.data.get('password')
        }
        employer = employers.objects.get(emp_id=emp_id,company_id=company_id)
        serializer = employerSerializer(employer,request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'Data Updated','note':'only name and password can be changed'})
        return Response(serializer.errors)    
class employer_profiles(APIView):
    authentication_classes=[JWTAuthentication]
    permission_classes=[companyPermission]
    def get(self,request,pk=None):
        id=pk
        company_id=request.session['company_id']
        if id is not None:
            
            data=employer_profile.objects.get(company_id=company_id,emp_id=id)  
            serializer=employer_profileSerializer(data)
            return Response(serializer.data) 
        return Response({'message':'emp_id must be present in url'})
       
    def post(self,request):
        data={
    "emp_id":request.data.get('emp_id'),       
	"dob":request.data.get('dob'),
    "joining_date":request.data.get('joining_date'),
	"address":request.data.get('address'),
	"mobile_no":request.data.get('mobile_no'),
    "gender":request.data.get('gender'),
	"company_id":request.session['company_id'],
    "project_id":request.data.get('project_id'),
    "department_id":request.data.get('department_id'),
    "status":request.data.get('status'),
    "job_type":request.data.get('job_type'),

        }
        serializer=employer_profileSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'saved successfully'})
        return Response(serializer.errors)           

    def patch(self, request,pk,format=None):
        emp_id=pk
        data={      
	"dob":request.data.get('dob'),
    "joining_date":request.data.get('joining_date'),
	"address":request.data.get('address'),
	"mobile_no":request.data.get('mobile_no'),
    "gender":request.data.get('gender'),
	"company_id":request.session['company_id'],
    "project_id":request.data.get('project_id'),
    "department_id":request.data.get('department_id'),

        }
        company_id = request.session['company_id']
       
        employer = employer_profile.objects.get(emp_id=emp_id,company_id=company_id)
        serializer = employerSerializer(employer,request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'Data Updated','note':'empid and company_id never changed'})
        return Response(serializer.errors)    

class employer_id(APIView):
    authentication_classes=[JWTAuthentication]
    permission_classes=[companyPermission]
    def post(self,request):
        email=request.data.get('email')
        company_id=request.session['company_id']        
        data=employers.objects.get(email=email,company_id=company_id)
        serializer=employerSerializer(data)
        return Response(serializer.data)