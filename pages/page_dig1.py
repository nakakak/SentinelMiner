import os
import sys
import pandas as pd
import numpy as np
from PyQt5.QtWidgets import QFileDialog, QMessageBox
import joblib
from sklearn.metrics import classification_report, confusion_matrix

def resource_path(relative_path):
    """资源路径处理（兼容打包后的exe和开发环境）"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

 示例数据路径
EXAMPLE_X_PATH = resource_path("example/dig1/X_test.csv")
EXAMPLE_Y_PATH = resource_path("example/dig1/y_test.csv")

 模型与工具加载（只加载一次）
model = joblib.load(resource_path("al/dig1/fake_news_classifier.pkl"))
scaler = joblib.load(resource_path("al/dig1/scaler.pkl"))   scaler 可选

def setup_dig1_page(ui):
    ui.selected_truth_path = None

    def select_file():
        path, _ = QFileDialog.getOpenFileName(ui, "选择 CSV 文件", "", "CSV Files (*.csv)")
        if path:
            ui.selected_truth_path = path
            ui.line_truth_filepath.setText(path)

    def show_uploaded_data():
        if ui.selected_truth_path:
            try:
                df = pd.read_csv(ui.selected_truth_path)
                ui.Browser_owndig1.setText(df.head(100).to_string())
            except Exception as e:
                QMessageBox.critical(ui, "读取失败", str(e))

    def show_example_data():
        try:
            df = pd.read_csv(EXAMPLE_X_PATH)
            ui.Browser_exampledig1.setText(df.head(100).to_string())
        except Exception as e:
            QMessageBox.critical(ui, "读取失败", str(e))

    def run_prediction(X_test, y_test=None):
        try:
            y_pred = model.predict(X_test)

            result_text = pd.DataFrame(y_pred, columns=["预测结果（0假，1真）"]).to_string(index=False)
            ui.Browerdig1data.setText(result_text)

            if y_test is not None:
                report = classification_report(y_test, y_pred)
                matrix = confusion_matrix(y_test, y_pred)
                result_text += "\n\nClassification Report:\n" + report
                result_text += "\nConfusion Matrix:\n" + str(matrix)
                ui.Browerdig1data.setText(result_text)

            ui.latest_truth_result = pd.DataFrame({"预测结果": y_pred})
            ui.stackedWidget.setCurrentWidget(ui.page_dig1data)

        except Exception as e:
            QMessageBox.critical(ui, "预测失败", str(e))

    def run_example_detection():
        try:
            X_test = pd.read_csv(EXAMPLE_X_PATH).values
            y_test = pd.read_csv(EXAMPLE_Y_PATH).values.ravel()
            run_prediction(X_test, y_test)
        except Exception as e:
            QMessageBox.critical(ui, "示例数据运行失败", str(e))

    def run_own_detection():
        try:
            df = pd.read_csv(ui.selected_truth_path)
            X_test = df.values
            run_prediction(X_test)
        except Exception as e:
            QMessageBox.critical(ui, "上传数据运行失败", str(e))

    def save_result_to_file():
        if not hasattr(ui, "latest_truth_result"):
            QMessageBox.warning(ui, "提示", "没有可保存的内容")
            return
        save_path, _ = QFileDialog.getSaveFileName(ui, "保存预测结果", "truth_result.csv", "CSV Files (*.csv)")
        if save_path:
            try:
                ui.latest_truth_result.to_csv(save_path, index=False)
                QMessageBox.information(ui, "保存成功", f"已保存至：{save_path}")
            except Exception as e:
                QMessageBox.critical(ui, "保存失败", str(e))

     按钮绑定
    ui.btn_filedig1.clicked.connect(select_file)
    ui.data_owndig1.clicked.connect(show_uploaded_data)
    ui.data_exampledig1.clicked.connect(show_example_data)
    ui.select_exampledig1.clicked.connect(run_example_detection)
    ui.select_owndig1.clicked.connect(run_own_detection)
    ui.btn_backdig1.clicked.connect(lambda: ui.stackedWidget.setCurrentWidget(ui.page_dig))
    ui.btn_exitdig1.clicked.connect(ui.close)

    ui.btn_backdig1data.clicked.connect(lambda: ui.stackedWidget.setCurrentWidget(ui.page_dig1))
    ui.btn_exitdig1data.clicked.connect(ui.close)
    ui.btn_savedig1data.clicked.connect(save_result_to_file)
