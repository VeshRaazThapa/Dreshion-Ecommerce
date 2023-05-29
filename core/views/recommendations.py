from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, View
from .constants import body_types
from core.models import Item, OrderItem, Order, BillingAddress, Payment, Coupon, Refund, Category, BodyType, Occasion, UNDER_TONE_CHOICES,SKIN_TONE_CHOICES
from webcolors import hex_to_rgb, rgb_to_hex
import numpy as np
from math import sqrt
import colorsys

from django.http import JsonResponse


def filter_data(request):
    # Retrieve filter parameters from GET request
    occasion_filter = request.GET.get('occasion_id')
    # filter2 = request.GET.get('filter2')
    # print(occasion_filter)

    user_profile = request.user.profile
    user_body_type = user_body_type_detection(user_profile.bust, user_profile.hip,
                                              user_profile.high_hip, user_profile.waist,
                                              user_profile.gender)
    # Search for the row with the given ID
    if occasion_filter == '0':
        # for all occasion data
        data = Item.objects.filter(category=1, body_type=user_body_type, is_active=True)
    else:
        data = Item.objects.filter(category=1, body_type=user_body_type,occasion=occasion_filter, is_active=True)


    # Filter the data based on the provided filters
    # data = Item.objects.filter(field1=filter1, field2=filter2).values('field1', 'field2', 'field3')

    # Return the filtered data as a html response
    return render(request, 'filters.html', {'data':data})

def get_recommendation(user,category):

    user_profile = user.profile
    user_body_type = user_body_type_detection(user_profile.bust, user_profile.hip,
                                              user_profile.high_hip, user_profile.waist,
                                              user_profile.gender)

    # print(user_body_type)
    # Search for the row with the given ID
    user_appropriate_clothes = Item.objects.filter(category=1, gender=user_profile.gender, body_type=user_body_type, is_active=True)

    # Display the result
    # print(user_appropriate_clothes)
    context = {
        'test': 'test',
        'object_list': user_appropriate_clothes,
        'category_title': category.title,
        'category_description': category.description,
        'category_image': category.image,
        'user_profile':user_profile,
        'user_body_type':user_body_type,
        'occasions':Occasion.objects.all(),
        'skin_tone':dict(SKIN_TONE_CHOICES),
        'under_tone':dict(UNDER_TONE_CHOICES),
    }
    return context

def user_body_type_detection(bust, hip, high_hip, waist, gender):

    body_type_prediction = ''
    # body_types = BodyType.objects.all()
    if (bust - hip) <= 1 and (hip - bust) < 3.6 and (bust - waist) >= 9 or (hip - waist) >= 10:
        if gender == 'female':

            body_type_prediction = body_types[0]['name']
        else:
            body_type_prediction = body_types[3]['name']
    if gender == 'female':
        if 1 < (bust - hip) <= 10 and (bust - waist) >= 9:
            body_type_prediction = body_types[1]['name']

        if 3.6 <= (hip - bust) < 10 and (hip - waist) >= 9 and (high_hip / waist) < 1.193:
            body_type_prediction = body_types[2]['name']

    if 2 < (hip - bust) and (hip - waist) >= 7 and (high_hip / waist) < 1.193:
        body_type_prediction = body_types[4]['name']

    if (bust - hip) >= 3.6 and (bust - waist) < 9:
        body_type_prediction = body_types[5]['name']

    if (hip - bust) < 3.6 and (bust - hip) < 3.6 and (bust - waist) < 9 and (hip - waist) < 10:
        body_type_prediction = body_types[6]['name']
        # print('-------body type prediction -------')
    if (hip - bust) >= 3.6 and (hip - waist) < 9:
        body_type_prediction = body_types[7]['name']
    return BodyType.objects.get(name=body_type_prediction)
    # return body_type_prediction


def calculate_harmony_score(target, cloth_options):
    harmony_score = 0
    for cloth_option in cloth_options:
        color = cloth_option['color']
        hue1, lightness1, saturation1 = colorsys.rgb_to_hls(*hex_to_rgb(target))
        hue2, lightness2, saturation2 = colorsys.rgb_to_hls(*hex_to_rgb(color))
        hue_diff = min(abs(hue1 - hue2), 1 - abs(hue1 - hue2))
        lightness_diff = abs(lightness1 - lightness2)
        saturation_diff = abs(saturation1 - saturation2)
        harmony_score += (1 - (hue_diff + lightness_diff + saturation_diff) / 3)
    return harmony_score / len(cloth_options)


print('-------bottom options---------')

# Define a function to find the closest color match using the color distance formula
def closest_color_cloth(target, clothes):
    closest_color_cloth = None
    min_distance = float('inf')
    for cloth in clothes: # [{'cloth':'','color':''}]
        color = cloth['color']
        distance = sqrt(sum((int(target[i:i + 2], 16) - int(color[i:i + 2], 16)) ** 2 for i in (1, 3, 5)))
        if distance < min_distance:
            closest_color_cloth = cloth
            min_distance = distance
    return closest_color_cloth['cloth']

# Define a function to recommend the appropriate bottom cloth using the color theory rules
def recommend_matching_cloth(top_color, bottom_cloth_options, num_analogous=2, num_monochromatic=2, num_triadic=1,
                           harmony_weight: float = 0.5):
    harmony_scores = {}
    recommended_bottom_cloth = {}

    for bottom_cloth_option in bottom_cloth_options:
        harmony_scores[bottom_cloth_option['cloth']] = calculate_harmony_score(bottom_cloth_option['color'], bottom_cloth_options)

    # Convert the top color to RGB
    r, g, b = tuple(int(top_color[i:i + 2], 16) for i in (1, 3, 5))

    # Define the complementary color and find the closest match among the bottom options
    complementary_color = '#{:02x}{:02x}{:02x}'.format(255 - r, 255 - g, 255 - b)
    complementary_cloth_id = closest_color_cloth(complementary_color, bottom_cloth_options)
    recommended_bottom_cloth['complementary'] = [
     { 'cloth':complementary_cloth_id ,'score': harmony_weight * harmony_scores[complementary_cloth_id]}]

    # Calculate triadic colors (120 degrees apart)
    triadic_colors = []
    # Convert RGB to HSL
    h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
    for i in range(num_triadic):
        hue = (h + i / 3) % 1
        triadic_color = tuple(round(i * 255) for i in colorsys.hls_to_rgb(hue, l, s))
        triadic_hex_code = '#' + "".join([hex(c)[2:].zfill(2) for c in triadic_color])
        triadic_cloth_id = closest_color_cloth(triadic_hex_code, bottom_cloth_options)
        triadic_colors.append({'cloth':triadic_cloth_id, 'score': harmony_weight * harmony_scores[triadic_cloth_id]})
    recommended_bottom_cloth['triadic'] = triadic_colors
    # Define the analogous colors and find the closest matches among the bottom options

    analogous = []
    for i in range(-num_analogous // 2, num_analogous // 2 + 1):
        analogous_color = '#{:02x}{:02x}{:02x}'.format((r + i * 30) % 256, g, b)
        analogous_cloth_id = closest_color_cloth(analogous_color, bottom_cloth_options)
        analogous.append({'cloth': analogous_cloth_id, 'score': harmony_weight * harmony_scores[analogous_cloth_id]})
    recommended_bottom_cloth['analogous'] = analogous
    #
    # Define the monochromatic colors and find the closest matches among the bottom options
    monochromatic = []
    for i in range(-num_monochromatic // 2, num_monochromatic // 2 + 1):
        mono_color = '#{:02x}{:02x}{:02x}'.format(r, (g + i * 30) % 256, b)
        mono_cloth_id = closest_color_cloth(mono_color, bottom_cloth_options)
        monochromatic.append({'cloth':mono_cloth_id, 'score': harmony_weight * harmony_scores[mono_cloth_id]})
    recommended_bottom_cloth['monochromatic'] = monochromatic
    # Rank the recommended bottom cloth options based on harmony score and weight
    print(recommended_bottom_cloth)
    for key in recommended_bottom_cloth:
        recommended_bottom_cloth[key].sort(key=lambda x: x['score'], reverse=True)

    # Return the recommended bottom cloth options for each color theory rule
    return recommended_bottom_cloth