from django.shortcuts import redirect, render
from django.urls import reverse


def home(request):
    if request.user.is_authenticated:
        return redirect(reverse("cred:cred_list"))
    else:
        nextpage = request.GET.get("next", "")
        return render(request, "home.html", {"next": nextpage})

def handle500(request):
    return render(request, "500.html", status=500)

def handle404(request, exception):
    return render(request, "404.html", status=404)
