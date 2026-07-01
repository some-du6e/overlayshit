from flask import Flask, request, render_template# type: ignore
import components.overlay as overlayer
import os
app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), "..", "templates"))

@app.route("/")
def home():
    amount = overlayer.getoverlayamount()
    return render_template("home.html", overlay_amt=amount)

@app.route("/overlay", methods=["POST"])
def overlay(id, base):
    if request.method == "POST" or id:
        base = request.files.get("base") or base
        overlayid = request.form.get("overlay") or id

        if not base or not overlayid:
            return "400"

        overlayinfo = overlayer.getoverlay(overlayid)

        if not overlayinfo:
            return "404"
        
        overlaypic = overlayer.getoverlayimage(overlayinfo)

        overlayed = overlayer.overlayPicture(base, overlaypic)

        
        return overlayed





@app.route("/overlay/multi", methods=["POST"])
def overlay_multi():
    if request.method == "POST":
        base = request.files.get("base")
        overlayids = request.form.getlist("overlays")

        if not base or not overlayids:
            return "400"

        print("overlays ids", overlayids)
        
        if overlayids[0] == "all":
            overlayids = overlayer.getalloverlays(asIds=True)

        overlayed = None
        for overlayid in overlayids:
            temp = overlay(overlayid, base)
            if temp == "404":
                print(f"overlay with id {overlayid} not found mate")
            else:
                overlayed = temp

        if overlayed is None:
            return "404"

        return overlayed