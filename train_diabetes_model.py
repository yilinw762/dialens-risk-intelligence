import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.utils.class_weight import compute_class_weight
from sklearn.metrics import accuracy_score, roc_auc_score, classification_report
from tensorflow import keras
from tensorflow.keras import layers, callbacks, regularizers
import joblib
import os

df = pd.read_csv('Datasets/diabetes_binary_health_indicators_BRFSS2015.csv')
X = df.drop('Diabetes_binary', axis=1)
y = df['Diabetes_binary']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

class_weights = compute_class_weight(
    class_weight='balanced', classes=np.unique(y_train), y=y_train
)
class_weight_dict = dict(enumerate(class_weights))

model = keras.Sequential([
    layers.Dense(256, activation='relu', input_shape=(X_train.shape[1],), kernel_regularizer=regularizers.l2(0.001)),
    layers.Dropout(0.4),
    layers.Dense(128, activation='relu', kernel_regularizer=regularizers.l2(0.001)),
    layers.Dropout(0.3),
    layers.Dense(64, activation='relu', kernel_regularizer=regularizers.l2(0.001)),
    layers.Dense(1, activation='sigmoid')
])

model.compile(
    optimizer=keras.optimizers.Adam(learning_rate=0.001),
    loss='binary_crossentropy',
    metrics=['accuracy', keras.metrics.AUC(name='auc')]
)

early_stop = callbacks.EarlyStopping(
    monitor='val_auc', patience=10, restore_best_weights=True, mode='max'
)
checkpoint = callbacks.ModelCheckpoint(
    'diabetes_nn_model_best.keras', monitor='val_auc', save_best_only=True, mode='max'
)

history = model.fit(
    X_train_scaled, y_train,
    epochs=80,
    batch_size=64,
    validation_split=0.15,
    class_weight=class_weight_dict,
    callbacks=[early_stop, checkpoint],
    verbose=2
)

model.load_weights('diabetes_nn_model_best.keras')
y_pred_prob = model.predict(X_test_scaled).flatten()
y_pred = (y_pred_prob > 0.5).astype(int)

acc = accuracy_score(y_test, y_pred)
auc = roc_auc_score(y_test, y_pred_prob)
print(f"Test Accuracy: {acc:.4f}")
print(f"Test ROC AUC: {auc:.4f}")
print("Classification Report:\n", classification_report(y_test, y_pred))

model.save('diabetes_nn_model.keras')
joblib.dump(scaler, 'diabetes_scaler.pkl')

try:
    import eli5
    from eli5.sklearn import PermutationImportance
    import tensorflow as tf
    from sklearn.linear_model import LogisticRegression

    lr = LogisticRegression(max_iter=1000)
    lr.fit(X_train_scaled, y_train)
    perm = PermutationImportance(lr, random_state=42).fit(X_test_scaled, y_test)
    importances = perm.feature_importances_
    feature_importance = pd.Series(importances, index=X.columns).sort_values(ascending=False)
    print("\nFeature importances (Logistic Regression, Permutation):")
    print(feature_importance)
except ImportError:
    print("eli5 not installed, skipping feature importance.")

pd.DataFrame(history.history).to_csv('training_history.csv', index=False)