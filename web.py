from nicegui import ui
import stream_radio as sr
import threading

'''
Web表示(niceGUI)
'''

class stream_radio():
    def __init__(self, name, url, q="best") -> None:
        self.name = name
        self.url = url
        self.q = q

    def turn(self, vol=100):
        self.c = sr.start_stream(name=self.name, url=self.url, q=self.q, vol=vol)
        log.push("Open:" + self.url)

    def stop(self):
        try:
            sr.kill_pid(name=self.name)
            # self.c.kill()
            log.push("Stop:" + self.url)
            return
        except NameError:
            return

# Radio Stations
radio_nhk = stream_radio(name="NHK_FM", url="https://radiko.jp/#!/live/JOAK-FM", q="best")
#
ui.markdown('''# Raspi Radio Station''')
ui.markdown('''## NHK FM''')
with ui.row():
    ui.button('Radio NHK FM', on_click=lambda e: radio_nhk.turn(vol=vol_slider.value))
    ui.button('STOP NHK FM', on_click=radio_nhk.stop)
# Vol
ui.label('Volume.')
vol_slider = ui.slider(min=0, max=100, value=100)
ui.label().bind_text_from(vol_slider, 'value')
# Log
ui.markdown('''Log''')
log = ui.log(max_lines=20).classes('w-full h-32')
# Run
ui.run(show=False, title="RADIO")
