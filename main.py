import sys
import os
import ui.resources_rc
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QMessageBox
from PyQt5.QtGui import QPixmap
from pages.page_home import setup_home_page
from pages.page_login import setup_login_page, clear_login_fields
from pages.page_register import setup_register_page
from pages.page_homed import setup_homed_page
from pages.page_dig import setup_dig_page
from pages.page_dec import setup_dec_page
from pages.page_dec2 import setup_dec2_page
from pages.page_dec3 import setup_dec3_page
from pages.page_dig1 import setup_dig1_page
from pages.page_dig2 import setup_dig2_page
from pages.page_dig3 import setup_dig3_page
from pages.page_dig4 import setup_dig4_page
from pages.page_dig5 import setup_dig5_page

def resource_path(relative_path):
    """获取资源文件路径（兼容打包后的exe和开发环境）"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi(resource_path("ui/mainwindow6.ui"), self)
        self.actionHelpDoc.triggered.connect(self.open_help_doc)
        setup_home_page(self)
        setup_login_page(self)
        setup_register_page(self)
        setup_homed_page(self)
        setup_dig_page(self)
        setup_dec_page(self)
        setup_dec2_page(self)
        setup_dec3_page(self)
        setup_dig1_page(self)
        setup_dig2_page(self)
        setup_dig3_page(self)
        setup_dig4_page(self)
        setup_dig5_page(self)
        self.go_home()
    def open_help_doc(self):
        pdf_path = resource_path("ui/help.pdf")

        if not os.path.exists(pdf_path):
            QMessageBox.warning(self, "错误", "未找到帮助文档！")
            return

        try:
            if sys.platform.startswith('darwin'):
                os.system(f"open '{pdf_path}'")
            elif os.name == 'nt':
                os.startfile(pdf_path)
            elif os.name == 'posix':
                os.system(f"xdg-open '{pdf_path}'")
        except Exception as e:
            QMessageBox.critical(self, "打开失败", f"无法打开文档：{e}")



    def go_home(self):
        self.logged_user = None
        clear_login_fields(self)
        self.stackedWidget.setCurrentWidget(self.page_home)

    def set_logged_out(self):
        self.logged_user = None
        clear_login_fields(self)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
