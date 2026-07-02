from flask import Flask, request, render_template# type: ignore
import components.overlay as overlayer
import os
from PIL import Image # type: ignore
app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), "..", "templates"))

@app.route("/")
def home():
    amount = overlayer.getoverlayamount()
    return render_template("home.html", overlay_amt=amount)

@app.route("/overlaying")
def overlaying():
    return render_template("overlaying.html")

@app.route("/overlay", methods=["POST"])
def overlay():
    base = request.files.get("base")
    overlayid = request.form.get("overlay")

    if not base or not overlayid:
        return "400", 400

    overlayinfo = overlayer.getoverlay(overlayid)

    if not overlayinfo:
        return "404", 404
    
    overlaypic = overlayer.getoverlayimage(overlayinfo)

    overlayed = overlayer.overlayPicture(base, overlaypic)

    return overlayed





@app.route("/overlay/multi", methods=["POST"])
def overlay_multi():
    if request.method == "POST":
        base = request.files.get("base")
        overlayids = request.form.getlist("overlays")

        if not base or not overlayids:
            return "400", 400

        print("overlays ids", overlayids)
        
        if overlayids[0] == "all":
            overlayinfos = overlayer.getalloverlays()
        else:
            overlayinfos = [
                overlayinfo
                for overlayid in overlayids
                if (overlayinfo := overlayer.getoverlay(overlayid))
            ]

        overlayed = Image.open(base).convert("RGBA")
        for overlayinfo in overlayinfos:
            overlaypic = overlayer.getoverlayimage(overlayinfo)
            overlayed = overlayer.applyOverlay(overlayed, overlaypic)

        if overlayed is None:
            return "404", 404

        return overlayer.imageResponse(overlayed)
