#
# This is a very simple serial terminal with GUI which is tkinter
#
# In this code i used  https://github.com/pyserial/pyserial
#
# this code is written by Amir otd :)))

import tkinter as tk
from tkinter import ttk, messagebox
from threading import Thread
import serial  # pip install pyserial


_baudrate_choices = [50, 75, 110, 134, 150, 200, 300, 600, 1200, 1800, 2400, 4800,
                     9600, 19200, 38400, 57600, 115200, 230400, 460800, 500000,
                     576000, 921600, 1000000, 1152000, 1500000, 2000000, 2500000,
                     3000000, 3500000, 4000000]

_handShake_choices = ['None', 'RTS/CTS', 'Xon/Xoff']

_dataSize = {5: serial.FIVEBITS, 6: serial.SIXBITS, 7: serial.SEVENBITS, 8: serial.EIGHTBITS}
_stopBit = {'One': serial.STOPBITS_ONE, 'OnePointFive': serial.STOPBITS_ONE_POINT_FIVE,
            'Two': serial.STOPBITS_TWO}
_parity = {'None': serial.PARITY_NONE, 'Even': serial.PARITY_EVEN, 'Odd': serial.PARITY_ODD,
           'Mark': serial.PARITY_MARK, 'space': serial.PARITY_SPACE}

_stop_thread = True
ser = serial.Serial()


class MySerialWindow(tk.Tk):

    def __init__(self):

        super().__init__()

        # ____________________tkinter initial window configuration

        self.title("Serial Terminal")
        self.geometry('1000x470+200+100')
        self['padx'] = 20
        self['pady'] = 20

        # ____________________column configuration
        self.grid_columnconfigure(0, weight=10)
        self.grid_columnconfigure(1, weight=1)

        # ____________________row configuration
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=15)

        # ____________________receive data box configuration
        self.receive_box = tk.Text(self, height=8)
        self.receive_box.grid(column=0, row=1, sticky='nsew', padx=(0, 10))
        self.scroll = tk.Scrollbar(self, orient=tk.VERTICAL, command=self.receive_box.yview)
        self.scroll.grid(column=0, row=1, sticky='nse')
        self.receive_box["yscrollcommand"] = self.scroll.set

        # ____________________send data frame configuration
        self.send_frame = tk.LabelFrame(self, text='Send Data')
        self.send_frame.grid(column=0, row=0, sticky='wens', padx=(0, 10), pady=(0, 10))
        self.send_frame['padx'] = 10
        self.send_box = tk.Text(self.send_frame, height=1)
        self.send_box.grid(column=0, row=0, padx=(10, 5))
        self.send_button = tk.Button(self.send_frame, text='Send', width=7, command=self.send_data)
        self.send_button.grid(column=1, row=0, padx=(10, 10))

        # ____________________serial settings box configuration
        self.serial_frame = tk.LabelFrame(self, text='Serial Port Settings')
        self.serial_frame.grid(column=1, row=0, rowspan=2, sticky='esn', padx=(10, 5))

        self.portName_var = tk.StringVar(self)
        self.portName_frame = tk.LabelFrame(self.serial_frame, text='Port Name')
        self.portName_box = tk.Entry(self.portName_frame, textvariable=self.portName_var)
        self.portName_frame.grid(column=0, row=0)
        self.portName_box.grid(column=0, row=0)

        self.baudVar = tk.IntVar(self)
        self.baudVar.set(9600)
        self.baudrate_frame = tk.LabelFrame(self.serial_frame, text='Baudrate')
        self.baudrate_frame.grid(column=0, row=1)
        self.baudrate_box = ttk.Combobox(self.baudrate_frame, text=self.baudVar, value=self.baudVar)
        self.baudrate_box.grid(column=0, row=0)
        self.baudrate_box['values'] = _baudrate_choices

        self.dataVar = tk.IntVar(self)
        self.dataVar.set(8)
        self.dataSize_frame = tk.LabelFrame(self.serial_frame, text='Data Size')
        self.dataSize_frame.grid(column=0, row=2)
        self.dataSize_box = ttk.Combobox(self.dataSize_frame, text=self.dataVar, value=self.dataVar)
        self.dataSize_box.grid(column=0, row=0)
        self.dataSize_box['values'] = list(_dataSize.keys())

        self.parityVar = tk.StringVar(self)
        self.parityVar.set('None')
        self.parity_frame = tk.LabelFrame(self.serial_frame, text='Parity')
        self.parity_frame.grid(column=0, row=3)
        self.parity_box = ttk.Combobox(self.parity_frame, text=self.parityVar, value=self.parityVar)
        self.parity_box.grid(column=0, row=0)
        self.parity_box['values'] = list(_parity.keys())

        self.stopBitVar = tk.StringVar(self)
        self.stopBitVar.set('One')
        self.stopBit_frame = tk.LabelFrame(self.serial_frame, text='Stop Bit')
        self.stopBit_frame.grid(column=0, row=4)
        self.stopBit_box = ttk.Combobox(self.stopBit_frame, text=self.stopBitVar, value=self.stopBitVar)
        self.stopBit_box.grid(column=0, row=0)
        self.stopBit_box['values'] = list(_stopBit.keys())

        self.handShakeVar = tk.StringVar(self)
        self.handShakeVar.set('None')
        self.handShake_frame = tk.LabelFrame(self.serial_frame, text='HandShake')
        self.handShake_frame.grid(column=0, row=5)
        self.handShake_box = ttk.Combobox(self.handShake_frame, text=self.handShakeVar, value=self.handShakeVar)
        self.handShake_box.grid(column=0, row=0)
        self.handShake_box['values'] = _handShake_choices

        # ____________________button for opening the serial port
        self.open_photo = tk.PhotoImage(file='./icons/open.png')
        self.close_photo = tk.PhotoImage(file='./icons/close.png')
        self.open_label = tk.Label(self.serial_frame, image=self.open_photo)
        self.open_label.grid(column=0, row=6, sticky='w', padx=(10, 0), pady=(10, 0))
        self.open_button = tk.Button(self.serial_frame, text='Open Port', command=self.open_port, width=10)
        self.open_button.grid(column=0, row=6, pady=(10, 0), padx=(40, 0))

        # ____________________label and button for clearing the receive data box details
        self.clear_photo = tk.PhotoImage(file='./icons/clear.png')
        self.clear_Label = tk.Label(self.serial_frame, image=self.clear_photo)
        self.clear_Label.grid(column=0, row=7, sticky='w', padx=(10, 0), pady=(5, 0))
        self.clear_button = tk.Button(self.serial_frame, text='Clear Output',
                                      command=lambda: self.receive_box.delete('1.0', tk.END))
        self.clear_button.grid(column=0, row=7, padx=(40, 0), pady=(5, 0))

        # ____________________Plot button
        self.plot_photo = tk.PhotoImage(file='./icons/chart.png')
        self.plot_label = tk.Label(self.serial_frame, image=self.plot_photo)
        self.plot_label.grid(column=0, row=8, sticky='w', padx=(10, 0), pady=(5, 0))
        plot_button = tk.Button(self.serial_frame, text='Plot on Chart', width=10)
        plot_button.grid(column=0, row=8, pady=(5, 0), padx=(40, 0))

        # ____________________ABOUT message box button
        self.about_photo = tk.PhotoImage(file='./icons/about.png')
        self.about_label = tk.Label(self.serial_frame, image=self.about_photo)
        self.about_label.grid(column=0, row=9, sticky='w', padx=(10, 0), pady=(5, 0))
        self.about_button = tk.Button(self.serial_frame, text='ABOUT', foreground='blue', width=10,
                                      command=self.show_info)
        self.about_button.grid(column=0, row=9, pady=(5, 0), padx=(40, 0))

    def open_port(self):
        try:
            ser.port = self.portName_var.get()
            ser.baudrate = self.baudVar.get()
            ser.bytesize = _dataSize[self.dataVar.get()]
            ser.parity = _parity[self.parityVar.get()]
            ser.stopbits = _stopBit[self.stopBitVar.get()]

            if self.handShakeVar.get() == 'RTS/CTS':
                ser.rtscts = 1
                ser.xonxoff = False
            elif self.handShakeVar.get() == 'Xon/Xoff':
                ser.xonxoff = 1
                ser.rtscts = False
            else:
                ser.xonxoff = False
                ser.rtscts = False

            ser.open()
            open_label_1 = tk.Label(self.serial_frame, image=self.close_photo)
            open_label_1.grid(column=0, row=6, sticky='w', padx=(10, 0), pady=(10, 0))
            open_button_1 = tk.Button(self.serial_frame, text='Close Port', command=self.close_port, width=10)
            open_button_1.grid(column=0, row=6, pady=(10, 0), padx=(40, 0))

            try:
                task.start()
            except RuntimeError:
                global _stop_thread
                _stop_thread = True

        except serial.serialutil.SerialException:
            print("Please Enter a Valid Port Name!!")
            messagebox.showerror("Error", "Please Enter a Valid Port Name!!")

    def print_result(self):
        while True:
            global _stop_thread
            while _stop_thread:
                self.receive_box.insert(tk.END, ser.read())
                self.receive_box.see(tk.END)
                print(ser.baudrate, ser.bytesize, ser.parity, ser.stopbits,
                      ser.rtscts, ser.xonxoff, ser.is_open is False)

    def close_port(self):
        global _stop_thread
        _stop_thread = False
        ser.close()

        open_label_1 = tk.Label(self.serial_frame, image=self.open_photo)
        open_label_1.grid(column=0, row=6, sticky='w', padx=(10, 0), pady=(10, 0))
        open_button_1 = tk.Button(self.serial_frame, text='Open Port', command=self.open_port, width=10)
        open_button_1.grid(column=0, row=6, pady=(10, 0), padx=(40, 0))

    def send_data(self):
        try:
            temp_send_data = self.send_box.get("1.0", "end-1c")
            ser.write(temp_send_data.encode('utf-8'))
            print(temp_send_data)
        except serial.serialutil.SerialException:
            print("First Open a Port!!!")
            messagebox.showerror("Error", "First Open a Port!!!")

    @staticmethod
    def show_info():
        print(":)))))")
        messagebox.showinfo("About", "This program is written in python and\n it's"
                                     " using pyserial library and tkinter GUI")


if __name__ == '__main__':
    app = MySerialWindow()
    task = Thread(target=app.print_result)
    task.setDaemon(True)
    app.mainloop()
