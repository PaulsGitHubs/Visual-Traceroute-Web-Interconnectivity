import os
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, LineString
import IP2Location
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget, QFileDialog, QPushButton, QInputDialog
from PyQt5.QtCore import pyqtSignal
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import ipaddress
from scapy.all import rdpcap
from scapy.layers.inet import IP
from scapy.error import Scapy_Exception

class MyDynamicMplCanvas(FigureCanvas):
    def __init__(self, parent=None, lat=0, lon=0, *args, **kwargs):
        fig = Figure(figsize=(10, 10))
        self.axes = fig.add_subplot(111)
        self.parent = parent  # reference to parent to use parent's methods
        self.ip2location_path = None
        self.packets_dir = None

        self.user_loc = (lat, lon)  # User location

        FigureCanvas.__init__(self, fig)
        self.setParent(None)

    def set_user_location(self, lat, lon):
        self.user_loc = (lat, lon)
        if self.ip2location_path is None or self.packets_dir is None:
            self.plot(None, None)  # replot with updated location
        elif self.ip2location_path and self.packets_dir:
            self.plot(self.ip2location_path, self.packets_dir)  # replot with updated location


    def get_user_location(self):
        return self.user_loc

    def get_location(self, database, ip):
        ip_int = int(ipaddress.IPv4Address(ip))

        # check if the IP address is private
        if ipaddress.ip_address(ip).is_private:
            return self.get_user_location()  # Return user location if IP is private
 
        if isinstance(database, pd.DataFrame):
            loc = database[(database['ip_from'].apply(int) <= ip_int) & (database['ip_to'].apply(int) >= ip_int)]
            if not loc.empty:
                return loc.iloc[0]['latitude'], loc.iloc[0]['longitude']
        else:  # IP2Location database
            loc = database.get_all(ip)
            if loc:
                return loc.latitude, loc.longitude
        return self.get_user_location()  # Return user location if IP location not found


    def get_pcap_data(self, filepath):
        try:
            packets = rdpcap(filepath)
        except Scapy_Exception as e:
            print(f"Warning: Error reading file {filepath}. Message: {str(e)}")
            return pd.DataFrame()
        data = []
        for packet in packets:
            if IP in packet:
                try:
                    src_ip = packet[IP].src
                    dst_ip = packet[IP].dst
                    data.append({'Source IP': src_ip, 'Destination IP': dst_ip})
                except:
                    continue
        return pd.DataFrame(data)
        
    # New method for loading CSV data
    def get_csv_data(self, filepath):
        try:
            df = pd.read_csv(filepath)
        except Exception as e:
            print(f"Warning: Error reading file {filepath}. Message: {str(e)}")
            return pd.DataFrame()
        data = []
        for _, row in df.iterrows():
            try:
                src_ip = row['Source IP']
                dst_ip = row['Destination IP']
                data.append({'Source IP': src_ip, 'Destination IP': dst_ip})
            except:
                continue
        return pd.DataFrame(data)
    def plot_label(self, x, y, label):
        try:
            x = float(x)
            y = float(y)
            self.axes.text(x, y, label, fontsize=8, ha='right')
        except Exception as e:
            print(f"Warning: Could not plot label '{label}' at ({x},{y}). Error: {str(e)}")
            
    def plot(self, ip2location_file, packets_dir):
        self.axes.clear()
        if ip2location_file is None or packets_dir is None:
            self.axes.figure.canvas.draw()
            return
        if ip2location_file.endswith('.BIN') or ip2location_file.endswith('.bin'):
            database = IP2Location.IP2Location(ip2location_file)
        else:  # assume it's CSV
            column_names = ['ip_from', 'ip_to', 'country_code', 'country_name', 'region_name', 'city_name', 'latitude',
                            'longitude', 'zip_code', 'time_zone']
            database = pd.read_csv(ip2location_file, delimiter=",", names=column_names, index_col=False)
        
        #this one loads faster
        #world = gpd.read_file('https://www.naturalearthdata.com/http//www.naturalearthdata.com/download/110m/cultural/ne_110m_admin_0_countries.zip')
        world = gpd.read_file('https://www.naturalearthdata.com/http//www.naturalearthdata.com/download/10m/cultural/ne_10m_admin_0_countries.zip')

        world.plot(ax=self.axes, color='white', edgecolor='black')

        for filename in os.listdir(packets_dir):
            if filename.endswith(".pcap"):
                filepath = os.path.join(packets_dir, filename)
                df = self.get_pcap_data(filepath)
            elif filename.endswith(".csv"):
                filepath = os.path.join(packets_dir, filename)
                df = self.get_csv_data(filepath)
            else:
                continue

            for _, row in df.iterrows():
                src_ip = row['Source IP']
                dst_ip = row['Destination IP']

                src_loc = self.get_location(database, src_ip)
                dst_loc = self.get_location(database, dst_ip)

                if src_loc[0] is not None and dst_loc[0] is not None:
                    src_point = Point(src_loc[1], src_loc[0])  # lon, lat
                    dst_point = Point(dst_loc[1], dst_loc[0])

                    line = LineString([src_point, dst_point])
                    self.axes.plot(*line.xy, color='green', linewidth=0.5)  # line from source to destination

                    self.axes.plot(*src_point.xy, color='red', markersize=5)  # source point
                    self.plot_label(src_loc[1], src_loc[0], src_ip)

                    self.axes.plot(*dst_point.xy, color='blue', markersize=5)  # destination point
                    self.plot_label(float(dst_loc[1]), float(dst_loc[0]), dst_ip)

        self.axes.figure.canvas.draw()


class ApplicationWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.canvas = MyDynamicMplCanvas(self)

        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

        self.button_set_location = QPushButton("Set My Location", self)
        self.button_set_location.clicked.connect(self.set_location)
        layout.addWidget(self.button_set_location)
        
        self.button_select_files = QPushButton("Select IPLocation and PCAP or CSV Directory", self)  # Rename button
        self.button_select_files.clicked.connect(self.select_files)
        layout.addWidget(self.button_select_files)

        # load last paths
        self.ip2location_path, self.packets_path = self.load_last_paths()

    def select_files(self):
        ip2location_file, _ = QFileDialog.getOpenFileName(self, 'Open IP2Location file', self.ip2location_path)
        packets_dir = QFileDialog.getExistingDirectory(self, 'Open PCAP or CSV Directory', self.packets_path)  # Change here
        if ip2location_file and packets_dir:
            self.canvas.plot(ip2location_file, packets_dir)
            self.save_last_paths(ip2location_file, packets_dir)

    def set_location(self):
        lat, ok1 = QInputDialog.getDouble(self, 'Set Latitude', 'Latitude:')
        lon, ok2 = QInputDialog.getDouble(self, 'Set Longitude', 'Longitude:')
        if ok1 and ok2:
            self.canvas.set_user_location(lat, lon)
            self.canvas.plot(self.ip2location_path, self.packets_path)  # refresh plot with new user location


    def load_last_paths(self):
        if os.path.exists('last_paths.txt'):
            with open('last_paths.txt', 'r') as file:
                lines = file.readlines()
                return lines[0].strip(), lines[1].strip()
        else:
            return "", ""

    def save_last_paths(self, ip2location_path, packets_path):
        with open('last_paths.txt', 'w') as file:
            file.write(f"{ip2location_path}\n{packets_path}")


if __name__ == "__main__":
    app = QApplication([])

    window = ApplicationWindow()
    window.show()

    app.exec_()
