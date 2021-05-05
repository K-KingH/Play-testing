from kivy.uix.gridlayout import GridLayout
# from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.app import App
from kivy.uix.textinput import TextInput
from datetime import datetime, date
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse, Line
from random import random
import os


class Control(GridLayout):
    def __init__(self, **kwargs):
        super(Control, self).__init__(**kwargs)
        self.cols = 2

        if os.path.isfile("details.txt"):
            with open("details.txt", "r") as f:
                s = f.read().split(",")
                prev_user = s[0]
                prev_email = s[1]
                prev_pass = s[2]
        else:
            prev_user = ""
            prev_email = ""
            prev_pass = ""

        self.add_widget(Label(text="Username:"))
        self.user = TextInput(text=prev_user, multiline=False, write_tab=False)
        self.add_widget(self.user)

        self.add_widget(Label(text="Email:"))
        self.email = TextInput(text=prev_email, multiline=False, write_tab=False)
        self.add_widget(self.email)

        self.add_widget(Label(text="Password:"))
        self.password = TextInput(text=prev_pass, multiline=False, write_tab=False)
        self.add_widget(self.password)

        self.add_widget(Label())
        self.joining = Button(text="Join")
        self.joining.bind(on_press=self.btn_click)
        self.add_widget(self.joining)

    def btn_click(self, instance):
        user = self.user.text
        email = self.email.text
        password = self.password.text
        ahead = datetime.now().strftime("%H:%M:%S")
        d = date.today()

        with open("details.txt", "w") as f:
            f.write(f"{user},{email},{password}")
        m = f"Joined on {d} at {ahead} as {user}.\n Email: {email}"

        Drake.info.update(m)
        Drake.sm.current = "Display Info"


class MyPaintWidget(Widget):
    def on_touch_down(self, touch):
        color = (random(), random(), random())
        with self.canvas:
            Color(*color)
            d = 45.
            Ellipse(pos=(touch.x - d / 2, touch.y - d / 2), size=(d, d))
            touch.ud['line'] = Line(points=(touch.x, touch.y))

    def on_touch_move(self, touch):
        touch.ud['line'].points += [touch.x, touch.y]


class Information(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1

        self.message = Label(font_size=25, halign="center", valign="middle")
        self.message.bind(width=self.update_text_width)
        self.add_widget(self.message)

        self.ret = Button(text="Return to Home Screen")
        self.ret.bind(on_press=self.back)
        self.add_widget(self.ret)

    def update_text_width(self, *_):
        self.message.text_size = (self.message.width*0.9, None)

    def update(self, message):
        self.message.text = message

    @staticmethod
    def back(instance):
        Drake.sm.current = "Movie"


class BackApp(App):
    def build(self):
        self.sm = ScreenManager()

        self.fill = Control()
        screen = Screen(name="Fill In")
        screen.add_widget(self.fill)
        self.sm.add_widget(screen)

        self.info = Information()
        screen = Screen(name="Display Info")
        screen.add_widget(self.info)
        self.sm.add_widget(screen)

        self.movie = MyPaintWidget()
        screen = Screen(name="Movie")
        screen.add_widget(self.movie)
        self.sm.add_widget(screen)

        return self.sm


if __name__ == "__main__":
    Drake = BackApp()
    Drake.run()
