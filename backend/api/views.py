from rest_framework.views import APIView
from rest_framework.response import Response
import numpy as np
import joblib
from tensorflow import keras
import os
import requests
from dotenv import load_dotenv

load_dotenv()

MODEL_PATH = os.path.join(os.path.dirname(__file__), 'model_files', 'diabetes_nn_model.h5')
SCALER_PATH = os.path.join(os.path.dirname(__file__), 'model_files', 'diabetes_scaler.pkl')
MODEL = keras.models.load_model(MODEL_PATH)
SCALER = joblib.load(SCALER_PATH)

class GeminiChat(APIView):
    def post(self, request):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            return Response({"error": "GEMINI_API_KEY is not set in the environment variables."}, status=500)
        
        prompt = request.data.get("prompt")
        if not prompt:
            return Response({"error": "No prompt provided."}, status=400)
        
        gemini_api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
        payload = {
            "contents": [
                {"parts": [{"text": prompt}]}
            ]
        }
        headers = {"Content-Type": "application/json"}
        response = requests.post(gemini_api_url, headers=headers, json=payload)
        if response.status_code != 200:
            print("Gemini API error:", response.text)
        if response.status_code == 200:
            result = response.json()
            try:
                reply = result["candidates"][0]["content"]["parts"][0]["text"]
            except (KeyError, IndexError):
                reply = "No response generated."
            return Response({"reply": reply})
        else:
            return Response({"error": "Gemini API error", "details": response.text}, status=response.status_code)

class DiabetesNNPredict(APIView):
    def post(self, request):
        feature_names = [
            "HighBP","HighChol","CholCheck","BMI","Smoker","Stroke","HeartDiseaseorAttack",
            "PhysActivity","Fruits","Veggies","HvyAlcoholConsump","AnyHealthcare","NoDocbcCost",
            "GenHlth","MentHlth","PhysHlth","DiffWalk","Sex","Age","Education","Income"
        ]
        features = [float(request.data.get(f, 0)) for f in feature_names]
        import pandas as pd
        X = pd.DataFrame([features], columns=feature_names)
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
        feature_names = [
            "HighBP","HighChol","CholCheck","BMI","Smoker","Stroke","HeartDiseaseorAttack",
            "PhysActivity","Fruits","Veggies","HvyAlcoholConsump","AnyHealthcare","NoDocbcCost",
            "GenHlth","MentHlth","PhysHlth","DiffWalk","Sex","Age","Education","Income"
        ]
        features = [float(request.data.get(f, 0)) for f in feature_names]
        import pandas as pd
        X = pd.DataFrame([features], columns=feature_names)
        X_scaled = SCALER.transform(X)
        pred = MODEL.predict(X_scaled)[0][0]
        return Response({'risk': float(pred)})

class HealthAdvice(APIView):
    def post(self, request):
        print("Received data:", request.data)

        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            return Response({"error": "GEMINI_API_KEY is not set in the environment variables."}, status=500)

        form = request.data.get('form')
        probability = request.data.get('probability')

        if not form or probability is None:
            return Response({"error": "Form data or probability missing."}, status=400)

        prompt = (
            f"The following user provided these health indicators: {form}. "
            f"Their predicted diabetes risk is {float(probability)*100:.2f}%. "
            "Give clear, practical, and positive health advice tailored to this user. "
            "Focus on actionable steps to reduce diabetes risk and improve overall health. "
            "Use simple language."
        )

        payload = {
            "contents": [
                {"parts": [{"text": prompt}]}
            ]
        }

        gemini_api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
        headers = {"Content-Type": "application/json"}
        response = requests.post(gemini_api_url, headers=headers, json=payload)

        if response.status_code == 200:
            result = response.json()
            try:
                advice = result["candidates"][0]["content"]["parts"][0]["text"]
                import re
                advice = re.sub(r'\*\*([^*]+)\*\*', r'\1', advice)  #remove bold
                advice = re.sub(r'\*([^*]+)\*', r'\1', advice)      #remove italics
            except (KeyError, IndexError):
                advice = "No advice generated."
            return Response({'advice': advice})
        else:
            return Response({"error": "Gemini API error", "details": response.text}, status=response.status_code)

class APIRoot(APIView):
    def get(self, request):
        return Response({
            "bmi": "/api/bmi/",
            "risk": "/api/risk/",
            "advice": "/api/advice/",
            "nn_predict": "/api/nn_predict/",
            "gemini_chat": "/api/gemini_chat/"
        })