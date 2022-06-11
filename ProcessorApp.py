from PyQt5.QtCore import QThread, pyqtSignal
from youtube_dl import YoutubeDL


class Processor(QThread):
    chunks = pyqtSignal(int)
    info_video = pyqtSignal(str, str)

    def __init__(self, url, path):
        super().__init__()

        self.url = url
        self.path = path

    def run(self):
        try:
            with YoutubeDL({'quiet': True}) as ydl:
                info_dict = ydl.extract_info(self.url, download=False)
                video_title = info_dict.get('title', None)
                video_description = info_dict.get('description', None)

                self.info_video.emit(video_title, video_description)

                dl_options = {
                    'format': 'best',
                    'outtmpl': self.path + "/" + video_title + ".mp4",
                    'progress_hooks': [self.progress]
                }

                with YoutubeDL(dl_options) as dl:
                    dl.download([self.url])
        except Exception as ex:
            print(ex)

    def progress(self, percent):
        if percent['status'] == 'downloading':
            result = round(percent['downloaded_bytes'] / percent['total_bytes'] * 100, 1)

            print(round(percent['downloaded_bytes'] / percent['total_bytes'] * 100, 1))
            self.chunks.emit(result)


