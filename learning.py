from kivy.uix.gridlayout import GridLayout
from kivy.app import App
from datetime import datetime, date


class Exp(GridLayout):
    pass


class Trust(App):
    def build(self):
        return Exp()

    def btn_click(self, *args):
        user = self.root.ids.user.text
        email = self.root.ids.email.text
        password = self.root.ids.password.text
        d = datetime.now().strftime("%H:%M:%S")
        now = date.today()

        with open("pass.txt", "w") as f:
            f.write(f"{user}, {email}, {password}")
        m = f"Joined on {now} at {d} as {user}.\n Email: {email}"


Trust().run()
