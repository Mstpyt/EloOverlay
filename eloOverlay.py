from dearpygui import core, simple
import threading
from time import sleep
from dearpygui.core import mvGuiCol_Text, mvGuiCol_WindowBg, mvGuiCol_Button, mvGuiCol_Separator, mvGuiCol_Border, \
    mvGuiCol_BorderShadow, mvGuiCol_ButtonHovered, mvGuiCol_ButtonActive
from function import api_reader
from config import Streamer

"""
This app is build to integrate an Overlay into Obs or Streamlabs.
The goal of the app was a background-synced api overlay.
For the background-sync i use Thread
"""


class Worker:
    def __init__(self):
        self.iElo = 0
        self.acEloToday = 0
        self.iRank = 0
        self.acResult = ""
        self.acScore = ""
        self.acKd = 0
        self.acMap = ""
        self.iStreak = 0

    def run(self):
        while 1:
            self.iElo, self.acEloToday, self.iRank, self.acResult, \
            self.acScore, self.acKd, self.acMap, self.iStreak = api_reader()
            if "NaN" in self.acEloToday:
                core.set_value("elotoday##", f"Reloading API")
            else:
                core.set_value("elotoday##", f"{self.acEloToday}")
            core.set_value("streak##", f"{self.iStreak}")
            core.set_value("map##", f"\t{self.acMap}:")
            core.set_value("result##", f"{self.acResult}")
            core.set_value("elo##", f"{self.iElo}")
            core.set_value("rank##", f"{self.iRank}")
            core.set_value("score##", f"{self.acScore}")
            core.set_value("kd##", f"{self.acKd}")

            sleep(60)


def long_process():
    w = Worker()
    d = threading.Thread(name='daemon', target=w.run, daemon=True)
    d.start()


def add_faceit(iElo, iRank, acEloToday, iStreak):
    core.add_button("\t\tFACEIT STATS\t\t")
    core.add_text("\tCurrent Elo")
    core.add_same_line(xoffset=130)
    core.add_text("elo##", default_value=f"{iElo}")
    core.add_text("\tRank")
    core.add_same_line(xoffset=130)
    core.add_text("rank##", default_value=f"{iRank}")
    core.add_text("\tElo Today")
    core.add_same_line(xoffset=130)
    core.add_text("elotoday##", default_value=f"{acEloToday}")
    core.add_text("\tWin Streak")
    core.add_same_line(xoffset=130)
    core.add_text("streak##", default_value=f"{iStreak}")


def add_last_game(acMap, acResult, acScore, acKd):
    """
    LAST Game Header
    """
    core.add_button("\t\t LAST GAME\t\t  ")
    core.add_text("map##", default_value=f"\t{acMap}: ")
    core.add_same_line(xoffset=115)
    core.add_text("result##", default_value=f"{acResult}")
    core.add_same_line(xoffset=130)
    core.add_text("score##", default_value=f"{acScore}")
    core.add_text("\tK/D:")
    core.add_same_line(xoffset=130)
    core.add_text("kd##", default_value=f"{acKd}")
    core.add_spacing(count=1)
    core.add_text("powered by Dear PyGui")
    core.add_same_line()
    core.add_image("image##demo", "6727dpg.ico")


"""
Create the Window with dear pyGui
"""
with simple.window(Streamer):
    simple.set_window_pos(Streamer, 0, 0)
    core.set_main_window_title(Streamer)
    """
    Set some Background and Font Colors
    also the frame rounding and the window size
    """
    core.set_theme_item(mvGuiCol_Text, 255, 255, 255, 255)
    core.set_theme_item(mvGuiCol_WindowBg, 16, 18, 32, 255)
    core.set_theme_item(mvGuiCol_Border, 24, 111, 179, 225)
    core.set_theme_item(mvGuiCol_BorderShadow, 24, 111, 179, 255)
    core.set_style_frame_border_size(1.00)
    core.set_theme_item(mvGuiCol_Button, 33, 150, 243, 255)
    core.set_theme_item(mvGuiCol_ButtonHovered, 33, 150, 243, 150)
    core.set_theme_item(mvGuiCol_ButtonActive, 33, 150, 243, 150)
    core.set_main_window_size(215, 250)
    core.set_style_frame_rounding(6.00)
    core.add_additional_font("OpenSans-Regular.ttf", size=14)
    """
    Get Data from the API
    """
    iElo, acEloToday, iRank, acResult, acScore, acKd, acMap, iStreak = api_reader()
    """
    Build the Faceit Header and Data
    """
    add_faceit(iElo, iRank, acEloToday, iStreak)
    """
    Build the Last Game Header and Data
    """
    add_last_game(acMap, acResult, acScore, acKd)

    """
    START
    """
    core.set_start_callback(long_process)
    core.enable_docking(dock_space=False)
    core.start_dearpygui(primary_window=Streamer)
