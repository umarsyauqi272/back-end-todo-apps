from django.shortcuts import render

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
 
from todos.models import Todo
from todos.serializers import TodoSerializer
from rest_framework.decorators import api_view


@api_view(['GET', 'POST', 'DELETE'])
def todo_list(request):
    if request.method == 'GET':
        todos = Todo.objects.all()
        
        title = request.GET.get('title', None)
        if title is not None:
            todos = todos.filter(title__icontains=title)
        
        todos_serializer = TodoSerializer(todos, many=True)
        return JsonResponse(todos_serializer.data, safe=False)
        # 'safe=False' for objects serialization
 
    elif request.method == 'POST':
        todo_data = JSONParser().parse(request)
        todo_serializer = TodoSerializer(data=todo_data)
        if todo_serializer.is_valid():
            todo_serializer.save()
            return JsonResponse(todo_serializer.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(todo_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        count = Todo.objects.all().delete()
        return JsonResponse({'message': '{} All Todo Items were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)
 
 
@api_view(['GET', 'PUT', 'DELETE'])
def todo_detail(request, pk):
    try: 
        todo = Todo.objects.get(pk=pk) 
    except Todo.DoesNotExist: 
        return JsonResponse({'message': 'Todo Item does not exist'}, status=status.HTTP_404_NOT_FOUND) 
 
    if request.method == 'GET': 
        todo_serializer = TodoSerializer(todo) 
        return JsonResponse(todo_serializer.data) 
 
    elif request.method == 'PUT': 
        todo_data = JSONParser().parse(request) 
        todo_serializer = TodoSerializer(todo, data=todo_data) 
        if todo_serializer.is_valid(): 
            todo_serializer.save() 
            return JsonResponse(todo_serializer.data) 
        return JsonResponse(todo_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
 
    elif request.method == 'DELETE': 
        todo.delete() 
        return JsonResponse({'message': 'Todo Item was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
    
        
@api_view(['GET'])
def todo_list_finished(request):
    todos = Todo.objects.filter(finished=True)
    if request.method == 'GET':
        todos_serializer = TodoSerializer(todos, many=True)
        return JsonResponse(todos_serializer.data, safe=False)