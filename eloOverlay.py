from dearpygui import core, simple
import threading
from time import sleep
from dearpygui.core import mvGuiCol_Text, mvGuiCol_WindowBg, mvGuiCol_Button, mvGuiCol_Separator, mvGuiCol_Border, \
    mvGuiCol_BorderShadow, mvGuiCol_ButtonHovered, mvGuiCol_ButtonActive
from functions import api_reader

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
                core.set_value(f"{acEloToday}", f"Reloading API")
            else:
                core.set_value(f"{acEloToday}", f"{self.acEloToday}")
            core.set_value(f"{iStreak}", f"{self.iStreak}")
            core.set_value(f"{acMap}", f"{self.acMap}")
            core.set_value(f"{acResult}", f"{self.acResult}")
            core.set_value(f"{iElo}", f"{self.iElo}")
            core.set_value(f"{iRank}", f"{self.iRank}")
            core.set_value(f"{acScore}", f"{self.acScore}")
            core.set_value(f"{acKd}", f"{self.acKd}")

            sleep(60)


def long_process():
    w = Worker()
    d = threading.Thread(name='daemon', target=w.run, daemon=True)
    d.start()


"""
Create the Window with dear pyGui
"""
with simple.window("Maniac Elo"):
    simple.set_window_pos("Maniac Elo", 0, 0)
    core.set_main_window_title("Maniac Elo")
    """
    Set some Background and Font Colors
    also the frame rounding and the window size
    """
    core.set_theme_item(mvGuiCol_Text, 255, 255, 255, 255)
    core.set_theme_item(mvGuiCol_WindowBg, 0, 0, 0, 255)
    core.set_theme_item(mvGuiCol_Separator, 130, 221, 168, 255)
    core.set_theme_item(mvGuiCol_Border, 130, 221, 168, 225)
    core.set_theme_item(mvGuiCol_BorderShadow, 130, 221, 168, 0)
    core.set_style_frame_border_size(1.00)
    core.set_theme_item(mvGuiCol_Button, 130, 221, 168, 150)
    core.set_theme_item(mvGuiCol_ButtonHovered, 130, 221, 168, 255)
    core.set_theme_item(mvGuiCol_ButtonActive, 130, 221, 168, 255)
    core.set_main_window_size(250, 225)
    core.set_style_frame_rounding(6.00)

    """
    Get Data from the API
    """
    iElo, acEloToday, iRank, acResult, acScore, acKd, acMap, iStreak = api_reader()

    """
    Fill the {} with data and build up the App with fields
    Header is build with a button xD
    """
    core.add_button("\t\tFACEIT STATS\t\t")
    core.add_text("\tCurrent Elo")
    core.add_same_line(xoffset=130)
    core.add_text(f"{iElo}")
    core.add_text("\tRank")
    core.add_same_line(xoffset=130)
    core.add_text(f"{iRank}")
    core.add_text("\tElo Today")
    core.add_same_line(xoffset=130)
    core.add_text(f"{acEloToday}")
    core.add_text("\tWin Streak")
    core.add_same_line(xoffset=130)
    core.add_text(f"{iStreak}")
    """
    LAST Game Header
    """
    core.add_button("\t\t LAST GAME\t\t  ")
    core.add_text(f"\t{acMap}: ")
    core.add_same_line(xoffset=115)
    core.add_text(f"{acResult}")
    core.add_same_line(xoffset=130)
    core.add_text(f"{acScore}")
    core.add_text("\tK/D:")
    core.add_same_line(xoffset=130)
    core.add_text(f"{acKd}")
    core.add_spacing(count=1)
    core.add_text("powered by Dear PyGui")
    core.add_same_line()
    core.add_image("image##demo", "6727dpg.ico")
    """
    START
    """
    core.set_start_callback(long_process)
    core.enable_docking(dock_space=False)
    core.start_dearpygui(primary_window="Maniac Elo")
