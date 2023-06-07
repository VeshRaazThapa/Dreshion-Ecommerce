"""this section is for skin color and skin type extraction"""
import base64
import colorsys

import webcolors
from django.http import JsonResponse
from django.core.files.storage import default_storage
import face_recognition
from PIL import Image

import face_recognition

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.image as mpimg
from django.shortcuts import render

from PIL import Image
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import cv2
import extcolors

from colormap import rgb2hex
from django.conf import settings

from core.views import rank_matching_color_cloth
from core.views.utils import recognize_face, color_to_df
import os
from django.core.files.base import ContentFile

from colormath.color_objects import sRGBColor, HSLColor, LabColor
from colormath.color_diff import delta_e_cie2000
from colormath.color_conversions import convert_color
import matplotlib.pyplot as plt
import numpy as np
from webcolors import hex_to_rgb, rgb_to_hex, rgb_to_name


def face_dominant_color_extraction(request):
    if request.method == 'POST' and request.POST.get('image_data'):
        print('-------post----request')
        image_data = request.POST['image_data']
        image_data = image_data.replace("data:image/jpeg;base64,", "")
        image_binary = base64.b64decode(image_data)
        filename = "images/screen_capture.jpg"  # You can modify this to generate a unique filename if needed
        image_file = ContentFile(image_binary)
        saved_image_path = default_storage.save(filename, image_file)
        saved_image_abs_path = os.path.join(settings.MEDIA_ROOT, saved_image_path)
        resize = 900
        tolerance = 12
        zoom = 2.5
        output_width = resize
        img = recognize_face(saved_image_abs_path)
        if img.size[0] >= resize:
            wpercent = (output_width / float(img.size[0]))
            hsize = int((float(img.size[1]) * float(wpercent)))
            img = img.resize((output_width, hsize), Image.ANTIALIAS)
            resize_name = 'resize_' + saved_image_abs_path
            img.save(resize_name)
        else:
            resize_name = saved_image_abs_path
            img.save(resize_name)

        # create dataframe
        img_url = resize_name
        colors_x = extcolors.extract_from_path(img_url, tolerance=tolerance, limit=13)
        df_color = color_to_df(colors_x)

        # annotate text
        list_color = list(df_color['c_code'])
        list_precent = [int(i) for i in list(df_color['occurence'])]
        index = list_precent.index(max(list_precent))
        if list_color[index] == '#FFFFFF':
            index = index + 1
        max_color = list_color[index]
        palette = color_palette_generator(max_color)
        # print(max_color)
        # rgb = hex_to_rgb(max_color)
        return render(request, 'colors.html', {'identified_face_color': max_color,
                                               'identified_face_color_description': classify_skin_tone(max_color),
                                               **palette
                                               })

    return JsonResponse({'error': 'Invalid request'})


def color_palette_generator(hex_code):
    # Convert the given hex code to an sRGBColor object
    color = sRGBColor.new_from_rgb_hex(hex_code)

    # Calculate the delta E values to find matching colors
    delta_e = 20  # Adjust this threshold to control the similarity of colors

    # Generate a list of matching colors
    matching_colors = []
    for i in range(5):
        # Adjust the hue and saturation values to create variations
        new_color = convert_color(color, HSLColor)
        new_color.hsl_h += (i * 72) % 360  # Vary the hue by 72 degrees
        new_color.hsl_s *= 0.8 + (i * 0.05)  # Vary the saturation
        new_color = convert_color(new_color, sRGBColor)
        # Add the color to the palette if it's different enough from the original color
        if delta_e_cie2000(convert_color(color, LabColor), convert_color(new_color, LabColor)) > delta_e:
            matching_colors.append(new_color.get_rgb_hex())
            # Convert the color  to RGB
    r, g, b = tuple(int(hex_code[i:i + 2], 16) for i in (1, 3, 5))

    # Define the complementary color
    complementary_color = '#{:02x}{:02x}{:02x}'.format(255 - r, 255 - g, 255 - b)
    # Calculate triadic colors (120 degrees apart)
    triadic_colors = []
    # Convert RGB to HSL
    h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
    for i in range(3):
        hue = (h + i / 3) % 1
        triadic_color = tuple(round(i * 255) for i in colorsys.hls_to_rgb(hue, l, s))
        triadic_hex_code = '#' + "".join([hex(c)[2:].zfill(2) for c in triadic_color])
        # triadic_cloth_id = closest_color_cloth(triadic_hex_code, bottom_cloth_options)
        triadic_colors.append(
            triadic_hex_code
        )
    analogous = []
    for i in range(-3 // 2, 3 // 2 + 1):
        analogous_color = '#{:02x}{:02x}{:02x}'.format((r + i * 30) % 256, g, b)
        analogous.append(analogous_color)
    monochromatic = []
    for i in range(-3 // 2, 3 // 2 + 1):
        mono_color = '#{:02x}{:02x}{:02x}'.format(r, (g + i * 30) % 256, b)
        monochromatic.append(mono_color)

        return {'identified_face_color_description': classify_skin_tone(hex_code), 'matching': matching_colors,
                'complementary': complementary_color, 'triadic': triadic_colors, 'analogous': analogous,
                'monochromatic': monochromatic}


def get_color_palette(request):
    if request.method == 'GET' and request.GET.get('color'):
        color = request.GET.get('color')
        palette = color_palette_generator(color)
        return render(request, 'components/matching_colors.html', palette)

    return JsonResponse({'error': 'Invalid request'})


def get_matching_clothes(request):
    if request.method == 'GET' and request.GET.get('color'):
        color = request.GET.get('color')
        matching_color_cloths = rank_matching_color_cloth(color)
        return render(request, 'components/color_matched_clothes.html', {'object_list':matching_color_cloths})

    return JsonResponse({'error': 'Invalid request'})


def classify_skin_tone(hex_code):
    try:
        # Convert hex code to RGB values
        rgb = webcolors.hex_to_rgb(hex_code)

        # Separate the RGB values
        red, green, blue = rgb

        # Define warm and cool thresholds
        warm_threshold = 30
        cool_threshold = 25

        print(blue - red)
        print(blue - green)
        # Check if the color is warm, cool, or neutral based on RGB values
        if red - blue > warm_threshold and red - green > warm_threshold:
            return "Warm"
        elif blue - red > cool_threshold and blue - green > cool_threshold:
            return "Cool"
        else:
            return "Neutral"
    except ValueError:
        return "Invalid hex code"

# return JsonResponse({'error': 'Invalid request'})
