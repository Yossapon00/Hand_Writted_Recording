from flask import Flask, render_template, request
from tensorflow.keras.models import load_model
from tensorflow.keras.utils import load_img , img_to_array
app = Flask(__name__)

model = load_model("model2.h5")

def predict_label(img_path):
	
	i = load_img(img_path, target_size=(28,28))
	i = img_to_array(i)
	i = i.reshape(1,28,28,3)

	p = model.predict(i)
	
	if(p[0][0] > 0.5):
		p[0][0] *= 100
		txt = " ENG" 
		predic = '%.2f'%(p[0][0])
	else:
		p[0][0] *= 100
		txt = "TH"
		
	predic = '%.2f'%(p[0][0])

	return predic,txt

# routes
@app.route("/", methods=['GET', 'POST'])
def main():
	return render_template("index.html")

@app.route("/submit", methods = ['GET', 'POST'])
def get_output():
	if request.method == 'POST':
		img = request.files['my_image']

		img_path = "static/" + img.filename	
		img.save(img_path)

		p = predict_label(img_path)
	return render_template("index.html", prediction = p[0] , TEXT = p[1] ,  img_path = img_path)


if __name__ =='__main__':
	app.run(port=3000,debug = True)