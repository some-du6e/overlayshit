import io
import requests as req
from PIL import Image

OVERLAYS_URL = "https://pfp.hackclub.com/api/styles"



def overlayPicture(base, overlay):
    print(base, overlay)
    baseimg = Image.open(base)
    overlayimg = (
        Image.open(io.BytesIO(overlay))
        if isinstance(overlay, bytes)
        else Image.open(overlay)
    )

    overlayimg.thumbnail(baseimg.size, Image.LANCZOS)
    x = (baseimg.width - overlayimg.width) // 2
    y = (baseimg.height - overlayimg.height) // 2

    baseimg.paste(overlayimg, (x, y), mask=overlayimg)
    baseimg.show()
    input()


def getoverlays():
    overlays = req.get(OVERLAYS_URL).json()
    return overlays



def getoverlay(id):
    overlays = getoverlays()

    option = next(
        opt
        for s in overlays["styles"]
        for opt in s["options"]
        if opt["id"] == id
    )

    return option
    

def downloadoverlay(overlayurl):
    overlay = req.get(overlayurl)
    return overlay.content



def getoverlayimage(overlay):
    url = overlay["overlayPath"]

    return downloadoverlay(url) 