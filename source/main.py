import GUI_Localization
import Localization
import tkinter as tk

if __name__ == "__main__":
    root = tk.Tk()
    localization = Localization.Localization(root)

    root = tk.Tk()
    app = GUI_Localization.GUI_Localization(root)

    while True:        
        # # request to connect
        localization.loop_collect_data()

        # # parse data from server
        localization.loop(app)
        
        # update GUI
        app.update_localization_data()
        root.update()

        # time.sleep(0.5)