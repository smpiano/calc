import tkinter as tk
import time


class CalcVisual:

    def __init__(self, master, controller):
        self.controller = controller
        frame = tk.Frame(master)
        frame.grid(padx=15,pady=15)

        gDisplay = tk.LabelFrame(frame,text="display")
        gDisplay.grid(sticky=tk.W+tk.E,row=0,columnspan=4,padx=0,pady=10)

        self.display = tk.StringVar()
        display = tk.Label(
            gDisplay,
            textvariable=self.display,
            font=("Helvetica", 16))
        display.grid(sticky=tk.W+tk.E)

        self.operator = tk.StringVar()
        operator = tk.Label(
            gDisplay,
            textvariable=self.operator,
            fg="blue",
            font=("Helvetica", 8))
        operator.grid(sticky=tk.E)

        gButtons = tk.LabelFrame(frame,padx=5,pady=5)
        gButtons.grid(row=1)
        self.buttons = []
        for x in range(0,10):
            button = tk.Button(
                gButtons,
                text=x,
                fg="black",
                command=lambda y=x: self.controller.write(str(y)))
            if x!=0:
                button.grid(row=2+(x-1)//3,column=(x-1)%3)
            self.buttons.append(button)
        self.buttons[0].grid(row=5,column=0)


        self.operations={
            "equal":{
                "row":5,
                "column":2,
                "text":"=",
                "command":self.controller.equal
            },
            "comma":{
                "row":5,
                "column":1,
                "text":".",
                "command":lambda x='.':self.controller.write(x)
            },
            "clear":{
                "row":6,
                "columnspan":4,
                "text":"C",
                "command":self.controller.clear
            },
            "add":{
                "row":2,
                "column":3,
                "text":"+",
                "fg":"blue",
                "command":self.controller.add
            },
            "sub":{
                "row":3,
                "column":3,
                "text":"-",
                "fg":"blue",
                "command":self.controller.sub
            },
            "div":{
                "row":4,
                "column":3,
                "text":"/",
                "fg":"blue",
                "command":self.controller.div
            },
            "mult":{
                "row":5,
                "column":3,
                "text":"x",
                "fg":"blue",
                "command":self.controller.mul
            }
        }
        for name,val in self.operations.items():
            self.operations[name]['button'] = tk.Button(
                gButtons,
                text=val['text'],
                fg=val.get('fg',"red"),
                command=val['command'])
            self.operations[name]['button'].grid(
                row=val['row'],
                column=val.get('column',None),
                columnspan=val.get('columnspan',1),
                sticky=tk.W+tk.E
            )


class CalcModel:
    def __init__(self, controller):
        self.controller=controller
        self.accum=None
        self.display=0.0
        self.op=None
        self.calc={
            "+":lambda x,y:x+y,
            "-":lambda x,y:x-y,
            "/":lambda x,y:x/y,
            "*":lambda x,y:x*y
        }

    def update(self, num):
        self.display = num
        self.notify()

    def reset(self):
        self.accum=None
        self.display=0.0
        self.op = None
        self.notify()

    def equal(self):
        try:
            self.accum = self.calc[self.op](self.accum, self.display) if self.op else self.display
            self.op = None
            self.display=0.0
            self.notify()
        except ZeroDivisionError:
            self.err('Can\'t divide by 0.')
        except:
            self.err('PANIC.')

    def add(self):
        if self.op == '+':
            self.accum=self.calc["+"](self.accum, self.display)
        if self.accum == None:
            self.accum=self.display
        self.op="+"
        self.display=0.0
        self.notify()

    def substract(self):
        if self.op == '-':
            self.accum=self.calc["-"](self.accum, self.display)
        if self.accum == None:
            self.accum=self.display
        # self.accum=self.display
        self.op="-"
        self.display=0.0
        self.notify()

    def divide(self):
        if self.op == '/':
            self.accum=self.calc["/"](self.accum, self.display)
        if self.accum == None:
            self.accum=self.display
        # self.accum=self.display
        self.op="/"
        self.display=0.0
        self.notify()

    def multiplicate(self):
        if self.op == '*':
            self.accum=self.calc["*"](self.accum, self.display)
        if self.accum == None:
            self.accum=self.display
        self.op="*"
        self.display=0.0
        self.notify()

    def err(self, msg):
        self.controller.err(msg)

    def notify(self):
        self.controller.update()


class CalcController:
    def __init__(self, title, icon):
        self.model = CalcModel(self)
        self.root = tk.Tk()
        self.visual = CalcVisual(master=self.root, controller=self)
        img = tk.PhotoImage(file=icon)
        self.root.iconphoto(True,img)
        self.root.title(title)
        # self.root.bind("<Key>", self.key_events)
        self.root.bind("<KeyPress>", self.key_events_pressed)
        self.root.bind("<KeyRelease>", self.key_events_released)
        self.keys = {
            "KP_Divide":{ "command":self.div, "button":"div" },
            "KP_Multiply":{ "command":self.mul, "button":"mult" },
            "KP_Subtract":{ "command":self.sub, "button":"sub" },
            "KP_Add":{ "command":self.add, "button":"add" },
            "KP_Enter":{ "command":self.equal, "button":"equal" },
            "BackSpace":{ "command":self.clear, "button":"clear" },
            "KP_Decimal":{ "command":lambda x='.':self.write(x), "button":"comma" }
        }
        for x in range(0,10):
            self.keys[f'KP_{x}']={}
            self.keys[f'KP_{x}']['command']=lambda y=x:self.write(str(y))
        self.keypad_mapping = {
            "KP_Insert":"KP_0",
            "KP_End":"KP_1",
            "KP_Down":"KP_2",
            "KP_Next":"KP_3",
            "KP_Left":"KP_4",
            "KP_Begin":"KP_5",
            "KP_Right":"KP_6",
            "KP_Home":"KP_7",
            "KP_Up":"KP_8",
            "KP_Prior":"KP_9",
            "KP_Delete":"KP_Decimal",
            "KP_Divide":"KP_Divide",
            "KP_Multiply":"KP_Multiply",
            "KP_Subtract":"KP_Subtract",
            "KP_Add":"KP_Add",
            "KP_Enter":"KP_Enter",
            "BackSpace":"BackSpace"
        }
        self.clear()
        self.root.mainloop()

    def err(self, msg):
        self.visual.display.set(msg)

    def update(self):
        print("====")
        print(f"accum {self.model.accum}")
        print(f"display {self.model.display}")
        print(f"op {self.model.op}")

        d=self.model.display
        self.visual.display.set(
            int(d) if d.is_integer() else d
        )
        self.visual.operator.set(f'ANS:{self.model.accum if self.model.accum else "-"} OP: {self.model.op if self.model.op else ""}')

    def write(self, number):
        vd=self.visual.display.get()
        if number == '.':
            if not '.' in vd:
                now=vd + number
                self.visual.display.set(now)
        else:
            try:
                now=float(vd + number)
            except:
                self.err('BAD ENTRY.')
            self.model.update(now)

    def clear(self):
        print("Display reset")
        self.model.reset()

    def equal(self):
        self.model.equal()

    def add(self):
        self.model.add()

    def sub(self):
        self.model.substract()

    def div(self):
        self.model.divide()

    def mul(self):
        self.model.multiplicate()

    def key_events_pressed(self, event):
        if event.keysym in self.keys.keys():
            key_obj = self.keys[event.keysym]
            button = self.visual.buttons[int(event.char)] if event.char in [str(x) for x in range(0,10)] else self.visual.operations[key_obj['button']]['button']
            button['relief'] = tk.SUNKEN
            key_obj['command']()
        return False

    def key_events_released(self, event):
        if event.keysym in self.keypad_mapping.keys():
            keypad_map = self.keypad_mapping[event.keysym]
            key_obj = self.keys[keypad_map]
            button = self.visual.buttons[int(keypad_map[3])] if 'button' not in key_obj else self.visual.operations[key_obj['button']]['button']
            button['relief'] = tk.RAISED
        return False

    def key_events(self, event):
        print(f'event: {event}')
        if event.keysym in self.keys.keys():
            self.keys[event.keysym]['command']()


# Main App
controller = CalcController("Mi Calculadora", './assets/calc.png')
