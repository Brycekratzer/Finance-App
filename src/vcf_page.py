"""
VCF Page module.

This module defines the VCFPage class, which represents the View Current Financials (VCF) page of the application.
It allows users to view the current distribution of their financial data based on the latest paystub and
the total distribution across all paystubs.
"""

import kivy

kivy.require('2.3.0')  # replace with your current kivy version!

from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle
from kivy.storage.jsonstore import JsonStore
from kivy.uix.button import Label


class VCFPage(Screen):
    """
    View Current Financials (VCF) page class.

    This class represents the VCF page of the application, where users can view the current distribution
    of their financial data based on the latest paystub and the total distribution across all paystubs.
    """

    def __init__(self, **kwargs):
        """
        Initialize the VCFPage.

        This method sets up the user interface layout, including the current distribution and total
        distribution sections, and loads the financial data from the JSON store.
        """
        super().__init__(**kwargs)

        # Load financial data from a JSON file named 'finance.json'
        self.finance_store = JsonStore('finance.json')

        # Set up the layout of the screen
        layout = GridLayout(cols=1, spacing=20, padding=30)


        # Add a top box with a back button
        top_box = BoxLayout(orientation='vertical', size_hint=(1, None), height=50)
        back_button = Button(
            text='Home',
            background_normal='',
            background_color=(14/255, 40/255, 62/255, 1),
            color=(1, 1, 1, 1),
            font_size=18,
            font_name='Roboto',
            size_hint=(0.09, 1),
            on_press=self.go_back  # Bind the go_back method to the button press
        )
        top_box.add_widget(back_button)
        layout.add_widget(top_box)

        # Add a label for the current distribution section
        current_distribution_label = Label(text='Current Distribution', size_hint=(1, None), height=50, font_size=40, font_name='Roboto', bold=True)
        layout.add_widget(current_distribution_label)

        # Create a grid layout for displaying the current distribution
        self.current_distribution_box = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.current_distribution_box.bind(minimum_height=self.current_distribution_box.setter('height'))
        layout.add_widget(self.current_distribution_box)

        # Add a label for the total distribution section
        total_distribution_label = Label(text='Total Distribution', size_hint=(1, None), height=50, font_size=40, font_name='Roboto', bold=True)
        layout.add_widget(total_distribution_label)

        # Create a grid layout for displaying the total distribution
        self.total_distribution_box = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.total_distribution_box.bind(minimum_height=self.total_distribution_box.setter('height'))
        layout.add_widget(self.total_distribution_box)

        self.add_widget(layout)

        # Load the current and total distribution data
        self.load_current_distribution()
        self.load_total_distribution()

        # Set up a dark blue background color for the screen
        with self.canvas.before:
            Color(0/255, 24/255, 44/255, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)

        # Bind the _update_rect method to the size and position properties
        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        """
        Update the background rectangle to match the size and position of the screen.

        Args:
            instance (Widget): The widget instance.
            value (list): The size or position value.
        """
        instance.rect.pos = instance.pos
        instance.rect.size = instance.size

    def load_current_distribution(self):
        """
        Load and display the current distribution of financial data.
        """
        self.finance_store = JsonStore('finance.json')
        self.current_distribution_box.clear_widgets()
        latest_paystub = self.get_latest_paystub()
        if latest_paystub:
            distribution = self.finance_store.get(latest_paystub)
            total_amount = sum(distribution.values())

            # Add a box displaying the total amount
            total_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, padding=10)
            with total_box.canvas.before:
                Color(14/255, 40/255, 62/255, 1)
                total_box.rect = Rectangle(size=total_box.size, pos=total_box.pos)
            total_box.bind(size=self._update_distribution_rect, pos=self._update_distribution_rect)

            total_label = Label(text=f"Total: ${total_amount:.2f}", font_name='Roboto')
            total_box.add_widget(total_label)
            self.current_distribution_box.add_widget(total_box)

            # Add boxes displaying the distribution for each category
            for category, amount in distribution.items():
                distribution_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, padding=10)
                with distribution_box.canvas.before:
                    Color(14/255, 40/255, 62/255, 1)
                    distribution_box.rect = Rectangle(size=distribution_box.size, pos=distribution_box.pos)
                distribution_box.bind(size=self._update_distribution_rect, pos=self._update_distribution_rect)

                distribution_label = Label(text=f"{category}: ${amount:.2f}", font_name='Roboto')
                distribution_box.add_widget(distribution_label)
                self.current_distribution_box.add_widget(distribution_box)
        else:
            # If no paystub data is available, display a label
            no_data_label = Label(text="No paystub data available", font_name='Roboto')
            self.current_distribution_box.add_widget(no_data_label)

    def load_total_distribution(self):
        """
        Load and display the total distribution of financial data across all paystubs.
        """
        self.finance_store = JsonStore('finance.json')
        self.total_distribution_box.clear_widgets()
        total_distribution = {}

        # Aggregate the distribution data for each category across all paystubs
        for paystub_date in self.finance_store.keys():
            distribution = self.finance_store.get(paystub_date)
            for category, amount in distribution.items():
                total_distribution[category] = total_distribution.get(category, 0) + amount

        total_amount = sum(total_distribution.values())

        # Add a box displaying the total amount
        total_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, padding=10)
        with total_box.canvas.before:
            Color(14/255, 40/255, 62/255, 1)
            total_box.rect = Rectangle(size=total_box.size, pos=total_box.pos)
        total_box.bind(size=self._update_distribution_rect, pos=self._update_distribution_rect)

        total_label = Label(text=f"Total: ${total_amount:.2f}", font_name='Roboto')
        total_box.add_widget(total_label)
        self.total_distribution_box.add_widget(total_box)

        # Add boxes displaying the distribution for each category
        for category, amount in total_distribution.items():
            distribution_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, padding=10)
            with distribution_box.canvas.before:
                Color(14/255, 40/255, 62/255, 1)
                distribution_box.rect = Rectangle(size=distribution_box.size, pos=distribution_box.pos)
            distribution_box.bind(size=self._update_distribution_rect, pos=self._update_distribution_rect)

            distribution_label = Label(text=f"{category}: ${amount:.2f}", font_name='Roboto')
            distribution_box.add_widget(distribution_label)
            self.total_distribution_box.add_widget(distribution_box)

    def _update_distribution_rect(self, instance, value):
        """
        Update the background rectangles for the distribution boxes.

        Args:
            instance (Widget): The widget instance.
            value (list): The size or position value.
        """
        instance.rect.pos = instance.pos
        instance.rect.size = instance.size

    def get_latest_paystub(self):
        """
        Return the date of the latest paystub in the JSON file, or None if no paystubs are available.

        Returns:
            str or None: The date of the latest paystub, or None if no paystubs are available.
        """
        if len(self.finance_store.keys()) > 0:
            return sorted(self.finance_store.keys())[-1]
        else:
            return None

    def go_back(self, instance):
        """
        Navigate to the 'front' screen.

        Args:
            instance (Button): The button instance.
        """
        self.manager.current = 'front'

    def on_enter(self):
        """
        Reload the current and total distribution data when the screen is entered.
        """
        self.load_current_distribution()
        self.load_total_distribution()