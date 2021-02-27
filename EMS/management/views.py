
from django.shortcuts import render
from rest_framework import status
from rest_framework import serializers
from rest_framework.serializers import Serializer
from rest_framework.views import APIView
from rest_framework.response import Response
from users.JWTTokens import *
from users.JWTTokenAuthentication import JWTAuthentication
from users.permissions import *
from users.backend  import MyAuthentication
from users.models import employers,employer_profile,companies,company_profile
from  users.serializer import companySerializer,employerSerializer,company_profileSerializer, employer_profileSerializer,employer_profileSerializer
from .serializer import SalarySerializer,ProjectSerializer,LeaveSerializer,DepartmentSerializer,AttendanceSerializer, company_department_serializer
from .models import Attendance, Department_company, Leave, Project,Department,Salary

class projects(APIView):
    authentication_classes=[JWTAuthentication]
    permission_classes=[companyPermission]
    def get(self,request,pk=None):
      company_id=request.session['company_id']
      if pk is None:
        try:  
            all_project=Project.objects.filter(company_id=company_id)
            serializer=ProjectSerializer(all_project,many=True)
            return Response(serializer.data)
        except Exception as e:
            print(e)
            return Response({'message':'You have no company'})  
      else:
         try:
          all_project=Project.objects.get(company_id=company_id,project_id=pk)
          serializer=ProjectSerializer(all_project)
          return Response(serializer.data)
         except:
             return Response({'message':'project id is wrong'})

    def post(self,request):
        request.data['company_id']=request.session['company_id']
        serializer=ProjectSerializer(data=request.data)    
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'Project added'})
        return Response(serializer.errors)    
    def put(self, request,pk=None):
        
        id =pk
        company_id=request.session['company_id']
        project = Project.objects.get(project_id=id,company_id=company_id)
        serializer = ProjectSerializer(project,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'Data Updated'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)     

    def patch(self, request,pk=None):
        id =pk
        company_id=request.session['company_id']
        project = Project.objects.get(project_id=id,company_id=company_id)
        serializer = ProjectSerializer(project,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'Data Updated'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
    def delete(self, request, pk, format=None):
        id = pk
        company_id=request.session['company_id']
        project = Project.objects.get(project_id=id,company_id=company_id)
        project.delete()
        return Response({'message':'Project Deleted'})        

class leaves(APIView):
    authentication_classes=[JWTAuthentication]
    permission_classes=[OnlyCompanyPermission]
    def get(self,request,pk=None):
        id=pk
        company_id=request.session['company_id']
        if id is None:
            data=Leave.objects.filter(company_id=company_id)
            serializer=LeaveSerializer(data,many=True)
            return Response(serializer.data)
        else:
            data=Leave.objects.get(leave_id=id,company_id=company_id)
        
            serializer=LeaveSerializer(data)
            return Response(serializer.data)
   
    def patch(self,request,pk=None):
        if pk is not None:
            leave_id=pk
            company_id=request.session['company_id']
            data1=Leave.objects.get(leave_id=leave_id,company_id=company_id)    
            serializer=LeaveSerializer(data1,data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'message':'updated'})
            return Response(serializer.errors) 
        return Response({'message':'leave_id required in params'})      
    def delete(self,request,pk=None): 
        leave_id=pk
        company_id=request.session['company_id']
      
        leave_obj=Leave.objects.get(leave_id=leave_id,company_id=company_id)    
        leave_obj.delete()
        return Response({'message':'deleted successfully'})

class leave_detail(APIView):
    authentication_classes=[JWTAuthentication]
    permission_classes=[OnlyEmployerPermission]
    def get(self,request):
        emp_id=request.session['emp_id']
        company_id=request.session['company_id']
        data=Leave.objects.filter(emp_id=emp_id,company_id=company_id)
        serializer=LeaveSerializer(data,many=True)
        return Response(serializer.data)      

    def post(self,request):
        data={
            "emp_id":request.session['emp_id'],
            "company_id":request.session['company_id'],
            "subject":request.data.get('subject'),
            "to_date":request.data.get('to_date'),
            "from_date":request.data.get('from_date'),
            "reason":request.data.get('reason'),
            "leave_type":request.data.get('leave_type'),
        }
        serializer=LeaveSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'request done'})      
        return Response(serializer.errors) 
  

class all_departments(APIView):
    authentication_classes=[JWTAuthentication]
   
    def get(self,request):
        all_department=Department.objects.all()
        serializer=DepartmentSerializer(all_department,many=True)
        return Response(serializer.data)   
    def post(self,request):
        data={
            'department_name':request.data.get('department_name'),
            'created_by':request.session['company_id']

        }
        serializer=DepartmentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'requested successfully'})  
        return Response(serializer.errors)     

class add_department(APIView):
    authentication_classes=[JWTAuthentication]
    def get(self,request):
        all_department=Department_company.objects.filter(company_id=request.session['company_id'])
        serializer=company_department_serializer(all_department,many=True)
        return Response(serializer.data)
    def post(self,request):
        data={
            "company_id":request.session['company_id'],
            "dept_id":request.data.get('department_id')
        }
        serializer=company_department_serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'Added'})
        return Response(serializer.errors)    
    def delete(self,request,pk=None):
        dept_obj=Department_company.objects.get(id=pk)
        dept_obj.delete()
        return Response({'message':'deleted'})    



class salary(APIView):
    authentication_classes=[JWTAuthentication]
    permission_classes=[OnlyCompanyPermission]
    def get(self,request,pk=None):
        if pk is not None:
            all_salaries=Salary.objects.filter(emp_id=pk,company_id=request.session['company_id'])
            serializer=SalarySerializer(all_salaries,many=True)
            return Response(serializer.data)
        else:
            all_salaries=Salary.objects.filter(company_id=request.session['company_id'])
            serializer=SalarySerializer(all_salaries,many=True)
            return Response(serializer.data)


    def post(self,request,pk=None):
        company_id=request.session['company_id']
        print(request.data)
        print(pk)
        data={
            "emp_id":pk,
            "company_id":company_id,
            "month":request.data.get('month'),
            "paid_date":request.data.get('paid_date'),
            "salary":request.data.get('salary'),
            
        
        }
        serializer=SalarySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'salary paid successfully'})
        return Response(serializer.errors)
    def patch(self,request,pk=None):
        emp_id=pk
        company_id=request.session['company_id']
        data1=salary.objects.filter(emp_id=emp_id,company_id=company_id)    
        serializer=SalarySerializer(data1,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'updated'})
        return Response(serializer.errors)    
    def delete(self,request,pk=None):
        emp_id=pk
        company_id=request.session['company_id']
        data1=salary.objects.filter(emp_id=emp_id,company_id=company_id)    
        data1.delete()
        return Response({'message':'deleted'})            
class salary_detail(APIView):
    authentication_classes=[JWTAuthentication]
    permission_classes=[OnlyEmployerPermission]
    def get(self,request):      
        all_salaries=Salary.objects.filter(emp_id=request.session['emp_id'],company_id=request.session['company_id'])
        serializer=SalarySerializer(all_salaries,many=True)
        return Response(serializer.data)




class attendance(APIView):
    authentication_classes=[JWTAuthentication]
    permission_classes=[OnlyCompanyPermission]
    def get(self,request):
        data=Attendance.objects.filter(company_id=request.session['company_id'])
        serializer=AttendanceSerializer(data,many=True)
        return Response(serializer.data)
    def patch(self,request,pk=None):
        attend_obj=Attendance.objects.get(attendance_id=pk,company_id=request.session['company_id'])    
        serializer=AttendanceSerializer(attend_obj,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'updated'})
        return Response(serializer.errors)    
    def delete(self,request,pk=None):
         attend_obj=Attendance.objects.get(attendance_id=pk,company_id=request.session['company_id']) 
         attend_obj.delete()
         return Response({'message':'deleted'})
    def post(self,request):
        #request.data['company_id']=request.session['company_id']
        serializer=AttendanceSerializer(data=request.data,many=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'saved'})
        return Response(serializer.errors)       
class my_attendance(APIView):
    authentication_classes=[JWTAuthentication]
    permission_classes=[OnlyEmployerPermission]
    def get(self,request):
      
        data=Attendance.objects.filter(emp_id=request.session['emp_id'],company_id=request.session['company_id'])
        serializer=AttendanceSerializer(data,many=True)
        return Response(serializer.data)

class check(APIView):
    def post(self,request):
        print(request.data)
        return Response({'message':'done'})          

class salary1(APIView):
     authentication_classes=[JWTAuthentication]
     def post(self,request,pk=None):
         company_id=request.session['company_id']
         print(request.data)
         print(pk)
         data={
             "emp_id":pk,
             "company_id":company_id,
             "month":request.data.get('month'),
             "paid_date":request.data.get('paid_date'),
             "salary":request.data.get('salary'),
             
            
         }
         serializer=SalarySerializer(data=data)
         if serializer.is_valid():
             serializer.save()
             return Response({'message':'salary paid successfully'})
         return Response(serializer.errors)
         #return Response({'message':data})

