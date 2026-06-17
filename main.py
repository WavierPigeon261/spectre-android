import sys
from PyQt6.QtCore import QUrl
from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
                             QWidget, QLineEdit, QPushButton, QTabWidget)
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEnginePage

class CustomWebEnginePage(QWebEnginePage):
    def __init__(self, tab_widget):
        super().__init__()
        self.tab_widget = tab_widget

    def createWindow(self, _type):
        # When a link requests a new window, create a new tab instead
        return self.tab_widget.add_new_tab()

class PrivacyBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Spectre Browser")
        self.setGeometry(100, 100, 1200, 800)

        # Tab Widget Setup
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)

        # Main Layout
        container = QWidget()
        layout = QVBoxLayout()
        
        # Navigation Bar
        nav_layout = QHBoxLayout()
        
        back_btn = QPushButton("◀")
        back_btn.clicked.connect(lambda: self.tabs.currentWidget().back())
        
        forward_btn = QPushButton("▶")
        forward_btn.clicked.connect(lambda: self.tabs.currentWidget().forward())
        
        reload_btn = QPushButton("⟳")
        reload_btn.clicked.connect(lambda: self.tabs.currentWidget().reload())
        
        new_tab_btn = QPushButton("+")
        new_tab_btn.clicked.connect(lambda: self.add_new_tab())
        
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("🔍 Search Spectre")
        self.search_bar.returnPressed.connect(self.execute_search)

        nav_layout.addWidget(back_btn)
        nav_layout.addWidget(forward_btn)
        nav_layout.addWidget(reload_btn)
        nav_layout.addWidget(new_tab_btn)
        nav_layout.addWidget(self.url_bar, stretch=3)
        nav_layout.addWidget(self.search_bar, stretch=2)

        layout.addLayout(nav_layout)
        layout.addWidget(self.tabs)
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Add initial tab
        self.add_new_tab(QUrl("https://spectre-search.onrender.com"))

    def add_new_tab(self, qurl=None):
        browser = QWebEngineView()
        browser.setPage(CustomWebEnginePage(self))
        if qurl:
            browser.setUrl(qurl)
        else:
            browser.setUrl(QUrl("https://spectre-search.onrender.com"))
        
        i = self.tabs.addTab(browser, "New Tab")
        self.tabs.setCurrentIndex(i)
        
        # Connect signals
        browser.urlChanged.connect(lambda q, b=browser: self.update_url_bar(q, b))
        browser.loadFinished.connect(lambda _, i=i, b=browser: self.tabs.setTabText(i, b.page().title()))
        
        return browser.page()

    def close_tab(self, i):
        if self.tabs.count() > 1:
            self.tabs.removeTab(i)

    def navigate_to_url(self):
        url = self.url_bar.text()
        if not url.startswith("http"): url = "https://" + url
        self.tabs.currentWidget().setUrl(QUrl(url))

    def execute_search(self):
        query = self.search_bar.text().replace(" ", "+")
        self.tabs.currentWidget().setUrl(QUrl(f"https://spectre-search.onrender.com/search?q={query}"))

    def update_url_bar(self, q, browser=None):
        if browser != self.tabs.currentWidget(): return
        self.url_bar.setText(q.toString())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PrivacyBrowser()
    window.show()
    sys.exit(app.exec())
