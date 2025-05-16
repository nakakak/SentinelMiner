from utils.hover_helper import SimpleHover


def setup_dec_page(ui):
    ui.btn_backdec.clicked.connect(lambda: ui.stackedWidget.setCurrentWidget(ui.page_homed))
    ui.btn_decexit.clicked.connect(lambda: ui.close())

    进入 page_dec2 页面
    ui.btn_dec2.clicked.connect(lambda: ui.stackedWidget.setCurrentWidget(ui.page_dec2))
    进入 page_dec2 页面
    ui.btn_dec3.clicked.connect(lambda: ui.stackedWidget.setCurrentWidget(ui.page_dec3))


    hover_map = {
        ui.btn_dec2: "本模块通过对标准入侵检测数据集（如KDD99、NSL-KDD、CICIDS等）中的网络流量特征进行分析，结合多种机器学习分类算法，实现对不同类型网络攻击（如DDoS、扫描、暴力破解、Web攻击等）的精准识别与分类。系统支持上传用户采集的网络数据，自动完成攻击类型预测与结果输出，辅助用户快速定位网络异常行为，提升入侵防御能力。适用于企业网络安全监控、攻击行为分类分析、入侵检测系统（IDS）优化与验证等场景。",
        ui.btn_dec3: "本模块针对程序代码、可执行文件或网络传输数据中的潜在恶意内容进行检测，通过特征提取与分类识别方法，发现并标记包含病毒、木马、勒索软件或后门程序的恶意样本。系统支持对静态文本数据或流量数据进行分析，结合多维度特征（如指令模式、字符串特征、行为特征等）进行恶意代码的自动识别。适用于软件供应链安全检测、病毒传播路径分析、恶意文件筛查与安全防护建设等应用场景。"
    }

    ui.hover_helper_dec = SimpleHover(hover_map, ui.textBrowserdec)
