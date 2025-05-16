import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_pdf import PdfPages

from al.dig4.hotwords_processor import extract_hotwords_from_dataframe

def resource_path(relative_path):
    """资源路径处理（兼容打包后的exe和开发环境）"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

EXAMPLE_PATH = resource_path("example/dig4/processed_news.csv")

def setup_dig4_page(ui):
    ui.selected_hotwords_path = None
    ui.selected_hotwords_df = None

    def select_file():
        path, _ = QFileDialog.getOpenFileName(ui, "选择 CSV 文件", "", "CSV Files (*.csv)")
        if path:
            ui.selected_hotwords_path = path
            ui.line_filepathdig4.setText(path)

    def show_uploaded_data():
        if ui.selected_hotwords_path:
            try:
                df = pd.read_csv(ui.selected_hotwords_path)
                ui.selected_hotwords_df = df
                ui.Browser_owndig4.setText(df.head(100).to_string())
            except Exception as e:
                QMessageBox.critical(ui, "读取失败", str(e))
        else:
            QMessageBox.information(ui, "提示", "请先上传数据")

    def show_example_data():
        try:
            df = pd.read_csv(EXAMPLE_PATH)
            ui.Browser_exampledig4.setText(df.head(100).to_string())
        except Exception as e:
            QMessageBox.critical(ui, "读取失败", str(e))

    def show_hotwords_chart(df):
        layout = ui.chart_hotwords_widget.layout()
        if layout:
            for i in reversed(range(layout.count())):
                layout.itemAt(i).widget().setParent(None)
        else:
            layout = QVBoxLayout()
            ui.chart_hotwords_widget.setLayout(layout)

        fig = plt.figure(figsize=(5, 3))
        ax = fig.add_subplot(111)
        df.plot.bar(x="word", y="count", color="orange", legend=False, ax=ax)
        ax.set_title("Top 20 Hot Words")
        ax.set_xticklabels(df["word"], rotation=45)

        canvas = FigureCanvas(fig)
        layout.addWidget(canvas)

    def show_results_to_page(hotwords_df):
        ui.stackedWidget.setCurrentWidget(ui.page_dig4data)
        ui.Browerdig4data.setText(hotwords_df.to_string(index=False))
        show_hotwords_chart(hotwords_df)
        ui.latest_hotwords_df = hotwords_df.copy()

    def run_example_detection():
        try:
            df = pd.read_csv(EXAMPLE_PATH)
            hotwords = extract_hotwords_from_dataframe(df)
            show_results_to_page(hotwords)
        except Exception as e:
            QMessageBox.critical(ui, "运行错误", f"示例数据检测失败：{e}")

    def run_own_detection():
        try:
            df = pd.read_csv(ui.selected_hotwords_path)
            hotwords = extract_hotwords_from_dataframe(df)
            show_results_to_page(hotwords)
        except Exception as e:
            QMessageBox.critical(ui, "运行错误", f"上传数据检测失败：{e}")

    def save_result_to_pdf():
        if not hasattr(ui, "latest_hotwords_df"):
            return

        save_path, _ = QFileDialog.getSaveFileName(
            ui, "保存热词结果", "hotwords_result.pdf", "PDF Files (*.pdf)"
        )
        if not save_path:
            return

        try:
            with PdfPages(save_path) as pdf:
                fig_text = plt.figure(figsize=(8.5, 11))
                text = "Top 20 热词词频表：\n\n" + ui.latest_hotwords_df.to_string(index=False)
                fig_text.text(0.1, 0.9, text, fontsize=10, va="top", wrap=True)
                pdf.savefig(fig_text)
                plt.close(fig_text)

                fig_chart = plt.figure(figsize=(8.5, 5))
                ax = fig_chart.add_subplot(111)
                ui.latest_hotwords_df.plot.bar(x="word", y="count", color="orange", legend=False, ax=ax)
                ax.set_title("Top 20 Hot Words")
                ax.set_xticklabels(ui.latest_hotwords_df["word"], rotation=45)
                plt.tight_layout()
                pdf.savefig(fig_chart)
                plt.close(fig_chart)

            QMessageBox.information(ui, "保存成功", f"文件已保存至：\n{save_path}")
        except Exception as e:
            QMessageBox.critical(ui, "保存失败", str(e))

     按钮绑定
    ui.btn_filedig4.clicked.connect(select_file)
    ui.data_owndig4.clicked.connect(show_uploaded_data)
    ui.data_exampledig4.clicked.connect(show_example_data)
    ui.select_exampledig4.clicked.connect(run_example_detection)
    ui.select_owndig4.clicked.connect(run_own_detection)
    ui.btn_backdig4.clicked.connect(lambda: ui.stackedWidget.setCurrentWidget(ui.page_dig))
    ui.btn_exitdig4.clicked.connect(ui.close)
    ui.btn_backdec4data.clicked.connect(lambda: ui.stackedWidget.setCurrentWidget(ui.page_dig4))
    ui.btn_exitdec4data.clicked.connect(ui.close)
    ui.btn_savedec4data.clicked.connect(save_result_to_pdf)
