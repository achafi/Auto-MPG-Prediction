import pickle
import os
from flask import Flask, request, render_template
from flask_cors import cross_origin
from flask import  jsonify
from model_files.ml_model import predict_mpg
from flask_mail import Mail, Message



app = Flask("mpg_prediction")
app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME = 'assia.chafii93@gmail.com',
    MAIL_PASSWORD = 'AM_bh-MALAK159'
    #MAIL_PASSWORD = os.environ['MAIL_PASSWORD']
    )

mail = Mail(app)
@app.route("/", methods =['Get'])
@cross_origin()
def ping():
    return render_template("home.html")




@app.route('/predict', methods=['POST'])
def predict():
    if request.method == "POST":

        cylinders = int(request.form["Cylinders"])
        displacement = int(request.form["Horsepower"])
        horsepower = int(request.form["Horsepower"])
        Weight = int(request.form["Weight"])
        acceleration = int(request.form["Acceleration"])
        modelyear = int(request.form["ModelYear"])
        Origin =  request.form["Origin"]
        if Origin == 'India':
            origin = [1,2,3]
        elif Origin == 'USA':
            origin = [2,3,1]
        elif Origin == 'Germany':
            origin = [3,1,2]
        
        vehicle_config = {'Cylinders': [cylinders, 6, 8],
                          'Displacement': [displacement, 160.0, 165.5],
                          'Horsepower': [horsepower, 130.0, 98.0],
                          'Weight': [Weight, 3150.0, 2600.0],
                          'Acceleration': [acceleration, 14.0, 16.0],
                          'Model Year': [modelyear, 80, 78],
                          'Origin': origin
                        }

        print(vehicle_config)
        with open('./model_files/model.bin', 'rb') as f_in:
            model = pickle.load(f_in)
            f_in.close()
            predictions = predict_mpg(vehicle_config, model)
            
        output=round(predictions[0],2)

        return render_template('home.html',prediction_text= "MPG = %.2f" %output)


    return render_template("home.html")
        
    """
    vehicle = request.get_json()
    print(vehicle)
    with open('./model_files/model.bin', 'rb') as f_in:
        model = pickle.load(f_in)
        f_in.close()
    predictions = predict_mpg(vehicle, model)

    result = {
        'mpg_prediction': list(predictions)
    }
    return jsonify(result)
    """

    
@app.route('/send_message', methods=['POST', 'GET'])
def send_message():
    if request.method == "POST":
        name = request.form['Name']
        Email = request.form['Email']
        message = name + "\n" + Email +"\n"+ request.form['Message']
        #msg = Message(message, sender=['assia.chafii93@gmail.com'], recipients=['assia.chafii93@gmail.com'])
        msg = Message('Hello', sender = 'assia.chafii93@gmail.com', recipients = ['assia.chafii93@gmail.com'])
        msg.body = message
        mail.send(msg)
        
        return render_template('home.html', message_sent= 'message sent!')
    return "message sent !"
if __name__ == '__main__' : 
    app.run(debug = True)
