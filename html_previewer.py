from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget,
                            QVBoxLayout, QHBoxLayout, QTextEdit,
                            QPushButton, QSplitter, QMessageBox)
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QDesktopServices
import sys
import os
import tempfile

class HTMLPreviewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('HTML 预览器')
        self.setGeometry(100, 100, 1200, 700)

        # 创建主窗口部件
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        # 创建布局
        main_layout = QVBoxLayout()
        main_widget.setLayout(main_layout)

        # 创建按钮容器 (移到这里)
        button_container = QWidget()
        button_layout = QHBoxLayout()
        button_container.setLayout(button_layout)
        # 减少上下边距，设置为最小值
        button_layout.setContentsMargins(10, 0, 10, 0)  # 上下边距设为0
        button_layout.setSpacing(10)  # 减少控件之间的间距
        button_container.setFixedWidth(300)  # 设置固定宽度
        button_container.setFixedHeight(50)  # 设置固定高度，减少上下空白
        
        # 预览按钮
        preview_btn = QPushButton('预览')
        preview_btn.setFixedSize(120, 40)
        preview_btn.clicked.connect(self.preview_html)
        button_layout.addWidget(preview_btn)

        # 添加按钮之间的间距（减少间距）
        button_layout.addSpacing(10)  # 从20减少到10

        # 浏览器打开按钮
        browser_btn = QPushButton('通过浏览器打开')
        browser_btn.setFixedSize(120, 40)
        browser_btn.clicked.connect(self.open_in_browser)
        button_layout.addWidget(browser_btn)
        
        # 不需要添加stretch，因为我们已经固定了容器宽度
        # button_layout.addStretch()

        # 将按钮容器添加到主布局 (在分割器之前)
        main_layout.addWidget(button_container)

        # 创建分割器容器
        splitter_container = QWidget()
        splitter_layout = QHBoxLayout()
        splitter_container.setLayout(splitter_layout)

        # 创建分割器
        splitter = QSplitter()
        splitter_layout.addWidget(splitter)

        # 左侧代码编辑区域
        self.code_editor = QTextEdit()
        self.code_editor.setPlaceholderText("在此输入HTML代码...")
        splitter.addWidget(self.code_editor)

        # 右侧HTML预览区域
        self.web_view = QWebEngineView()
        
        # 创建一个容器来包装 QWebEngineView
        web_container = QWidget()
        web_layout = QVBoxLayout(web_container)
        web_layout.setContentsMargins(10, 10, 10, 10)
        web_layout.addWidget(self.web_view)
        
        # 设置容器的样式
        web_container.setStyleSheet("""
            QWidget {
                background-color: white;
                border: 1px solid #cccccc;
                border-radius: 4px;
            }
        """)
        
        self.web_view.setHtml("<h3>HTML预览区域</h3>")
        splitter.addWidget(web_container)

        # 将分割器容器添加到主布局
        main_layout.addWidget(splitter_container)

        # 设置分割器初始比例（5:5）
        splitter.setSizes([int(self.width()*0.5), int(self.width()*0.5)])

    def preview_html(self):
        try:
            html_code = self.code_editor.toPlainText()
            self.web_view.setHtml(html_code)
        except Exception as e:
            QMessageBox.warning(self, "预览错误", f"HTML预览失败：{str(e)}")

    def open_in_browser(self):
        html_code = self.code_editor.toPlainText()
        if not html_code.strip():
            QMessageBox.warning(self, "警告", "编辑器内容为空！")
            return
            
        temp_path = None
        try:
            # 获取临时文件路径
            temp_path = os.path.join(tempfile.gettempdir(), "preview.html")
            with open(temp_path, "w", encoding="utf-8", errors='ignore') as f:
                f.write(html_code)
                
            # 使用系统默认程序打开
            QDesktopServices.openUrl(QUrl.fromLocalFile(temp_path))
        except Exception as e:
            QMessageBox.critical(self, "错误", f"打开文件失败：{str(e)}")
        finally:
            # 延迟删除临时文件（给浏览器一些时间加载文件）
            if temp_path and os.path.exists(temp_path):
                try:
                    # 使用 QTimer 延迟删除文件
                    from PyQt5.QtCore import QTimer
                    QTimer.singleShot(1000, lambda: os.remove(temp_path))
                except:
                    pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = HTMLPreviewer()
    window.show()
    sys.exit(app.exec_())