from flask import Flask, request
import xgboost as xgb
import pickle
import numpy as np

# Create a Flask application
app = Flask(__name__)

# Dictionary for zone encoding
zone_encoding = {'KDBK': 0, 'MiraB': 1, 'Mumbai_City': 2, 'Palghar': 3, 'Panvel_NM': 4, 'Thane': 5, 'VasaiVirar': 6}

@app.route("/")
def root():
    return """
    <html>
        <head>
            <title>House Price Predictor</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f4;
                    margin: 0;
                    padding: 0;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                }
                .container {
                    background-color: #fff;
                    padding: 30px;
                    border-radius: 10px;
                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                    max-width: 500px;
                    text-align: center;
                }
                h1 {
                    color: #333;
                    margin-bottom: 20px;
                }
                form {
                    display: flex;
                    flex-direction: column;
                }
                label {
                    font-weight: bold;
                    margin: 10px 0 5px;
                    text-align: left;
                }
                input[type="number"], select {
                    padding: 10px;
                    border-radius: 5px;
                    border: 1px solid #ccc;
                    margin-bottom: 15px;
                }
                input[type="submit"] {
                    background-color: #007BFF;
                    color: white;
                    padding: 10px;
                    border: none;
                    border-radius: 5px;
                    cursor: pointer;
                    font-size: 16px;
                }
                input[type="submit"]:hover {
                    background-color: #0056b3;
                }
                p {
                    color: #555;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>House Price Predictor</h1>
                <p>Enter the details below to predict the house price in Mumbai.</p>
                <form action="/predict" method="POST">
                    <label>Area (in sq. ft.)</label>
                    <input type="number" name="Area" required>

                    <label>BHK</label>
                    <input type="number" name="BHK" required>

                    <label>Zone</label>
                    <select name="zone" required>
                        <option value="KDBK">KDBK</option>
                        <option value="MiraB">MiraB</option>
                        <option value="Mumbai_City">Mumbai_City</option>
                        <option value="Palghar">Palghar</option>
                        <option value="Panvel_NM">Panvel_NM</option>
                        <option value="Thane">Thane</option>
                        <option value="VasaiVirar">VasaiVirar</option>
                        <option value="None">None</option>
                    </select>

                    <input type="submit" value="Predict Price">
                </form>
            </div>
        </body>
    </html>
    """


@app.route("/predict", methods=["POST"])
def predict():
    # Get input values from the form
    Area = float(request.form['Area'])
    BHK = float(request.form['BHK'])
    zone = request.form['zone']

    # Encode the zone using the zone_encoding dictionary
    zone_encoded = zone_encoding[zone]

    # Load the scaler
    with open('./scaler.pkl', 'rb') as f:
        scaler = pickle.load(f)

    # Load the model from model.pkl file
    with open('./model.pkl', 'rb') as file:
        model = pickle.load(file)

    # Prepare the input for prediction
    input_data = np.array([[Area, BHK, zone_encoded]])
    # Apply the same scaling as during model training
    input_data_scaled = scaler.transform(input_data)

    # Get the prediction using the model
    prediction = model.predict(input_data_scaled)
    predicted_price = prediction[0]  # Assuming the model returns a single prediction

    return f"""
    <html>
        <head>
            <title>Prediction Result</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f4;
                    margin: 0;
                    padding: 0;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                }}
                .container {{
                    background-color: #fff;
                    padding: 30px;
                    border-radius: 10px;
                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                    max-width: 500px;
                    text-align: center;
                }}
                h1 {{
                    color: #333;
                    margin-bottom: 20px;
                }}
                p {{
                    font-size: 18px;
                    color: #555;
                }}
                .price {{
                    font-size: 24px;
                    font-weight: bold;
                    color: #007BFF;
                    margin-top: 10px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Prediction Result</h1>
                <p>Based on the provided Area, BHK, and Zone, the predicted house price is:</p>
                <p class="price">₹{predicted_price:.2f}</p>
            </div>
        </body>
    </html> 
    """


if __name__ == "__main__":
    app.run(debug=True)