import json
import sys
import os
from PyQt5.QtWidgets import QMessageBox

def resource_path(relative_path):
    """资源路径处理（兼容打包后的exe和开发环境）"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

 登录页初始化绑定
def setup_login_page(ui):
    ui.btn_makelogin.clicked.connect(lambda: handle_login(ui))
    ui.btn_back.clicked.connect(lambda: [
        clear_login_fields(ui),
        ui.set_logged_out(),
        ui.stackedWidget.setCurrentWidget(ui.page_home)
    ])

def handle_login(ui):
    username = ui.edit_account.text().strip()
    password = ui.edit_encode.text().strip()

    if not username or not password:
        QMessageBox.warning(ui, "登录失败", "请填写完整的账号和密码")
        return

    try:
        with open(resource_path("data/users.json"), "r", encoding="utf-8") as f:
            users = json.load(f)
    except FileNotFoundError:
        users = {}

    if username in users and users[username] == password:
        ui.logged_user = username

        if hasattr(ui, "label_welcomed"):
            ui.label_welcomed.setText(f"欢迎您，{username}！")
        if hasattr(ui, "lable_decwelcome"):
            ui.lable_decwelcome.setText(f"欢迎您，{username}！")
        if hasattr(ui, "lable_digwelcome"):
            ui.lable_digwelcome.setText(f"欢迎您，{username}！")

        clear_login_fields(ui)
        ui.stackedWidget.setCurrentWidget(ui.page_homed)
    else:
        QMessageBox.warning(ui, "登录失败", "账号或密码错误")

def clear_login_fields(ui):
    ui.edit_account.clear()
    ui.edit_encode.clear()
