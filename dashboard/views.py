
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from .forms import UploadFileForm


def home(request):
    form = UploadFileForm()
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            return HttpResponse("File uploaded successfully")

    context = {'form': form}
    return render(request, 'dashboard/home.html',context)
