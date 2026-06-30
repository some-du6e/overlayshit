from flask import Flask, request # type: ignore
import components.overlay as overlayer
app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>bye, World!</p>"

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
