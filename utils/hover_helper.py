from PyQt5.QtCore import QObject, QEvent

class SimpleHover(QObject):
    def __init__(self, hover_map, display_widget):
        super().__init__()
        self.hover_map = hover_map
        self.display_widget = display_widget

        for widget in hover_map:
            widget.installEventFilter(self)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Enter and obj in self.hover_map:
            self.display_widget.setText(self.hover_map[obj])
        elif event.type() == QEvent.Leave and obj in self.hover_map:
            self.display_widget.setText("请将鼠标悬停在按钮上查看说明")
        return False
