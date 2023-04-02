import sys
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QTabWidget, QVBoxLayout, QWidget, QPushButton, QHBoxLayout, QListWidget, QListWidgetItem, QLineEdit
from PyQt5.QtWebEngineWidgets import QWebEngineView

class Browser(QWidget):
    def __init__(self):
        super().__init__()

        self.bookmarks = []

        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)

        back_button = QPushButton("Back")
        back_button.setIcon(QIcon("left_arrow_icon.png"))
        back_button.clicked.connect(self.back)

        reload_button = QPushButton("Reload")
        reload_button.setIcon(QIcon("spiral_pointing_icon.png"))
        reload_button.clicked.connect(self.reload)

        home_button = QPushButton()
        home_button.setIcon(QIcon("home.png"))
        home_button.clicked.connect(self.home)

        bookmark_button = QPushButton()
        bookmark_button.setIcon(QIcon("bookmark.png"))
        bookmark_button.clicked.connect(self.bookmark)

        show_bookmarks_button = QPushButton("Bookmarks")
        show_bookmarks_button.clicked.connect(self.toggle_bookmarks)

        new_tab_button = QPushButton("+")
        new_tab_button.clicked.connect(self.new_tab)

        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)

        top_layout = QHBoxLayout()
        top_layout.addWidget(back_button)
        top_layout.addWidget(reload_button)
        top_layout.addWidget(home_button)
        top_layout.addWidget(bookmark_button)
        top_layout.addWidget(show_bookmarks_button)
        top_layout.addWidget(self.url_bar)
        top_layout.addWidget(new_tab_button)

        self.bookmarks_list = QListWidget()
        self.bookmarks_list.itemDoubleClicked.connect(self.navigate_to_bookmark)
        self.bookmarks_list.hide()

        layout = QVBoxLayout(self)
        layout.addLayout(top_layout)
        layout.addWidget(self.tabs)
        layout.addWidget(self.bookmarks_list)

        self.add_tab(QUrl("https://www.bing.com"))

    def add_tab(self, url):
      view = QWebEngineView()
      view.load(url)

      i = self.tabs.addTab(view, url.host())
      self.tabs.setCurrentIndex(i)

    def close_tab(self, index):
      self.tabs.removeTab(index)

    def new_tab(self):
      self.add_tab(QUrl("https://www.bing.com"))

    def back(self):
      current_view = self.tabs.currentWidget()
      if current_view:
          current_view.back()

    def reload(self):
      current_view = self.tabs.currentWidget()
      if current_view:
          current_view.reload()

    def home(self):
      current_view = self.tabs.currentWidget()
      if current_view:
          current_view.load(QUrl("https://www.bing.com"))

    def bookmark(self):
      currentIndex=self.tabs.currentIndex()
      currentView=self.tabs.currentWidget()
      if currentView:
          url=currentView.url().toString()
          title=self.tabs.tabText(currentIndex)
          bookmark={"title":title,"url":url}
          if bookmark not in self.bookmarks:
              self.bookmarks.append(bookmark)
              item=QListWidgetItem(title)
              item.setData(1,url)
              self.bookmarks_list.addItem(item)

    def navigate_to_bookmark(self,item):
      url=item.data(1)
      if url:
          self.add_tab(QUrl(url))

    def toggle_bookmarks(self):
      if self.bookmarks_list.isVisible():
          self.bookmarks_list.hide()
      else:
          self.bookmarks_list.show()

    def navigate_to_url(self):
      url = QUrl.fromUserInput(self.url_bar.text())
      if url.isValid():
          self.add_tab(url)

app = QApplication(sys.argv)

browser = Browser()
browser.show()

sys.exit(app.exec_())