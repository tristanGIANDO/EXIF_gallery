import os, sys
from PyQt5 import QtWidgets, QtGui
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.dates as mdates
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from geopy.geocoders import Nominatim
from datetime import datetime, timedelta
from datalens.ui import envs
from datalens.api import utils
from collections import Counter

def create_website(paths:list[str], delivery_path:str,
                   user:list[str]=None, overlays:str=None,
                   albums:list[str]=["Home"], website_name:str="datalens_portfolio"):
    """
    file_path (str): the source file
    delivery_path (str): the destination folder where to write HTML file.
    """
    title = "My portfolio"
    subtitle = "Powered by Datalens"
    thumbnail = envs.ICONS.get("logo")

    if len(user) >= 3:
        title = f"{user[1]} {user[2]}" # first name + last name
    if len(user) >= 4:
        subtitle = user[3]
    if len(user) >= 5:
        thumbnail = user[4]

    html_content = f'''
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="icon" href={envs.ICONS.get("logo")} type="image/x-icon">\n
    <title>{title} portfolio</title>\n
    '''

    html_content += '''
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 0;
            background-color: rgb(34, 34, 34);
            color: white;
        }
        header {
            padding: 10px;
            text-align: center;
            background-color: rgb(34, 34, 34);
        }
        .circle {
            width: 150px;
            height: 150px;
            border-radius: 50%;
            overflow: hidden;
            margin: 0 auto;
            display: flex;
            justify-content: center;
            align-items: center;
            background-color: #f0f0f0;
        }
        .circle img {
            max-width: 100%;
            max-height: 100%;
            object-fit: cover;
        }
        nav {
            background-color: #4e4e4e;
            color: #ffffff;
            padding: 10px;
            text-align: center;
        }
        nav a {
            color: #ffffff;
            text-decoration: none;
            margin: 0 10px;
        }
        h2 {
            color: #197092
        }
        .image-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 10px;
            /* position: relative;
            overflow: hidden; */
        }
        .image-item {
            width: 100%;
            padding-bottom: 100%;
            box-sizing: border-box;
            position: relative;
            overflow: hidden;
        }
        .image-item img {
            position: absolute;
            width: 100%;
            height: 100%;
            object-fit: cover;
        }
        .overlay {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 0, 0, 0.5);
            display: none;
            border-radius: inherit;
            z-index: 1;
        }
        .image-item:hover .overlay {
            display: block;
        }
        .overlay-text {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            text-align: center;
            color: white;
            font-size: 16px;
            z-index: 2;
        }
        footer {
            background-color: #4e4e4e;
            padding: 10px;
            text-align: center;
        }
    </style>
</head>
<body>
    <header>
        <div class="circle">\n
    '''
    html_content += f'''
            <img src="{thumbnail}" alt="Thumbnail">
        </div>
        <h1>{title}</h1>
        <h2>{subtitle}</h2>\n
    </header>
    <nav>\n
    '''

    html_content += '''
    </nav>
    <div class="image-grid">\n
    '''
    for path, overlay in zip(paths,overlays):
        html_content += f'''
        <div class="image-item">
            <img src="{path}" alt="{path}">
            <div class="overlay">
                <div class="overlay-text">
                    {overlay}
                </div>
            </div>
        </div>\n
        '''

    html_content += '''
    </div>
<footer>
        <p>Powered by DataLens</p>
    </footer>
</body>
</html>
'''

    html_file = os.path.join(delivery_path, f"{website_name}.html")

    with open(html_file, "w") as f:
        f.write(html_content)

    return html_file

class WorldMapUI(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Select a location")
        self.setGeometry(100, 100, 800, 600)
        self.setWindowIcon(envs.ICONS.get("logo"))

        self._longitude_shift = 0.0
        self._latitude_shift = 20.0
        self._zoom = 1.0

        # widgets
        self.text = QtWidgets.QLineEdit()
        self.text.setPlaceholderText("Click on the map...")
        self.zoom_in_btn = QtWidgets.QPushButton("Zoom In", self)
        self.zoom_out_btn = QtWidgets.QPushButton("Zoom Out", self)
        self.move_left_btn = QtWidgets.QPushButton("Move Left", self)
        self.move_right_btn = QtWidgets.QPushButton("Move Right", self)
        self.move_up_btn = QtWidgets.QPushButton("Move Up", self)
        self.move_down_btn = QtWidgets.QPushButton("Move Down", self)
        self.canvas = FigureCanvas(plt.figure())
        self.ok_btn = QtWidgets.QPushButton("OK")
        self.cancel_btn = QtWidgets.QPushButton("Cancel")

        # layouts
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.canvas)
        layout.addWidget(self.text)
        layout.addWidget(self.zoom_in_btn)
        layout.addWidget(self.zoom_out_btn)
        layout.addWidget(self.move_left_btn)
        layout.addWidget(self.move_right_btn)
        layout.addWidget(self.move_up_btn)
        layout.addWidget(self.move_down_btn)
        layout.addWidget(self.ok_btn)
        layout.addWidget(self.cancel_btn)
        
        # update
        self.projection = ccrs.PlateCarree()
        self.ax = self.canvas.figure.add_subplot(1, 1, 1, projection=self.projection)
        self.update_map()
        
        # connections
        self.zoom_in_btn.clicked.connect(self.zoom_in)
        self.zoom_out_btn.clicked.connect(self.zoom_out)
        self.move_left_btn.clicked.connect(self.move_left)
        self.move_right_btn.clicked.connect(self.move_right)
        self.move_up_btn.clicked.connect(self.move_up)
        self.move_down_btn.clicked.connect(self.move_down)
        self.ok_btn.clicked.connect(self.on_ok_clicked)
        self.cancel_btn.clicked.connect(self.on_cancel_clicked)
        self.canvas.mpl_connect('button_press_event', self.on_map_click)

    def on_map_click(self, event):
        if event.inaxes is not None:
            lon, lat = self.ax.transData.inverted().transform((event.x, event.y))
            self.text.setText(self.get_location_name(lat,lon))
            utils.get_bortle_level(lat, lon)

    def get_location_name(self, latitude, longitude):
        geolocator = Nominatim(user_agent="WorldMapUI")
        location = geolocator.reverse((latitude, longitude), exactly_one=True)
        if location:
            adress = location.raw.get("address", {})
            return f'{adress.get("state")}, {adress.get("country")}'
        else:
            return "Unknown"
        
    def update_map(self):
        self.ax.clear()
        self.ax.set_global()
        self.ax.stock_img()
        self.ax.add_feature(cfeature.BORDERS, linestyle=':')
        self.ax.coastlines()
        self.ax.set_extent([-180 * self._zoom + self._longitude_shift, 180 * self._zoom + self._longitude_shift,
                            -90 * self._zoom + self._latitude_shift, 90 * self._zoom + self._latitude_shift],
                           crs=ccrs.PlateCarree())
        self.canvas.draw()

    def zoom_in(self):
        self._zoom *= 0.8
        self.update_map()

    def zoom_out(self):
        self._zoom *= 1.25
        self.update_map()

    def move_up(self):
        self._latitude_shift += 5.0
        self.update_map()

    def move_down(self):
        self._latitude_shift -= 5.0
        self.update_map()

    def move_left(self):
        self._longitude_shift -= 5.0
        self.update_map()

    def move_right(self):
        self._longitude_shift += 5.0
        self.update_map()

    def read(self):
        return self.text.text()
    
    def on_ok_clicked(self):
        self.deleteLater()
        self.accept()

    def on_cancel_clicked(self):
        self.deleteLater()
        self.reject()

class GraphUI(QtWidgets.QDialog):
    def __init__(self, db, files):
        super().__init__()
        self.setWindowTitle("Number of photos taken")
        self.setGeometry(100, 100, 800, 600)

        self._db = db
        self._dates = []
        self._times = []
        self._isos = []
        self._fnumbers = []
        for file in files:
            id = file[0]
            str_date = self._db._astro_files.get_date(id)
            splits = str_date.split(",")
            date = f"{splits[0]},{splits[1]},{splits[2]}"
            self._dates.append(date)
            self._times.append(self._db._astro_files.get_total_time(id))
            self._isos.append(self._db._astro_files.get_iso(id))
            self._fnumbers.append(self._db._astro_files.get_f_number(id))

        # favourites
        fav_layout = QtWidgets.QVBoxLayout()
        self.total_time_lbl = QtWidgets.QLabel("Your average exposure time is :")
        self.total_time_lbl.setFont(QtGui.QFont("Arial", 10, QtGui.QFont.Bold))
        self.total_time_nb_lbl = QtWidgets.QLabel()
        self.total_time_nb_lbl.setFont(QtGui.QFont("Arial", 14, QtGui.QFont.Bold))

        self.iso_lbl = QtWidgets.QLabel("Your favourite ISO is :")
        self.iso_lbl.setFont(QtGui.QFont("Arial", 10, QtGui.QFont.Bold))
        self.iso_nb_lbl = QtWidgets.QLabel()
        self.iso_nb_lbl.setFont(QtGui.QFont("Arial", 14, QtGui.QFont.Bold))

        self.fnumber_lbl = QtWidgets.QLabel("Your favourite LENS APERTURE is :")
        self.fnumber_lbl.setFont(QtGui.QFont("Arial", 10, QtGui.QFont.Bold))
        self.fnumber_nb_lbl = QtWidgets.QLabel()
        self.fnumber_nb_lbl.setFont(QtGui.QFont("Arial", 14, QtGui.QFont.Bold))

        fav_layout.addWidget(self.total_time_lbl)
        fav_layout.addWidget(self.total_time_nb_lbl)
        fav_layout.addWidget(self.iso_lbl)
        fav_layout.addWidget(self.iso_nb_lbl)
        fav_layout.addWidget(self.fnumber_lbl)
        fav_layout.addWidget(self.fnumber_nb_lbl)
        fav_layout.addStretch(1)

        # GRAPH
        # convert and conform datetime format
        converted_dates = []
        for str_date in self._dates or []:
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

        layout = QtWidgets.QHBoxLayout(self)

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)
        layout.addLayout(fav_layout)

        self.plot_graph()
        self.update_favourites()

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

    def update_favourites(self):
        # total time
        lengths = [datetime.strptime(d, "%H:%M:%S") - datetime.strptime("0:0:0", "%H:%M:%S") for d in self._times]
        sums = sum(lengths, timedelta())
        time = str(sums / len(lengths))
        if "." in time:
            time = time.split(".")[0]
        text =  f"{str(time)} hours"
        self.total_time_nb_lbl.setText(text)

        # iso
        count = Counter(self._isos)
        fav, c = count.most_common(1)[0]
        self.iso_nb_lbl.setText(str(fav))

        # f number
        count = Counter(self._fnumbers)
        fav, c = count.most_common(1)[0]
        self.fnumber_nb_lbl.setText(str(fav))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = WorldMapUI()
    window.show()
    sys.exit(app.exec_())
