 pages/page_homed.py
from utils.hover_helper import SimpleHover

def setup_homed_page(ui):
    ui.btn_digre.clicked.connect(lambda: ui.stackedWidget.setCurrentWidget(ui.page_dig))
    ui.btn_decre.clicked.connect(lambda: ui.stackedWidget.setCurrentWidget(ui.page_dec))
    ui.btn_exitre.clicked.connect(ui.close)

    hover_map = {
        ui.btn_digre: "点击进入数据挖掘模块,本软件的数据挖掘模块集成了六大核心功能，涵盖信息真伪辨别、文本聚类分析、实体关系可视化、热点关键词提取、事件抽取与时间线建立，以及多源事件共识提取。通过全面的数据处理、分析与可视化技术，帮助用户高效挖掘海量文本中的关键信息与内在规律，适用于新闻审核、舆情监控、事件追踪、主题分析与信息融合等多种应用场景。模块设计注重操作简洁、流程清晰，既满足专业分析需求，又便于快速上手和灵活扩展。",
        ui.btn_decre: "点击进入攻击检测模块，本软件的攻击检测模块集成了多种网络安全威胁识别功能，涵盖加密暗网流量分析、物联网设备入侵检测、入侵攻击类型分类与恶意代码检测等领域。系统通过结合特征提取、机器学习分类与异常模式识别技术，能够高效检测加密通信中的隐匿威胁，精准识别不同类型的网络攻击，发现潜在的物联网安全风险，及时检测程序及流量中的恶意代码。模块设计注重多样性、实用性与实时性，广泛适用于网络安全审计、智能设备防护、恶意软件筛查与企业级安全防护建设等多种应用场景。"
    }
    ui.hover_helper_homed = SimpleHover(hover_map, ui.textBrowserdre)
