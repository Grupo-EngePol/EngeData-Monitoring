'''
This file is used for handling anything image related.
I suggest handling the local file encoding/decoding here as well as fetching any external images.
'''

# package imports
import base64
import os

# image CDNs
image_cdn = 'https://images.dog.ceo/breeds'

# logo information
cwd = os.getcwd()

logo_EngeData_path_white = os.path.join(cwd, 'assets', 'logos', 'EngeData_transparente.png')
logo_EngeData_tunel_white = base64.b64encode(open(logo_EngeData_path_white, 'rb').read())
logo_EngeData_encoded_white = 'data:image/png;base64,{}'.format(logo_EngeData_tunel_white.decode())


logo_EngeData_path_dark = os.path.join(cwd, 'assets', 'logos', 'EngeData_transparente.png')
logo_EngeData_tunel_dark = base64.b64encode(open(logo_EngeData_path_dark, 'rb').read())
logo_EngeData_encoded_dark = 'data:image/png;base64,{}'.format(logo_EngeData_tunel_dark.decode())







def get_dog_image(breed, name):
    '''
    This method assumes that you are fetching specific images hosted on a CDN.
    For instance, random dog pics given a breed.
    '''
    if breed and name:
        return f'{image_cdn}/{breed}/{name}.jpg'
    return None