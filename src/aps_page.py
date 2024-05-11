"""
APS Page module.

This module defines the APSPage class, which represents the add pay stub (APS) page of the application.
It allows users to view and add paystubs, and calculates the distribution of income based on bills and distribution settings.
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
from datetime import datetime
from kivy.uix.popup import Popup


class APSPage(Screen):
    """
    Add Pay Stub (APS) page class.

    This class represents the APS page of the application, where users can view and add paystubs,
    and the system calculates the distribution of income based on bills and distribution settings.
    """

    def __init__(self, **kwargs):
        """
        Initialize the APSPage.

        This method sets up the user interface layout, including the past pay stubs section,
        add pay stub section, and loads the existing paystubs from the JSON store.
        """
        super().__init__(**kwargs)
        # Files for Storing Paystub and distribution
        self.paystub_store = JsonStore('paystub.json')
        self.distribution_store = JsonStore('distribution.json')

        # Main layout setup
        layout = GridLayout(cols=1, spacing=20, padding=30)

        # Top navigation box
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

        # Past Pay Stubs section
        paystub_label = Label(text='Past Pay Stubs', size_hint=(1, None), height=50, font_size=40, font_name='Roboto', bold=True)
        layout.add_widget(paystub_label)

        # Scrollable box for displaying past paystubs
        paystub_scroll = ScrollView(size_hint=(1, 0.3))
        self.paystub_box = GridLayout(cols=1, spacing=5, size_hint_y=None)
        self.paystub_box.bind(minimum_height=self.paystub_box.setter('height'))
        paystub_scroll.add_widget(self.paystub_box)
        layout.add_widget(paystub_scroll)

        # Add Pay Stub section
        add_paystub_label = Label(text='Add Pay Stub', size_hint=(1, None), height=50, font_size=40, font_name='Roboto', bold=True)
        layout.add_widget(add_paystub_label)

        # Layout for adding new paystubs
        paystub_input_layout = GridLayout(cols=1, spacing=10, size_hint=(1, None), height=200, padding=20)
        paystub_amount_input = TextInput(multiline=False, hint_text='Enter pay stub amount', font_name='Roboto', size_hint=(1, None), height=50)
        paystub_input_layout.add_widget(paystub_amount_input)

        add_paystub_button = Button(
            text='Add Pay Stub',
            background_normal='',
            background_color=(14/255, 40/255, 62/255, 1),
            color=(1, 1, 1, 1),
            font_size=24,
            font_name='Roboto',
            size_hint=(1, None),
            height=50,
            on_press=lambda x: self.add_paystub(paystub_amount_input.text)
        )
        paystub_input_layout.add_widget(add_paystub_button)

        layout.add_widget(paystub_input_layout)

        self.add_widget(layout)
        self.load_paystubs()

        # Set background color
        with self.canvas.before:
            Color(0, 24/255, 44/255, 1)  # Dark blue background color
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        """
        Update the position and size of the background rectangle.

        Args:
            instance (Widget): The widget instance.
            value (list): The size or position value.
        """
        instance.rect.pos = instance.pos
        instance.rect.size = instance.size

    def load_paystubs(self):
        """Load and display the paystubs from the JSON store."""
        self.paystub_store = JsonStore('paystub.json')
        self.paystub_box.clear_widgets()  # Clear the existing widgets before loading
        for paystub_date in self.paystub_store.keys():
            paystub_amount = self.paystub_store.get(paystub_date)['amount']

            # Create a box layout to hold the paystub label and set its properties
            paystub_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, padding=10)

            # Set the background color of the paystub box
            with paystub_box.canvas.before:
                Color(14/255, 40/255, 62/255, 1)  # Lighter dark blue color for content box
                paystub_box.rect = Rectangle(size=paystub_box.size, pos=paystub_box.pos)

            # Bind the size and position of the paystub box to update its rectangle
            paystub_box.bind(size=self._update_paystub_rect, pos=self._update_paystub_rect)

            # Create a label to display the paystub date and amount
            paystub_label = Label(text=f"Date: {paystub_date}, Amount: ${paystub_amount}", font_name='Roboto')
            paystub_box.add_widget(paystub_label)

            # Add the paystub box to the main paystub box layout
            self.paystub_box.add_widget(paystub_box)

    def _update_paystub_rect(self, instance, value):
        """
        Update the position and size of the paystub content box rectangle.

        Args:
            instance (Widget): The widget instance.
            value (list): The size or position value.
        """
        instance.rect.pos = instance.pos
        instance.rect.size = instance.size

    def add_paystub(self, paystub_amount):
        """
        Add a new paystub with the specified amount.

        Args:
            paystub_amount (str): The amount of the paystub.
        """
        if paystub_amount:
            # Create a popup for confirmation
            confirm_popup = Popup(title='Confirm', size_hint=(0.5, 0.3))
            confirm_layout = BoxLayout(orientation='vertical', spacing=10)

            # Add a label to the confirmation popup with the paystub amount
            confirm_label = Label(text=f"Is the pay stub amount of ${paystub_amount} correct?\n *You can not delete a paystub*", font_name='Roboto')
            confirm_layout.add_widget(confirm_label)

            # Add buttons to the confirmation popup for user action
            button_layout = BoxLayout(spacing=10)
            yes_button = Button(text='Yes', font_name='Roboto', on_press=lambda x: self.save_paystub(paystub_amount, confirm_popup))
            no_button = Button(text='No', font_name='Roboto', on_press=confirm_popup.dismiss)
            button_layout.add_widget(yes_button)
            button_layout.add_widget(no_button)
            confirm_layout.add_widget(button_layout)

            confirm_popup.content = confirm_layout
            confirm_popup.open()

    def save_paystub(self, paystub_amount, popup):
        """
        Save the paystub to the JSON store and perform distribution calculations.

        Args:
            paystub_amount (str): The amount of the paystub.
            popup (Popup): The confirmation popup instance.
        """
        paystub_date = datetime.now().strftime('%Y-%m-%d')
        self.paystub_store.put(paystub_date, amount=paystub_amount)
        self.load_paystubs()
        popup.dismiss()

        # Perform calculations and distribute the money
        self.calculate_distribution(paystub_date, float(paystub_amount))

    def calculate_distribution(self, paystub_date, paystub_amount):
        """
        Calculate the distribution of the paystub amount based on bills and distribution settings.

        Args:
            paystub_date (str): The date of the paystub.
            paystub_amount (float): The amount of the paystub.
        """
        bills_store = JsonStore('bills.json')
        utility_store = JsonStore('utility.json')
        distribution_store = JsonStore('distribution.json')

        # Calculate Total Bills based on bi-weekly pay
        total_bills = 0
        utility_bills = 0

        # Iterate over the bills store and sum up the bill amounts
        for bill_name in bills_store.keys():
            total_bills += float(bills_store.get(bill_name)['amount'])

        # Check if utility bill exists and add it to the total bills
        if utility_store.exists('utility'):
            utility_bills += float(utility_store.get('utility')['amount'])
            utility_bills *= 1.15  # Account for fluctuating utilities
            total_bills += utility_bills

        # Divide the total bills by 2 to get the bi-weekly amount
        total_bills /= 2

        # Calculate the remaining income after deducting the bills
        remaining_income = paystub_amount - total_bills

        # Get the distribution settings from the distribution store
        if distribution_store.exists('distribution'):
            distribution = distribution_store.get('distribution')
        else:
            # Set default distribution if it doesn't exist
            distribution = {'Debt': 8, 'Savings': 9, 'Leisure': 2, 'Food': 5}

        total_proportion = sum(distribution.values())

        # Distribute the remaining income based on the distribution settings
        categories = ['Debt', 'Savings', 'Leisure', 'Food']
        for category in categories:
            amount = (distribution[category] / total_proportion) * remaining_income
            self.update_finance(paystub_date, category, amount)

    def get_distribution(self):
        """
        Get the distribution settings from the JSON store.

        Returns:
            dict: The distribution settings.
        """
        if not self.distribution_store.exists('distribution'):
            # Set default distribution if it doesn't exist
            default_distribution = {'Debt': 8, 'Savings': 9, 'Leisure': 2, 'Food': 5}
            self.distribution_store.put('distribution', **default_distribution)

        return self.distribution_store.get('distribution')

    def update_finance(self, paystub_date, category, amount):
        """
        Update the finance data in the JSON store with the distributed amount.

        Args:
            paystub_date (str): The date of the paystub.
            category (str): The category of the distribution.
            amount (float): The amount to be distributed.
        """
        finance_store = JsonStore('finance.json')
        if finance_store.exists(paystub_date):
            # If the paystub date exists in the finance store, update the category amount
            paystub_data = finance_store.get(paystub_date)
            paystub_data[category] = paystub_data.get(category, 0) + amount
            finance_store.put(paystub_date, **paystub_data)
        else:
            # If the paystub date doesn't exist, create a new entry with the category amount
            finance_store.put(paystub_date, **{category: amount})

    def go_back(self, instance):
        """
        Navigate back to the front page.

        Args:
            instance (Button): The button instance.
        """
        self.manager.current = 'front'

    def on_enter(self):
        """Refresh the paystubs when the page is entered."""
        self.load_paystubs()