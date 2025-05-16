import json
import os
import sys
from PyQt5.QtWidgets import QMessageBox

def resource_path(relative_path):
    """资源路径处理（兼容打包后的exe和开发环境）"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def setup_register_page(ui):
    ui.btn_makeregister.clicked.connect(lambda: handle_register(ui))
    ui.btn_back1.clicked.connect(lambda: clear_register_fields(ui))

def handle_register(ui):
    username = ui.edit_account1.text().strip()
    password = ui.edit_encode1.text().strip()
    confirm = ui.edit_conencode1.text().strip()

    if not username or not password or not confirm:
        QMessageBox.warning(ui, "注册失败", "所有字段均不能为空")
        return

    if password != confirm:
        QMessageBox.warning(ui, "注册失败", "两次输入密码不一致")
        return

    try:
        with open(resource_path("data/users.json"), "r", encoding="utf-8") as f:
            users = json.load(f)
    except FileNotFoundError:
        users = {}

    if username in users:
        QMessageBox.warning(ui, "注册失败", "用户名已存在")
        return

    users[username] = password
    with open(resource_path("data/users.json"), "w", encoding="utf-8") as f:
        json.dump(users, f, indent=2, ensure_ascii=False)

    QMessageBox.information(ui, "注册成功", "请前往登录")

    clear_register_fields(ui)
    ui.stackedWidget.setCurrentWidget(ui.page_login)

def clear_register_fields(ui):
    ui.edit_account1.clear()
    ui.edit_encode1.clear()
    ui.edit_conencode1.clear()
    ui.stackedWidget.setCurrentWidget(ui.page_home)
