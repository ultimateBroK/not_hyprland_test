# Not Hyprland

A minimal X11 window manager and compositor written in Python, inspired by Hyprland.

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