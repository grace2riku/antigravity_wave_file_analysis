import customtkinter as ctk
from tkinter import filedialog, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

from analyzer import WaveAnalyzer

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class WaveAnalyzerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Wave File Analyzer")
        self.geometry("1000x700")
        self.minsize(800, 600)

        self.analyzer = None
        
        # Grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Header Frame
        self.header_frame = ctk.CTkFrame(self)
        self.header_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        
        self.open_button = ctk.CTkButton(self.header_frame, text="Open .wav File", command=self.open_file)
        self.open_button.pack(side="left", padx=10, pady=10)
        
        self.file_label = ctk.CTkLabel(self.header_frame, text="No file selected")
        self.file_label.pack(side="left", padx=10, pady=10)

        # Main Content Frame
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        self.main_frame.grid_columnconfigure(1, weight=3)
        self.main_frame.grid_rowconfigure(0, weight=1)

        # Sidebar for metadata
        self.sidebar_frame = ctk.CTkFrame(self.main_frame, width=250)
        self.sidebar_frame.grid(row=0, column=0, sticky="ns", padx=10, pady=10)
        
        self.metadata_title = ctk.CTkLabel(self.sidebar_frame, text="Metadata", font=ctk.CTkFont(size=16, weight="bold"))
        self.metadata_title.pack(pady=10)
        
        self.metadata_textbox = ctk.CTkTextbox(self.sidebar_frame, width=230, height=200)
        self.metadata_textbox.pack(padx=10, pady=10, fill="both", expand=True)
        self.metadata_textbox.insert("0.0", "Open a file to see metadata...")
        self.metadata_textbox.configure(state="disabled")

        # Plot Area
        self.plot_frame = ctk.CTkFrame(self.main_frame)
        self.plot_frame.grid(row=0, column=1, sticky="nsew", padx=(0, 10), pady=10)
        
        self.figure, (self.ax1, self.ax2) = plt.subplots(2, 1, figsize=(6, 8))
        self.figure.tight_layout(pad=3.0)
        
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.plot_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def open_file(self):
        filepath = filedialog.askopenfilename(
            title="Select a Wave File",
            filetypes=[("Wave files", "*.wav"), ("All files", "*.*")]
        )
        if filepath:
            self.file_label.configure(text=filepath)
            self.analyze_file(filepath)

    def analyze_file(self, filepath):
        # Update UI to show loading
        self.file_label.configure(text=f"Loading: {filepath}")
        self.update_idletasks()
        
        try:
            self.analyzer = WaveAnalyzer(filepath)
            self.update_metadata()
            self.update_plots()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open or analyze file:\n{e}")

    def update_metadata(self):
        if not self.analyzer:
            return
            
        self.metadata_textbox.configure(state="normal")
        self.metadata_textbox.delete("0.0", "end")
        self.metadata_textbox.insert("0.0", self.analyzer.get_metadata_string())
        self.metadata_textbox.configure(state="disabled")

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

if __name__ == "__main__":
    app = WaveAnalyzerApp()
    app.mainloop()
