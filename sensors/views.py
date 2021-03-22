from django.shortcuts import render


# Create your views here.
def index(request):
    '''Вьюха отображения главной страницы'''
    # получаем список тегов из GET запроса

    data = 'привет'
    return render(request, 'index.html', context={'data': data, })
