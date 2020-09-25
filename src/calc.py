import tkinter as tk


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
            button = tk.Button(
                gButtons,
                text=val['text'],
                fg=val.get('fg',"red"),
                command=val['command'])
            button.grid(
                row=val['row'],
                column=val.get('column',None),
                columnspan=val.get('columnspan',1),
                sticky=tk.W+tk.E
            )


class CalcModel:
    def __init__(self, controller):
        self.controller=controller
        self.accum=0.0
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
        self.accum=0.0
        self.display=0.0
        self.notify()

    def equal(self):
        try:
            self.display = self.calc[self.op](self.accum, self.display) if self.op else self.display
            self.accum=self.display
            self.notify()
        except ZeroDivisionError:
            self.err('Can\'t divide by 0.')
        except:
            self.err('PANIC.')

    def add(self):
        self.accum=self.display
        self.op="+"
        self.display=0.0
        self.notify()

    def substract(self):
        self.accum=self.display
        self.op="-"
        self.display=0.0
        self.notify()

    def divide(self):
        self.accum=self.display
        self.op="/"
        self.display=0.0
        self.notify()

    def multiplicate(self):
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
        self.visual.operator.set(f'ANS:{self.model.accum} OP: {self.model.op if self.model.op else ""}')

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

# Main App
controller = CalcController("Mi Calculadora", './src/calc.png')
