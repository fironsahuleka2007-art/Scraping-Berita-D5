import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QFileDialog
from PyQt5.QtCore import QThread, pyqtSignal
from scraper import scrape_berita
import pandas as pd


class ScraperThread(QThread):
    result = pyqtSignal(list)
    progress = pyqtSignal(int)

    def __init__(self, url, limit):
        super().__init__()
        self.url = url
        self.limit = limit

    def run(self):

        data = scrape_berita(self.url, self.limit)

        for i in range(len(data)):
            persen = int((i + 1) / len(data) * 100)
            self.progress.emit(persen)

        self.result.emit(data)


class App(QMainWindow):

    def __init__(self):
        super().__init__()
        uic.loadUi("ui/scraping_berita.ui", self)

        self.data = []

        self.pushButton.clicked.connect(self.start_scraping)
        self.pushButton_2.clicked.connect(self.export_excel)
        self.pushButton_3.clicked.connect(self.close)
        self.pushButton_4.clicked.connect(self.lineEdit_2.clear)
        

    def start_scraping(self):

        url = self.lineEdit_2.text()
        limit = self.spinBox.value()

        self.thread = ScraperThread(url, limit)

        self.thread.result.connect(self.show_data)
        self.thread.progress.connect(self.progressBar.setValue)

        self.progressBar.setValue(0)

        self.thread.start()

        print("Mulai scraping:", url)

    def show_data(self, data):

        self.data = data

        self.tableWidget.setRowCount(len(data))

        for row, berita in enumerate(data):
            self.tableWidget.setItem(row, 0, QTableWidgetItem(str(row + 1)))
            self.tableWidget.setItem(row, 1, QTableWidgetItem(berita["judul"]))
            self.tableWidget.setItem(row, 2, QTableWidgetItem(berita["tanggal"]))
            self.tableWidget.setItem(row, 3, QTableWidgetItem(berita["link"]))

    def export_excel(self):

        if len(self.data) == 0:
            print("Tidak ada data untuk diekspor")
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save File",
            "",
            "Excel Files (*.xlsx)"
        )

        if file_path:
            df = pd.DataFrame(self.data)
            df.to_excel(file_path, index=False)
            print("File berhasil disimpan:", file_path)


app = QApplication(sys.argv)
window = App()
window.show()
sys.exit(app.exec_())