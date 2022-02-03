from django.shortcuts import render

# Create your views here.
def main_view(request):
    return render(request, 'movie/main.html')

def genre_view(request):
    return render(request, 'movie/genre.html')

def contents_view(request):
    return render(request, 'movie/contents.html')