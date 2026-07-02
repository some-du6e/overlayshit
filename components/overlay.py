import requests as req # pyright: ignore[reportMissingModuleSource, reportMissingImports]
from PIL import Image # pyright: ignore[reportMissingImports]
from flask import Response # pyright: ignore[reportMissingModuleSource]
import io
from urllib.parse import urljoin

OVERLAYS_URL = "https://pfp.hackclub.com/api/styles"
PFP_BASE_URL = "https://pfp.hackclub.com"
OVERLAY_CACHE = {}



def overlayPicture(base, overlay):
    baseimg = Image.open(base).convert("RGBA")
    baseimg = applyOverlay(baseimg, overlay)

    buffer = io.BytesIO()
    baseimg.save(buffer, format="PNG")
    buffer.seek(0)

    return Response(buffer, mimetype="image/png")


def applyOverlay(baseimg, overlay):
    overlayimg = (
        Image.open(io.BytesIO(overlay))
        if isinstance(overlay, bytes)
        else Image.open(overlay)
    ).convert("RGBA")

    overlayimg.thumbnail(baseimg.size, Image.LANCZOS)
    x = (baseimg.width - overlayimg.width) // 2
    y = (baseimg.height - overlayimg.height) // 2

    baseimg.paste(overlayimg, (x, y), mask=overlayimg)
    return baseimg


def imageResponse(image):
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)
    return Response(buffer, mimetype="image/png")


def getoverlays():
    overlays = req.get(OVERLAYS_URL).json()
    return overlays



def getoverlay(id):
    overlays = getoverlays()

    option = next(
        (opt
        for s in overlays["styles"]
        for opt in s["options"]
        if opt["id"] == id),
        None
    )

    return option
    

def downloadoverlay(overlayurl):
    overlayurl = urljoin(PFP_BASE_URL, overlayurl)
    if overlayurl in OVERLAY_CACHE:
        return OVERLAY_CACHE[overlayurl]

    overlay = req.get(overlayurl, timeout=10)
    overlay.raise_for_status()
    OVERLAY_CACHE[overlayurl] = overlay.content
    return OVERLAY_CACHE[overlayurl]



def getoverlayimage(overlay):
    url = overlay["overlayPath"]

    return downloadoverlay(url) 

def getoverlayamount():
    overlays = getoverlays()
    amount = 0 

    for i in overlays["styles"]:

        amount += len(i["options"])
    
    return amount



def getalloverlays(asIds=False):
    overlays = getoverlays()
    all = []

    for i in overlays["styles"]:

        for x in i["options"]:
            if asIds:
                all.append(x["id"])
            else:
                all.append(x)

    return all
