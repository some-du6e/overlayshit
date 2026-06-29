import requests as req

OVERLAYS_URL = "https://pfp.hackclub.com/api/styles"



def overlayPicture(base, overlay):
    pass


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

    print(option)


def getoverlayimage(overlay):
    return overlay["overlayPath"]