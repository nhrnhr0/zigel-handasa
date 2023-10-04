from django.shortcuts import render

# from rest_framework import generics, permissions
# from rest_framework import generics

# from rejectedProject.models import RejectedReason
# from .models import AwaitingProject
# from .serializers import AwaitingProjectSerializer
# import django_filters.rest_framework
# from rest_framework import filters

# from core.filters import BaseDateFilter

# from django_filters import rest_framework
# from rest_framework.decorators import api_view
# from core.pagination import StandardResultsSetPagination
# from core.filters import MultiSelectFilter, CreatedAtBetweenDateFilterBackend, UpdatedAtBetweenDateFilterBackend,multiSelectFilterFactory

# from rest_framework.views import APIView
# from rest_framework.request import Request
# from awaiting_projects.models import AwaitingProject
# from rest_framework.response import Response
# from rest_framework import status
# from django.shortcuts import get_object_or_404
# from project.models import Project
from rest_framework.decorators import api_view
from .models import FileUpload
from .serializers import ProjectFilesSerializer
from django.http import JsonResponse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.base import ContentFile
from base_project.models import BaseProject
from rest_framework import status
@api_view(['GET'])
def get_files(request,project_id):
    print(project_id)
    try:
        project_files=BaseProject.objects.get(pk=project_id)
        queryset = project_files.files.all()
        serializer_class = ProjectFilesSerializer(queryset, many=True)
        return JsonResponse(serializer_class.data, safe=False)
    except BaseProject.DoesNotExist:
        return JsonResponse({'error': 'Project not found'}, status=404)

@api_view(['POST'])
def add_new_file(request):
    try:
        project_id = request.POST['projectId']
        project = BaseProject.objects.get(pk=project_id)
        
        if 'files' in request.FILES:
            file_list = request.FILES.getlist('files')
            file_names = request.POST.getlist('fileNames')

            for i in range(len(file_list)):
                current_file = FileUpload.objects.create(file_name=file_names[i], file=file_list[i])
                project.files.add(current_file)

        elif 'file' in request.FILES:
            file = request.FILES['file']
            file_name = request.POST['fileName']
            new_file = FileUpload.objects.create(file_name=file_name, file=file)
            project.files.add(new_file)

        else:
            return JsonResponse({'error': 'No files were provided in the request.'}, status=status.HTTP_400_BAD_REQUEST)

        project.save()
        queryset = project.files.all()
        serializer_class = ProjectFilesSerializer(queryset, many=True)
        return JsonResponse(serializer_class.data, safe=False)
    
    except BaseProject.DoesNotExist:
        return JsonResponse({'error': 'Project does not exist.'}, status=status.HTTP_404_NOT_FOUND)
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def delete_file(request):
    try:
        file_id = request.POST['fileId']
        project_id = request.POST['projectId']
        
        try:
            delete_file = FileUpload.objects.get(pk=file_id)
        except FileUpload.DoesNotExist:
            return JsonResponse({'error': 'File does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        
        delete_file.delete()
        
        try:
            files = BaseProject.objects.get(pk=project_id)
        except BaseProject.DoesNotExist:
            return JsonResponse({'error': 'Project does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        
        queryset = files.files.all()
        serializer = ProjectFilesSerializer(queryset, many=True)
        return JsonResponse(serializer.data, safe=False)
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

