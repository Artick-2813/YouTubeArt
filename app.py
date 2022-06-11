from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QFileDialog
from WidgetsApp import Ui_MainWindow
from MessageApp import MessageInfo
from ProcessorApp import Processor
import sys


try:
    # Отображает иконку на панели задач
    from PyQt5.QtWinExtras import QtWin
    app_version = u'mycompany.myproduct.subproduct.version'
    QtWin.setCurrentProcessExplicitAppUserModelID(app_version)
except ImportError:
    print('[ERROR] The icon cannot be displayed')


class App(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self):
        super(App, self).__init__()

        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon('images/YouTube-icon.png'))
        self.setWindowTitle('Youtube Downloader')
        self.ButtonChoosePath.clicked.connect(self.select_directory)
        self.ButtonDownload.clicked.connect(self.download)

    def select_directory(self):
        path = QFileDialog.getExistingDirectory(self, 'Выберите папку', ".")
        self.InputShowPath.setText(path)

    def download(self):

        path = self.InputShowPath.text()
        url = self.InputUrl.text()

        if path and url:
            self.start_thread = Processor(url, path)
            self.start_thread.start()

            self.InputShowPath.setText('')
            self.InputUrl.setText('')
            self.start_thread.chunks.connect(self.progress)
            self.start_thread.info_video.connect(self.show_info)

        else:
            if path == '':
                MessageInfo.message_path(self)

            elif url == '':
                MessageInfo.message_url(self)

    def progress(self, chunks):
        self.progressBar.setValue(chunks)

        if self.progressBar.value() == 100:
            self.progressBar.setValue(0)

            self.TitleVideo.setText('Загрузка видео завершенна')
            self.ShowDescription.setText('')

    def show_info(self, title, description):
        self.TitleVideo.setText(title)
        self.ShowDescription.setText(description)


def start_app():
    app = QtWidgets.QApplication(sys.argv)
    window = App()
    window.show()
    app.exec_()


if __name__ == '__main__':
    start_app()

