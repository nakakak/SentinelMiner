from utils.hover_helper import SimpleHover
from PyQt5.QtWidgets import QMessageBox

def setup_home_page(ui):
    ui.btn_login.pressed.connect(
        lambda: print("pressed 信号响应！") or ui.stackedWidget.setCurrentWidget(ui.page_login))

    按钮跳转逻辑
    ui.btn_login.clicked.connect(lambda: ui.stackedWidget.setCurrentWidget(ui.page_login))
    ui.btn_register.clicked.connect(lambda: ui.stackedWidget.setCurrentWidget(ui.page_register))
    ui.btn_exit.clicked.connect(ui.close)

    悬浮提示说明绑定（保持不变）
    hover_map = {
        ui.btn_dig: "点击进入数据挖掘模块,但请先登录。本软件的数据挖掘模块集成了六大核心功能，涵盖信息真伪辨别、文本聚类分析、实体关系可视化、热点关键词提取、事件抽取与时间线建立，以及多源事件共识提取。通过全面的数据处理、分析与可视化技术，帮助用户高效挖掘海量文本中的关键信息与内在规律，适用于新闻审核、舆情监控、事件追踪、主题分析与信息融合等多种应用场景。模块设计注重操作简洁、流程清晰，既满足专业分析需求，又便于快速上手和灵活扩展。",
        ui.btn_dec: "点击进入数据挖掘模块,但请先登录。本软件的攻击检测模块集成了多种网络安全威胁识别功能，涵盖加密暗网流量分析、物联网设备入侵检测、入侵攻击类型分类与恶意代码检测等领域。系统通过结合特征提取、机器学习分类与异常模式识别技术，能够高效检测加密通信中的隐匿威胁，精准识别不同类型的网络攻击，发现潜在的物联网安全风险，及时检测程序及流量中的恶意代码。模块设计注重多样性、实用性与实时性，广泛适用于网络安全审计、智能设备防护、恶意软件筛查与企业级安全防护建设等多种应用场景。"
    }
    ui.hover_helper_home = SimpleHover(hover_map, ui.textBrowserd)

    def dig_action():
        if ui.logged_user is None:
            QMessageBox.warning(ui, "未登录", "请先登录使用数据挖掘")
        else:
            ui.stackedWidget.setCurrentWidget(ui.page_dig)

    def dec_action():
        if ui.logged_user is None:
            QMessageBox.warning(ui, "未登录", "请先登录使用攻击检测")
        else:
            ui.stackedWidget.setCurrentWidget(ui.page_dec)

    ui.btn_dec.clicked.connect(dec_action)
    ui.btn_dig.clicked.connect(dig_action)
