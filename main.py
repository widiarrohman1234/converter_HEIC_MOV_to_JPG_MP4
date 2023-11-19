import os
from pathlib import Path
from PIL import Image
from pillow_heif import register_heif_opener
import tkinter as tk
from tkinter import filedialog
from moviepy.editor import VideoFileClip


def convert_heic_to_jpg(heic_path, output_folder, log_text):
    register_heif_opener()

    heic_path = Path(heic_path)
    output_folder = Path(output_folder)

    if not output_folder.exists():
        output_folder.mkdir(parents=True)

    for heic_file in heic_path.glob("*.heic"):
        try:
            image = Image.open(heic_file)
            jpg_path = output_folder / (heic_file.stem + ".jpg")
            image.convert("RGB").save(jpg_path, "JPEG")
            log_text.insert(tk.END, f"Converted {heic_file} to {jpg_path}\n")
            log_text.see(tk.END)  # Auto-scroll to the end
        except Exception as e:
            log_text.insert(tk.END, f"Error converting {heic_file}: {e}\n")
            log_text.see(tk.END)

def convert_mov_to_mp4(mov_path, output_folder, log_text):
    mov_path = Path(mov_path)
    output_folder = Path(output_folder)

    if not output_folder.exists():
        output_folder.mkdir(parents=True)

    mp4_path = output_folder / (mov_path.stem + ".mp4")

    clip = VideoFileClip(str(mov_path))
    clip.write_videofile(str(mp4_path), codec="libx264", audio_codec="aac")
    log_text.insert(tk.END, f"Converted {mov_path} to {mp4_path}\n")
    log_text.see(tk.END)

def browse_mov_folder():
    folder_selected = filedialog.askdirectory()
    mov_folder_entry.delete(0, tk.END)
    mov_folder_entry.insert(0, folder_selected)

def browse_heic_folder():
    folder_selected = filedialog.askdirectory()
    heic_folder_entry.delete(0, tk.END)
    heic_folder_entry.insert(0, folder_selected)

def browse_output_folder():
    folder_selected = filedialog.askdirectory()
    output_folder_entry.delete(0, tk.END)
    output_folder_entry.insert(0, folder_selected)

def convert_button_callback():
    selected_folder = heic_folder_entry.get()
    output_folder = output_folder_entry.get()

    for file in Path(selected_folder).iterdir():
        if file.suffix.lower() == ".mov":
            convert_mov_to_mp4(file, output_folder, log_text)
        elif file.suffix.lower() == ".heic":
            convert_heic_to_jpg(file, output_folder, log_text)
    # Tambahkan pesan setelah selesai
    log_text.insert(tk.END, "Program Selesai\n")
    log_text.see(tk.END)

# Create the main Tkinter window
root = tk.Tk()
root.title("HEIC to JPG or MOV to MP4 Converter")

# Create and place GUI components
tk.Label(root, text="HEIC Folder:").grid(row=0, column=0, padx=10, pady=5)
heic_folder_entry = tk.Entry(root, width=50)
heic_folder_entry.grid(row=0, column=1, padx=10, pady=5)
tk.Button(root, text="Browse", command=browse_heic_folder).grid(row=0, column=2, padx=5, pady=5)

tk.Label(root, text="Output Folder:").grid(row=1, column=0, padx=10, pady=5)
output_folder_entry = tk.Entry(root, width=50)
output_folder_entry.grid(row=1, column=1, padx=10, pady=5)
tk.Button(root, text="Browse", command=browse_output_folder).grid(row=1, column=2, padx=5, pady=5)

convert_button = tk.Button(root, text="Convert", command=convert_button_callback)
convert_button.grid(row=2, column=1, pady=10)

# Add a Text widget for logging
log_text = tk.Text(root, height=10, width=50)
log_text.grid(row=3, column=0, columnspan=3, padx=10, pady=10)


# Start the Tkinter event loop
root.mainloop()
