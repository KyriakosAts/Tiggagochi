import json
import os
class Tigga:
    CONFIG_FILE = "config.json"

    def __init__(self):
        self.name = "Tigga"
        self.hunger = 50
        self.happiness = 50
        self.energy = 50
        self.status_msg = "Meow! I'm Tigga."
        self.current_state = "idle" 
        self.action_timer = 0
        self.load_state()

    def load_state(self):
        if os.path.exists(self.CONFIG_FILE):
            try:
                with open(self.CONFIG_FILE, "r") as f:
                    data = json.load(f)
                    self.hunger = data.get("hunger", 50)
                    self.happiness = data.get("happiness", 50)
                    self.energy = data.get("energy", 50)
            except (json.JSONDecodeError, IOError):
                pass
        self._update_state()

    def save_state(self):
        data = {"hunger": self.hunger, "happiness": self.happiness, "energy": self.energy}
        with open(self.CONFIG_FILE, "w") as f:
            json.dump(data, f, indent=4)

    def _update_state(self):
        if self.action_timer > 0:
            return # Keep the action animation active
        
        if self.energy < 20: self.current_state = "tired"
        elif self.hunger > 80: self.current_state = "hungry"
        elif self.happiness > 80: self.current_state = "happy"
        else: self.current_state = "idle"

    def _clamp(self, value):
        return max(0, min(100, value))

    def set_action(self, state: str, msg: str, duration: int = 20):
        self.current_state = state
        self.status_msg = msg
        self.action_timer = duration

    def tick_action_timer(self, delta: float = 1.0):
        if self.action_timer <= 0:
            return

        self.action_timer = max(0, self.action_timer - delta)
        if self.action_timer == 0:
            self._update_state()

    def feed(self):
        if self.hunger <= 0:
            self.status_msg = "I'm already full! *purr*"
            return
        self.hunger = self._clamp(self.hunger - 30)
        self.happiness = self._clamp(self.happiness + 5)
        self.set_action("eating", "Munch munch... so tasty! 🐟", 30)
        self.save_state()

    def play(self):
        if self.energy < 20:
            self.status_msg = "Too tired to play... *yawn*"
            return
        self.happiness = self._clamp(self.happiness + 25)
        self.energy = self._clamp(self.energy - 20)
        self.hunger = self._clamp(self.hunger + 10)
        self.set_action("playing", "Zoomies!! Catch the laser! 🔴", 30)
        self.save_state()

    def pet(self):
        self.happiness = self._clamp(self.happiness + 15)
        self.set_action("petting", "*Purrrrrrrrrr* More scratches please!", 25)
        self.save_state()

    def sleep(self):
        if self.energy >= 100:
            self.status_msg = "I'm not tired! *zoom*"
            return
        self.current_state = "sleeping"
        self.energy = self._clamp(self.energy + 50)
        self.hunger = self._clamp(self.hunger + 5)
        self.status_msg = "Zzzzz... dreaming of birds..."
        self.save_state()
        
    def pass_time(self):
        # Slower decay: Happens every ~10s in main loop
        if self.current_state != "sleeping":
            self.hunger = self._clamp(self.hunger + 1)
            self.happiness = self._clamp(self.happiness - 0.5)
            self.energy = self._clamp(self.energy - 0.5)

        self.tick_action_timer()
        self.save_state()

    def get_ascii(self, frame: int = 0) -> str:
        blink = frame % 15 == 0
        tail_pos = "/" if frame % 4 < 2 else "\\"
        
        if self.current_state == "sleeping":
            return rf"""
      |\      _,,,---,,_
ZZZ  /,`.-'`'    -.  ;-;;,_
    |,4-  ) )-,_. ,\ (  `'-'
   '---''(_/--'  `-'\_)
"""

        if self.current_state == "eating":
            bowl = r"[bold yellow]\_( )_/[/bold yellow]" if frame % 2 == 0 else r"[bold yellow]\___/[/bold yellow]"
            return rf"""
    [bold white] /\_/\ [/bold white]
    [bold white]( o o )[/bold white]
    [bold white] > ^ < [/bold white]
   [bold white] /     \ [/bold white]
  [bold white] |       | [/bold white] {tail_pos}
  [bold white]  \__{bowl}__/ [/bold white]
"""

        if self.current_state == "playing":
            jump = " " * (frame % 3)
            return rf"""
{jump}    [bold white]  /\_/\ [/bold white]
{jump}    [bold white] ( >ω< )[/bold white]  [bold red]*POP*[/bold red]
{jump}    [bold white]  > ^ < [/bold white]
{jump}    [bold white] /  |  \ [/bold white]
{jump}    [bold white] |  |  | [/bold white] {tail_pos}
"""

        if self.current_state == "petting":
            hand = " (¯`·._.·" if frame % 2 == 0 else "  (¯`·._"
            return rf"""
   [bold white]{hand}[/bold white]
    [bold white] /\_/\ [/bold white]
    [bold white]( ^ ᵕ ^)[/bold white]
    [bold white] > ^ < [/bold white]
   [bold white] /     \ [/bold white]
  [bold white] |       | [/bold white] {tail_pos}
"""

        eye = "-" if blink else "^"
        if self.current_state == "happy": eye = "♥"
        elif self.current_state == "hungry": eye = "o"
        elif self.current_state == "tired": eye = "."

        return rf"""
    [bold white] /\_/\ [/bold white]
    [bold white]( {eye} {eye} )[/bold white]
    [bold white] > ^ < [/bold white]
   [bold white] /     \ [/bold white]
  [bold white] |       | [/bold white] {tail_pos}
  [bold white]  \__ _ / [/bold white]
"""
