"""
UI Page module.

This module defines the UIPage class, which represents the user input page of the application.
It allows users to view, add, edit, and delete bills, as well as set the monthly utility amount.
"""

import kivy

kivy.require('2.3.0')

from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle
from kivy.storage.jsonstore import JsonStore


class UIPage(Screen):
    """
    User Interface page class.

    This class represents the user interface page of the application. It allows users to view,
    add, edit, and delete bills, as well as set the monthly utility amount.
    """

    def __init__(self, **kwargs):
        """
        Initialize the UIPage.

        This method sets up the user interface layout, including the current bills display,
        add/edit bills section, and utility bill section. It also loads the existing bills
        and utility amount from JSON storage.
        """
        super().__init__(**kwargs)
        self.store = JsonStore('bills.json')
        self.utility_store = JsonStore('utility.json')

        # Set up main layout and top back button box
        layout = GridLayout(cols=1, spacing=20, padding=30)
        top_box = BoxLayout(orientation='vertical', size_hint=(1, None), height=50)

        back_button = Button(
            text='Home',
            background_normal='',
            background_color=(14/255, 40/255, 62/255, 1),
            color=(1, 1, 1, 1),
            font_size=18,
            font_name='Roboto',
            size_hint=(0.09, 1),
            on_press=self.go_back
        )
        top_box.add_widget(back_button)
        layout.add_widget(top_box)

        # Set up display for current bills
        current_bills_label = Label(text='Current Bills', size_hint=(1, None), height=50, font_size=40, font_name='Roboto', bold=True)
        layout.add_widget(current_bills_label)

        scroll_view = ScrollView(size_hint=(1, 0.3))
        self.current_bills_box = GridLayout(cols=1, spacing=5, size_hint_y=None)
        self.current_bills_box.bind(minimum_height=self.current_bills_box.setter('height'))
        scroll_view.add_widget(self.current_bills_box)
        layout.add_widget(scroll_view)

        add_bill_label = Label(text='Add/Edit Bills', size_hint=(1, None), height=50, font_size=40, font_name='Roboto', bold=True)
        layout.add_widget(add_bill_label)

        # Sets up input text boxes in own grid layout
        add_edit_layout = GridLayout(cols=2, spacing=20, size_hint=(1, None), height=300, padding=10)  # Main Layout that stores both utility and adding bills

        add_bill_panel = GridLayout(cols=1, padding=20, spacing=10)
        add_bill_panel_bg = Rectangle(size=add_bill_panel.size, pos=add_bill_panel.pos)
        add_bill_panel.bind(size=self._update_rect, pos=self._update_rect)
        with add_bill_panel.canvas.before:
            Color(0, 0.1, 0.1, 1)
            add_bill_panel.rect = add_bill_panel_bg

        add_bill_sub_label = Label(
            text='Input Bills',
            height=30,
            font_size=30,
            font_name='Roboto',
            size_hint=(1, None)
        )
        add_bill_panel.add_widget(add_bill_sub_label)

        bill_name_input = TextInput(
            multiline=False,
            hint_text='Bill name',
            font_name='Roboto',
            size_hint=(1, None),
            height=50
        )
        add_bill_panel.add_widget(bill_name_input)

        bill_amount_input = TextInput(
            multiline=False,
            hint_text='USD Amount',
            font_name='Roboto',
            size_hint=(1, None),
            height=50
        )
        add_bill_panel.add_widget(bill_amount_input)

        add_button = Button(
            text='Add Bill',
            background_normal='',
            background_color=(14/255, 40/255, 62/255, 1),
            font_size=24,
            font_name='Roboto',
            size_hint=(1, None),
            height=50,
            on_press=lambda x: self.add_update_bill(bill_name_input.text, bill_amount_input.text)
        )
        add_bill_panel.add_widget(add_button)

        utility_bill_panel = GridLayout(cols=1, padding=20, spacing=10)
        utility_bill_panel_bg = Rectangle(size=utility_bill_panel.size, pos=utility_bill_panel.pos)
        utility_bill_panel.bind(size=self._update_rect, pos=self._update_rect)
        with utility_bill_panel.canvas.before:
            Color(0.1, 0.1, 0.1, 1)
            utility_bill_panel.rect = utility_bill_panel_bg

        utility_label = Label(
            text='Monthly Utility (Average)',
            height=30,
            font_size=30,
            font_name='Roboto',
            size_hint=(1, None)
        )
        utility_bill_panel.add_widget(utility_label)

        self.utility_display = Label(
            text='',
            size_hint=(1, None),
            height=30,
            font_name='Roboto'
        )
        utility_bill_panel.add_widget(self.utility_display)
        self.load_utility()

        utility_input = TextInput(
            multiline=False,
            hint_text='Enter utility amount',
            font_name='Roboto',
            size_hint=(1, None),
            height=50
        )
        utility_bill_panel.add_widget(utility_input)

        utility_button = Button(
            text='Update Utility',
            background_normal='',
            background_color=(14/255, 40/255, 62/255, 1),
            color=(1, 1, 1, 1),
            font_size=20,
            font_name='Roboto',
            size_hint=(1, None),
            height=50,
            on_press=lambda x: self.update_utility(utility_input.text)
        )
        utility_bill_panel.add_widget(utility_button)

        add_edit_layout.add_widget(add_bill_panel)
        add_edit_layout.add_widget(utility_bill_panel)
        layout.add_widget(add_edit_layout)

        self.add_widget(layout)
        self.load_bills()
        self.load_utility()

        with self.canvas.before:
            Color(0, 24/255, 44/255, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        """
        Update the rectangle size and position when the window is resized.

        Args:
            instance (Widget): The widget instance.
            value (list): The size or position value.
        """
        instance.rect.pos = instance.pos
        instance.rect.size = instance.size

    def add_update_bill(self, bill_name, bill_amount):
        """
        Add or update a bill in the JSON storage.

        Args:
            bill_name (str): The name of the bill.
            bill_amount (str): The amount of the bill.
        """
        if bill_name and bill_amount:
            self.store.put(bill_name, amount=bill_amount)
            self.load_bills()

    def load_bills(self):
        """
        Load the bills from JSON storage and display them.
        """
        self.store = JsonStore('bills.json')
        self.current_bills_box.clear_widgets()
        for bill_name in self.store.keys():
            bill_amount = self.store.get(bill_name)['amount']
            bill_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=100, padding=30)
            with bill_box.canvas.before:
                Color(14/255, 40/255, 62/255, 1)  # Lighter dark blue color for content box
                bill_box.rect = Rectangle(size=bill_box.size, pos=bill_box.pos)
            bill_box.bind(size=self._update_bill_rect, pos=self._update_bill_rect)

            bill_info = BoxLayout(orientation='horizontal', size_hint=(0.6, 1))
            bill_name_label = Label(text=f"{bill_name}", size_hint=(0.8, 1), font_name='Roboto')
            bill_info.add_widget(bill_name_label)
            bill_amount_label = Label(text=f"${bill_amount}", size_hint=(0.2, 1), font_name='Roboto')
            bill_info.add_widget(bill_amount_label)
            bill_box.add_widget(bill_info)

            delete_button = Button(
                text='Delete',
                size_hint=(0.2, 1),
                font_size=14,
                font_name='Roboto',
                background_normal='',
                background_color=(0, 24/255, 44/255),
                color=(1, 1, 1, 1),
                on_press=lambda x, bill=bill_name: self.delete_bill(bill)
            )
            bill_box.add_widget(delete_button)

            self.current_bills_box.add_widget(bill_box)

    def delete_bill(self, bill_name):
        """
        Delete a bill from the JSON storage.

        Args:
            bill_name (str): The name of the bill to delete.
        """
        if self.store.exists(bill_name):
            self.store.delete(bill_name)
            self.load_bills()

    def _update_bill_rect(self, instance, value):
        """
        Update the bill rectangle size and position when the window is resized.

        Args:
            instance (Widget): The widget instance.
            value (list): The size or position value.
        """
        instance.rect.pos = instance.pos
        instance.rect.size = instance.size

    def go_back(self, instance):
        """
        Navigate back to the front page.

        Args:
            instance (Button): The button instance.
        """
        self.manager.current = 'front'

    def load_utility(self):
        """
        Load the utility amount from JSON storage and display it.
        """
        self.utility_store = JsonStore('utility.json')
        if self.utility_store.exists('utility'):
            utility_amount = self.utility_store.get('utility')['amount']
            self.utility_display.text = f"Current Utility: ${utility_amount}"
        else:
            self.utility_display.text = "No utility set"

    def update_utility(self, utility_amount):
        """
        Update the utility amount in the JSON storage.

        Args:
            utility_amount (str): The new utility amount.
        """
        if utility_amount:
            self.utility_store.put('utility', amount=utility_amount)
            self.load_utility()

    def on_enter(self):
        """
        Refresh the utility amount and bills when the page is entered.
        """
        self.load_utility()
        self.load_bills()