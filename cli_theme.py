from rich.console import Console, Group
from rich.panel import Panel
from rich.progress import ProgressBar
from rich.layout import Layout
from rich.table import Table
from rich.text import Text
from typing import Dict, Any

class StatusDisplay:
    def __init__(self, console: Console):
        self.console = console

    def create_stat_bar(self, label: str, value: float, color: str) -> Group:
        percentage = f"{int(value)}%"
        return Group(
            Text(f"{label:10} {percentage:>4}", style=f"bold {color}"),
            ProgressBar(total=100, completed=value, width=30, style=f"{color}", finished_style=f"{color}")
        )

    def render_tigga_ui(self, ascii_art: str, stats: Dict[str, float], status_msg: str) -> Layout:
        layout = Layout()
        layout.split_column(
            Layout(name="top", ratio=3),
            Layout(name="msg", size=3)
        )
        
        top_row = Layout()
        top_row.split_row(
            Layout(name="art", ratio=2),
            Layout(name="stats", ratio=3)
        )
        layout["top"].update(top_row)

        # Art Panel (Centered content)
        art_panel = Panel(
            Text.from_markup(ascii_art),
            title="[bold magenta]Tigga[/bold magenta]",
            border_style="magenta",
            expand=True
        )
        top_row["art"].update(art_panel)

        # Stats Panel
        stats_group = Group(
            self.create_stat_bar("Hunger", stats['hunger'], "red" if stats['hunger'] > 80 else "green"),
            "\n",
            self.create_stat_bar("Happiness", stats['happiness'], "yellow" if stats['happiness'] < 30 else "cyan"),
            "\n",
            self.create_stat_bar("Energy", stats['energy'], "red" if stats['energy'] < 20 else "blue")
        )

        stats_panel = Panel(
            stats_group,
            title="[bold cyan]Stats[/bold cyan]",
            border_style="cyan",
            padding=(1, 2)
        )
        top_row["stats"].update(stats_panel)

        # Message Panel (Safe for long text)
        msg_panel = Panel(
            Text(status_msg, justify="center", style="italic bold white"),
            border_style="white"
        )
        layout["msg"].update(msg_panel)

        return layout

    def render_controls(self) -> Panel:
        controls = Table.grid(padding=(0, 2))
        controls.add_column(style="bold yellow", justify="right")
        controls.add_column(style="white")
        
        controls.add_row("[F]", "Feed Tigga (Bowl animation)")
        controls.add_row("[L]", "pLay with Tigga (Jump animation)")
        controls.add_row("[P]", "Pet Tigga (Purr animation)")
        controls.add_row("[S]", "Sleep (Dreaming animation)")
        controls.add_row("[Q]", "Quit and Save")

        return Panel(
            controls,
            title="[bold]Care Controls[/bold]",
            border_style="dim white"
        )
