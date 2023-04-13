import tkinter as tk
import pyyni.pyyni as yni
import os
import tkinter.filedialog as fd

COLOR_PLACEHOLDER = '#707070'
COLOR_WINDOW_BACKGROUND = '#e5e5e5'
COLOR_WIDGET_BACKGROUND = '#d0d0d0'
COLOR_FONT = '#000000'

button_status = False


class BaseEntry(tk.Entry):
    def __init__(self, master=None, placeholder='', value=None, **kwargs):
        super().__init__(master, **kwargs)

        self.placeholder = placeholder
        self.placeholder_color = COLOR_PLACEHOLDER
        self.fg = self.placeholder_color
        self.color_sv = self['fg']
        self.is_placeholder = True

        self.bind('<FocusIn>', self.erase)
        self.bind('<FocusOut>', self.fill)

        if value == None:
            self.fill()
        else:
            self.is_placeholder = False
            self.insert(0, value)
            self.config(fg=self.color_sv)

    def fill(self, *args):
        if self.get() == '':
            self.is_placeholder = True
            self.insert(0, self.placeholder)
            self.config(fg=self.placeholder_color)

    def erase(self, *args):
        if self.is_placeholder:
            self.is_placeholder = False
            self.delete(0, 'end')
            self['fg'] = self.color_sv


class MainWin:
    def __init__(self):
        self.win = tk.Tk()
        self.win.title("YNI GUI")
        self.win.geometry("1000x500+100+100")
        self.win.resizable(True, True)
        self.win.config(bg=COLOR_WINDOW_BACKGROUND)

        self.textsave = ''
        self.basesave = None
        self.filename = None

        self.input_stage()
        self.win.protocol('WM_DELETE_WINDOW', self.on_close)

    def on_close(self):
        if tk.messagebox.askyesno('확인', '정말 종료하겠습니까?'):
            self.quit()

    def run(self):
        self.win.mainloop()

    def quit(self):
        self.win.destroy()
        del (self)

    def input_stage(self):
        menu = tk.Menu(self.win)
        menu_file = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="File", menu=menu_file)
        menu_file.add_command(
            label="Open", command=self.input_menu_file_open)
        menu_file.add_command(
            label="Save", command=self.input_menu_file_save)
        menu_file.add_command(label="Save as...",
                              command=self.input_menu_file_save_as)
        self.win.config(menu=menu)

        self.scroll = tk.Scrollbar(self.win, orient='vertical')
        self.scroll.place(relx=.98, rely=.01, relheight=.90)

        self.textbox = tk.Text(self.win, fg=COLOR_FONT, bg=COLOR_WIDGET_BACKGROUND,
                               yscrollcommand=self.scroll.set)
        self.textbox.insert(0.0, self.textsave)
        self.textbox.place(relx=.01, rely=.01, relwidth=.97,
                           relheight=.90)

        self.scroll.config(command=self.textbox.yview)

        self.basebox_vcmd = self.win.register(self.basebox_validate)
        self.basebox = BaseEntry(self.win, placeholder='2', value=self.basesave, fg=COLOR_FONT, bg=COLOR_WIDGET_BACKGROUND, validate='all',
                                 validatecommand=(self.basebox_vcmd, '%P'))

        self.basebox.place(relx=.7, rely=.93, relwidth=.03,
                           relheight=.05)

        self.baselabel = tk.Label(
            self.win, fg=COLOR_FONT, bg=COLOR_WINDOW_BACKGROUND, text='진수')
        self.baselabel.place(relx=.73, rely=.93)

        self.button = tk.Button(self.win, text='변환하기',
                                command=self.on_output_btn_pressed)
        self.button.place(relx=.85, rely=.93, relwidth=.1, relheight=.05)

    def input_menu_file_open(self):
        self.textsave = self.textbox.get(0.0, 'end - 1c')
        if self.textsave != '':
            answer = tk.messagebox.askyesno(
                '파일 열기', '지금까지 쓴 것이 삭제됩니다. 진행하겠습니까?')
            if not answer:
                return

        filename = fd.askopenfilename(initialdir="/", title="파일 열기",
                                      filetypes=(("Text Files", "*.txt"),
                                                 ("all files", "*.*")))
        if filename == ():
            return

        self.filename = filename
        f = open(self.filename, 'r')
        self.textsave = f.read()

        for widget in self.win.winfo_children():
            widget.destroy()
        self.input_stage()

    def input_menu_file_save(self):
        self.textsave = self.textbox.get(0.0, 'end - 1c')
        if self.filename != None and os.path.exists(self.filename):
            f = open(self.filename, 'w', encoding="utf-8")
            f.write(self.textsave)
        else:
            self.input_menu_file_save_as()

    def input_menu_file_save_as(self):
        self.textsave = self.textbox.get(0.0, 'end - 1c')
        filename = fd.asksaveasfilename(initialdir="/", title="파일 저장",
                                        filetypes=(("Text Files", "*.txt"),
                                                   ("all files", "*.*")))
        if filename == ():
            return

        self.filename = filename
        f = open(self.filename, 'w', encoding="utf-8")
        f.write(self.textsave)

    def basebox_validate(self, P):
        if len(P) == 0:
            return True
        if P.isdigit() and len(P) <= 2:
            return True
        return False

    def on_output_btn_pressed(self):
        try:
            self.basesave = int(self.basebox.get())
        except:
            self.basesave = int(self.basebox.placeholder)

        # remove LF at the end
        self.textsave = self.textbox.get(0.0, 'end - 1c')

        self.outtext = yni.to_base_str(self.textsave, self.basesave)
        for widget in self.win.winfo_children():
            widget.destroy()

        self.output_stage()

    def output_stage(self):
        menu = tk.Menu(self.win)
        menu_file = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="File", menu=menu_file)
        menu_file.add_command(label="Save as...",
                              command=self.output_menu_file_save_as)
        self.win.config(menu=menu)

        self.scroll = tk.Scrollbar(self.win, orient='vertical')
        self.scroll.place(relx=.98, rely=.01, relheight=.9)

        self.output = tk.Text(self.win, fg=COLOR_FONT,
                              bg=COLOR_WIDGET_BACKGROUND, yscrollcommand=self.scroll.set, wrap='word', spacing2=10)
        self.output.insert('end', self.outtext)
        self.output.configure(state="disabled")
        self.output.place(relx=.01, rely=.01, relwidth=.97,
                          relheight=.9)

        self.scroll.config(command=self.output.yview)

        self.returnbtn = tk.Button(self.win, text='돌아가기',
                                   command=self.on_return_btn_pressed)
        self.returnbtn.place(relx=.1, rely=.93, relwidth=.1, relheight=.05)

    def output_menu_file_save_as(self):
        filename = fd.asksaveasfilename(initialdir="/", title="파일 저장",
                                        filetypes=(("Text Files", "*.txt"),
                                                   ("all files", "*.*")))
        if filename == ():
            return

        f = open(filename, 'w', encoding="utf-8")
        f.write(self.outtext)

    def on_return_btn_pressed(self):
        for widget in self.win.winfo_children():
            widget.destroy()
        self.input_stage()


def main():
    w = MainWin()
    w.run()


if __name__ == '__main__':
    main()
