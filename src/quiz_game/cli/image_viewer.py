from pathlib import Path
from PIL import Image, ImageTk
import tkinter as tk
from utils.paths import PLACEHOLDER_IMAGE_PATH

class ImageViewer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Geography Quiz")

        self.label = tk.Label(self.root)
        self.label.pack()
    
    def show(self, image_path: str):
        if (image_path is None) or (not Path(image_path).exists()):
            image_path = PLACEHOLDER_IMAGE_PATH

        image = Image.open(image_path)
        image.thumbnail((800, 800))
        self.photo = ImageTk.PhotoImage(image)
        self.label.configure(image=self.photo) 
            
        # keep window responsive 
        self.root.update() 
            
    def hide(self):
        self.label.configure(image="")

        self.photo = None

        self.root.update_idletasks()
        self.root.update()

    def close(self):
        self.root.destroy()

    