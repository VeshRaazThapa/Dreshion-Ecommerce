from django.db.models.signals import post_save, post_delete, pre_delete
from django.dispatch import receiver
from django.conf import settings
from core.models import Item,Profile
from django.core.files.base import ContentFile

import json
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder

from django.core.files import File
API_BASE_URL = 'http://127.0.0.1:5000'
@receiver(post_save, sender=Item)
def clothing_preprocessing(sender, instance, created, **kwargs):

    if created or instance.process_image:

        # Open the file and create a requests.FileAdapter for it
        with instance.image.open() as f:
            file = File(f)
            file_data = file.read()

        # Construct the data payload for the POST request
        data = {
            'item_id': instance.id,
        }

        # Construct the files payload for the POST request
        files = {
            'image': ('cloth.jpg', file_data, 'image/jpeg'),
        }
        # multipart_data = MultipartEncoder(fields=data)

        # Make the POST request to the API endpoint
        response = requests.post(API_BASE_URL+'/process-cloth-image', data=data,files=files
                                 # headers={'Content-Type': multipart_data.content_type}
                                 )

        instance.process_image = False
        instance.save()

        # Check the response status code
        if response.status_code == 200:
            print('Image file sent successfully!')
            instance.edge_image.save('test_edge.png', ContentFile(response.content), save=True)


        else:
            print(f'Error sending image file: {response.text}')@receiver(post_save, sender=Item)

@receiver(post_save, sender=Profile)

def person_preprocessing(sender, instance, created, **kwargs):

    if created or instance.process_image:
    # if False:

        # Open the file and create a requests.FileAdapter for it
        with instance.front_image.open() as f:
            file = File(f)
            file_data = file.read()

        # Construct the data payload for the POST request
        data = {
            'item_id': instance.id,
        }

        # Construct the files payload for the POST request
        files = {
            'image': ('person.jpg', file_data, 'image/jpeg'),
        }
        # multipart_data = MultipartEncoder(fields=data)

        # Make the POST request to the API endpoint
        response = requests.post(API_BASE_URL+'/process-person-image', data=data,files=files
                                 # headers={'Content-Type': multipart_data.content_type}
                                 )

        instance.process_image = False
        instance.save()

        # Check the response status code
        if response.status_code == 200:
            print('Image file sent successfully!')

            zip_file = response.content
            import tempfile
            import zipfile
            import os
            # create a temporary file to save the zip file to
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_file.write(zip_file)
                temp_file_path = temp_file.name

            # extract individual files from the zip file and save them to model fields
            with zipfile.ZipFile(temp_file_path, mode='r') as zip_file:
                file1_contents = zip_file.read('file1.json')
                file2_contents = zip_file.read('file2.png')

            # content_file = file1_contents.read()
            # Profile.objects.filter(pk=instance.pk).update(pose_keypoints=content_file, update_fields=['pose_keypoints'])
            # content_file.close()
            # Profile.objects.filter(pk=instance.pk).update(label_image=ContentFile(file2_contents), update_fields=['label_image'])


            instance.pose_keypoints.save('person_pose_keypoints.json', ContentFile(file1_contents), save=True)
            instance.label_image.save('person.png', ContentFile(file2_contents), save=True)

        else:
            print(f'Error sending image file: {response.text}')