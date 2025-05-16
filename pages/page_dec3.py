import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_pdf import PdfPages
from al.dec3.predict_pipeline import full_predict

def resource_path(relative_path):
    """资源路径处理（兼容打包后的exe和开发环境）"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

 模型映射表
ALGORITHM_MAP = {
    "随机森林": "randomforest",
    "KNN": "KNN",
    "决策树": "decisiontree",
    "XGBoost": "xgboost",
    "梯度提升": "gradientboosting",
    "逻辑回归": "logisticregression",
    "KMeans+RF": "KMeans+RF",
    "DBSCAN+RF": "DBSCAN+RF",
    "投票集成": "voting_ensemble",
    "堆叠集成": "stacking_ensemble"
}

EXAMPLE_PATH = resource_path(os.path.join("example", "dec3", "test.csv"))

def setup_dec3_page(ui):
    ui.selected_filepath = None
    ui.selected_df = None

    if ui.combo_algorithm3.count() == 0:
        ui.combo_algorithm3.addItems(ALGORITHM_MAP.keys())

    def select_file():
        path, _ = QFileDialog.getOpenFileName(ui, "选择CSV文件", "", "CSV Files (*.csv)")
        if path:
            ui.selected_filepath = path
            ui.line_filepathdec3.setText(path)

    def show_uploaded_data():
        if not ui.selected_filepath:
            QMessageBox.information(ui, "提示", "请先上传CSV文件")
            return
        try:
            df = pd.read_csv(ui.selected_filepath)
            ui.selected_df = df
            ui.Browser_owndec3.setText(df.head(100).to_string())
        except Exception as e:
            QMessageBox.critical(ui, "读取失败", str(e))

    def show_example_data():
        try:
            df = pd.read_csv(EXAMPLE_PATH)
            ui.Browser_exampledec3.setText(df.head(100).to_string())
        except Exception as e:
            QMessageBox.critical(ui, "读取示例数据失败", str(e))

    def show_bar_chart(counts_dict):
        layout = ui.chart_dec3_widget.layout()
        if layout:
            for i in reversed(range(layout.count())):
                layout.itemAt(i).widget().setParent(None)
        else:
            layout = QVBoxLayout()
            ui.chart_dec3_widget.setLayout(layout)

        fig = plt.figure(figsize=(5, 3))
        ax = fig.add_subplot(111)
        pd.Series(counts_dict).plot.bar(color="skyblue", ax=ax)
        ax.set_title("预测结果标签频次")
        ax.set_ylabel("次数")
        ax.set_xlabel("标签")
        ax.tick_params(axis='x', rotation=45)

        canvas = FigureCanvas(fig)
        layout.addWidget(canvas)

    def show_results_page(labels):
        counts = pd.Series(labels).value_counts().to_dict()

        ui.stackedWidget.setCurrentWidget(ui.page_dec3data)

        df_result = pd.DataFrame(labels, columns=["预测结果"])
        ui.Browerdec3data.setText(df_result.to_string(index=False))

        show_bar_chart(counts)

        ui.latest_prediction_result = df_result
        ui.latest_prediction_counts = counts

    def run_uploaded_detection():
        if not ui.selected_filepath:
            QMessageBox.warning(ui, "提示", "请先上传CSV文件")
            return
        model_key = ALGORITHM_MAP.get(ui.combo_algorithm3.currentText())
        if not model_key:
            QMessageBox.warning(ui, "提示", "请选择算法")
            return
        try:
            labels = full_predict(ui.selected_filepath, model_key)
            if labels is None:
                raise ValueError("预测结果为空")
            show_results_page(labels)
        except Exception as e:
            QMessageBox.critical(ui, "预测失败", str(e))

    def run_example_detection():
        model_key = ALGORITHM_MAP.get(ui.combo_algorithm3.currentText())
        if not model_key:
            QMessageBox.warning(ui, "提示", "请选择算法")
            return
        try:
            labels = full_predict(EXAMPLE_PATH, model_key)
            if labels is None:
                raise ValueError("预测结果为空")
            show_results_page(labels)
        except Exception as e:
            QMessageBox.critical(ui, "预测失败", str(e))

    def save_result_to_pdf():
        if not hasattr(ui, "latest_prediction_result"):
            QMessageBox.warning(ui, "提示", "没有可以保存的内容")
            return
        save_path, _ = QFileDialog.getSaveFileName(
            ui, "保存预测结果", "prediction_result.pdf", "PDF Files (*.pdf)"
        )
        if not save_path:
            return

        try:
            with PdfPages(save_path) as pdf:
                fig_text = plt.figure(figsize=(8.5, 11))
                text = "预测结果列表：\n\n" + ui.latest_prediction_result.to_string(index=False)
                fig_text.text(0.1, 0.9, text, fontsize=10, va="top", wrap=True)
                pdf.savefig(fig_text)
                plt.close(fig_text)

                fig_chart = plt.figure(figsize=(8.5, 5))
                ax = fig_chart.add_subplot(111)
                pd.Series(ui.latest_prediction_counts).plot.bar(color="skyblue", ax=ax)
                ax.set_title("预测标签频次分布")
                ax.set_ylabel("数量")
                ax.set_xlabel("标签")
                ax.tick_params(axis='x', rotation=45)
                plt.tight_layout()
                pdf.savefig(fig_chart)
                plt.close(fig_chart)

            QMessageBox.information(ui, "保存成功", f"PDF文件已保存至:\n{save_path}")

        except Exception as e:
            QMessageBox.critical(ui, "保存失败", str(e))

     按钮绑定
    ui.btn_filedec3.clicked.connect(select_file)
    ui.data_owndec3.clicked.connect(show_uploaded_data)
    ui.data_exampledec3.clicked.connect(show_example_data)
    ui.select_owndec3.clicked.connect(run_uploaded_detection)
    ui.select_exampledec3.clicked.connect(run_example_detection)
    ui.btn_backdec3.clicked.connect(lambda: ui.stackedWidget.setCurrentWidget(ui.page_dec))
    ui.btn_exitdec3.clicked.connect(ui.close)

    ui.btn_backdec3data.clicked.connect(lambda: ui.stackedWidget.setCurrentWidget(ui.page_dec3))
    ui.btn_exitdec3data.clicked.connect(ui.close)
    ui.btn_savedec3data.clicked.connect(save_result_to_pdf)
