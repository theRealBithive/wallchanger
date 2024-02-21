WALLCHANGER
------------------

Wrapper around feh. Changes the wallpaper according to the current time of day.
Specify the times of day and the corresponding wallpapers in the configuration file.

Example configuration file:

```
[time]
morning = 06:00
day = 09:00
evening = 18:00
night = 21:00


[wallpapers]
morning = /path/to/morning/wallpaper
day = /path/to/day/wallpaper
evening = /path/to/evening/wallpaper
night = /path/to/night/wallpaper

[wallchanger]
command = feh --bg-fill

```

Installation
------------
1. Clone the repository
2. Create a configuration in `~/.config/wallchanger/conf.ini` (see example above) or specify a diffrent configuration as an argument to the script
3. Add the script to your autostart (I tried systemd, but it didn't work for me, see: https://unix.stackexchange.com/a/397911)
4. Enjoy the wallpaper changes!

FAQ
---
Q: What time format should I use in the configuration file?
A: The time format is HH:MM.

Q: What happens if the script doesn't find a wallpaper for the current time of day?
A: The script will change the wallpaper to the first wallpaper it finds in the configuration file.

Q: What happens if the script doesn't find a time of day for the current time?
A: The script will change the wallpaper to the first wallpaper it finds in the configuration file.

Q: What happens if the script doesn't find a configuration file?
A: It will yell at you and exit.

Q: What happens if the script finds a configuration file with the wrong format?
A: It will yell at you and exit.

Q: What happens if the script finds a configuration file with the wrong permissions?
A: It will yell at you and exit.
