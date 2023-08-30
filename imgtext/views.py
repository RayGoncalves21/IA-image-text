import os
import random
import string

import cv2
import numpy as np
import pytesseract
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from PIL import Image


def home(request):
    if request.method == "GET":
        full_filename = 'images/white_bg.jpg'
        return render(request, "index.html", {'full_filename': full_filename})

    if request.method == "POST":
        image_upload = request.FILES['image_upload']
        imagename = image_upload.name
        image = Image.open(image_upload)

        image_arr = np.array(image.convert('RGB'))
        gray_img_arr = cv2.cvtColor(image_arr, cv2.COLOR_BGR2GRAY)
        image = Image.fromarray(gray_img_arr)

        letters = string.ascii_lowercase
        name = ''.join(random.choice(letters) for i in range(10)) + '.png'
        full_filename = 'uploads/' + name

        custom_config = r'-l eng --oem 3 --psm 6'
        text = pytesseract.image_to_string(image, config=custom_config)

        characters_to_remove = "!()@"
        new_string = text
        for character in characters_to_remove:
            new_string = new_string.replace(character, "")

        new_string = new_string.split("\n")
        option_bet_line1 = new_string[0]
        option_bet_line2 = new_string[1]
        print('Opção aposta: ', new_string[0], new_string[1])

        game = new_string[2][:-17]
        game_new_string = game.split(" v ")
        print(game_new_string)
        print('Times: ', game)
        
        fs = FileSystemStorage()
        filename = fs.save(os.path.join('uploads', name), image_upload)
        uploaded_file_url = fs.url(filename)
        print(uploaded_file_url)

        return render(request, 'index.html', {'full_filename':  uploaded_file_url, 'text': new_string})

# Note: In Django, the equivalent of "__name__ == '__main__'" is typically not used,
# as the application is managed by the Django framework itself.

    return render(request,'home.html')
