# auto-typer
An auto typer because I HATE MurGee

How to Use This Program
Clone or Download
Package this file (e.g., as autotyper.py) into your GitHub repository.

Install Dependencies
Run the following command in your terminal:

bash
Copy
pip install pyautogui keyboard pyperclip
Run the Program
Execute the program:

bash
Copy
python autotyper.py
Customize Settings via the GUI

Text Box: Paste or type the text you wish to auto-type. If left empty, the program will type text from your clipboard.
Typing Speed: Adjust the base delay and random delay variation.
Start Delay: Set how many seconds to wait before auto-typing starts (after you press the hotkey).
Hotkey: Change the global hotkey (for example, f2, f5, etc.).
Click "Apply Settings & Register Hotkey" to update the settings. A message will confirm that your hotkey is registered.
Using the Hotkey

When auto‑typing is not in progress: Press your hotkey to start. After the start delay (during which you can focus your target window), the program will begin typing the text.
While auto‑typing is in progress: Press the same hotkey again to cancel/stop the typing immediately.
