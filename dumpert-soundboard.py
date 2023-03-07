import requests
import os
import eyed3

METADATA_URL = 'https://video-snippets.dumpert.nl/soundboard.json'

# Create output dir
os.makedirs("output", exist_ok=True)

# Get meta
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/110.0'}
cookies = {'__cf_bm': 'oJ3drJj31_Tp.x8U25D10dveJPSq91LwXW4n_mqXRKg-1677849352-0-AYDRw3cDaqfIqxIL1XMZMRpgwhwV4sOIjQyr/5RI+QQDdtRsaLTq1vEfHo2W5zS69xVvYKRUAh7MAFuxVCNC6BU='}
r = requests.get(METADATA_URL, headers=headers, cookies=cookies)
metadata = r.json()

for soundbite in metadata:
    # Prepare filename
    filename = f"output/{soundbite['name']}.mp3"

    # Download and save
    r = requests.get(soundbite["url"], headers=headers, cookies=cookies)
    with open(filename, "wb") as f:
        f.write(r.content)

    # Put name and thumbnail in ID3
    r = requests.get(soundbite["thumbnail"], headers=headers, cookies=cookies)
    imagedata = r.content

    audiofile = eyed3.load(filename)
    audiofile.tag.title = soundbite["name"]
    audiofile.tag.images.set(3, imagedata, "image/png")
    audiofile.tag.save()
