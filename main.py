import time
import traceback
from rich.console import Console
from rich.live import Live
from rich.layout import Layout
from tigga import Tigga
from cli_theme import StatusDisplay

try:
    import msvcrt
    WINDOWS = True
except ImportError:
    WINDOWS = False
    import select
    import termios
    import tty


class InputReader:
    def __init__(self):
        self.stdin = None
        self.fd = None
        self.original_attrs = None

    def __enter__(self):
        if not WINDOWS:
            import sys

            self.stdin = sys.stdin
            if self.stdin.isatty():
                self.fd = self.stdin.fileno()
                self.original_attrs = termios.tcgetattr(self.fd)
                tty.setcbreak(self.fd)
        return self

    def __exit__(self, exc_type, exc, tb):
        if not WINDOWS and self.fd is not None and self.original_attrs is not None:
            termios.tcsetattr(self.fd, termios.TCSADRAIN, self.original_attrs)

    def get_key(self):
        if WINDOWS:
            if msvcrt.kbhit():
                key = msvcrt.getch().lower()
                return None if key in {b"\x00", b"\xe0"} else key
            return None

        if self.stdin is None or self.fd is None:
            return None

        ready, _, _ = select.select([self.stdin], [], [], 0)
        if not ready:
            return None

        key = self.stdin.read(1)
        return key.lower().encode() if key else None

class TamagotchiGame:
    def __init__(self):
        self.console = Console()
        self.tigga = Tigga()
        self.display = StatusDisplay(self.console)
        self.running = True
        self.frame_count = 0

    def handle_key(self, key):
        # f=feed, l=play, p=pet, s=sleep, q=quit
        if key == b'q' or key == b'\x03': self.running = False
        elif key == b'f': self.tigga.feed()
        elif key == b'l': self.tigga.play()
        elif key == b'p': self.tigga.pet()
        elif key == b's': self.tigga.sleep()

    def run(self):
        self.console.clear()
        self.console.print("[bold magenta]Tigga is waking up...[/bold magenta]")
        time.sleep(1)

        with InputReader() as reader, Live(refresh_per_second=20, screen=True, auto_refresh=False, console=self.console) as live:
            while self.running:
                self.frame_count += 1
                key = reader.get_key()
                if key:
                    self.handle_key(key)

                # Slower time passage
                if self.frame_count % 100 == 0:
                    self.tigga.pass_time()
                else:
                    self.tigga.tick_action_timer(0.1)

                stats = {"hunger": self.tigga.hunger, "happiness": self.tigga.happiness, "energy": self.tigga.energy}
                ascii_art = self.tigga.get_ascii(self.frame_count)

                main_layout = Layout()
                main_layout.split_column(
                    Layout(self.display.render_tigga_ui(ascii_art, stats, self.tigga.status_msg), name="main", ratio=3),
                    Layout(self.display.render_controls(), name="controls", ratio=1)
                )
                live.update(main_layout, refresh=True)
                time.sleep(0.05)

        self.console.clear()
        self.tigga.save_state()
        self.console.print("[bold magenta]Tigga is fast asleep. See you next time! *purr*[/bold magenta]")

if __name__ == "__main__":
    game = TamagotchiGame()
    try:
        game.run()
    except Exception:
        traceback.print_exc()
    finally:
        input("\nPress Enter to exit...")
