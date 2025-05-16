from utils.simple_hover import SimpleHover


def setup_dig_page(ui):
    ui.btn_backdig.clicked.connect(lambda: ui.stackedWidget.setCurrentWidget(ui.page_homed))
    ui.btn_digexit.clicked.connect(lambda: ui.close())

     进入 page_dig1 页面
    ui.btn_dig1.clicked.connect(lambda: ui.stackedWidget.setCurrentWidget(ui.page_dig1))
     进入 page_dig2 页面
    ui.btn_dig2.clicked.connect(lambda: ui.stackedWidget.setCurrentWidget(ui.page_dig2))
     进入 page_dig3 页面
    ui.btn_dig3.clicked.connect(lambda: ui.stackedWidget.setCurrentWidget(ui.page_dig3))
     进入 page_dig4 页面
    ui.btn_dig4.clicked.connect(lambda: ui.stackedWidget.setCurrentWidget(ui.page_dig4))
     进入 page_dig5 页面
    ui.btn_dig5.clicked.connect(lambda: ui.stackedWidget.setCurrentWidget(ui.page_dig5))

    hover_map = {
        ui.btn_dig1: "本模块实现了从数据上传、数据查看，到模型检测、结果展示及结果保存的完整流程。界面操作简洁，步骤明确，支持用户高效进行文本信息的真假判别分析，适用于新闻审核、社交媒体内容过滤等场景。",
        ui.btn_dig2: "本模块实现了从文本数据上传、查看，到自动化聚类分析、结果展示及PDF保存的完整流程。通过关键词提取和主题跟踪，用户能够快速掌握大量文本数据中的核心主题分布，适用于新闻聚类、社交话题分析、事件演化追踪等应用场景。",
        ui.btn_dig3: "本模块通过抽取文本中的实体、动作和关系，构建实体关系网络，并以交互式可视化图形式展示，极大地方便了用户对大规模文本数据中实体交互模式的直观理解与探索。适用于舆情分析、新闻事件关系梳理、情报挖掘等应用场景。",
        ui.btn_dig4: "本模块通过快速高效的热词提取和可视化展示，帮助用户快速识别文本数据中的关键词热点和主题倾向，适用于新闻热点挖掘、社交舆情分析、文本内容分布洞察等场景。",
        ui.btn_dig5: "本模块通过对文本内容的事件抽取、时间轴构建和实体关系识别，为用户提供了直观的事件发展脉络及交互网络视角。操作流畅，输出信息丰富，适合用于新闻追踪、事件演变分析、舆情关系梳理等场景。"

    }

    ui.hover_helper_dig = SimpleHover(hover_map, ui.textBrowserdig)
