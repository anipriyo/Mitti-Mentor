#from flask_ngrok import run_with_ngrok
import os  #type: ignore
import numpy as np  #type: ignore
from flask import Flask, render_template, request
from tensorflow.keras.models import load_model  #type: ignore
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from werkzeug.utils import secure_filename  #type: ignore

app = Flask('app')

model_path = "soilClassify.h5"
#SoilNet = load_model(model_path)

alluvial = """Alluvial soils support more than 40% of India's population by providing the most productive agricultural lands. The soil is porous because of its loamy nature. The proportion of potash, phosphoric acid and alkalies are adequate in alluvial soils. 
Crops: rice, wheat, sugarcane, tobacco, cotton, jute, maize, oilseeds, vegetables and fruits"""

black = """Black soils when seen in uplands are considered to be present with low fertility while those in the valleys are very fertile. The black colour arises due to the presence of a small proportion of titaniferous magnetite or iron and black constituents of the parent rock. 
Crops: cotton (best suited), wheat, jowar, linseed, Virginia, tobacco, castor, sunflower, millets"""

clay = """Clay soil has a smooth texture because of its small particle size. It feels sticky and rolls like plasticine when wet. The clay soil swells when wetted and shrink when dried, so a certain amount of restructuring can take place in these soils depending on weather conditions. Because of its density, the clay soil retains moisture well. 
Crops: paddy (best), vegetables, fruits"""

red = """Red soils originate from parent rocks which are crystalline and metamorphic in nature like acid granites, gneisses and quartzites. On the uplands, the red soils are poor, gravelly and porous but in the lower areas, they are rich, deep dark and fertile. The red color is due to the presence of iron oxide. 
Crops: cotton, wheat, rice, pulses, millets, tobacco, oil seeds, potatoes and fruits"""


def predict_model(img_path, model):
  img = load_img(img_path, target_size=(224, 224))
  img = img_to_array(img)
  img = img / 255
  img = np.expand_dims(img, axis=0)

  result = np.argmax(model.predict(img))
  return result


@app.route("/predictSoil", methods=["GET", "POST"])
def predictSoil():
  if request.method == "POST":
    uploadedImg = request.files["image"]
    nameUploadedImg = uploadedImg.filename
    print("You have uploaded ", nameUploadedImg)
    print("Predicting soil.....")
    if nameUploadedImg is None:
      return "An error occurred"
    uploadedImg_path = os.path.join('static', 'uploads',
                                    secure_filename(nameUploadedImg))
    uploadedImg.save(uploadedImg_path)
    print("Predicting soil.....")
    SoilNet = load_model(model_path)
    result = predict_model(uploadedImg_path, SoilNet)
    print("Soil Detected : ", result)
    if (result == 0):
      return render_template("afterUploadSoil.html",
                             soil_type='Alluvial',
                             user_image_path=uploadedImg_path,
                             desc=alluvial)
    elif (result == 1):
      return render_template("afterUploadSoil.html",
                             soil_type='Black',
                             user_image_path=uploadedImg_path,
                             desc=black)
    elif result == 2:
      return render_template("afterUploadSoil.html",
                             soil_type='Clay',
                             user_image_path=uploadedImg_path,
                             desc=clay)
    elif result == 3:
      return render_template("afterUploadSoil.html",
                             soil_type='Red',
                             user_image_path=uploadedImg_path,
                             desc=red)
    else:
      return "An error occurred"
  return render_template("uploadSoil.html")


@app.route("/predictCrop", methods=["GET", "POST"])
def predictCrop():
  if request.method == "POST":
    uploadedImg = request.files["image"]
    nameUploadedImg = uploadedImg.filename
    print("You have uploaded ", nameUploadedImg)
    if nameUploadedImg is None:
      return "An error occurred"
    uploadedImg_path = os.path.join('static', 'uploads', nameUploadedImg)
    uploadedImg.save(uploadedImg_path)

    print("Predicting crop.....")
    SoilNet = load_model(model_path)
    result = predict_model(uploadedImg_path, SoilNet)

    if (result == 0):
      return render_template("alluvialCrop.html")
    elif (result == 1):
      return render_template("blackCrop.html")
    elif result == 2:
      return render_template("clayCrop.html")
    elif result == 3:
      return render_template("redCrop.html")
    return "An error occurred"
  return render_template("uploadCrop.html")


@app.route('/home')
def home():
  return render_template('index.html')


@app.route("/uploadSoil")
def uploadSoil():
  return render_template("uploadSoil.html")


@app.route("/uploadCrop")
def uploadCrop():
  return render_template("uploadCrop.html")


@app.route("/alluvial")
def Alluvial():
  return render_template("alluvialCrop.html")


@app.route("/black")
def Black():
  return render_template("blackCrop.html")


@app.route("/red")
def Red():
  return render_template("redCrop.html")


@app.route("/clay")
def Clay():
  return render_template("clayCrop.html")


app.run(host='0.0.0.0', port=3000)
