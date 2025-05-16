import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_pdf import PdfPages
from al.dig5.timeline_extractor import extract_timeline_from_dataframe
import en_core_web_sm

def resource_path(relative_path):
    """资源路径处理（兼容打包后的exe和开发环境）"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

EXAMPLE_PATH = resource_path("example/dig4/processed_news.csv")

nlp = en_core_web_sm.load()

def setup_dig5_page(ui):
    ui.selected_timeline_path = None
    ui.selected_timeline_df = None

    def select_file():
        path, _ = QFileDialog.getOpenFileName(ui, "选择 CSV 文件", "", "CSV Files (*.csv)")
        if path:
            ui.selected_timeline_path = path
            ui.line_filepathdig5.setText(path)

    def show_uploaded_data():
        if ui.selected_timeline_path:
            try:
                df = pd.read_csv(ui.selected_timeline_path)
                ui.selected_timeline_df = df
                ui.Browser_owndig5.setText(df.head(100).to_string())
            except Exception as e:
                QMessageBox.critical(ui, "读取失败", str(e))
        else:
            QMessageBox.information(ui, "提示", "请先上传数据")

    def show_example_data():
        try:
            df = pd.read_csv(EXAMPLE_PATH)
            ui.Browser_exampledig5.setText(df.head(100).to_string())
        except Exception as e:
            QMessageBox.critical(ui, "读取失败", str(e))

    def show_results_to_page(df, timeline_df, relations):
        ui.stackedWidget.setCurrentWidget(ui.page_dig4data)
        ui.Browerdig4data.setText(timeline_df.to_string(index=False))
        ui.latest_timeline_df = timeline_df.copy()

        layout = ui.chart_hotwords_widget.layout()
        if layout is None:
            layout = QVBoxLayout()
            ui.chart_hotwords_widget.setLayout(layout)
        else:
            for i in reversed(range(layout.count())):
                layout.itemAt(i).widget().setParent(None)

        try:
            date_counts = timeline_df["date"].value_counts().sort_index()
            fig1 = plt.figure(figsize=(5, 3))
            ax1 = fig1.add_subplot(111)
            date_counts.plot(kind="bar", color="orange", ax=ax1)
            ax1.set_title("Number of Events per Date")
            ax1.set_ylabel("Event Count")
            ax1.set_xlabel("Date")
            plt.xticks(rotation=45)
            canvas1 = FigureCanvas(fig1)
            layout.addWidget(canvas1)
        except Exception as e:
            QMessageBox.warning(ui, "图表绘制失败", f"时间线图绘制失败：{e}")

        if relations:
            try:
                fig2 = plt.figure(figsize=(5, 3))
                G = nx.DiGraph()
                for src, rel, tgt in relations:
                    G.add_edge(src, tgt, label=rel)
                pos = nx.spring_layout(G)
                nx.draw(G, pos, with_labels=True, node_color="lightblue", node_size=1000, font_size=8)
                edge_labels = nx.get_edge_attributes(G, 'label')
                nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=7)
                plt.title("Entity Relationship Graph")
                canvas2 = FigureCanvas(fig2)
                layout.addWidget(canvas2)
            except Exception as e:
                QMessageBox.warning(ui, "关系图绘制失败", f"实体关系图绘制失败：{e}")

    def extract_relations_from_text(text):
        doc = nlp(text)
        relations = []
        for sent in doc.sents:
            sent_doc = nlp(sent.text)
            subject = None
            verb = None
            obj = None
            for token in sent_doc:
                if token.dep_ in ("nsubj", "nsubjpass"):
                    subject = token
                elif token.dep_ == "dobj":
                    obj = token
                elif token.pos_ == "VERB":
                    verb = token
            if subject and verb and obj:
                relations.append((subject.text, verb.lemma_, obj.text))
        return relations

    def run_example_detection():
        try:
            df = pd.read_csv(EXAMPLE_PATH)
            timeline_df = extract_timeline_from_dataframe(df)
            all_text = " ".join(df["content"].dropna().astype(str))
            relations = extract_relations_from_text(all_text)
            show_results_to_page(df, timeline_df, relations)
        except Exception as e:
            QMessageBox.critical(ui, "运行错误", f"示例数据处理失败：{e}")

    def run_own_detection():
        try:
            df = pd.read_csv(ui.selected_timeline_path)
            timeline_df = extract_timeline_from_dataframe(df)
            all_text = " ".join(df["content"].dropna().astype(str))
            relations = extract_relations_from_text(all_text)
            show_results_to_page(df, timeline_df, relations)
        except Exception as e:
            QMessageBox.critical(ui, "运行错误", f"上传数据处理失败：{e}")

    def save_result_to_pdf():
        if not hasattr(ui, "latest_timeline_df"):
            return

        save_path, _ = QFileDialog.getSaveFileName(
            ui, "保存结果", "result_summary.pdf", "PDF Files (*.pdf)"
        )
        if not save_path:
            return

        try:
            with PdfPages(save_path) as pdf:
                fig_text = plt.figure(figsize=(8.5, 11))
                text = ui.latest_timeline_df.to_string(index=False)
                fig_text.text(0.05, 0.95, text, fontsize=10, va="top", wrap=True)
                pdf.savefig(fig_text)
                plt.close(fig_text)

                timeline_df = ui.latest_timeline_df
                fig1 = plt.figure(figsize=(8.5, 5))
                ax1 = fig1.add_subplot(111)
                date_counts = timeline_df["date"].value_counts().sort_index()
                date_counts.plot(kind="bar", color="orange", ax=ax1)
                ax1.set_title("Number of Events per Date")
                ax1.set_ylabel("Event Count")
                ax1.set_xlabel("Date")
                plt.xticks(rotation=45)
                plt.tight_layout()
                pdf.savefig(fig1)
                plt.close(fig1)

            QMessageBox.information(ui, "保存成功", f"结果已保存至：{save_path}")
        except Exception as e:
            QMessageBox.critical(ui, "保存失败", str(e))

    ui.btn_filedig5.clicked.connect(select_file)
    ui.data_owndig5.clicked.connect(show_uploaded_data)
    ui.data_exampledig5.clicked.connect(show_example_data)
    ui.select_exampledig5.clicked.connect(run_example_detection)
    ui.select_owndig5.clicked.connect(run_own_detection)
    ui.btn_backdig5.clicked.connect(lambda: ui.stackedWidget.setCurrentWidget(ui.page_dig))
    ui.btn_exitdig5.clicked.connect(ui.close)
    ui.btn_backdec4data.clicked.connect(lambda: ui.stackedWidget.setCurrentWidget(ui.page_dig4))
    ui.btn_exitdec4data.clicked.connect(ui.close)
    ui.btn_savedec4data.clicked.connect(save_result_to_pdf)
