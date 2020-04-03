from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .forms import UploadFileForm
from .utils import get_params, handle_uploaded_file


@csrf_exempt
def save_file(request):
    if request.method == "POST":
            form = UploadFileForm(get_params(request), request.FILES)
            if form.is_valid():
                path = handle_uploaded_file(request.FILES['file'])
            else:
                path = ""
    return path