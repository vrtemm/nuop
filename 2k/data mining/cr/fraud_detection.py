# Імпорт бібліотек
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, precision_recall_curve, auc, f1_score, confusion_matrix
from sklearn.ensemble import IsolationForest
from sklearn.svm import OneClassSVM
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense
import matplotlib.pyplot as plt
import seaborn as sns


data = pd.read_csv('creditcard.csv')


print(data.info())
print(data['Class'].value_counts(normalize=True)) 


data.drop(columns=['Time'], inplace=True)
scaler = StandardScaler()
data['Amount'] = scaler.fit_transform(data['Amount'].values.reshape(-1, 1))


X = data.drop(columns=['Class'])
y = data['Class']


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)


iso_forest = IsolationForest(contamination=0.001, random_state=42)  
iso_forest.fit(X_train)


y_pred_iso = iso_forest.predict(X_test)
y_pred_iso = np.where(y_pred_iso == 1, 0, 1) 


print("Isolation Forest Metrics:")
print(classification_report(y_test, y_pred_iso))
f1_iso = f1_score(y_test, y_pred_iso)
precision, recall, _ = precision_recall_curve(y_test, y_pred_iso)
pr_auc_iso = auc(recall, precision)
conf_matrix_iso = confusion_matrix(y_test, y_pred_iso)


oc_svm = OneClassSVM(nu=0.001, kernel='rbf', gamma='scale')  
oc_svm.fit(X_train)


y_pred_svm = oc_svm.predict(X_test)
y_pred_svm = np.where(y_pred_svm == 1, 0, 1)  


print("One-Class SVM Metrics:")
print(classification_report(y_test, y_pred_svm))
f1_svm = f1_score(y_test, y_pred_svm)
precision, recall, _ = precision_recall_curve(y_test, y_pred_svm)
pr_auc_svm = auc(recall, precision)
conf_matrix_svm = confusion_matrix(y_test, y_pred_svm)


input_dim = X_train.shape[1]
encoding_dim = 14  

input_layer = Input(shape=(input_dim,))
encoded = Dense(encoding_dim, activation="relu")(input_layer)
decoded = Dense(input_dim, activation="sigmoid")(encoded)

autoencoder = Model(inputs=input_layer, outputs=decoded)
autoencoder.compile(optimizer='adam', loss='mean_squared_error')

autoencoder.fit(X_train, X_train, epochs=20, batch_size=32, shuffle=True, validation_data=(X_test, X_test), verbose=1)


reconstructions = autoencoder.predict(X_test)
mse = np.mean(np.power(X_test - reconstructions, 2), axis=1)
threshold = np.percentile(mse, 95) 
y_pred_ae = (mse > threshold).astype(int)


print("AutoEncoder Metrics:")
print(classification_report(y_test, y_pred_ae))
f1_ae = f1_score(y_test, y_pred_ae)
precision, recall, _ = precision_recall_curve(y_test, y_pred_ae)
pr_auc_ae = auc(recall, precision)
conf_matrix_ae = confusion_matrix(y_test, y_pred_ae)


metrics = {
    'Model': ['Isolation Forest', 'One-Class SVM', 'AutoEncoder'],
    'F1-Score': [f1_iso, f1_svm, f1_ae],
    'Precision-Recall AUC': [pr_auc_iso, pr_auc_svm, pr_auc_ae],
    'False Positives': [conf_matrix_iso[0, 1], conf_matrix_svm[0, 1], conf_matrix_ae[0, 1]],
    'False Negatives': [conf_matrix_iso[1, 0], conf_matrix_svm[1, 0], conf_matrix_ae[1, 0]]
}

metrics_df = pd.DataFrame(metrics)
print(metrics_df)


plt.figure(figsize=(10, 6))
sns.histplot(mse, bins=50, kde=True)
plt.axvline(threshold, color='r', linestyle='--', label=f'Threshold: {threshold:.2f}')
plt.title("Reconstruction Error Distribution")
plt.xlabel("MSE")
plt.ylabel("Frequency")
plt.legend()
plt.show()


fig, axes = plt.subplots(1, 3, figsize=(18, 5))
models = ['Isolation Forest', 'One-Class SVM', 'AutoEncoder']
conf_matrices = [conf_matrix_iso, conf_matrix_svm, conf_matrix_ae]

for i, (model, conf_matrix) in enumerate(zip(models, conf_matrices)):
    sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues', ax=axes[i])
    axes[i].set_title(f'{model} Confusion Matrix')
    axes[i].set_xlabel('Predicted')
    axes[i].set_ylabel('Actual')

plt.tight_layout()
plt.show()