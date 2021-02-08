#
# This is a very simple serial terminal with GUI which is tkinter
#
# In this code i used  https://github.com/pyserial/pyserial
#
# this code is written by Amir otd :)))

from __future__ import print_function

try:
    import tkinter as tk
    from tkinter import ttk, messagebox
except ImportError:
    import Tkinter as tk
    from Tkinter import ttk, messagebox

from threading import Thread
import serial  # pip install pyserial


_baudrate_choices = [50, 75, 110, 134, 150, 200, 300, 600, 1200, 1800, 2400, 4800,
                     9600, 19200, 38400, 57600, 115200, 230400, 460800, 500000,
                     576000, 921600, 1000000, 1152000, 1500000, 2000000, 2500000,
                     3000000, 3500000, 4000000]

_handShake_choices = ['None', 'RTS/CTS', 'Xon/Xoff']

_dataSize = {5: serial.FIVEBITS, 6: serial.SIXBITS, 7: serial.SEVENBITS, 8: serial.EIGHTBITS}
_stopBit = {'One': serial.STOPBITS_ONE, 'OnePointFive': serial.STOPBITS_ONE_POINT_FIVE, 'Two': serial.STOPBITS_TWO}
_parity = {'None': serial.PARITY_NONE, 'Even': serial.PARITY_EVEN, 'Odd': serial.PARITY_ODD,
           'Mark': serial.PARITY_MARK, 'space': serial.PARITY_SPACE}

ser = serial.Serial()


def open_port():
    try:
        ser.port = portName_var.get()
        ser.baudrate = baudVar.get()
        ser.bytesize = _dataSize[dataVar.get()]
        ser.parity = _parity[parityVar.get()]
        ser.stopbits = _stopBit[stopBitVar.get()]

        if handShakeVar.get() == 'RTS/CTS':
            ser.rtscts = 1
            ser.xonxoff = False
        elif handShakeVar.get() == 'Xon/Xoff':
            ser.xonxoff = 1
            ser.rtscts = False
        else:
            ser.xonxoff = False
            ser.rtscts = False

        ser.open()
        task = Thread(target=print_result)
        task.setDaemon(True)
        task.start()

    except serial.serialutil.SerialException:
        print("Please Enter a Valid Port Name!!")
        messagebox.showerror("Error", "Please Enter a Valid Port Name!!")


def print_result():
    while True:
        receive_box.insert(tk.INSERT, ser.read())
        print(ser.baudrate, ser.bytesize, ser.parity, ser.stopbits, ser.rtscts, ser.xonxoff)


def send_data():
    try:
        temp_send_data = send_box.get("1.0", "end-1c")
        ser.write(temp_send_data.encode('utf-8'))
        print(temp_send_data)
    except serial.serialutil.SerialException:
        print("First Open a Port!!!")
        messagebox.showerror("Error", "First Open a Port!!!")


def show_info():
    print(":)))))")
    messagebox.showinfo("About", "This program is written in python and\n it's"
                                 " using pyserial library and tkinter GUI")


def run():
    window.mainloop()


# ____________________tkinter initial window configuration
window = tk.Tk()

window.title("Serial Terminal")
window.geometry('1000x425+200+100')
window['padx'] = 20
window['pady'] = 20

# ____________________column configuration
window.grid_columnconfigure(0, weight=10)
window.grid_columnconfigure(1, weight=1)

# ____________________row configuration
window.grid_rowconfigure(0, weight=1)
window.grid_rowconfigure(1, weight=15)

# ____________________receive data box configuration
receive_box = tk.Text(window, height=8)
receive_box.grid(column=0, row=1, sticky='nsew', padx=(0, 10))
scroll = tk.Scrollbar(window, orient=tk.VERTICAL, command=receive_box.yview)
scroll.grid(column=0, row=1, sticky='nse')
receive_box["yscrollcommand"] = scroll.set

# ____________________send data frame configuration
send_frame = tk.LabelFrame(window, text='Send Data')
send_frame.grid(column=0, row=0, sticky='wens', padx=(0, 10), pady=(0, 10))
send_frame['padx'] = 10
# sendBox_label = tk.Label(send_frame, text='Send Data:')
# sendBox_label.grid(column=0, row=0)
send_box = tk.Text(send_frame, height=1)
send_box.grid(column=0, row=0, padx=(10, 5))
send_button = tk.Button(send_frame, text='Send', width=7, command=send_data)
send_button.grid(column=1, row=0, padx=(10, 10))

# ____________________serial settings box configuration
serial_frame = tk.LabelFrame(window, text='Serial Port Settings')
serial_frame.grid(column=1, row=0, rowspan=2, sticky='esn', padx=(10, 5))

portName_var = tk.StringVar(window)
portName_frame = tk.LabelFrame(serial_frame, text='Port Name')
portName_box = tk.Entry(portName_frame, textvariable=portName_var)
portName_frame.grid(column=0, row=0)
portName_box.grid(column=0, row=0)

baudVar = tk.IntVar(window)
baudVar.set(9600)
baudrate_frame = tk.LabelFrame(serial_frame, text='Baudrate')
baudrate_frame.grid(column=0, row=1)
baudrate_box = ttk.Combobox(baudrate_frame, text=baudVar, value=baudVar)
baudrate_box.grid(column=0, row=0)
baudrate_box['values'] = _baudrate_choices

dataVar = tk.IntVar(window)
dataVar.set(8)
dataSize_frame = tk.LabelFrame(serial_frame, text='Data Size')
dataSize_frame.grid(column=0, row=2)
dataSize_box = ttk.Combobox(dataSize_frame, text=dataVar, value=dataVar)
dataSize_box.grid(column=0, row=0)
dataSize_box['values'] = list(_dataSize.keys())

parityVar = tk.StringVar(window)
parityVar.set('None')
parity_frame = tk.LabelFrame(serial_frame, text='Parity')
parity_frame.grid(column=0, row=3)
parity_box = ttk.Combobox(parity_frame, text=parityVar, value=parityVar)
parity_box.grid(column=0, row=0)
parity_box['values'] = list(_parity.keys())

stopBitVar = tk.StringVar(window)
stopBitVar.set('One')
stopBit_frame = tk.LabelFrame(serial_frame, text='Stop Bit')
stopBit_frame.grid(column=0, row=4)
stopBit_box = ttk.Combobox(stopBit_frame, text=stopBitVar, value=stopBitVar)
stopBit_box.grid(column=0, row=0)
stopBit_box['values'] = list(_stopBit.keys())

handShakeVar = tk.StringVar(window)
handShakeVar.set('None')
handShake_frame = tk.LabelFrame(serial_frame, text='HandShake')
handShake_frame.grid(column=0, row=5)
handShake_box = ttk.Combobox(handShake_frame, text=handShakeVar, value=handShakeVar)
handShake_box.grid(column=0, row=0)
handShake_box['values'] = _handShake_choices

# ____________________button for opening the serial port
open_photo = tk.PhotoImage(file='open.png')
open_label = tk.Label(serial_frame, image=open_photo).grid(column=0, row=6, sticky='w', padx=(10, 0), pady=(10, 0))
open_button = tk.Button(serial_frame, text='Open Port', command=open_port, width=10)
open_button.grid(column=0, row=6, pady=(10, 0), padx=(40, 0))

# ____________________label and button for clearing the receive data box details
clear_photo = tk.PhotoImage(file='clear2.png')
clear_Label = tk.Label(serial_frame, image=clear_photo).grid(column=0, row=7, sticky='w', padx=(10, 0), pady=(5, 0))
clear_button = tk.Button(serial_frame, text='Clear Output',
                         command=lambda: receive_box.delete('1.0', tk.END))
clear_button.grid(column=0, row=7, padx=(40, 0), pady=(5, 0))

# ____________________ABOUT message box button
about_photo = tk.PhotoImage(file='about.png')
about_label = tk.Label(serial_frame, image=about_photo).grid(column=0, row=8, sticky='w', padx=(10, 0), pady=(5, 0))
about_button = tk.Button(serial_frame, text='ABOUT', foreground='blue', width=10, command=show_info)
about_button.grid(column=0, row=8, pady=(5, 0), padx=(40, 0))

if __name__ == '__main__':
    run()
