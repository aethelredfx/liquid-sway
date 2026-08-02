#lshell

Minimalist configuration for SwayFX (Wayland).

## Preview
<img width="1922" height="1080" alt="image" src="https://github.com/user-attachments/assets/119fbc7a-217b-44ef-9d0c-073d4173a9aa" />
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/482e03bf-f52c-48f1-bf3b-b4157683d255" />

## Wallpapers
<img width="3600" height="2000" alt="moon-black-background-space-planet-full-moon-3600x2000-2043" src="https://github.com/user-attachments/assets/7a45f092-5f38-4362-a7d1-54b412ec7cf1" />
<img width="3840" height="2160" alt="europa-jupiter-moon-3840x2160-26741" src="https://github.com/user-attachments/assets/1e841bd2-adcc-4274-aa99-1a48383a1a97" />



## Components
| Component | Application | Notes |
| :--- | :--- | :--- |
| **Window Manager** | SwayFX | Blur & Radius enabled |
| **Bar** | Waybar | Custom CSS, MPRIS, & Pomodoro |
| **Terminal** | Kitty | Custom Theme |
| **Launcher** |	Rofi |	Run / Drun / Window modes
| **Compositor** | Native |	SwayFX handles composition

### Key Bindings

<details>
<summary>Click to view full keybindings list</summary>



| Keybind | Action | Command |
| :--- | :--- | :--- |
| **Applications** | | |
| `Mod` + `s` | Config Settings | `kitty python3 $HOME/.config/lshell.py` |
| `Mod` + `Enter` | Open Terminal | `$term (Kitty)` |
| `Mod` + `d` | App Launcher | `rofi -show drun` |
| `Mod` + `c` | Clipboard Manager | `cliphist` |
| `Mod` + `b` | Browser | `firefox` |
| `Mod` + `n` | File Manager | `dolphin` |
| `Mod` + `w` | Wallpaper Manager | `waytrogen` |
| `Mod` + `.` | Emoji Launcher | `rofi -show emoji` |
| `Mod` + `shift` + `e` | Logout Manager | `wlogout` |
| **Navigation & Workspaces** | | |
| `Mod` + `Tab` | Visual Window List | `rofi -show window` |
| **System** | | |
| `Mod` + `q` | Kill Focused Window | `kill` |
| `Mod` + `Shift` + `x` | Lock Screen | `swaylock` |
| `Mod` + `Shift` + `c` | Reload Configuration | `reload` |
| `Mod` + `Shift` + `e` | Exit Sway | `swaynag` |
| **Screenshots** | | |
| `Mod` + `Shift` + `s` | Region Screenshot | `grim + slurp` |
| `Print` | Full Screenshot | `grim` |
| **Window Management** | | |
| `Mod` + `Shift` + `Space` | Toggle Floating | `floating toggle` |
| `Mod` + `Shift` + `Minus` | Scratchpad (Move) | `move scratchpad` |
| **Hardware / Media** | | |
| `Vol Up/Down/Mute` | Audio Control | `pactl` |
| `Play/Next/Prev` | Media Control | `playerctl` |


</details>

# Install
## Arch Linux
```bash
sudo pacman -Syyu
sudo pacman -S git autotiling swaybg swaync waybar kitty rofi swaylock papirus-icon-theme ttf-fira-code ttf-jetbrains-mono-nerd ttf-nerd-fonts-symbols ttf-font-awesome noto-fonts-emoji gsimplecal wtype rofi-emoji dolphin bluez bluez-utils blueman python
yay -S waytrogen wlogout swayfx
cd ~
git clone https://github.com/aethelredfx/lshell
cp -r ~/lshell/* ~/.config/
rm -rf ~/lshell
```

# Once installed, do this
Open the terminal and enter the command
```bash
nano ~/.config/waybar/config
```
Press Ctrl + W and find "timezone" 
Replace London with your city.
In the "Pictures" directory, paste the wallpaper file, Press Mod+w and select wallpaper.
