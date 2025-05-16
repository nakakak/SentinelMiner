import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import joblib
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QVBoxLayout
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

def resource_path(relative_path):
    """资源路径处理（兼容打包后的exe和开发环境）"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

 模型映射
MODEL_MAP = {
    "逻辑回归（LR）": resource_path("al/dec2/LR/model.joblib"),
    "决策树（DT）": resource_path("al/dec2/DT/dt_model.joblib"),
    "随机森林（RF）": resource_path("al/dec2/RF/rf_model.joblib"),
    "支持向量机（SVM）": resource_path("al/dec2/SVM/svm_model.joblib"),
    "多层感知机（MLP）": resource_path("al/dec2/MLP/mlp_model.joblib"),
    "梯度提升树（GBT）": resource_path("al/dec2/GBT/gb_model.joblib"),
    "K最近邻（KNN）": resource_path("al/dec2/KNN/knn_model.joblib"),
    "朴素贝叶斯（NB）": resource_path("al/dec2/NB/nb_model.joblib"),
    "AdaBoost": resource_path("al/dec2/AdaBoost/adaboost_model.joblib"),
    "XGBoost": resource_path("al/dec2/XGBoost/xgboost_model.joblib"),
}

EXAMPLE_DATA_PATH = resource_path("example/dec2/feature_vectors_syscallsbinders_frequency_5_Cat.csv")

def setup_dec2_page(ui):
    ui.selected_test_path = None
    ui.selected_X_test = None

    if ui.combo_algorithm2.count() == 0:
        ui.combo_algorithm2.addItems(MODEL_MAP.keys())

    def select_file():
        path, _ = QFileDialog.getOpenFileName(ui, "选择测试数据文件（csv）", "", "CSV 文件 (*.csv)")
        if path:
            ui.selected_test_path = path
            ui.line_filepathdec2.setText(path)

    def show_uploaded_data():
        if not ui.selected_test_path:
            QMessageBox.information(ui, "提示", "请先上传文件")
            return
        try:
            df = pd.read_csv(ui.selected_test_path)
            ui.selected_X_test = df.drop(columns=["Class"], errors='ignore').values
            ui.Browser_owndec2.setText(df.head(100).to_string())
        except Exception as e:
            QMessageBox.critical(ui, "读取失败", str(e))

    def show_example_data():
        try:
            df = pd.read_csv(EXAMPLE_DATA_PATH)
            ui.Browser_exampledec2.setText(df.head(100).to_string())
        except Exception as e:
            QMessageBox.critical(ui, "读取示例数据失败", str(e))

    def plot_bar_chart(predictions):
        layout = ui.chart_dec2_widget.layout()
        if layout:
            for i in reversed(range(layout.count())):
                layout.itemAt(i).widget().setParent(None)
        else:
            layout = QVBoxLayout()
            ui.chart_dec2_widget.setLayout(layout)

        fig = plt.figure(figsize=(5, 3))
        ax = fig.add_subplot(111)
        pd.Series(predictions).value_counts().plot.bar(color="skyblue", ax=ax)
        ax.set_title("预测类别频次统计")
        ax.set_ylabel("数量")
        ax.set_xlabel("类别")
        ax.tick_params(axis='x', rotation=45)

        canvas = FigureCanvas(fig)
        layout.addWidget(canvas)

    def show_results(predictions):
        df_result = pd.DataFrame(predictions, columns=["预测类别"])
        ui.Browerdec2data.setText(df_result.to_string(index=False))
        plot_bar_chart(predictions)
        ui.latest_predictions = df_result
        ui.stackedWidget.setCurrentWidget(ui.page_dec2data)

    def run_uploaded_detection():
        if not hasattr(ui, "selected_X_test"):
            QMessageBox.warning(ui, "提示", "请先上传并读取测试数据")
            return
        try:
            model_name = ui.combo_algorithm2.currentText()
            model_path = MODEL_MAP.get(model_name)
            if not model_path or not os.path.exists(model_path):
                QMessageBox.warning(ui, "提示", "模型文件不存在或选择错误")
                return
            model = joblib.load(model_path)
            preds = model.predict(ui.selected_X_test)
            show_results(preds)
        except Exception as e:
            QMessageBox.critical(ui, "预测失败", str(e))

    def run_example_detection():
        try:
            df = pd.read_csv(EXAMPLE_DATA_PATH)
            X_test = df.drop(columns=["Class"], errors='ignore').values
            model_name = ui.combo_algorithm2.currentText()
            model_path = MODEL_MAP.get(model_name)
            if not model_path or not os.path.exists(model_path):
                QMessageBox.warning(ui, "提示", "模型文件不存在或选择错误")
                return
            model = joblib.load(model_path)
            preds = model.predict(X_test)
            show_results(preds)
        except Exception as e:
            QMessageBox.critical(ui, "示例检测失败", str(e))

    def save_result_to_pdf():
        if not hasattr(ui, "latest_predictions"):
            QMessageBox.warning(ui, "提示", "没有可保存的内容")
            return
        save_path, _ = QFileDialog.getSaveFileName(
            ui, "保存预测结果", "prediction_result.pdf", "PDF Files (*.pdf)"
        )
        if not save_path:
            return
        try:
            with PdfPages(save_path) as pdf:
                fig_text = plt.figure(figsize=(8.5, 11))
                text = "预测结果：\n\n" + ui.latest_predictions.to_string(index=False)
                fig_text.text(0.1, 0.9, text, fontsize=10, va="top", wrap=True)
                pdf.savefig(fig_text)
                plt.close(fig_text)

                fig_chart = plt.figure(figsize=(8.5, 5))
                ax = fig_chart.add_subplot(111)
                pd.Series(ui.latest_predictions["预测类别"]).value_counts().plot.bar(color="skyblue", ax=ax)
                ax.set_title("预测类别频次")
                ax.set_ylabel("数量")
                ax.set_xlabel("类别")
                ax.tick_params(axis='x', rotation=45)
                plt.tight_layout()
                pdf.savefig(fig_chart)
                plt.close(fig_chart)

            QMessageBox.information(ui, "保存成功", f"PDF文件已保存到:\n{save_path}")
        except Exception as e:
            QMessageBox.critical(ui, "保存失败", str(e))

     按钮绑定
    ui.btn_filedec2.clicked.connect(select_file)
    ui.data_owndec2.clicked.connect(show_uploaded_data)
    ui.data_exampledec2.clicked.connect(show_example_data)
    ui.select_owndec2.clicked.connect(run_uploaded_detection)
    ui.select_exampledec2.clicked.connect(run_example_detection)
    ui.btn_savedec2data.clicked.connect(save_result_to_pdf)

    ui.btn_backdec2.clicked.connect(lambda: ui.stackedWidget.setCurrentWidget(ui.page_dec))
    ui.btn_exitdec2.clicked.connect(ui.close)
    ui.btn_backdec2data.clicked.connect(lambda: ui.stackedWidget.setCurrentWidget(ui.page_dec2))
    ui.btn_exitdec2data.clicked.connect(ui.close)
