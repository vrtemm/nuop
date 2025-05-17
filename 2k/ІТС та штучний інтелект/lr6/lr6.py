# файл: runway_calibration_lab6.py
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# Завантаження даних
df = pd.read_csv("flights_sample_3m.csv")

# Вибір релевантних змінних для моделі
df = df[['DEP_DELAY', 'DISTANCE', 'ARR_DELAY', 'DELAY_DUE_WEATHER', 'DELAY_DUE_CARRIER']].dropna()

# Підготовка ознак і цільової змінної
X = df[['DEP_DELAY', 'DISTANCE', 'DELAY_DUE_WEATHER', 'DELAY_DUE_CARRIER']]
y = df['ARR_DELAY']

# Розділення на тренувальну і тестову вибірки
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Побудова та навчання моделі
model = LinearRegression()
model.fit(X_train, y_train)

# Прогнозування
y_pred = model.predict(X_test)

# Метрики якості
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
print(f"Середньоквадратична помилка (MSE): {mse:.2f}")
print(f"Коефіцієнт детермінації R^2: {r2:.2f}")

# Візуалізація результатів
plt.figure(figsize=(8, 6))
plt.scatter(y_test, y_pred, alpha=0.6, color='blue')
plt.plot([y.min(), y.max()], [y.min(), y.max()], 'r--')
plt.xlabel("Фактичні затримки (ARR_DELAY)")
plt.ylabel("Передбачені затримки")
plt.title("Фактичні vs Передбачені затримки рейсів")
plt.grid(True)
plt.tight_layout()
plt.show()
