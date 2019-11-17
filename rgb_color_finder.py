"""
    RGB to Hex Color Finder 
    
    A simple program that allows you to change the 
    red, greed, and blue values on the color sliders and see the resulting
    color and HEX value. Click the hex value button to copy the value to your
    clipboard.

    Author      :   Israel Dryer
    Modified    :   2019-11-17
"""
import PySimpleGUI as sg
from operator import itemgetter

sg.change_look_and_feel('Material2')

def get_contrast_yiq(hex_color):
    """ get contrasting black or white text color for a hex color """
    r = int(hex_color[1:3], 16)
    g = int(hex_color[3:5], 16)
    b = int(hex_color[5:7], 16)
    # scale according to visual impact compare to middle
    yiq = ((r*299)+(g*587)+(b*114))//1000
    if yiq >= 128:
        return '#000000' # black
    else:
        return '#FFFFFF' # white

# ----- GUI Layout -----------------------------------------------------------
def slider_row(name):
    txt = sg.Text(name)
    slider = sg.Slider(
        range=(0, 255), 
        default_value=0, 
        orientation='h', 
        enable_events=True,
        key=name)
    return [txt, slider]

col1 = [slider_row('R'), slider_row('G'), slider_row('B')]    
col2 = [[sg.Button(
            '#000000', size=(20, 5), border_width=0, 
            font=(sg.DEFAULT_FONT, 14, 'bold'), button_color=('white', 'black'), 
            key='color')]]

layout = [[sg.Column(col1), sg.Column(col2, key='col2')]]
window = sg.Window('RBG to Hex Color Finder', layout, finalize=True, )

# expand button column to fill vertical space
window['color'].expand(expand_y=True)
window['col2'].expand(expand_y=True)


# ----- MAIN EVENT LOOP ------------------------------------------------------
while True:
    event, values = window.read()
    if event is None:
        break
    if event == 'color':
        window.TKroot.clipboard_clear()
        # get rgb colors from slider values
        color = tuple([int(c) for c in itemgetter('R','G','B')(values)])
        # convert rgb to hex
        hex_color = sg.rgb(*color)
        # append color to clipboard
        window.TKroot.clipboard_append(hex_color)
        sg.popup(f"{hex_color} added to the clipboard", title='HEX Color')
    else:
        # get rgb colors from slider values
        color = tuple([int(c) for c in itemgetter('R','G','B')(values)])
        # convert rgb to hex
        hex_color = sg.rgb(*color)
        # update button color and text
        window['color'].update(
            button_color=(get_contrast_yiq(hex_color), hex_color), text=hex_color)
        
        