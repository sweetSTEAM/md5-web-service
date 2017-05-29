from django.shortcuts import render

def index(request):
    ''' Just delivering the main page '''
    return render(request, 'index.html', None)