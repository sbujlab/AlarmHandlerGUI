'''
Green Monster GUI Revamp
Code Commissioned 2019-01-04
Code by A.J. Zec
'''
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk


class GreenMonster:
    def __init__(self):
        self.green_color = '#3C8373'
        self.win = tk.Tk()
        self.win.title("Green Monster")
        self.win.configure(background=self.green_color)
        self.adc_options_vars = [tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar()]
        self.bm_test_setting = tk.StringVar()
        self.clean_setting = tk.StringVar()
        self.get_green_monster_style()
        self.create_widgets()

    def get_green_monster_style(self):
        style = ttk.Style()
        style.theme_create("green_monster", parent="alt", settings={
            "TNotebook": {"configure": {"background": self.green_color}},
            "TNotebook.Tab": {"configure": {"background": self.green_color}}})
        style.theme_use("green_monster")

    def quit(self):
        self.win.quit()
        self.win.destroy()
        exit()

    @staticmethod
    def set_text(entry, text):
        entry.delete(0, tk.END)
        entry.insert(0, str(text))
        return entry

    def timeboard_tab(self, tab):
        ch_frame = tk.LabelFrame(tab, text='CH', background=self.green_color, width=500)
        tk.Label(ch_frame, text='Ramp Delay', background=self.green_color).grid(
            row=0, column=0, padx=10, pady=5, sticky='W')
        self.set_text(tk.Entry(ch_frame), '40').grid(row=0, column=1)
        tk.Label(ch_frame, text='Integrate Time', background=self.green_color).grid(
            row=1, column=0, padx=10, pady=5, sticky='W')
        self.set_text(tk.Entry(ch_frame), '13200').grid(row=1, column=1)
        tk.Label(ch_frame, text='Oversampling', background=self.green_color).grid(
            row=2, column=0, padx=10, pady=5, sticky='W')
        self.set_text(tk.Entry(ch_frame), '0').grid(row=2, column=1)
        tk.Button(ch_frame, text='Get Settings', background=self.green_color).grid(row=3, column=0, pady=10)
        tk.Button(ch_frame, text='Apply Settings', background=self.green_color).grid(row=3, column=1, pady=10)
        ch_frame.pack(padx=20, pady=10, anchor='w')

    def vqwk_tab(self, tab):
        ch_frame = tk.LabelFrame(tab, text='CH', background=self.green_color, width=500)
        inj_frame = tk.LabelFrame(tab, text='Inj', background=self.green_color, width=500)
        tk.Label(ch_frame, text='Samples Per Block', background=self.green_color).grid(
            row=0, column=0, padx=10, pady=5, sticky='W')
        tk.Label(ch_frame, text='Gate Delay', background=self.green_color).grid(
            row=1, column=0, padx=10, pady=5, sticky='W')
        tk.Label(ch_frame, text='Number of Blocks', background=self.green_color).grid(
            row=2, column=0, padx=10, pady=5, sticky='W')
        self.set_text(tk.Entry(ch_frame), '4141').grid(row=0, column=1)
        self.set_text(tk.Entry(ch_frame), '10').grid(row=1, column=1)
        self.set_text(tk.Entry(ch_frame), '4').grid(row=2, column=1)
        tk.Label(inj_frame, text='Samples Per Block', background=self.green_color).grid(
            row=0, column=0, padx=10, pady=5, sticky='W')
        tk.Label(inj_frame, text='Gate Delay', background=self.green_color).grid(
            row=1, column=0, padx=10, pady=5, sticky='W')
        tk.Label(inj_frame, text='Number of Blocks', background=self.green_color).grid(
            row=2, column=0, padx=10, pady=5, sticky='W')
        self.set_text(tk.Entry(inj_frame), '496').grid(row=0, column=1)
        self.set_text(tk.Entry(inj_frame), '10').grid(row=1, column=1)
        self.set_text(tk.Entry(inj_frame), '4').grid(row=2, column=1)
        tk.Button(ch_frame, text='Get Settings', background=self.green_color).grid(row=3, column=0, pady=10)
        tk.Button(ch_frame, text='Apply Settings', background=self.green_color).grid(row=3, column=1, pady=10)
        tk.Button(inj_frame, text='Get Settings', background=self.green_color).grid(row=3, column=0, pady=10)
        tk.Button(inj_frame, text='Apply Settings', background=self.green_color).grid(row=3, column=1, pady=10)
        ch_frame.grid(row=0, column=0, padx=20, pady=10)
        inj_frame.grid(row=0, column=1, padx=20, pady=10)

    def adcs_tab(self, tab):
        ch_frame = tk.LabelFrame(tab, text='CH', background=self.green_color)
        labels = ['Label', 'Int', 'Conv', '-----', 'DAC', 'Settings', '-----', 'Sample by:']
        for i, label in enumerate(labels):
            tk.Label(ch_frame, text=label, background=self.green_color).grid(
                row=0, column=i, padx=8, pady=10, sticky='W')
        adcs = [8, 10, 10, 11]
        for i in range(1, 5):
            tk.Label(ch_frame, text='ADC ' + str(adcs[i - 1]), background=self.green_color).grid(
                row=i, column=0, padx=10, pady=10, sticky='W')
            self.set_text(tk.Entry(ch_frame, width=3), '3').grid(row=i, column=1, padx=10, pady=10)
            self.set_text(tk.Entry(ch_frame, width=3), '0').grid(row=i, column=2, padx=10, pady=10)
            setting = self.adc_options_vars[i-1]
            settings = ['Tri', 'Saw', 'Const', 'Off']
            setting.set('Tri')
            for j, s in enumerate(settings):
                tk.Radiobutton(ch_frame, text=s, variable=setting, value=s, background=self.green_color).grid(
                    row=i, column=j+3, padx=5, pady=10, sticky='W')
            sample_by = tk.IntVar()
            sample_by.set(1)
            tk.OptionMenu(ch_frame, sample_by, 1, 2, 4, 8).grid(row=i, column=7)
        tk.Button(ch_frame, text='Get Settings', background=self.green_color).grid(
            row=6, column=1, columnspan=2, pady=50, sticky='S')
        tk.Button(ch_frame, text='Apply Settings', background=self.green_color).grid(
            row=6, column=3, columnspan=2, pady=50, sticky='S')
        tk.Button(ch_frame, text='Cancel', background=self.green_color).grid(
            row=6, column=5, pady=50, sticky='S')
        ch_frame.pack(padx=20, pady=20)

    def bmw_tab(self, tab):
        bm_frame = tk.LabelFrame(tab, text='Beam Modulation', background=self.green_color)
        script_frame = tk.LabelFrame(bm_frame, text='Beam Modulation Script', background=self.green_color)
        script_frame.grid(row=0, column=0, pady=10, sticky='W')
        test_frame = tk.LabelFrame(bm_frame, text='Beam Modulation - TEST', background=self.green_color)
        test_frame.grid(row=1, column=0, pady=10, sticky='W')
        self.script_frame_layout(script_frame)
        self.test_frame_layout(test_frame)
        bm_frame.pack(padx=20, pady=20, anchor='w')

    def script_frame_layout(self, frame):
        tk.Label(frame, text='Kill Switch is OFF', background=self.green_color).grid(
            row=0, column=0, padx=10, pady=10, sticky='W')
        tk.Button(frame, text='Check Status', background=self.green_color).grid(
            row=0, column=1, padx=10, pady=10, sticky='W')
        tk.Label(frame, text='**********', background=self.green_color).grid(
            row=0, column=2, padx=10, pady=10, sticky='W')
        tk.Button(frame, text='Start Beam Modulation', background=self.green_color).grid(
            row=1, column=0, padx=10, pady=10, sticky='W')
        tk.Label(frame, text='Beam Modulation script is ****', background=self.green_color).grid(
            row=1, column=1, padx=10, pady=10, sticky='W')

    def test_frame_layout(self, frame):
        tk.Button(frame, text='Enable BMW Test', background=self.green_color).grid(
            row=0, column=0, columnspan=2, padx=10, pady=10)
        tk.Button(frame, text='Toggle Kill Switch', background=self.green_color).grid(
            row=0, column=2, columnspan=2, padx=10, pady=10)
        button_titles = ['MHF1C01H', 'MHF1C02H', 'MHF1C03V', 'MHF1C08H',
                         'MHF1C08V', 'MHF1C10H', 'MHF1C10V', 'SL Zone 20']
        self.bm_test_setting.set(button_titles[0])
        for r in range(0, 2):
            for c in range(0, 4):
                tk.Radiobutton(frame, text=button_titles[r*4+c], variable=self.bm_test_setting,
                               value=button_titles[r*4+c], background=self.green_color).grid(
                    row=r+1, column=c, padx=2, pady=2, sticky='W')
        self.set_text(tk.Entry(frame, width=12), '0').grid(row=3, column=0, padx=3, pady=3, sticky='W')
        tk.Label(frame, text='Set Point\n(mA or keV)', bg=self.green_color).grid(
            row=3, column=1, padx=5, pady=5, sticky='W')

    def vxworks_tab(self, tab):
        vx_frame = tk.Frame(tab, bg=self.green_color)
        tk.Button(vx_frame, text='Kill VXWorks Server, CH', bg=self.green_color, width=30).grid(
            row=0, column=0, padx=2, pady=2)
        tk.Button(vx_frame, text='Kill VXWorks Server, Inj', bg=self.green_color, width=30).grid(
            row=1, column=0, padx=2, pady=2)
        vx_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    def scan_util_tab(self, tab):
        util_frame = tk.LabelFrame(tab, text='SCAN UTILITY', bg=self.green_color)
        options = ['CLEAN', 'NOT CLEAN']
        self.clean_setting.set(options[0])
        for i, op in enumerate(options):
            tk.Radiobutton(util_frame, text=op, variable=self.clean_setting,
                           value=op, bg=self.green_color).grid(row=0, column=i, padx=10, pady=10, sticky='W')
        inj_frame = tk.LabelFrame(util_frame, text='Inj', bg=self.green_color)
        for r in range(0, 4):
            tk.Label(inj_frame, text='Set Point ' + str(r+1), bg=self.green_color).grid(
                row=r, column=0, padx=15, pady=10, sticky='E')
            self.set_text(tk.Entry(inj_frame), '0').grid(row=r, column=1, padx=10, pady=10, sticky='W')
        inj_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky='W')
        tk.Button(util_frame, text='Check Status', bg=self.green_color).grid(row=2, column=0, padx=10, pady=10)
        tk.Button(util_frame, text='Set Values', bg=self.green_color).grid(row=2, column=1, padx=10, pady=10)
        util_frame.pack(padx=20, pady=20, anchor='w')

    def create_widgets(self):
        gui_style = ttk.Style()
        gui_style.configure('My.TButton', foreground=self.green_color)
        gui_style.configure('My.TFrame', background=self.green_color)

        tab_control = ttk.Notebook(self.win)
        tab_titles = ['TimeBoard', 'VQWK ADCs', 'ADC18s, CH', 'BMW', 'VXWorks Server', 'ScanUtil']
        for title in tab_titles:
            tab = ttk.Frame(tab_control, width=800, height=600, style="My.TFrame")
            tab_control.add(tab, text=title)
            if 'Time' in title:
                self.timeboard_tab(tab)
            elif 'VQWK' in title:
                self.vqwk_tab(tab)
            elif 'ADC18s' in title:
                self.adcs_tab(tab)
            elif 'BMW' in title:
                self.bmw_tab(tab)
            elif 'VXWorks' in title:
                self.vxworks_tab(tab)
            elif 'Scan' in title:
                self.scan_util_tab(tab)
        tab_control.grid(row=0, column=0, columnspan=2)
        fenway = ImageTk.PhotoImage(Image.open('Green_Monster.jpg'))
        fenway_pahk = tk.Label(self.win, image=fenway, background=self.green_color)
        fenway_pahk.image = fenway
        fenway_pahk.grid(row=1, column=0, padx=5, pady=10, sticky='W')
        tk.Button(self.win, text='QUIT', command=quit, background=self.green_color, width=20, height=4).grid(
            row=1, column=1, padx=15, pady=5, sticky='SE')


green_monster = GreenMonster()
green_monster.win.mainloop()
