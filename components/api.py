from flask import Flask, request, render_template# type: ignore
import components.overlay as overlayer
import os
app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), "..", "templates"))

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/overlay", methods=["POST"])
def overlay():
    if request.method == "POST":
        base = request.files.get("base")
        overlayid = request.form.get("overlay")

        if not base or not overlayid:
            return "400"

        overlayinfo = overlayer.getoverlay(overlayid)

        if not overlayinfo:
            return "404"
        
        overlaypic = overlayer.getoverlayimage(overlayinfo)

        overlayed = overlayer.overlayPicture(base, overlaypic)

        
        return overlayed
