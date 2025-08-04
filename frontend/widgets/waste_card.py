from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.properties import StringProperty, NumericProperty, ObjectProperty

Builder.load_string('''
<WasteCard>:
    orientation: 'vertical'
    spacing: 10
    size_hint_y: None
    height: 120
    padding: 10

    canvas.before:
        Color:
            rgba: 0.9, 0.9, 0.9, 1
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [10,]

    BoxLayout:
        size_hint_y: None
        height: 30
        spacing: 10

        Label:
            text: root.title
            font_size: 18
            halign: 'left'
            size_hint_x: 0.7

        Label:
            text: root.icon
            font_size: 20

    BoxLayout:
        size_hint_y: None
        height: 50
        spacing: 10

        Button:
            text: '-'
            size_hint_x: 0.2
            on_press: root.amount = max(0, root.amount - 1)

        Label:
            text: str(root.amount)
            font_size: 24
            size_hint_x: 0.6
            halign: 'center'

        Button:
            text: '+'
            size_hint_x: 0.2
            on_press: root.amount += 1

    Button:
        text: 'Добавить'
        size_hint_y: None
        height: 40
        on_press: root.add_waste()
''')


class WasteCard(BoxLayout):
    waste_type = StringProperty('')
    title = StringProperty('')
    icon = StringProperty('')
    amount = NumericProperty(0)
    on_add = ObjectProperty(None)

    def add_waste(self):
        if callable(self.on_add):
            self.on_add(self.waste_type, self.amount)