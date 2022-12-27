import PySimpleGUI as sg
import os
import atexit
import numpy as np


def clean_hard():
    dir_loc = os.listdir('avm')
    if len(dir_loc) == 0:
        os.rmdir('avm')
        return
    os.remove('avm/temp.mp4')
    os.rmdir('avm')


def clean_soft():
    dir_loc = os.listdir('avm')
    if len(dir_loc) == 0:
        return
    os.remove('avm/temp.mp4')


def calc(values):
    clean_soft()
    mix_val = values['mixWeight']
    weights = np.array([1, 1], dtype='float64')
    adj = np.array([-1, 1]) * mix_val / 100
    weights += adj
    weights /= max(weights)
    weights[0], weights[1] = round(weights[0], 2), round(weights[1], 2)
    # os.system(f'ffmpeg -i ' + values['-FILE-'] + ' -map 0 -map -0:a:0 -filter_complex "[0:a:0]volume=' + str(
    #     values['c1Volume']) + '[a]" -map "[a]" -c copy -c:a:1 aac tmp/temp.mp4')
    # os.system(f'ffmpeg -i tmp/temp.mp4 -map 0 -map -0:a:0 -filter_complex "[0:a:0]volume=' + str(
    #     values['c2Volume']) + '[a]" -map "[a]" -c copy -c:a:1 aac tmp/temp1.mp4')
    os.system(
        f'Binaries/ffmpeg -i ' + values['-FILE-'] + ' -filter_complex "[0:a:0][0:a:1]amix=2:longest:weights=' + str(weights[0]) + ' ' + str(
            weights[1]) + '[aout]" -map 0:V:0 -map "[aout]" -c:v copy -c:a aac -b:a 320k avm/temp.mp4')

def main():
    # Use a breakpoint in the code line below to debug your script.
    file_loaded = False
    os.mkdir('avm')
    #Change Them
    sg.theme('SystemDefault')  # Add a touch of color
    # All the stuff inside your window.
    layout = [[sg.FileBrowse('Select Video File', key='-FILE-', enable_events=True)],
              [sg.Text('Below is the mixing slider, left is more game sound, right is for more mic sound')],
              [sg.Text('Audio Mix Weight'), sg.Slider(range=(-100, 100),
                                                      default_value=0,
                                                      resolution=0.5,
                                                      size=(57, 15),
                                                      orientation='h',
                                                      font=('Helvetica', 12),
                                                      key='mixWeight',
                                                      pad=(0, 0),
                                                      tick_interval=10)],
              [sg.Button('Preview Changes w/ Video', key='Preview'),
               sg.Button('Save w/ Current Mix', key='Save')]
              ]

    # Create the Window
    window = sg.Window('Audio Mixer', layout)
    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Cancel':  # if user closes window or clicks cancel
            break
        if event == '-FILE-' and values['-FILE-']:
            file_loaded = True

        if event == 'Preview' and file_loaded:
            calc(values)
            video_path = "avm/temp.mp4"
            os.system(f'Binaries/ffplay avm/temp.mp4')

        if event == 'Save' and file_loaded:
            calc(values)
            os.rename('avm/temp.mp4', values['-FILE-'][:-4] + '_mixed.mp4')
            # mix audio and save w/ video as mp4
    window.close()


# Press the green button in the gutter to run the script.


if __name__ == '__main__':
    atexit.register(clean_hard)
    main()
