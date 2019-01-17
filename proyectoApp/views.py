from django.shortcuts import render

def index(request):
	return render(request, 'indexProyecto2.html')

def loginView(request):
	return render(request,'registration/login.html')