import sys
import time
import ctypes
import random
import threading
import warnings
import tkinter as tk
import pydirectinput

# Enforce clean standard console output tracking and silence deprecation warnings
sys.stderr = sys.stdout
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Disable pydirectinput's internal safe-mode delays for maximum execution speed
pydirectinput.PAUSE = 0.0
User32 = ctypes.windll.user32

# Timing configuration (9.5 minutes + 20 seconds buffer = 590 seconds total cycle time)
CYCLE_TIME = 590 

class CyberpunkBotGui:
    def __init__(self, root):
        self.root = root
        self.root.title("▼ RAGE_NET // HOTKEY_BYPASS v8.0")
        self.root.geometry("450x380")
        self.root.resizable(False, False)
        self.root.configure(bg="#0B0C10")

        # Runtime Engine Status Flags
        self.is_running = False
        self.cycle_count = 0
        self.time_left = CYCLE_TIME
        self.timer_loop_active = False 

        # Neon Matrix Shifting Laser Line Color Array
        self.rgb_colors = ["#00FFCC", "#FF0055", "#9400D3", "#00FF66", "#FFFF00"]
        self.rgb_index = 0

        # UI TOP DECORATION STRIP
        self.rgb_strip = tk.Frame(root, height=4, bg="#00FFCC")
        self.rgb_strip.pack(fill=tk.X, side=tk.TOP)

        self.header_frame = tk.Frame(root, bg="#0B0C10")
        self.header_frame.pack(fill=tk.X, pady=15)
        self.glitch_label = tk.Label(self.header_frame, text="[ R A G E _ N E T ]", font=("Courier New", 18, "bold"), bg="#0B0C10", fg="#00FFCC")
        self.glitch_label.pack()

        # HARDWARE HUD CONTROL MAIN DASHBOARD
        self.dashboard = tk.Frame(root, bg="#1F2833", bd=1, relief=tk.SOLID)
        self.dashboard.pack(padx=20, pady=5, fill=tk.BOTH, expand=True)

        self.dash_title = tk.Label(self.dashboard, text="◤ HOTKEY ENGINE CORE MONITOR ◢", font=("Arial", 8, "bold"), bg="#1F2833", fg="#45A29E")
        self.dash_title.pack(pady=4)

        self.status_frame = tk.Frame(self.dashboard, bg="#1F2833")
        self.status_frame.pack(pady=5)
        tk.Label(self.status_frame, text="SYS OPERATIONAL STATE:", font=("Courier New", 10), bg="#1F2833", fg="#C5C6C7").pack(side=tk.LEFT)
        self.status_val = tk.Label(self.status_frame, text="● DEACTIVATED", font=("Courier New", 10, "bold"), bg="#1F2833", fg="#FF0055")
        self.status_val.pack(side=tk.LEFT, padx=5)

        self.clock_container = tk.Frame(self.dashboard, bg="#0B0C10", bd=2, relief=tk.RIDGE)
        self.clock_container.pack(pady=10, padx=40, fill=tk.X)
        self.timer_label = tk.Label(self.clock_container, text=" 09 : 50 ", font=("Courier New", 32, "bold"), bg="#0B0C10", fg="#ffffff")
        self.timer_label.pack(pady=5)

        self.counter_frame = tk.Frame(self.dashboard, bg="#1F2833")
        self.counter_frame.pack(pady=5)
        self.cycle_left_bracket = tk.Label(self.counter_frame, text="[", font=("Courier New", 14), bg="#1F2833", fg="#00FFCC")
        self.cycle_left_bracket.pack(side=tk.LEFT)
        self.cycle_label = tk.Label(self.counter_frame, text="CYCLES INJECTED: 000", font=("Courier New", 11, "bold"), bg="#1F2833", fg="#C5C6C7")
        self.cycle_label.pack(side=tk.LEFT, padx=10)
        self.cycle_right_bracket = tk.Label(self.counter_frame, text="]", font=("Courier New", 14), bg="#1F2833", fg="#00FFCC")
        self.cycle_right_bracket.pack(side=tk.LEFT)

        self.dash_footer = tk.Label(self.dashboard, text="◣ INITIALIZATION READOUT OK ◢", font=("Arial", 7, "bold"), bg="#1F2833", fg="#45A29E")
        self.dash_footer.pack(side=tk.BOTTOM, pady=4)

        # INTERACTIVE OPERATION HUD INTERFACE BUTTONS
        self.controls = tk.Frame(root, bg="#0B0C10")
        self.controls.pack(pady=20)

        self.start_btn = tk.Button(self.controls, text="► INJECT PROTOCOL", font=("Courier New", 10, "bold"), bg="#0B0C10", fg="#00FFCC", activebackground="#00FFCC", activeforeground="#0B0C10", bd=2, relief=tk.SOLID, padx=15, pady=8, command=self.start_bot)
        self.start_btn.pack(side=tk.LEFT, padx=15)

        self.stop_btn = tk.Button(self.controls, text="■ TERMINATE", font=("Courier New", 10, "bold"), bg="#0B0C10", fg="#666666", activebackground="#FF0055", activeforeground="#ffffff", bd=2, relief=tk.SOLID, padx=15, pady=8, state=tk.DISABLED, command=self.stop_bot)
        self.stop_btn.pack(side=tk.LEFT, padx=15)

        # Start the RGB laser line loop right away
        self.animate_interface_colors()

    def animate_interface_colors(self):
        """Continuously loops shifting matrix cyber colors across the top bar and active widgets."""
        next_color = self.rgb_colors[self.rgb_index]
        self.rgb_strip.config(bg=next_color)
        
        if self.is_running:
            self.timer_label.config(fg=next_color)
            self.cycle_left_bracket.config(fg=next_color)
            self.cycle_right_bracket.config(fg=next_color)
        else:
            self.timer_label.config(fg="#ffffff")
            self.cycle_left_bracket.config(fg="#00FFCC")
            self.cycle_right_bracket.config(fg="#00FFCC")

        self.rgb_index = (self.rgb_index + 1) % len(self.rgb_colors)
        self.root.after(350, self.animate_interface_colors)

    def format_time(self, seconds):
        mins, secs = divmod(seconds, 60)
        return f" {mins:02d} : {secs:02d} "

    def update_timer_ui(self):
        """Visual countdown handler ticking layout assets down cleanly to zero state."""
        if self.is_running and self.time_left > 0:
            self.time_left -= 1
            self.timer_label.config(text=self.format_time(self.time_left))
            self.root.after(1000, self.update_timer_ui)
        else:
            self.timer_loop_active = False

    def trigger_taskbar_shortcut(self):
        """Simulates physical hardware press events for Windows Key + 1."""
        # 0x5B = Left Windows Key, 0x31 = '1' Key
        ctypes.windll.user32.keybd_event(0x5B, 0, 0, 0)  # Win Key Down
        ctypes.windll.user32.keybd_event(0x31, 0, 0, 0)  # 1 Key Down
        time.sleep(0.05)
        ctypes.windll.user32.keybd_event(0x31, 0, 2, 0)  # 1 Key Up
        ctypes.windll.user32.keybd_event(0x5B, 0, 2, 0)  # Win Key Up
        time.sleep(0.1)

    def start_bot(self):
        self.is_running = True
        self.time_left = CYCLE_TIME
        
        self.status_val.config(text="● ACTIVE & RUNNING", fg="#00FF66")
        self.timer_label.config(text=self.format_time(self.time_left))
        self.start_btn.config(state=tk.DISABLED, fg="#333333")
        self.stop_btn.config(state=tk.NORMAL, fg="#FF0055")
        
        # Fire off non-blocking daemon automation execution worker thread
        threading.Thread(target=self.bot_loop, daemon=True).start()
        
        # Thread safety lock configuration protects layout loop clock speeds
        if not self.timer_loop_active:
            self.timer_loop_active = True
            self.update_timer_ui()

    def stop_bot(self):
        self.is_running = False
        self.timer_loop_active = False
        self.status_val.config(text="● DEACTIVATED", fg="#FF0055")
        self.start_btn.config(state=tk.NORMAL, fg="#00FFCC")
        self.stop_btn.config(state=tk.DISABLED, fg="#666666")

    def bot_loop(self):
        movement_keys = ['w', 'a', 's', 'd']
        
        while self.is_running:
            try:
                # 1. Tap Windows + 1 shortcut combo to pull up the first taskbar pin program
                self.status_val.config(text="● OPENING APPLICATION...", fg="#FFFF00")
                self.trigger_taskbar_shortcut()
                time.sleep(1.0) # Allocation delay to ensure layout focus registration
                
                # 2. Pick a completely random step velocity index directions vector
                random_key = random.choice(movement_keys)
                self.status_val.config(text=f"● MOVING KEY: {random_key.upper()}", fg="#00FFCC")
                
                # Engage hardware level key state injection
                pydirectinput.keyDown(random_key)
                time.sleep(2.0) # <--- Holds the direction keys for exactly 2 seconds
                pydirectinput.keyUp(random_key)
                time.sleep(0.2)
                
                # 3. Tap Windows + 1 combo again to minimize back down and drop window layer context
                self.status_val.config(text="● MINIMIZING APPLICATION...", fg="#FFFF00")
                self.trigger_taskbar_shortcut()
                
                # Increment completion indexes parameters on HUD display frame
                self.cycle_count += 1
                self.cycle_label.config(text=f"CYCLES INJECTED: {self.cycle_count:03d}")
                
            except Exception as e:
                print(f"Error executing loop hotkey macro logic: {e}")

            # 4. Enforce structural countdown rest interval for exactly 9 minutes and 50 seconds
            if self.is_running:
                self.time_left = CYCLE_TIME
                self.status_val.config(text="● MONITORING: IDLE STANDBY", fg="#00FF66")
                
                # Re-engage verification loops structure parameters
                if not self.timer_loop_active:
                    self.timer_loop_active = True
                    self.update_timer_ui()

                for _ in range(CYCLE_TIME):
                    if not self.is_running:
                        break
                    time.sleep(1)

        self.status_val.config(text="● DEACTIVATED", fg="#FF0055")
        self.timer_label.config(text=" 09 : 50 ")

if __name__ == "__main__":
    try:
        app_root = tk.Tk()
        gui_app = CyberpunkBotGui(app_root)
        app_root.mainloop()
    except Exception as master_error:
        print(f"Critical execution fault error: {master_error}")
        input()
