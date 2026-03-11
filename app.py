import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QFileDialog, QTextEdit, QSplitter
)
from PyQt6.QtCore import Qt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np

from analyzer import WaveAnalyzer

class WaveAnalyzerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.analyzer = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Wave File Analyzer")
        self.resize(1000, 700)
        self.setMinimumSize(800, 600)

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Header Frame
        header_layout = QHBoxLayout()
        self.open_button = QPushButton("Open .wav File")
        self.open_button.clicked.connect(self.open_file)
        self.file_label = QLabel("No file selected")
        
        header_layout.addWidget(self.open_button)
        header_layout.addWidget(self.file_label)
        header_layout.addStretch()
        main_layout.addLayout(header_layout)

        # Splitter for Sidebar and Main Content
        splitter = QSplitter(Qt.Orientation.Horizontal)
        main_layout.addWidget(splitter, 1)

        # Sidebar (Metadata)
        sidebar_widget = QWidget()
        sidebar_layout = QVBoxLayout(sidebar_widget)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        
        metadata_title = QLabel("<b>Metadata</b>")
        self.metadata_textbox = QTextEdit()
        self.metadata_textbox.setReadOnly(True)
        self.metadata_textbox.setText("Open a file to see metadata...")
        
        sidebar_layout.addWidget(metadata_title)
        sidebar_layout.addWidget(self.metadata_textbox)
        
        # Plot Area
        plot_widget = QWidget()
        plot_layout = QVBoxLayout(plot_widget)
        plot_layout.setContentsMargins(0, 0, 0, 0)
        
        self.figure, (self.ax1, self.ax2) = plt.subplots(2, 1, figsize=(6, 8))
        self.figure.tight_layout(pad=3.0)
        self.canvas = FigureCanvas(self.figure)
        
        plot_layout.addWidget(self.canvas)

        # Add to splitter
        splitter.addWidget(sidebar_widget)
        splitter.addWidget(plot_widget)
        splitter.setSizes([250, 750])

    def open_file(self):
        filepath, _ = QFileDialog.getOpenFileName(
            self,
            "Select a Wave File",
            "",
            "Wave files (*.wav);;All files (*.*)"
        )
        if filepath:
            self.file_label.setText(filepath)
            self.analyze_file(filepath)

    def analyze_file(self, filepath):
        self.file_label.setText(f"Loading: {filepath}")
        QApplication.processEvents() # Force UI update
        
        try:
            self.analyzer = WaveAnalyzer(filepath)
            self.update_metadata()
            self.update_plots()
            self.file_label.setText(filepath)
        except Exception as e:
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.critical(self, "Error", f"Failed to open or analyze file:\n{e}")
            self.file_label.setText("Error loading file")

    def update_metadata(self):
        if not self.analyzer:
            return
        self.metadata_textbox.setText(self.analyzer.get_metadata_string())

    def update_plots(self):
        if not self.analyzer or self.analyzer.audio_data is None:
            return
            
        self.ax1.clear()
        self.ax2.clear()
        
        # Plot Waveform (first channel if stereo)
        time_array = self.analyzer.time_array
        audio_data = self.analyzer.audio_data
        
        if self.analyzer.metadata['n_channels'] > 1:
            plot_data = audio_data[:, 0]  # Just use Left channel for simplicity
            self.ax1.set_title("Waveform (Channel 1)")
        else:
            plot_data = audio_data
            self.ax1.set_title("Waveform")

        # Downsample for faster plotting if huge
        max_points = 500000
        if len(plot_data) > max_points:
            step = len(plot_data) // max_points
            time_plot = time_array[::step]
            data_plot = plot_data[::step]
        else:
            time_plot = time_array
            data_plot = plot_data
            
        self.ax1.plot(time_plot, data_plot, color='blue', alpha=0.7)
        self.ax1.set_xlabel("Time [s]")
        self.ax1.set_ylabel("Amplitude")
        self.ax1.grid(True)

        # Plot Spectrogram
        self.ax2.set_title("Spectrogram")
        # Ensure NFFT is valid
        nfft = 1024
        if len(plot_data) < nfft:
            nfft = max(2, len(plot_data) // 4)
            
        try:
            self.ax2.specgram(plot_data, Fs=self.analyzer.metadata['framerate'], NFFT=nfft, noverlap=nfft//2, cmap='viridis')
        except Exception as e:
            print(f"Error drawing spectrogram: {e}")
            self.ax2.text(0.5, 0.5, "Could not compute spectrogram", ha='center', va='center')
            
        self.ax2.set_xlabel("Time [s]")
        self.ax2.set_ylabel("Frequency [Hz]")
        
        self.figure.tight_layout()
        self.canvas.draw()

def main():
    app = QApplication(sys.argv)
    
    # Optional: Set a clean style
    app.setStyle("Fusion")
    
    window = WaveAnalyzerApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
