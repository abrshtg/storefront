from django.shortcuts import render


# Create your views here.
def greeting(request):
    name = request.GET["name"]
    return render(request, "playground/index.html", {"name": name})
