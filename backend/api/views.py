from rest_framework.views import APIView
from rest_framework.response import Response
import numpy as np
import joblib
from tensorflow import keras
import os
import requests


MODEL_PATH = os.path.join(os.path.dirname(__file__), 'model_files', 'diabetes_nn_model.h5')
SCALER_PATH = os.path.join(os.path.dirname(__file__), 'model_files', 'diabetes_scaler.pkl')
MODEL = keras.models.load_model(MODEL_PATH)
SCALER = joblib.load(SCALER_PATH)

class DiabetesNNPredict(APIView):
    def post(self, request):
        #features in order
        feature_names = [
            "HighBP","HighChol","CholCheck","BMI","Smoker","Stroke","HeartDiseaseorAttack",
            "PhysActivity","Fruits","Veggies","HvyAlcoholConsump","AnyHealthcare","NoDocbcCost",
            "GenHlth","MentHlth","PhysHlth","DiffWalk","Sex","Age","Education","Income"
        ]
        features = [float(request.data.get(f, 0)) for f in feature_names]
        X = np.array([features])
        X_scaled = SCALER.transform(X)
        pred = MODEL.predict(X_scaled)[0][0]
        return Response({'diabetes_probability': float(pred)})

class BMICalculate(APIView):
    def post(self, request):
        weight = float(request.data.get('weight'))
        height = float(request.data.get('height'))
        bmi = weight / ((height / 100) ** 2)
        return Response({'bmi': round(bmi, 2)})

class DiabetesRisk(APIView):
    def post(self, request):
        # dummy prediction for now
        bmi = float(request.data.get('bmi'))
        risk = 0.1 if bmi < 25 else 0.5 if bmi < 30 else 0.8
        return Response({'risk': risk})

class HealthAdvice(APIView):
    def post(self, request):
        prompt = request.data.get('prompt')

        headers = {
            "Authorization": f"Bearer {hf_api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "inputs": prompt,
            "parameters": {"max_new_tokens": 200}
        }
        response = requests.post(api_url, headers=headers, json=payload)
        print(response.status_code, response.text)  # For debugging

        if response.status_code == 200:
            result = response.json()
            # The response format may vary by model; adjust as needed
            if isinstance(result, list) and "generated_text" in result[0]:
                advice = result[0]["generated_text"]
            elif isinstance(result, dict) and "generated_text" in result:
                advice = result["generated_text"]
            else:
                advice = str(result)
            return Response({'advice': advice})
        else:
            return Response({'advice': 'No advice available (Hugging Face error)'})
            
class APIRoot(APIView):
    def get(self, request):
        return Response({
            "bmi": "/api/bmi/",
            "risk": "/api/risk/",
            "advice": "/api/advice/",
            "nn_predict": "/api/nn_predict/"
        })

