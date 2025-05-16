import os
import sys
import pandas as pd
import spacy
import en_core_web_sm
from pyvis.network import Network
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl

def resource_path(relative_path):
    """资源路径处理（兼容打包后的exe和开发环境）"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

EXAMPLE_PATH = resource_path("example/dig4/processed_news.csv")

nlp = en_core_web_sm.load()

def setup_dig3_page(ui):
    ui.selected_entity_path = None
    ui.selected_entity_df = None

    def select_file():
        path, _ = QFileDialog.getOpenFileName(ui, "选择CSV文件", "", "CSV Files (*.csv)")
        if path:
            ui.selected_entity_path = path
            ui.line_filepathdig3.setText(path)

    def show_uploaded_data():
        if ui.selected_entity_path:
            try:
                df = pd.read_csv(ui.selected_entity_path)
                ui.selected_entity_df = df
                ui.Browser_owndig3.setText(df.head(100).to_string())
            except Exception as e:
                QMessageBox.critical(ui, "读取失败", str(e))
        else:
            QMessageBox.information(ui, "提示", "请先上传CSV文件")

    def show_example_data():
        try:
            df = pd.read_csv(EXAMPLE_PATH)
            ui.Browser_exampledig3.setText(df.head(100).to_string())
        except Exception as e:
            QMessageBox.critical(ui, "示例数据读取失败", str(e))

    def extract_svo_with_ner(text):
        doc = nlp(text)
        ents = {ent.text: ent.label_ for ent in doc.ents}
        triplets = []
        for token in doc:
            if token.dep_ == "ROOT" and token.pos_ == "VERB":
                subj = [w.text for w in token.lefts if w.dep_ in ("nsubj", "nsubjpass")]
                obj = [w.text for w in token.rights if w.dep_ in ("dobj", "pobj", "attr")]
                if subj and obj:
                    triplets.append((subj[0], token.lemma_, obj[0]))
        return triplets, ents

    def generate_entity_graph(df, filename="entity_colored_graph.html"):
        all_triplets = []
        all_ents = {}

        for content in df["content"].dropna():
            triplets, ents = extract_svo_with_ner(content)
            all_triplets.extend(triplets)
            all_ents.update(ents)

        net = Network(height='750px', width='100%', directed=True, bgcolor="222222", font_color="white")
        net.force_atlas_2based()

        color_map = {
            "PERSON": "skyblue",
            "GPE": "lightgreen",
            "ORG": "orange",
            "OTHER": "lightgray"
        }

        added_nodes = set()
        for subj, verb, obj in all_triplets:
            for ent in [subj, obj]:
                if ent not in added_nodes:
                    label = all_ents.get(ent, "OTHER")
                    color = color_map.get(label, "lightgray")
                    net.add_node(ent, label=ent, title=f"{ent} ({label})", color=color)
                    added_nodes.add(ent)
            net.add_edge(subj, obj, label=verb, title=verb)

        save_dir = resource_path("outputs/dig3/")
        os.makedirs(save_dir, exist_ok=True)
        full_path = os.path.join(save_dir, filename)
        net.show(full_path, notebook=False, local=True)
        return full_path

    def show_results_to_page(html_path):
        ui.stackedWidget.setCurrentWidget(ui.page_dig3data)
        ui.Browerdig3data.setText(f"关系图已生成，文件路径：\n{html_path}")
        ui.latest_entity_graph_path = html_path

        try:
            abs_path = os.path.abspath(html_path)
            file_url = QUrl.fromLocalFile(abs_path)
            ui.webview_dig3.load(file_url)
        except Exception as e:
            QMessageBox.warning(ui, "网页加载失败", f"无法加载关系图：{e}")

    def run_example_detection():
        try:
            df = pd.read_csv(EXAMPLE_PATH)
            html_path = generate_entity_graph(df)
            show_results_to_page(html_path)
        except Exception as e:
            QMessageBox.critical(ui, "运行错误", f"示例数据检测失败：{e}")

    def run_own_detection():
        if not ui.selected_entity_path:
            QMessageBox.warning(ui, "提示", "请先选择上传CSV文件")
            return
        try:
            df = pd.read_csv(ui.selected_entity_path)
            html_path = generate_entity_graph(df)
            show_results_to_page(html_path)
        except Exception as e:
            QMessageBox.critical(ui, "运行错误", f"上传数据检测失败：{e}")

    def save_html_file():
        if not hasattr(ui, "latest_entity_graph_path"):
            QMessageBox.warning(ui, "提示", "当前没有生成的关系图可以保存")
            return
        save_path, _ = QFileDialog.getSaveFileName(
            ui, "保存HTML文件", "entity_colored_graph.html", "HTML Files (*.html)"
        )
        if save_path:
            try:
                os.replace(ui.latest_entity_graph_path, save_path)
                QMessageBox.information(ui, "保存成功", f"文件已保存至：\n{save_path}")
            except Exception as e:
                QMessageBox.critical(ui, "保存失败", str(e))

     按钮绑定
    ui.btn_filedig3.clicked.connect(select_file)
    ui.data_owndig3.clicked.connect(show_uploaded_data)
    ui.data_exampledig3.clicked.connect(show_example_data)
    ui.select_exampledig3.clicked.connect(run_example_detection)
    ui.select_owndig3.clicked.connect(run_own_detection)
    ui.btn_backdig3.clicked.connect(lambda: ui.stackedWidget.setCurrentWidget(ui.page_dig))
    ui.btn_exitdig3.clicked.connect(ui.close)
    ui.btn_backdig3data.clicked.connect(lambda: ui.stackedWidget.setCurrentWidget(ui.page_dig3))
    ui.btn_exitdig3data.clicked.connect(ui.close)
    ui.btn_savedig3data.clicked.connect(save_html_file)
