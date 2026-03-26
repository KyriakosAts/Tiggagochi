# Terminal Theme CLI

A polished, modular Python CLI that showcases the power of `Rich` for terminal styling. This project features interactive theme selection, live previews, and a suite of reusable themed components.

## Features

- **Interactive Selection:** Navigate through prebuilt themes with a live preview card updating in real-time.
- **Prebuilt Themes:**
    - Minimal Premium (Nord-inspired)
    - Dashboard CLI (High contrast)
    - Playful / Interactive (Vibrant colors)
    - Cyberpunk / Neon (Fluorescent aesthetics)
    - Nature / Soft Pastels (Calming tones)
    - Monochrome Elegance (Clean grayscale)
- **Reusable Components:** Integrated `ThemeManager` providing consistent `print_success`, `print_error`, and `print_section` methods.
- **Persistence:** Remembers your selected theme across sessions using `config.json`.
- **Micro-interactions:** Smooth progress bars and spinners to enhance user experience.

## Installation

1. Ensure you have Python 3.8+ installed.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the CLI:
```bash
python main.py
```

- Use **Up/Down arrows** to navigate the theme menu.
- Observe the **Live Preview** update on the right.
- Press **Enter** to apply the theme and see the micro-interactions demo.

## Project Structure

- `main.py`: Entry point with interactive menu logic.
- `cli_theme.py`: Theme definitions and reusable UI components.
- `config.json`: Stores user preferences.
- `requirements.txt`: Package dependencies.
