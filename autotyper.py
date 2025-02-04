import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import time
import random
import keyboard
import pyautogui
import pyperclip

# -----------------------------
# Global Variables & Settings
# -----------------------------
typing_in_progress = False
stop_requested = False
hotkey_id = None

# Default settings (can be modified via the GUI)
settings = {
    "base_delay": 0.1,  # Base delay (seconds) between keystrokes.
    "random_delay": 0.05,  # Random variation (seconds) added/subtracted.
    "start_delay": 3,  # Delay (seconds) before auto-typing starts.
    "hotkey": "f2"  # Global hotkey to start/stop typing.
}


# -----------------------------
# GUI Update Helper
# -----------------------------
def update_status(msg):
    """Update the status label in a thread-safe manner."""
    status_label.after(0, lambda: status_label.config(text=f"Status: {msg}"))


# -----------------------------
# Auto-Typing Functions
# -----------------------------
def human_like_type(text):
    """Types out text character by character with human-like delays."""
    global stop_requested, typing_in_progress
    for char in text:
        if stop_requested:
            update_status("Typing stopped by user.")
            break
        pyautogui.write(char)
        # Calculate a slightly randomized delay for each keystroke.
        delay = settings["base_delay"] + random.uniform(-settings["random_delay"], settings["random_delay"])
        time.sleep(max(delay, 0))
    typing_in_progress = False
    stop_requested = False
    update_status("Typing completed.")


def start_typing():
    """
    Waits for the specified start delay so you can focus the target window.
    Retrieves text either from the text box (if not empty) or from the clipboard,
    then begins typing.
    """
    global typing_in_progress, stop_requested
    typing_in_progress = True
    update_status(f"Typing will start in {settings['start_delay']} seconds. Focus the target window now.")

    # Countdown before starting typing, with the possibility of cancellation.
    start_time = time.time()
    while time.time() - start_time < settings["start_delay"]:
        if stop_requested:
            update_status("Typing canceled before start.")
            typing_in_progress = False
            stop_requested = False
            return
        time.sleep(0.1)

    # Determine text: if the text box is empty, use the clipboard.
    text = text_box.get("1.0", tk.END).strip()
    if not text:
        text = pyperclip.paste()
        if not text:
            update_status("No text found in text box or clipboard.")
            typing_in_progress = False
            return

    update_status("Typing started.")
    human_like_type(text)


def on_hotkey():
    """
    Callback function for the hotkey.
    - If typing is in progress, it stops the typing.
    - Otherwise, it starts the typing process in a new thread.
    """
    global typing_in_progress, stop_requested
    if typing_in_progress:
        update_status("Stop requested. Stopping typing...")
        stop_requested = True
    else:
        threading.Thread(target=start_typing, daemon=True).start()


# -----------------------------
# GUI Functions
# -----------------------------
def apply_settings():
    """
    Reads the current values from the GUI fields, updates the settings,
    and registers the global hotkey.
    """
    global settings, hotkey_id
    try:
        base_delay_val = float(base_delay_entry.get())
        random_delay_val = float(random_delay_entry.get())
        start_delay_val = float(start_delay_entry.get())
        hotkey_val = hotkey_entry.get().strip()
        if not hotkey_val:
            messagebox.showerror("Error", "Hotkey cannot be empty.")
            return
        settings["base_delay"] = base_delay_val
        settings["random_delay"] = random_delay_val
        settings["start_delay"] = start_delay_val
        settings["hotkey"] = hotkey_val
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numeric values for the delays.")
        return

    # Remove the previous hotkey registration if it exists.
    if hotkey_id is not None:
        keyboard.remove_hotkey(hotkey_id)

    # Register the new hotkey.
    hotkey_id = keyboard.add_hotkey(settings["hotkey"], on_hotkey)
    update_status(f"Hotkey '{settings['hotkey']}' registered. Press it to start/stop typing.")
    messagebox.showinfo("Settings Applied", "Settings have been updated and hotkey registered.")


# -----------------------------
# Build the GUI
# -----------------------------
root = tk.Tk()
root.title("Auto Typer")

# Main frame
frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# --- Text Input Section ---
text_label = ttk.Label(frame, text="Text to type (if empty, clipboard is used):")
text_label.grid(row=0, column=0, sticky=tk.W)
text_box = scrolledtext.ScrolledText(frame, width=50, height=10)
text_box.grid(row=1, column=0, columnspan=2, pady=5)

# --- Speed Settings ---
base_delay_label = ttk.Label(frame, text="Typing Speed (base delay in seconds):")
base_delay_label.grid(row=2, column=0, sticky=tk.W)
base_delay_entry = ttk.Entry(frame)
base_delay_entry.grid(row=2, column=1, sticky=tk.W)
base_delay_entry.insert(0, str(settings["base_delay"]))

random_delay_label = ttk.Label(frame, text="Random Delay Variation (in seconds):")
random_delay_label.grid(row=3, column=0, sticky=tk.W)
random_delay_entry = ttk.Entry(frame)
random_delay_entry.grid(row=3, column=1, sticky=tk.W)
random_delay_entry.insert(0, str(settings["random_delay"]))

start_delay_label = ttk.Label(frame, text="Start Delay (seconds before typing):")
start_delay_label.grid(row=4, column=0, sticky=tk.W)
start_delay_entry = ttk.Entry(frame)
start_delay_entry.grid(row=4, column=1, sticky=tk.W)
start_delay_entry.insert(0, str(settings["start_delay"]))

# --- Hotkey Setting ---
hotkey_label = ttk.Label(frame, text="Hotkey (global, e.g., f2):")
hotkey_label.grid(row=5, column=0, sticky=tk.W)
hotkey_entry = ttk.Entry(frame)
hotkey_entry.grid(row=5, column=1, sticky=tk.W)
hotkey_entry.insert(0, settings["hotkey"])

# --- Apply Settings Button ---
apply_button = ttk.Button(frame, text="Apply Settings & Register Hotkey", command=apply_settings)
apply_button.grid(row=6, column=0, columnspan=2, pady=10)

# --- Status Label ---
status_label = ttk.Label(frame, text="Status: Waiting for settings...", relief="sunken", anchor="w")
status_label.grid(row=7, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)

# Allow the GUI to resize properly.
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
frame.columnconfigure(0, weight=1)
frame.columnconfigure(1, weight=1)

# -----------------------------
# Start the GUI Loop
# -----------------------------
root.mainloop()
