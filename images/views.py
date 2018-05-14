from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from . import readimage
import pytesseract
from PIL import Image
from textblob import TextBlob
import cv2

def index(request):
    if request.method == 'POST' and request.FILES['photo']:
        myfile = request.FILES['photo']
        fs = FileSystemStorage('images/static/images/tmp')
        filename = fs.save(myfile.name, myfile)
        #uploaded_file_url = fs.url(filename)
        print(filename)
        uploaded_file_url = 'static/images/tmp/{}'.format(filename)
        file = readimage.get_text(filename)
        lang = request.POST['language']
        translation = readimage.translate(file, lang)
        print(uploaded_file_url)


        return render(request, 'images/index.html',{'uploaded_file_url':uploaded_file_url, 'message':file, 'translation':translation})

    default_image = " static/images/images/Tokyo.jpg "
    return render(request, 'images/index.html',{'uploaded_file_url': default_image})
# Create your views here.

def tess(request):
    if request.method == 'POST' and request.FILES['photo']:
        myfile = request.FILES['photo']
        fs = FileSystemStorage('images/static/images/tmp')
        filename = fs.save(myfile.name,myfile)
        origin = request.POST['origin']
        lang = request.POST['language']
        img = cv2.imread('images/static/images/tmp/{0}'.format(filename))
        img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        message = pytesseract.image_to_string(img, lang=origin)

        text = TextBlob(message)
        text = text.correct()
        try:
            after_translation = text.translate(to=lang)
        except:
            after_translation = "Cannot translate this message."
        return render(request, "images/tesser.html", {'message':message, 'translation':after_translation, 'image':'../static/images/tmp/{0}'.format(filename)})

    else:
        message = 'Translations can be a bit off at times, use common sense when interpreting the message.'
        return render(request, "images/tesser.html", {'message': message, 'image':' ../static/images/images/Tokyo.jpg'})
