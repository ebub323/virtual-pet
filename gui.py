import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from pet import VirtualPet

TICK_INTERVAL_MS = 3000   # how often the pet automatically updates (3 seconds)


class VirtualPetApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Virtual Pet Simulator")
        self.root.geometry("900x720")
        self.root.configure(bg="#0d1021")

        # Create the pet object (logic)
        self.pet = VirtualPet("Virtual Pet")

        # This stores the ID of the scheduled tick so we can cancel it
        self.after_id = None

        # Image references (prevent garbage collection)
        self.bg_img = None
        self.pet_img = None
        self.feed_img = None
        self.play_img = None
        self.rest_img = None

        # Progress bars for hunger/happiness/energy
        self.bars = {}

        # Store last 3 events to display
        self.event_history = []

        # Build GUI
        self._build_gui()

        # Set bar values
        self._update_bars()

        # Start automatic ticking loop
        self._start_game_loop()

    
    # BUILD THE GUI
    
    def _build_gui(self):
        tk.Label(
            self.root,
            text="VIRTUAL PET SIMULATOR",
            font=("Helvetica", 24, "bold"),
            fg="#ffd500",
            bg="#0d1021"
        ).pack(pady=10)

        # Background Image
        bg = Image.open("assets/background.png").resize((750, 330))
        self.bg_img = ImageTk.PhotoImage(bg)

        bg_label = tk.Label(self.root, image=self.bg_img, relief="ridge", bd=4)
        bg_label.pack(pady=10)

        # Pet Sprite
        pet = Image.open("assets/pet.png").resize((140, 140))
        self.pet_img = ImageTk.PhotoImage(pet)

        self.pet_sprite = tk.Label(self.root, image=self.pet_img, bg="#91d885")
        self.pet_sprite.place(x=410, y=170)

        #  STATUS BARS
        bar_frame = tk.Frame(self.root, bg="#101426")
        bar_frame.pack(pady=15)

        self._setup_bar_styles()

        self._create_status_bar(bar_frame, "Hunger", "Green.Horizontal.TProgressbar", 0)
        self._create_status_bar(bar_frame, "Happiness", "Orange.Horizontal.TProgressbar", 1)
        self._create_status_bar(bar_frame, "Energy", "Blue.Horizontal.TProgressbar", 2)

        #  BUTTONS 
        button_frame = tk.Frame(self.root, bg="#0d1021")
        button_frame.pack(pady=15)

        self.feed_img = ImageTk.PhotoImage(Image.open("assets/feed_btn.png").resize((200, 90)))
        self.play_img = ImageTk.PhotoImage(Image.open("assets/play_btn.png").resize((200, 90)))
        self.rest_img = ImageTk.PhotoImage(Image.open("assets/rest_btn.png").resize((200, 90)))

        self.btn_feed = tk.Button(button_frame, image=self.feed_img, borderwidth=0, command=self._on_feed)
        self.btn_play = tk.Button(button_frame, image=self.play_img, borderwidth=0, command=self._on_play)
        self.btn_rest = tk.Button(button_frame, image=self.rest_img, borderwidth=0, command=self._on_rest)

        self.btn_feed.grid(row=0, column=0, padx=20)
        self.btn_play.grid(row=0, column=1, padx=20)
        self.btn_rest.grid(row=0, column=2, padx=20)

        #  EVENT LOG 
        self.event_label = tk.Label(
            self.root,
            text="EVENT LOG:\nYour pet is ready!",
            font=("Helvetica", 12),
            fg="#ffd500",
            bg="#1b1e2b",
            width=70,
            height=4,
            anchor="nw",
            justify="left",
            padx=10
        )
        self.event_label.pack(pady=10)

    
    # PROGRESS BAR STYLE
    
    def _setup_bar_styles(self):
        style = ttk.Style()
        style.theme_use("default")

        style.configure("Green.Horizontal.TProgressbar", background="#23aa5b", troughcolor="#1b1e2b", thickness=25)
        style.configure("Orange.Horizontal.TProgressbar", background="#e67e22", troughcolor="#1b1e2b", thickness=25)
        style.configure("Blue.Horizontal.TProgressbar", background="#3498db", troughcolor="#1b1e2b", thickness=25)

    # CREATE ONE PROGRESS BAR
    def _create_status_bar(self, parent, label, style, row):
        tk.Label(
            parent,
            text=label + ":",
            font=("Helvetica", 12, "bold"),
            fg="#ffd500",
            bg="#101426"
        ).grid(row=row, column=0, padx=10, pady=5)

        bar = ttk.Progressbar(parent, length=420, maximum=100, style=style)
        bar.grid(row=row, column=1, padx=10, pady=5)

        self.bars[label.lower()] = bar

    # BUTTON ACTIONS

    def _on_feed(self):
        msg = self.pet.feed()
        self._process_action(msg)

    def _on_play(self):
        msg = self.pet.play()
        self._process_action(msg)

    def _on_rest(self):
        msg = self.pet.rest()
        self._process_action(msg)

    def _process_action(self, msg):
        """Runs after any user action."""
        self._update_bars()
        self._log_event(msg)

        # If the pet died after the action → handle game over
        if not self.pet.alive:
            self._game_over(msg)


    # GAME LOOP (AUTOMATIC UPDATES)

    def _start_game_loop(self):
        """Start automatic updates every 3 seconds.
        Cancel any old loop to prevent stacking (the crash you had).
        """
        if self.after_id is not None:
            try:
                self.root.after_cancel(self.after_id)
            except Exception:
                pass
            self.after_id = None

        # Start new loop
        self.after_id = self.root.after(TICK_INTERVAL_MS, self._game_tick)

    def _game_tick(self):
        """Runs automatically every few seconds."""

        # If pet is dead, stop all ticking entirely
        if not self.pet.alive:
            if self.after_id is not None:
                try:
                    self.root.after_cancel(self.after_id)
                except Exception:
                    pass
                self.after_id = None
            return

        msg = self.pet.tick()
        self._update_bars()

        # If tick produced a message (random event or game-over)
        if msg:
            self._log_event(msg)
            if not self.pet.alive:
                self._game_over(msg)
                return

        # Schedule next tick
        self.after_id = self.root.after(TICK_INTERVAL_MS, self._game_tick)

    
    # UPDATE GUI ELEMENTS
    
    def _update_bars(self):
        stats = self.pet.get_stats()
        self.bars["hunger"].config(value=stats["hunger"])
        self.bars["happiness"].config(value=stats["happiness"])
        self.bars["energy"].config(value=stats["energy"])

    def _log_event(self, msg):
        if not msg:
            return

        self.event_history.insert(0, msg)
        self.event_history = self.event_history[:3]  # keep only last 3

        self.event_label.config(text="EVENT LOG:\n" + "\n".join(self.event_history))

    
    # GAME OVER HANDLING
    
    def _game_over(self, reason):
        """Stop everything and show Game Over popup."""

        # STOP the scheduled automatic updates
        if self.after_id is not None:
            try:
                self.root.after_cancel(self.after_id)
            except Exception:
                pass
            self.after_id = None

        # Disable buttons
        self.btn_feed.config(state="disabled")
        self.btn_play.config(state="disabled")
        self.btn_rest.config(state="disabled")

        messagebox.showinfo("Game Over", reason)

        # Ask to restart
        if messagebox.askyesno("Restart", "Start a new pet?"):
            self._restart_game()

    def _restart_game(self):
        """Reset everything cleanly without leaving old timers running."""

        # Ensure no old timer exists
        if self.after_id is not None:
            try:
                self.root.after_cancel(self.after_id)
            except Exception:
                pass
            self.after_id = None

        # Re-create the pet
        self.pet = VirtualPet("Virtual Pet")
        self.event_history.clear()

        # Re-enable buttons
        self.btn_feed.config(state="normal")
        self.btn_play.config(state="normal")
        self.btn_rest.config(state="normal")

        # Reset bars + log
        self._update_bars()
        self._log_event("New pet created! Take care of it.")

        # Start a fresh timer safely
        self._start_game_loop()
