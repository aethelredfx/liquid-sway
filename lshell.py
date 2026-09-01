import curses, os, shutil, time

WAYBAR_TARGET = os.path.expanduser("~/.config/waybar")

BASE_CONFIG_TEMPLATE = """{
    "layer": "top",
    "position": "__POS__",
    "height": 32,
    "margin-top": 6,
    "margin-left": 16,
    "margin-right": 16,
    "margin-bottom": 6,
    "spacing": 0,
    "modules-left": ["custom/launcher", "sway/workspaces", "hyprland/workspaces", "custom/spotify", "custom/language"],
    "modules-center": ["clock#time", "clock#date"],
    "modules-right": ["pulseaudio", "network", "battery", "custom/power"],
    "custom/launcher": {
        "format": "Apps",
        "on-click": "rofi -show drun"
    },
    "custom/language": {
        "format": "{}",
        "exec": "swaymsg -t get_inputs | jq -r '.[] | select(.type == \\"keyboard\\") | .xkb_active_layout_name' | head -n1",
        "interval": 1,
        "on-click": "swaymsg input type:keyboard xkb_switch_layout next"
    },
    "sway/workspaces": {
        "disable-scroll": true,
        "all-outputs": true,
        "format": "{icon}",
        "format-icons": {
            "1": "●", "2": "●", "3": "●", "4": "●", "5": "●",
            "6": "●", "7": "●", "8": "●", "9": "●", "10": "●"
        }
    },
    "hyprland/workspaces": {
        "disable-scroll": true,
        "all-outputs": true,
        "format": "{name}"
    },
    "custom/spotify": {
        "format": "  {}",
        "escape": true,
        "interval": 1,
        "max-length": 25,
        "exec": "playerctl status 2>/dev/null | grep -q Playing && playerctl metadata --format '{{title}} - {{artist}}' || true",
        "on-click": "playerctl play-pause",
        "on-scroll-up": "playerctl next",
        "on-scroll-down": "playerctl previous"
    },
    "clock#time": {
        "format": "  {:%H:%M:%S}",
        "timezone": "__TZ__",
        "interval": 1,
        "tooltip-format": "<big>{:%Y %B}</big>\\n<tt><small>{calendar}</small></tt>"
    },
    "clock#date": {
        "format": "  {:%d %b, %a}"
    },
    "pulseaudio": {
        "format": "{icon} {volume}%",
        "format-muted": " Muted",
        "format-icons": {
            "headphone": "",
            "default": ["", "", ""]
        },
        "on-click": "blueman-manager"
    },
    "network": {
        "format-wifi": "  {essid}",
        "format-ethernet": "𖧧  {ifname}",
        "format-disconnected": "⚠️ Disconnected",
        "on-click": "kitty -- nmtui"
    },
    "battery": {
        "states": {
            "good": 95,
            "warning": 30,
            "critical": 15
        },
        "format": "{icon}  {capacity}%",
        "format-charging": " {capacity}%",
        "format-plugged": " {capacity}%",
        "format-alt": "{icon} {time}",
        "format-icons": ["", "", "", "", ""],
        "on-click": "swaync-client -t -sw"
    },
    "custom/power": {
        "format": "⏻",
        "on-click": "wlogout --protocol layer-shell --layout /etc/wlogout/layout --css ~/.config/wlogout/style.css"
    }
}"""

STYLE_CONTENT = """
window#waybar { 
    background-color: transparent; 
    font-family: "JetBrainsMono Nerd Font", "Roboto", sans-serif; 
    font-size: 13px; 
    font-weight: bold; 
    color: #ffffff; 
}

#workspaces { 
    background: rgba(255, 255, 255, 0.08); 
    border-radius: 16px; 
    border: 1px solid rgba(255, 255, 255, 0.15); 
    margin: 2px 4px; 
    padding: 3px 4px; 
}

#workspaces button { 
    background: transparent; 
    color: rgba(255, 255, 255, 0.4); 
    border: none; 
    border-radius: 10px; 
    margin: 2px 2px; 
    padding: 0px 10px; 
    transition: background 0.4s cubic-bezier(0.25, 1, 0.5, 1), color 0.4s cubic-bezier(0.25, 1, 0.5, 1);
}

#workspaces button.focused, 
#workspaces button.active { 
    background: rgba(125, 207, 255, 0.2); 
    color: #ffffff; 
}

#workspaces button:hover { 
    background: rgba(255, 255, 255, 0.1); 
    color: #ffffff;
}

#custom-launcher, 
#custom-language, 
#clock.time, 
#clock.date, 
#pulseaudio, 
#network, 
#battery { 
    background: rgba(255, 255, 255, 0.08); 
    border-radius: 16px; 
    border: 1px solid rgba(255, 255, 255, 0.15); 
    margin: 2px 4px; 
    padding: 2px 20px; 
    color: #ffffff; 
    transition: background 0.2s ease, border-color 0.2s ease, padding 0.3s cubic-bezier(0.25, 1, 0.5, 1);
}

#custom-power {
    background: rgba(255, 255, 255, 0.08); 
    border-radius: 16px; 
    border: 1px solid rgba(255, 255, 255, 0.15); 
    margin: 2px 4px; 
    padding: 2px 14px;
    color: #ffffff;
    transition: background 0.2s ease, border-color 0.2s ease, padding 0.3s cubic-bezier(0.25, 1, 0.5, 1);
}

#custom-launcher:hover, 
#custom-language:hover, 
#clock.time:hover, 
#clock.date:hover, 
#pulseaudio:hover, 
#network:hover, 
#battery:hover {
    background: rgba(255, 255, 255, 0.22);
    border-color: rgba(255, 255, 255, 0.4);
    padding: 2px 40px; 
}

#custom-power:hover {
    background: rgba(255, 255, 255, 0.22);
    border-color: rgba(255, 255, 255, 0.4);
    padding: 2px 22px;
}

#custom-spotify { 
    background: rgba(125, 207, 255, 0.1); 
    border-radius: 16px; 
    border: 1px solid rgba(125, 207, 255, 0.2); 
    margin: 2px 4px; 
    padding: 2px 14px; 
    color: #7dcfff; 
    transition: background 0.2s ease, border-color 0.2s ease;
}

#custom-spotify:hover {
    background: rgba(125, 207, 255, 0.2);
    border-color: rgba(125, 207, 255, 0.4);
}

#battery.charging, 
#battery.plugged { 
    color: #9ece6a; 
}

#battery.warning { 
    color: #e0af68; 
}

#battery.critical:not(.charging) { 
    color: #f7768e; 
    animation-name: blink; 
    animation-duration: 0.5s; 
    animation-timing-function: linear; 
    animation-iteration-count: infinite; 
    animation-direction: alternate; 
}

@keyframes blink { 
    to { 
        background: rgba(247, 118, 142, 0.25); 
        border-color: rgba(247, 118, 142, 0.4);
        color: #ffffff; 
    } 
}"""

ASCII_LOGO = """
              ___ _          _ _ 
   / /         / ____| |        | | |
  / /   __ | (___ | |__   ___| | |
 / /   |______| \\___ \\| '_ \\ / _ \\ | |
/ /___          ____) | | | |  __/ | |
\\_____|        |_____/|_| |_|\\___|_|_|
"""

TIMEZONES = [
    ("Kyiv (Europe/Kyiv)", "Europe/Kyiv"),
    ("Moscow (Europe/Moscow)", "Europe/Moscow"),
    ("London (Europe/London)", "Europe/London"),
    ("New York (America/New_York)", "America/New_York"),
    ("Tokyo (Asia/Tokyo)", "Asia/Tokyo"),
    ("Berlin (Europe/Berlin)", "Europe/Berlin"),
    ("Paris (Europe/Paris)", "Europe/Paris"),
    ("Local System Time (UTC)", "UTC")
]

def draw_appearance_animation(stdscr):
    curses.curs_set(0)
    stdscr.clear()
    curses.init_pair(4, curses.COLOR_MAGENTA, curses.COLOR_BLACK)

    lines = [line for line in ASCII_LOGO.splitlines() if line.strip()]
    height, width = stdscr.getmaxyx()

    logo_width = max(len(line) for line in lines)
    start_y = max(0, (height - len(lines)) // 2)

    for idx, line in enumerate(lines):
        if start_y + idx < height:
            x = max(0, (width - logo_width) // 2)
            stdscr.attron(curses.color_pair(4) | curses.A_BOLD)
            stdscr.addstr(start_y + idx, x, line)
            stdscr.attroff(curses.color_pair(4) | curses.A_BOLD)
            stdscr.refresh()
            time.sleep(0.04)

    time.sleep(0.2)

    bar_y = min(height - 2, start_y + len(lines) + 2)
    bar_width = min(40, width - 10)
    start_x_bar = max(0, (width - bar_width) // 2)

    for i in range(bar_width + 1):
        progress = int((i / bar_width) * 100)
        bar = "♦" * i + " " * (bar_width - i)
        text = f" [{bar}] {progress}%"
        stdscr.addstr(bar_y, start_x_bar, text)
        stdscr.refresh()
        time.sleep(0.015)

    time.sleep(0.3)

def apply_blocks_config(position, tz):
    try:
        if os.path.exists(WAYBAR_TARGET):
            shutil.rmtree(WAYBAR_TARGET) if os.path.isdir(WAYBAR_TARGET) else os.remove(WAYBAR_TARGET)
        os.makedirs(WAYBAR_TARGET, exist_ok=True)
        cfg = BASE_CONFIG_TEMPLATE.replace("__POS__", position).replace("__TZ__", tz)
        with open(os.path.join(WAYBAR_TARGET, "config"), "w", encoding="utf-8") as f: f.write(cfg)
        with open(os.path.join(WAYBAR_TARGET, "style.css"), "w", encoding="utf-8") as f: f.write(STYLE_CONTENT)
        os.system("pkill -9 waybar")
        os.system("killall -9 waybar")
        time.sleep(0.4)
        os.system("swaymsg reload")
        os.system("killall -9 waybar && nohup waybar > /dev/null 2>&1 &")
        return True, f"Applied {position} panel with {tz} timezone!"
    except Exception as e:
        return False, f"Error: {str(e)}"

def select_timezone_menu(stdscr):
    current_row = 0
    while True:
        stdscr.clear()
        height, width = stdscr.getmaxyx()
        title = "     Select Timezone  "
        stdscr.addstr(2, max(0, (width - len(title)) // 2), title, curses.A_REVERSE | curses.A_BOLD)
        for idx, (label, _) in enumerate(TIMEZONES):
            x = max(0, (width - len(label)) // 2)
            y = 6 + idx * 1
            if idx == current_row:
                stdscr.attron(curses.color_pair(1) | curses.A_BOLD)
                stdscr.addstr(y, x - 4, f"  ➤  {label}  ")
                stdscr.attroff(curses.color_pair(1) | curses.A_BOLD)
            else:
                stdscr.addstr(y, x, f"     {label}  ")
        stdscr.refresh()
        key = stdscr.getch()
        if key == 27 or key == ord('q'): return None
        elif key == curses.KEY_UP and current_row > 0: current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(TIMEZONES) - 1: current_row += 1
        elif key in [curses.KEY_ENTER, 10, 13]:
            return TIMEZONES[current_row][1]

def main_menu(stdscr):
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_MAGENTA)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)

    draw_appearance_animation(stdscr)

    options = [
        ("Panel (Top)", "top"),
        ("Panel (Bottom)", "bottom"),
        ("Exit", None)
    ]

    current_row = 0
    message = ""
    is_error = False

    while True:
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        title = "Select Panel Position"
        title_y = max(1, height // 2 - 5)
        stdscr.addstr(
            title_y,
            max(0, (width - len(title)) // 2),
            title,
            curses.A_REVERSE | curses.A_BOLD
        )

        for idx, (label, _) in enumerate(options):
            x = max(0, (width - len(label)) // 2)
            y = title_y + 3 + idx * 2

            if idx == current_row:
                text = f"  ➤  {label}  "
                stdscr.attron(curses.color_pair(1) | curses.A_BOLD)
                stdscr.addstr(y, max(0, (width - len(text)) // 2), text)
                stdscr.attroff(curses.color_pair(1) | curses.A_BOLD)
            else:
                text = f"     {label}  "
                stdscr.addstr(y, max(0, (width - len(text)) // 2), text)

        if message:
            msg_style = curses.color_pair(3) if is_error else curses.color_pair(2)
            msg_y = max(0, height - 3)
            stdscr.addstr(
                msg_y,
                max(0, (width - len(message) - 2) // 2),
                f"● {message}",
                msg_style | curses.A_BOLD
            )

        stdscr.refresh()
        key = stdscr.getch()

        if key == 27 or key == ord("q"):
            break
        elif key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(options) - 1:
            current_row += 1
        elif key in [curses.KEY_ENTER, 10, 13]:
            _, position = options[current_row]

            if position is None:
                break

            selected_tz = select_timezone_menu(stdscr)

            if selected_tz is not None:
                success, msg = apply_blocks_config(position, selected_tz)
                message = msg
                is_error = not success


if __name__ == "__main__":
    curses.wrapper(main_menu)
