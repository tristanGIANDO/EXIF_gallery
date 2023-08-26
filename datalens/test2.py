import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from geopy.geocoders import Nominatim

class WorldMapApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Select a location")
        self.setGeometry(100, 100, 800, 600)

        self.longitude_shift = 0.0

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        self.canvas = FigureCanvas(plt.figure())
        layout.addWidget(self.canvas)

        self.zoom_in_button = QPushButton("Zoom In", self)
        self.zoom_out_button = QPushButton("Zoom Out", self)
        self.move_left_button = QPushButton("Move Left", self)
        self.move_right_button = QPushButton("Move Right", self)
        layout.addWidget(self.zoom_in_button)
        layout.addWidget(self.zoom_out_button)
        layout.addWidget(self.move_left_button)
        layout.addWidget(self.move_right_button)
        
        self.zoom_level = 1.0  # Niveau de zoom initial
        
        self.zoom_in_button.clicked.connect(self.zoom_in)
        self.zoom_out_button.clicked.connect(self.zoom_out)
        self.move_left_button.clicked.connect(self.move_left)
        self.move_right_button.clicked.connect(self.move_right)

        self.move_up_button = QPushButton("Move Up", self)
        self.move_down_button = QPushButton("Move Down", self)
        layout.addWidget(self.move_up_button)
        layout.addWidget(self.move_down_button)
        
        self.latitude_shift = 20.0  # Ajustez la valeur selon votre préférence

        self.move_up_button.clicked.connect(self.move_up)
        self.move_down_button.clicked.connect(self.move_down)

        self.projection = ccrs.PlateCarree()
        self.ax = self.canvas.figure.add_subplot(1, 1, 1, projection=self.projection)
        self.update_map()
        
        self.canvas.mpl_connect('button_press_event', self.on_map_click)

    def on_map_click(self, event):
        if event.inaxes is not None:
            lon, lat = self.ax.transData.inverted().transform((event.x, event.y))
            print(f"Clicked on coordinates: {lat:.2f}, {lon:.2f}")
            print(self.get_location_name(lat,lon))

    def get_location_name(self, latitude, longitude):
        geolocator = Nominatim(user_agent="WorldMapApp")
        location = geolocator.reverse((latitude, longitude), exactly_one=True)
        if location:
            return location.address
        else:
            return "Unknown"
        
    def update_map(self):
        self.ax.clear()
        self.ax.set_global()
        self.ax.stock_img()
        self.ax.add_feature(cfeature.BORDERS, linestyle=':')
        self.ax.coastlines()
        self.ax.set_extent([-180 * self.zoom_level + self.longitude_shift, 180 * self.zoom_level + self.longitude_shift,
                            -90 * self.zoom_level + self.latitude_shift, 90 * self.zoom_level + self.latitude_shift],
                           crs=ccrs.PlateCarree())
        self.canvas.draw()

    def zoom_in(self):
        self.zoom_level *= 0.8
        self.update_map()

    def zoom_out(self):
        self.zoom_level *= 1.25
        self.update_map()

    def move_up(self):
        self.latitude_shift += 5.0
        self.update_map()

    def move_down(self):
        self.latitude_shift -= 5.0
        self.update_map()

    def move_left(self):
        self.longitude_shift -= 5.0
        self.update_map()

    def move_right(self):
        self.longitude_shift += 5.0
        self.update_map()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WorldMapApp()
    window.show()
    sys.exit(app.exec_())
