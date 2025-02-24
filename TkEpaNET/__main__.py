import tkinter as tk
from tkinter import filedialog, messagebox
import os
from epyt import epanet
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class EPANETGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("EPANET Simple GUI")
        self.root.geometry("800x600")
        
        # File selection button
        self.load_button = tk.Button(root, text="Load .inp File", command=self.load_file)
        self.load_button.pack(pady=5)
        
        # Run simulation button
        self.run_button = tk.Button(root, text="Run Simulation", command=self.run_simulation, state=tk.DISABLED)
        self.run_button.pack(pady=5)
        
        # Output label
        self.output_label = tk.Label(root, text="No file loaded.")
        self.output_label.pack(pady=5)
        
        # Matplotlib Figure for Network Visualization
        self.figure, self.ax = plt.subplots(figsize=(6, 4))
        self.canvas = FigureCanvasTkAgg(self.figure, master=root)
        self.canvas.get_tk_widget().pack()
        
        self.file_path = None
        self.network = None
    
    def load_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("EPANET Input Files", "*.inp")])
        if file_path:
            self.file_path = file_path
            self.output_label.config(text=f"Loaded: {os.path.basename(file_path)}")
            self.run_button.config(state=tk.NORMAL)
            self.display_network()
    
    def run_simulation(self):
        if not self.file_path:
            messagebox.showerror("Error", "No file selected!")
            return
        
        try:
            self.network = epanet(self.file_path)
            self.network.solveH()  # Run hydraulic simulation
            messagebox.showinfo("Success", "Simulation completed!")
        except Exception as e:
            messagebox.showerror("Error", f"EPANET Error: {e}")
    
    def display_network(self):
        if not self.file_path:
            return
        
        try:
            self.network = epanet(self.file_path)
            self.network.plot()
        except Exception as e:
            messagebox.showerror("Error", f"Visualization Error: {e}")
        
# Run GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = EPANETGUI(root)
    root.mainloop()
