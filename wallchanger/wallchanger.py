#!/usr/bin/env python3
import configparser
import sched
from loguru import logger

import os
import sys
import time
import subprocess

logger.add(
    "/home/bithive/.config/wallchanger/wallchanger.log",
    format="{time} {level} {message}",
    level="DEBUG",
)


class Wallchanger:
    def __init__(self):
        self.config = None

    def load(self, path: str):
        configer = configparser.ConfigParser()
        logger.debug(f"Loading config file: {path}")
        configer.read(path)
        self.config = configer
        try:
            assert self.config["time"]
            assert self.config["wallpapers"]
        except KeyError:
            logger.error("Config file is missing required sections.")
            sys.exit(1)

    def change_wallpaper(self, path: str):
        changing_engine = self.config["wallchanger"].get("command", "feh --bg-fill")
        logger.debug(f"Changing wallpaper to: {path} with command: {changing_engine}")
        subprocess.run(changing_engine.split() + [path])

    def run(self):
        while True:  # Infinite loop for continuous operation
            s = sched.scheduler(time.time, time.sleep)
            current_time = time.localtime()  # Current local time
            wallpaper_section = self.config["wallpapers"]
            time_section = self.config["time"]

            # Determine the closest past scheduled wallpaper to apply immediately
            now = time.time()
            closest_wallpaper_path = None
            closest_time_diff = float("inf")
            for wallpaper_key, wallpaper_path in wallpaper_section.items():
                time_value = time_section.get(wallpaper_key)
                if time_value is None:
                    logger.warning(f"No time specified for wallpaper: {wallpaper_key}")
                    continue

                schedule_time_struct = time.strptime(time_value, "%H:%M")
                scheduled_time_today = time.mktime(
                    time.struct_time(
                        (
                            current_time.tm_year,
                            current_time.tm_mon,
                            current_time.tm_mday,
                            schedule_time_struct.tm_hour,
                            schedule_time_struct.tm_min,
                            0,
                            0,
                            0,
                            -1,
                        )
                    )
                )
                # Check if this is the closest past time to now
                if scheduled_time_today < now:
                    time_diff = now - scheduled_time_today
                    if time_diff < closest_time_diff:
                        closest_time_diff = time_diff
                        closest_wallpaper_path = wallpaper_path

            # Apply the closest wallpaper if found
            if closest_wallpaper_path:
                logger.debug(f"Applying closest wallpaper: {closest_wallpaper_path}")
                self.change_wallpaper(closest_wallpaper_path)

            # Schedule wallpapers for the current day
            last_scheduled_time = 0
            for wallpaper_key in wallpaper_section:
                wallpaper_path = wallpaper_section[wallpaper_key]
                time_value = time_section.get(wallpaper_key)
                if time_value is None:
                    continue

                schedule_time_struct = time.strptime(time_value, "%H:%M")
                scheduled_time_today = time.mktime(
                    time.struct_time(
                        (
                            current_time.tm_year,
                            current_time.tm_mon,
                            current_time.tm_mday,
                            schedule_time_struct.tm_hour,
                            schedule_time_struct.tm_min,
                            0,
                            0,
                            0,
                            -1,
                        )
                    )
                )
                if scheduled_time_today < now:
                    scheduled_time_today += 86400  # Schedule for the next day

                last_scheduled_time = max(last_scheduled_time, scheduled_time_today)
                # Parse the float of scheduled_time_today to yyyy-mm-dd hh:mm:ss
                human_readable_time = time.strftime(
                    "%Y-%m-%d %H:%M:%S", time.localtime(scheduled_time_today)
                )
                logger.debug(
                    f"Scheduling wallpaper: {wallpaper_key} at {human_readable_time}"
                )
                s.enterabs(
                    scheduled_time_today,
                    1,
                    self.change_wallpaper,
                    argument=(wallpaper_path,),
                )

            s.run()  # Execute the scheduled events

            # Sleep until it's time to schedule the next day's wallpapers
            sleep_time = (
                last_scheduled_time - time.time() + 60
            )  # 60 seconds offset to ensure we are into the next day
            logger.debug(f"Sleeping for {sleep_time} seconds until the next cycle.")
            time.sleep(sleep_time)


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(
        f"/home/{os.environ.get('USER')}/.config/wallchanger/", "conf.ini"
    )

    wallchanger = Wallchanger()

    if len(sys.argv) > 1:
        path = sys.argv[1]
        wallchanger.load(path)
    else:
        wallchanger.load(config_path)

    wallchanger.run()
