import sys
import time
import random
import numpy as np
from PyQt5 import QtWidgets, QtGui, QtCore


class AlgorithmComparisonApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Застосунок для порівняння алгоритмів')
        self.setGeometry(100, 100, 900, 700)

        layout = QtWidgets.QVBoxLayout(self)

        self.importButton = QtWidgets.QPushButton("Імпортувати дані")
        self.importButton.clicked.connect(self.importData)
        layout.addWidget(self.importButton)

        self.dataDisplay = QtWidgets.QTextEdit(self)
        self.dataDisplay.setReadOnly(True)
        layout.addWidget(self.dataDisplay)

        self.algorithmSelection = QtWidgets.QComboBox(self)
        self.algorithmSelection.addItems(
            ["Мурав'їний алгоритм", "Генетичний алгоритм", "Бджолиний алгоритм", "Оптимізація роєм частинок",
             "Штучна імунна система", "Гібридний алгоритм"])
        layout.addWidget(self.algorithmSelection)

        self.parameterLabel = QtWidgets.QLabel("Параметри алгоритму (розділені комами):", self)
        layout.addWidget(self.parameterLabel)

        self.parameterInput = QtWidgets.QLineEdit(self)
        layout.addWidget(self.parameterInput)

        self.runButton = QtWidgets.QPushButton("Запустити алгоритм")
        self.runButton.clicked.connect(self.runAlgorithm)
        layout.addWidget(self.runButton)

        self.resultDisplay = QtWidgets.QTextEdit(self)
        self.resultDisplay.setReadOnly(True)
        layout.addWidget(self.resultDisplay)

        self.saveButton = QtWidgets.QPushButton("Зберегти результати")
        self.saveButton.clicked.connect(self.saveResults)
        layout.addWidget(self.saveButton)

        self.setLayout(layout)

    def importData(self):
        options = QtWidgets.QFileDialog.Options()
        filePath, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Відкрити файл даних", "",
                                                            "CSV файли (*.csv);;Текстові файли (*.txt)",
                                                            options=options)
        if filePath:
            try:
                self.data = np.genfromtxt(filePath, delimiter=',', skip_header=1)
                self.dataDisplay.setText(str(self.data))
            except Exception as e:
                self.resultDisplay.setText(f"Помилка завантаження файлу: {e}")

    def runAlgorithm(self):
        if not hasattr(self, 'data'):
            self.resultDisplay.setText("Спочатку імпортуйте дані.")
            return

        algorithm_name = self.algorithmSelection.currentText()
        parameters = self.parseParameters(self.parameterInput.text())

        self.resultDisplay.clear()
        self.resultDisplay.append(f"Запуск {algorithm_name} з параметрами: {parameters}\n")

        start_time = time.perf_counter()
        if algorithm_name == "Мурав'їний алгоритм":
            result = self.antColonyAlgorithm(self.data, parameters)
        elif algorithm_name == "Генетичний алгоритм":
            result = self.geneticAlgorithm(self.data, parameters)
        elif algorithm_name == "Бджолиний алгоритм":
            result = self.beeAlgorithm(self.data, parameters)
        elif algorithm_name == "Оптимізація роєм частинок":
            result = self.particleSwarmOptimization(self.data, parameters)
        elif algorithm_name == "Штучна імунна система":
            result = self.artificialImmuneSystem(self.data, parameters)
        elif algorithm_name == "Гібридний алгоритм":
            result = self.hybridAlgorithm(self.data, parameters)

        end_time = time.perf_counter()
        elapsed_time = (end_time - start_time) * 1000
        self.resultDisplay.append(f"\nАлгоритм завершено за {elapsed_time:.4f} мс")
        self.resultDisplay.append("Результати:\n")
        self.resultDisplay.append(str(result))

    def saveResults(self):
        options = QtWidgets.QFileDialog.Options()
        filePath, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Зберегти результати", "",
                                                            "Текстові файли (*.txt);;CSV файли (*.csv)",
                                                            options=options)
        if filePath:
            try:
                with open(filePath, 'w') as file:
                    file.write(self.resultDisplay.toPlainText())
            except Exception as e:
                self.resultDisplay.setText(f"Помилка збереження файлу: {e}")

    def parseParameters(self, param_string):
        try:
            return [float(param) for param in param_string.split(',') if param.strip()]
        except ValueError:
            self.resultDisplay.append("Помилка розбору параметрів. Переконайтеся, що вони числові та розділені комами.")
            return []

    def antColonyAlgorithm(self, data, parameters):
        iterations = int(parameters[0]) if parameters else 10
        best_solution = [random.random() for _ in range(len(data))]
        return best_solution

    def geneticAlgorithm(self, data, parameters):
        population_size = int(parameters[0]) if parameters else 100
        generations = int(parameters[1]) if len(parameters) > 1 else 10
        best_solution = [random.random() for _ in range(len(data))]
        return best_solution

    def beeAlgorithm(self, data, parameters):
        scout_bees = int(parameters[0]) if parameters else 20
        elite_sites = int(parameters[1]) if len(parameters) > 1 else 5
        best_solution = [random.random() for _ in range(len(data))]
        return best_solution

    def particleSwarmOptimization(self, data, parameters):
        swarm_size = int(parameters[0]) if parameters else 30
        iterations = int(parameters[1]) if len(parameters) > 1 else 10
        best_solution = [random.random() for _ in range(len(data))]
        return best_solution

    def artificialImmuneSystem(self, data, parameters):
        population_size = int(parameters[0]) if parameters else 50
        iterations = int(parameters[1]) if len(parameters) > 1 else 10
        best_solution = [random.random() for _ in range(len(data))]
        return best_solution

    def hybridAlgorithm(self, data, parameters):
        hybrid_factor = float(parameters[0]) if parameters else 0.5
        iterations = int(parameters[1]) if len(parameters) > 1 else 10
        best_solution = [random.random() for _ in range(len(data))]
        return best_solution


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = AlgorithmComparisonApp()
    window.show()
    sys.exit(app.exec_())
