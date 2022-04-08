from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.config import Config
from time import sleep
import ctypes


Config.set('graphics', 'resizable', 0)
Config.set('graphics', 'width', 600)
Config.set('graphics', 'height', 620)


def get_by_id(index_id):
    return ctypes.cast(index_id, ctypes.py_object).value


class TicTacToe(App):
    def __init__(self):
        super().__init__()
        self.move = 0
        self.now_move = 'X'
        self.field_matrix = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.move_label = Label(text=f'Now move: X', font_size=24)
        self.play_field = GridLayout(cols=3, size_hint=(1,0.85))
        for i in range(0, 9):
            now_button = Button(text='', background_color=(0.2, 0.2, 0.2), font_size=48)
            self.field_matrix[i] = id(now_button)
            now_button.bind(on_press=self.call_tap)
            self.play_field.add_widget(now_button)
        self.id_matrix = self.field_matrix.copy()
        self.win_lines = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),
            (0, 3, 6), (1, 4, 7), (2, 5, 8),
            (0, 4, 8), (2, 4, 6)]
        self.main_layout = BoxLayout(orientation='vertical')
        self.up_layout = BoxLayout(size_hint=(1, 0.15))
        self.rest_button = Button(text='Restart', on_press=self.restart, font_size=24, background_color=(0.3, 0.0, 0.0))

    def call_tap(self, instance):
        self.update_now_move()
        if instance.text == '':
            index = self.field_matrix.index(id(instance))
            if self.move % 2 == 0:
                instance.text = 'X'
                self.field_matrix[index] = 'X'
            else:
                instance.text = 'O'
                self.field_matrix[index] = 'O'
            self.move += 1
            instance.disabled = True
        if self.move == 9:
            self.move_label.text = f'Tie!'
        self.check_win()

    def change_color(self, instance):
        instance.background_color = (0.8, 0.2, 0.2)
        sleep(0.5)
        instance.background_color = (0.2, 0.2, 0.2)

    def update_now_move(self):
        if self.move % 2 != 0:
            self.now_move = 'X'
        else:
            self.now_move = 'O'
        self.move_label.text = f'Now move: {self.now_move}'

    def restart(self, *args):
        self.stop()
        return TicTacToe().run()

    def check_win(self):
        for elem in self.win_lines:
            res1 = elem[0]
            res2 = elem[1]
            res3 = elem[2]
            if self.field_matrix[res1] == self.field_matrix[res2] == self.field_matrix[res3]:
                for i in elem:
                    get_by_id(self.id_matrix[i]).background_color = (0, 0.8, 0)
                    self.move_label.text = f'{self.field_matrix[res1]} WON!'
                    self.disable_all_btns()

    def disable_all_btns(self):
        for elem in self.id_matrix:
            res = get_by_id(elem)
            res.disabled = True

    def build(self):
        self.move_label.text = f'Now move: {self.now_move}'
        self.up_layout.add_widget(self.move_label)
        self.up_layout.add_widget(self.rest_button)
        self.main_layout.add_widget(self.up_layout)
        self.main_layout.add_widget(self.play_field)
        return self.main_layout


TicTacToe().run()
