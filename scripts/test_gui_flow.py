# test_gui_flow.py
# This script tests the GUI's game-over flow without showing modal dialogs.

import os
import sys
import tkinter as tk
import tkinter.messagebox as messagebox

# Ensure repo root is on sys.path so top-level modules can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Monkeypatch messagebox functions so they don't block tests
messagebox.showinfo = lambda *a, **k: None

from gui import VirtualPetApp

root = tk.Tk()
root.withdraw()  # hide the main window for the test

app = VirtualPetApp(root)

# Test branch: user selects "No" to restart
messagebox.askyesno = lambda *a, **k: False
app.pet.alive = False
try:
    app._game_over("Simulated game over (no restart)")
    print("OK: _game_over (no restart) executed without exception")
except Exception as e:
    print("ERROR (no restart):", type(e).__name__, e)

# Test branch: user selects "Yes" to restart
messagebox.askyesno = lambda *a, **k: True
app.pet.alive = False
try:
    app._game_over("Simulated game over (with restart)")
    # after reset, pet should be alive again and event history cleared
    alive = getattr(app.pet, "alive", None)
    empty_history = (app.event_history == [])
    print("OK: _game_over (restart) executed without exception; pet.alive=", alive, "history_empty=", empty_history)
except Exception as e:
    print("ERROR (restart):", type(e).__name__, e)

finally:
    try:
        root.destroy()
    except Exception:
        pass
