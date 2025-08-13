import React, { useState } from 'react';
import axios from 'axios';

const initialState = {
  HighBP: 0,
  HighChol: 0,
  CholCheck: 0,
  BMI: 25,
  Smoker: 0,
  Stroke: 0,
  HeartDiseaseorAttack: 0,
  PhysActivity: 0,
  Fruits: 0,
  Veggies: 0,
  HvyAlcoholConsump: 0,
  AnyHealthcare: 0,
  NoDocbcCost: 0,
  GenHlth: 3,
  MentHlth: 0,
  PhysHlth: 0,
  DiffWalk: 0,
  Sex: 1,
  Age: 9,
  Education: 4,
  Income: 3,
};

export default function HealthForm() {
  const [form, setForm] = useState(initialState);
  const [result, setResult] = useState(null);
  const [history, setHistory] = useState([]);
  const [advice, setAdvice] = useState('');
  const [loadingAdvice, setLoadingAdvice] = useState(false);

  const handleChange = e => {
    const { name, value } = e.target;
    setForm({ ...form, [name]: value });
  };

  const handleSubmit = async e => {
    e.preventDefault();
    try {
      const res = await axios.post('http://localhost:8000/api/nn_predict/', {
        ...Object.fromEntries(Object.entries(form).map(([k, v]) => [k, Number(v)])),
      });
      setResult(res.data.diabetes_probability);
      setHistory([{ ...form, prediction: res.data.diabetes_probability }, ...history]);
      setAdvice('');
    } catch (err) {
      alert('Error: ' + err.message);
    }
  };

  const handleAskAdvice = async () => {
    setLoadingAdvice(true);
    try {
      const res = await axios.post('http://localhost:8000/api/advice/', {
        form,
        probability: result
      });
      setAdvice(res.data.advice);
    } catch (err) {
      setAdvice('Error getting advice.');
    }
    setLoadingAdvice(false);
  };

  return (
    <div className="max-w-xl mx-auto p-6 bg-white rounded shadow">
      <h2 className="text-2xl font-bold mb-4">Health Risk Assessment</h2>
      <form onSubmit={handleSubmit} className="space-y-3">
        <div>
          <label>BMI: </label>
          <input type="number" name="BMI" value={form.BMI} onChange={handleChange} className="border p-1" />
        </div>
        <div>
          <label>Age: </label>
          <input type="number" name="Age" value={form.Age} onChange={handleChange} className="border p-1" />
        </div>
        <div>
          <label>High Blood Pressure: </label>
          <select name="HighBP" value={form.HighBP} onChange={handleChange} className="border p-1">
            <option value={0}>No</option>
            <option value={1}>Yes</option>
          </select>
        </div>
        <div>
          <label>High Cholesterol: </label>
          <select name="HighChol" value={form.HighChol} onChange={handleChange} className="border p-1">
            <option value={0}>No</option>
            <option value={1}>Yes</option>
          </select>
        </div>
        <div>
          <label>Cholesterol Check: </label>
          <select name="CholCheck" value={form.CholCheck} onChange={handleChange} className="border p-1">
            <option value={0}>No</option>
            <option value={1}>Yes</option>
          </select>
        </div>
        <div>
          <label>Smoker: </label>
          <select name="Smoker" value={form.Smoker} onChange={handleChange} className="border p-1">
            <option value={0}>No</option>
            <option value={1}>Yes</option>
          </select>
        </div>
        <div>
          <label>Stroke: </label>
          <select name="Stroke" value={form.Stroke} onChange={handleChange} className="border p-1">
            <option value={0}>No</option>
            <option value={1}>Yes</option>
          </select>
        </div>
        <div>
          <label>Heart Disease or Attack: </label>
          <select name="HeartDiseaseorAttack" value={form.HeartDiseaseorAttack} onChange={handleChange} className="border p-1">
            <option value={0}>No</option>
            <option value={1}>Yes</option>
          </select>
        </div>
        <div>
          <label>Physical Activity: </label>
          <select name="PhysActivity" value={form.PhysActivity} onChange={handleChange} className="border p-1">
            <option value={0}>No</option>
            <option value={1}>Yes</option>
          </select>
        </div>
        <div>
          <label>Fruits: </label>
          <select name="Fruits" value={form.Fruits} onChange={handleChange} className="border p-1">
            <option value={0}>No</option>
            <option value={1}>Yes</option>
          </select>
        </div>
        <div>
          <label>Veggies: </label>
          <select name="Veggies" value={form.Veggies} onChange={handleChange} className="border p-1">
            <option value={0}>No</option>
            <option value={1}>Yes</option>
          </select>
        </div>
        <div>
          <label>Heavy Alcohol Consumption: </label>
          <select name="HvyAlcoholConsump" value={form.HvyAlcoholConsump} onChange={handleChange} className="border p-1">
            <option value={0}>No</option>
            <option value={1}>Yes</option>
          </select>
        </div>
        <div>
          <label>Any Healthcare: </label>
          <select name="AnyHealthcare" value={form.AnyHealthcare} onChange={handleChange} className="border p-1">
            <option value={0}>No</option>
            <option value={1}>Yes</option>
          </select>
        </div>
        <div>
          <label>No Doctor Because of Cost: </label>
          <select name="NoDocbcCost" value={form.NoDocbcCost} onChange={handleChange} className="border p-1">
            <option value={0}>No</option>
            <option value={1}>Yes</option>
          </select>
        </div>
        <div>
          <label>General Health (1=Excellent, 5=Poor): </label>
          <input type="number" name="GenHlth" min={1} max={5} value={form.GenHlth} onChange={handleChange} className="border p-1" />
        </div>
        <div>
          <label>Mental Health (days, 0-30): </label>
          <input type="number" name="MentHlth" min={0} max={30} value={form.MentHlth} onChange={handleChange} className="border p-1" />
        </div>
        <div>
          <label>Physical Health (days, 0-30): </label>
          <input type="number" name="PhysHlth" min={0} max={30} value={form.PhysHlth} onChange={handleChange} className="border p-1" />
        </div>
        <div>
          <label>Difficulty Walking: </label>
          <select name="DiffWalk" value={form.DiffWalk} onChange={handleChange} className="border p-1">
            <option value={0}>No</option>
            <option value={1}>Yes</option>
          </select>
        </div>
        <div>
          <label>Sex: </label>
          <select name="Sex" value={form.Sex} onChange={handleChange} className="border p-1">
            <option value={0}>Female</option>
            <option value={1}>Male</option>
          </select>
        </div>
        <div>
          <label>Education (1=Never attended, 6=College grad): </label>
          <input type="number" name="Education" min={1} max={6} value={form.Education} onChange={handleChange} className="border p-1" />
        </div>
        <div>
          <label>Income (1=Lowest, 8=Highest): </label>
          <input type="number" name="Income" min={1} max={8} value={form.Income} onChange={handleChange} className="border p-1" />
        </div>
        <button type="submit" className="bg-blue-600 text-white px-4 py-2 rounded">Get Prediction</button>
      </form>
      {result !== null && (
        <div className="mt-4 p-4 bg-green-100 rounded">
          <strong>Diabetes Probability:</strong> {(result * 100).toFixed(2)}%
          <div className="mt-2">
            <button
              className="bg-purple-600 text-white px-3 py-1 rounded"
              onClick={handleAskAdvice}
              disabled={loadingAdvice}
            >
              {loadingAdvice ? 'Getting Advice...' : 'Ask AI for Health Advice'}
            </button>
          </div>
          {advice && (
            <div className="mt-2 p-2 bg-purple-100 rounded text-purple-900">
              <strong>DiaLens AI Personalized Advice:</strong> {advice}
            </div>
          )}
        </div>
      )}
      {history.length > 0 && (
        <div className="mt-6">
          <h3 className="font-semibold mb-2">Prediction History</h3>
          <ul className="text-sm">
            {history.map((item, idx) => (
              <li key={idx} className="mb-1">
                BMI: {item.BMI}, Age: {item.Age}, Risk: {(item.prediction * 100).toFixed(2)}%
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}