# Not Hyprland

A minimal Wayland compositor written in Python, inspired by Hyprland.

## Features
- Basic window compositing
- Simple tiling window management
- Window focusing

## Installation

1. Install the required system dependencies:
```bash
# For Debian/Ubuntu
sudo apt-get install python3-dev libcairo2-dev libxcb-composite0-dev

# For Arch Linux
sudo pacman -S python cairo xcb-util
```

2. Install the Python package:
```bash
pip install -e .
```

## Usage

1. Add to your .xinitrc:
```bash
exec not-hyprland
```

2. Start X server:
```bash
startx
```

## Running from TTY (GNOME Session)

1. Open a terminal and navigate to the project directory
2. Make the run script executable:
   ```bash
   chmod +x scripts/run-in-tty.sh
   ```
3. Run the script:
   ```bash
   ./scripts/run-in-tty.sh
   ```

The script will:
- Stop the GNOME Display Manager (GDM)
- Switch to TTY2
- Start the not-hyprland compositor

To return to GNOME:
- Press Ctrl+C to exit the compositor
- The script will automatically restart GDM and return you to the GNOME session

## Keyboard Shortcuts
- Ctrl+Alt+F1: Return to GNOME TTY
- Ctrl+Alt+F2: Switch to compositor TTY
- Ctrl+C: Exit compositor and return to GNOME

## Development

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```
````
