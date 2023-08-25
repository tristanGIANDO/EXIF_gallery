import sys
import random
from PyQt5 import QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.dates as mdates
from datetime import datetime, timedelta

from datalens.api.database import Database

class PhotoGraphApp(QtWidgets.QDialog):
    def __init__(self, dates):
        super().__init__()
        self.setWindowTitle("Analyse de Photos")
        self.setGeometry(100, 100, 800, 600)

        # convert and conform datetime format
        converted_dates = []
        for str_date in dates:
            converted_dates.append([int(i) for i in str_date.split(",")])
        self.all_dates = [datetime(i[0],i[1],i[2]) for i in converted_dates]

        self._all_data = {}
        for date in self.all_dates:
            if date in self._all_data:
                self._all_data[date] += 1
            else:
                self._all_data[date] = 1
        self._dates = list(self._all_data.keys())
        self._counts = list(self._all_data.values())

        layout = QtWidgets.QVBoxLayout(self)

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        self.plot_graph()

    def plot_graph(self):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        ax.xaxis.set_major_locator(mdates.MonthLocator())

        ax.bar(self._dates, self._counts, width=10, color='tab:blue', label="Photos")

        ax.set_title("Number of photos taken")
        ax.set_xlabel("Date")
        ax.set_ylabel("Number of photos")
        ax.legend()
        ax.grid(True)

        self.figure.autofmt_xdate()
        self.canvas.draw()

if __name__ == "__main__":
    db = Database()
    files = db._files.select_rows()
    dates = []
    for file in files:
        id = file[0]
        str_date = db._files.get_date(id)
        splits = str_date.split(",")
        date = f"{splits[0]},{splits[1]},{splits[2]}"
        dates.append(date)

    app = QtWidgets.QApplication(sys.argv)
    window = PhotoGraphApp(dates)
    window.exec_()
    sys.exit(app.exec_())