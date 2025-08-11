import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow import keras
from tensorflow.keras import layers
import joblib

df = pd.read_csv('Datasets/diabetes_binary_health_indicators_BRFSS2015.csv')

X = df.drop('Diabetes_binary', axis=1)
y = df['Diabetes_binary']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

model = keras.Sequential([
    layers.Dense(32, activation='relu', input_shape=(X_train.shape[1],)),
    layers.Dense(16, activation='relu'),
    layers.Dense(1, activation='sigmoid')
])

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

#train
model.fit(X_train_scaled, y_train, epochs=20, batch_size=32, validation_split=0.1)

loss, acc = model.evaluate(X_test_scaled, y_test)
print(f"Test accuracy: {acc:.2f}")

model.save('diabetes_nn_model.h5')
joblib.dump(scaler, 'diabetes_scaler.pkl')