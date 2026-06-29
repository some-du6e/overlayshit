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
        overlay = request.form.get("overlay")

        if not base or not overlay:
            return "400"

        tobeorerlay = overlayer.getoverlay(overlay)


        overlayed = overlayer.overlayPicture(base, tobeorerlay)

        
        return "200"
