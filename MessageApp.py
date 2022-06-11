from PyQt5.QtWidgets import QMessageBox


class MessageInfo(object):
    def __init__(self):
        super().__init__()

    def message_path(self):
        message = QMessageBox()
        message.setIcon(QMessageBox.Information)
        message.setWindowTitle("Не выбрано место сохранения")
        message.setText('Пожалуйста, выберите директорию сохранения для видео')
        message.setStandardButtons(QMessageBox.Ok)
        message.exec_()

    def message_url(self):
        message = QMessageBox()
        message.setIcon(QMessageBox.Information)
        message.setWindowTitle("Нет url видео")
        message.setText('Пожалуйста, введите url видео')
        message.setStandardButtons(QMessageBox.Ok)
        message.exec_()

    def message_wrong_enter_url(self):
        message = QMessageBox()
        message.setIcon(QMessageBox.Information)
        message.setWindowTitle('Ошибка ввода url')
        message.setText('Неправильный ввод url')
        message.setStandardButtons(QMessageBox.Ok)
        message.exec_()

