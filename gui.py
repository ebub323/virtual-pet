# gui.py
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from pet import VirtualPet

TICK_INTERVAL_MS = 3000   # 3 seconds between updates


class VirtualPetApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Virtual Pet Simulator")
        self.root.geometry("900x720")
        self.root.configure(bg="#0d1021")

        self.pet = VirtualPet("Virtual Pet")

        # Photo image references must be stored to avoid garbage collection
        self.bg_img = None
        self.pet_img = None
        self.feed_img = None
        self.play_img = None
        self.rest_img = None

        self.bars = {}
        self.event_history = []

        # store the id returned from `after` so we can cancel it on restart/exit
        self.after_id = None

        self._build_gui()
        self._update_bars()
        self._start_game_loop()

    # ---------------- GUI BUILDING ----------------
    def _build_gui(self):
        # Title
        title_label = tk.Label(
            self.root, text="VIRTUAL PET SIMULATOR",
            font=("Helvetica", 24, "bold"),
            fg="#ffd500", bg="#0d1021"
        )
        title_label.pack(pady=10)

        # Background
        bg = Image.open("assets/background.png").resize((750, 330))
        self.bg_img = ImageTk.PhotoImage(bg)
        pet_area = tk.Label(self.root, image=self.bg_img, bd=4, relief="ridge")
        pet_area.pack(pady=10)

        # Pet sprite
        pet = Image.open("assets/pet.png").resize((140, 140))
        self.pet_img = ImageTk.PhotoImage(pet)
        self.pet_sprite = tk.Label(self.root, image=self.pet_img, bg="#91d885")
        self.pet_sprite.place(x=410, y=170)

        # Status bars
        bar_frame = tk.Frame(self.root, bg="#101426")
        bar_frame.pack(pady=15)
        self._setup_bar_styles()

        self._create_status_bar(bar_frame, "Hunger", "Green.Horizontal.TProgressbar", 0)
        self._create_status_bar(bar_frame, "Happiness", "Orange.Horizontal.TProgressbar", 1)
        self._create_status_bar(bar_frame, "Energy", "Blue.Horizontal.TProgressbar", 2)

        # Buttons
        button_frame = tk.Frame(self.root, bg="#0d1021")
        button_frame.pack(pady=15)

        self.feed_img = ImageTk.PhotoImage(Image.open("assets/feed_btn.png").resize((200, 90)))
        self.play_img = ImageTk.PhotoImage(Image.open("assets/play_btn.png").resize((200, 90)))
        self.rest_img = ImageTk.PhotoImage(Image.open("assets/rest_btn.png").resize((200, 90)))

        # Keep references to action buttons so we can enable/disable on reset
        self.action_buttons = []
        btn_feed = tk.Button(button_frame, image=self.feed_img, borderwidth=0, command=self._on_feed)
        btn_play = tk.Button(button_frame, image=self.play_img, borderwidth=0, command=self._on_play)
        btn_rest = tk.Button(button_frame, image=self.rest_img, borderwidth=0, command=self._on_rest)
        btn_feed.grid(row=0, column=0, padx=20)
        btn_play.grid(row=0, column=1, padx=20)
        btn_rest.grid(row=0, column=2, padx=20)
        self.action_buttons.extend([btn_feed, btn_play, btn_rest])

        # Event Log
        self.event_label = tk.Label(
            self.root, text="EVENT LOG:\nYour pet is ready!",
            font=("Helvetica", 12),
            fg="#ffd500", bg="#1b1e2b",
            width=70, height=4, anchor="nw", justify="left", padx=10
        )
        self.event_label.pack(pady=10)

    # Progress bar styling
    def _setup_bar_styles(self):
        style = ttk.Style()
        style.theme_use("default")

        style.configure("Green.Horizontal.TProgressbar", background="#2ecc71", troughcolor="#1b1e2b", thickness=25)
        style.configure("Orange.Horizontal.TProgressbar", background="#e67e22", troughcolor="#1b1e2b", thickness=25)
        style.configure("Blue.Horizontal.TProgressbar", background="#3498db", troughcolor="#1b1e2b", thickness=25)

    def _create_status_bar(self, parent, label, style, row):
        tk.Label(parent, text=label + ":", font=("Helvetica", 12, "bold"), fg="#ffd500", bg="#101426").grid(row=row, column=0, padx=10, pady=5)
        bar = ttk.Progressbar(parent, orient="horizontal", length=420, maximum=100, style=style)
        bar.grid(row=row, column=1, padx=10, pady=5)
        self.bars[label.lower()] = bar

    # ---------------- BUTTON ACTIONS ----------------
    def _on_feed(self):
        msg = self.pet.feed()
        self._after_action(msg)

    def _on_play(self):
        msg = self.pet.play()
        self._after_action(msg)

    def _on_rest(self):
        msg = self.pet.rest()
        self._after_action(msg)

    def _after_action(self, msg):
        self._update_bars()
        self._log_event(msg)
        if not self.pet.alive:
            self._game_over(msg)

    # ---------------- GAME LOOP ----------------
    def _start_game_loop(self):
        # store after id so it can be cancelled when restarting/quitting
        self.after_id = self.root.after(TICK_INTERVAL_MS, self._game_tick)

    def _game_tick(self):
        if not self.pet.alive:
            return

        msg = self.pet.tick()
        self._update_bars()

        if msg:
            self._log_event(msg)
            if not self.pet.alive:
                self._game_over(msg)
                return

        # schedule next tick and store id
        self.after_id = self.root.after(TICK_INTERVAL_MS, self._game_tick)

    # ---------------- UPDATES ----------------
    def _update_bars(self):
        stats = self.pet.get_stats()
        for key, bar in self.bars.items():
            bar.config(value=stats[key])

    def _log_event(self, message):
        if not message:
            return
        self.event_history.insert(0, message)
        self.event_history = self.event_history[:3]
        self.event_label.config(text="EVENT LOG:\n" + "\n".join(self.event_history))

    # ---------------- GAME OVER ----------------
    def _game_over(self, reason):
        # Cancel the scheduled tick if present to avoid duplicate callbacks
        try:
            if self.after_id is not None:
                self.root.after_cancel(self.after_id)
        except Exception:
            pass
        self.after_id = None

        messagebox.showinfo("Game Over", reason)

        if messagebox.askyesno("Restart", "Start a new pet?"):
            # Perform a clean reset without reconstructing widgets
            self._reset()
        else:
            # Disable button widgets so no further actions are possible
            for btn in getattr(self, "action_buttons", []):
                try:
                    btn.config(state="disabled")
                except Exception:
                    continue

    def _reset(self):
        """Reset the game state without rebuilding the entire GUI.

        Cancels any pending callbacks, creates a fresh `VirtualPet`, clears the
        event history, updates the status bars and event log, re-enables action
        buttons, and restarts the game loop.
        """
        # Cancel any pending after callback
        try:
            if self.after_id is not None:
                self.root.after_cancel(self.after_id)
        except Exception:
            pass
        self.after_id = None

        # Reset game state
        self.pet = VirtualPet(self.pet.name)
        self.event_history = []
        self.event_label.config(text="EVENT LOG:\nYour pet is ready!")
        self._update_bars()

        # Re-enable action buttons
        for btn in getattr(self, "action_buttons", []):
            try:
                btn.config(state="normal")
            except Exception:
                continue

        # Restart the loop
        self._start_game_loop()
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from pet import VirtualPet

TICK_INTERVAL_MS = 3000   # 3 seconds between updates


class VirtualPetApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Virtual Pet Simulator")
        self.root.geometry("900x720")
        self.root.configure(bg="#0d1021")

        self.pet = VirtualPet("Virtual Pet")

        # Photo image references must be stored to avoid garbage collection
        self.bg_img = None
        self.pet_img = None
        self.feed_img = None
        self.play_img = None
        self.rest_img = None

        self.bars = {}
        self.event_history = []

        self._build_gui()
        self._update_bars()
        self._start_game_loop()

    # ---------------- GUI BUILDING ----------------
    def _build_gui(self):
        # Title
        title_label = tk.Label(
            self.root, text="VIRTUAL PET SIMULATOR",
            font=("Helvetica", 24, "bold"),
            fg="#ffd500", bg="#0d1021"
        )
        title_label.pack(pady=10)

        # Background
        bg = Image.open("assets/background.png").resize((750, 330))
        self.bg_img = ImageTk.PhotoImage(bg)
        pet_area = tk.Label(self.root, image=self.bg_img, bd=4, relief="ridge")
        pet_area.pack(pady=10)

        # Pet sprite
        pet = Image.open("assets/pet.png").resize((140, 140))
        self.pet_img = ImageTk.PhotoImage(pet)
        self.pet_sprite = tk.Label(self.root, image=self.pet_img, bg="#91d885")
        self.pet_sprite.place(x=410, y=170)

        # Status bars
        bar_frame = tk.Frame(self.root, bg="#101426")
        bar_frame.pack(pady=15)
        self._setup_bar_styles()

        self._create_status_bar(bar_frame, "Hunger", "Green.Horizontal.TProgressbar", 0)
        self._create_status_bar(bar_frame, "Happiness", "Orange.Horizontal.TProgressbar", 1)
        self._create_status_bar(bar_frame, "Energy", "Blue.Horizontal.TProgressbar", 2)

        # Buttons
        button_frame = tk.Frame(self.root, bg="#0d1021")
        button_frame.pack(pady=15)

        self.feed_img = ImageTk.PhotoImage(Image.open("assets/feed_btn.png").resize((200, 90)))
        self.play_img = ImageTk.PhotoImage(Image.open("assets/play_btn.png").resize((200, 90)))
        self.rest_img = ImageTk.PhotoImage(Image.open("assets/rest_btn.png").resize((200, 90)))

        tk.Button(button_frame, image=self.feed_img, borderwidth=0, command=self._on_feed).grid(row=0, column=0, padx=20)
        tk.Button(button_frame, image=self.play_img, borderwidth=0, command=self._on_play).grid(row=0, column=1, padx=20)
        tk.Button(button_frame, image=self.rest_img, borderwidth=0, command=self._on_rest).grid(row=0, column=2, padx=20)

        # Event Log
        self.event_label = tk.Label(
            self.root, text="EVENT LOG:\nYour pet is ready!",
            font=("Helvetica", 12),
            fg="#ffd500", bg="#1b1e2b",
            width=70, height=4, anchor="nw", justify="left", padx=10
        )
        self.event_label.pack(pady=10)

    # Progress bar styling
    def _setup_bar_styles(self):
        style = ttk.Style()
        style.theme_use("default")

        style.configure("Green.Horizontal.TProgressbar", background="#2ecc71", troughcolor="#1b1e2b", thickness=25)
        style.configure("Orange.Horizontal.TProgressbar", background="#e67e22", troughcolor="#1b1e2b", thickness=25)
        style.configure("Blue.Horizontal.TProgressbar", background="#3498db", troughcolor="#1b1e2b", thickness=25)

    def _create_status_bar(self, parent, label, style, row):
        tk.Label(parent, text=label + ":", font=("Helvetica", 12, "bold"), fg="#ffd500", bg="#101426").grid(row=row, column=0, padx=10, pady=5)
        bar = ttk.Progressbar(parent, orient="horizontal", length=420, maximum=100, style=style)
        bar.grid(row=row, column=1, padx=10, pady=5)
        self.bars[label.lower()] = bar

    # ---------------- BUTTON ACTIONS ----------------
    def _on_feed(self):
        msg = self.pet.feed()
        self._after_action(msg)

    def _on_play(self):
        msg = self.pet.play()
        self._after_action(msg)

    def _on_rest(self):
        msg = self.pet.rest()
        self._after_action(msg)

    def _after_action(self, msg):
        self._update_bars()
        self._log_event(msg)
        if not self.pet.alive:
            self._game_over(msg)

    # ---------------- GAME LOOP ----------------
    def _start_game_loop(self):
        self.root.after(TICK_INTERVAL_MS, self._game_tick)

    def _game_tick(self):
        if not self.pet.alive:
            return

        msg = self.pet.tick()
        self._update_bars()

        if msg:
            self._log_event(msg)
            if not self.pet.alive:
                self._game_over(msg)
                return

        self.root.after(TICK_INTERVAL_MS, self._game_tick)

    # ---------------- UPDATES ----------------
    def _update_bars(self):
        stats = self.pet.get_stats()
        for key, bar in self.bars.items():
            bar.config(value=stats[key])

    def _log_event(self, message):
        if not message:
            return
        self.event_history.insert(0, message)
        self.event_history = self.event_history[:3]
        self.event_label.config(text="EVENT LOG:\n" + "\n".join(self.event_history))

    # ---------------- GAME OVER ----------------
    def _game_over(self, reason):
        messagebox.showinfo("Game Over", reason)

        if messagebox.askyesno("Restart", "Start a new pet?"):
            self.__init__(self.root)  # recreate the entire app
        else:
            for btn in self.root.winfo_children():
                if isinstance(btn, tk.Button):
                    btn.config(state="disabled")
