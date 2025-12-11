import sys

try:
	from gui import VirtualPetApp
except ModuleNotFoundError as e:
	# Provide a helpful message when Pillow (PIL) is missing so the user
	# doesn't just see a ModuleNotFoundError traceback.
	if getattr(e, "name", "") == "PIL":
		print("Missing dependency: Pillow (PIL). Install with:")
		print("  python3 -m pip install --upgrade pip")
		print("  python3 -m pip install pillow")
		sys.exit(1)
	raise

import tkinter as tk


root = tk.Tk()
app = VirtualPetApp(root)
root.mainloop()
