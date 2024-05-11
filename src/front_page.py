"""
Front Page module.

This module defines the FrontPage class, which represents the main page of the application.
It provides buttons for navigating to different pages and allows users to reset their financial data.
"""

import kivy

kivy.require('2.3.0')  # replace with your current kivy version!

from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle
from kivy.storage.jsonstore import JsonStore
from kivy.uix.popup import Popup


class FrontPage(Screen):
    """
    Front page class.

    This class represents the main page of the application, where users can navigate to different
    pages and reset their financial data.
    """

    def __init__(self, **kwargs):
        """
        Initialize the FrontPage.

        This method sets up the user interface elements, including buttons for navigating to different
        pages and resetting financial data. It also sets up the background color and binds the
        _update_rect method to the size and position properties.
        """
        super().__init__(**kwargs)

        # Initializing buttons for front page
        # User input button
        UIbutton = Button(
            text='Add/Edit Bills',
            background_normal='',
            background_color=(14/255, 40/255, 62/255, 1),
            color=(1, 1, 1, 1),
            font_size=24,
            font_name='Arial',
            size_hint=(0.2, 0.1),
            pos_hint={'center_x': 0.35, 'center_y': 0.70},
            on_press=self.go_to_UI_page
        )

        # Add pay stub button
        APSbutton = Button(
            text='Add pay stub',
            background_normal='',
            background_color=(14/255, 40/255, 62/255, 1),
            color=(1, 1, 1, 1),
            font_size=24,
            font_name='Arial',
            size_hint=(0.2, 0.1),
            pos_hint={'center_x': 0.35, 'center_y': 0.50},
            on_press=self.go_to_APS_page
        )

        # View current finances button
        VCFbutton = Button(
            text='Current Finances',
            background_normal='',
            background_color=(14/255, 40/255, 62/255, 1),
            color=(1, 1, 1, 1),
            font_size=24,
            font_name='Arial',
            size_hint=(0.2, 0.1),
            pos_hint={'center_x': 0.65, 'center_y': 0.70},
            on_press=self.go_to_VCF_page
        )

        ADButton = Button(
            text='Adjust Distributions',
            background_normal='',
            background_color=(14/255, 40/255, 62/255, 1),
            color=(1, 1, 1, 1),
            font_size=24,
            font_name='Arial',
            size_hint=(0.2, 0.1),
            pos_hint={'center_x': 0.65, 'center_y': 0.50},
            on_press=self.go_to_AD_page
        )

        # Reset current finances button
        ResetButton = Button(
            text='Reset',
            background_normal='',
            background_color=(14/255, 40/255, 62/255, 1),
            color=(1, 1, 1, 1),
            font_size=24,
            font_name='Arial',
            size_hint=(0.2, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.25},
            on_press=self.delete_current_finances
        )

        self.add_widget(VCFbutton)
        self.add_widget(APSbutton)
        self.add_widget(UIbutton)
        self.add_widget(ADButton)
        self.add_widget(ResetButton)

        with self.canvas.before:
            Color(0, 24/255, 44/255, 1)  # Set the color (RGBA values)
            self.rect = Rectangle(size=self.size, pos=self.pos)

        # Update the rectangle position and size when the window is resized
        self.bind(size=self._update_rect, pos=self._update_rect)

        self.add_widget(Label(text='Welcome to BBFM', pos_hint={'center_x': 0.5, 'center_y': 0.90}))

    def go_to_UI_page(self, instance):
        """
        Navigate to the 'UI page'.

        Args:
            instance (Button): The button instance.
        """
        self.manager.current = 'UI page'

    def go_to_APS_page(self, instance):
        """
        Navigate to the 'APS page'.

        Args:
            instance (Button): The button instance.
        """
        self.manager.current = 'APS page'

    def go_to_VCF_page(self, instance):
        """
        Navigate to the 'VCF page'.

        Args:
            instance (Button): The button instance.
        """
        self.manager.current = 'VCF page'

    def go_to_AD_page(self, instance):
        """
        Navigate to the 'AD page'.

        Args:
            instance (Button): The button instance.
        """
        self.manager.current = 'AD page'

    def delete_current_finances(self, instance):
        """
        Display a popup with reset options for deleting financial data.

        Args:
            instance (Button): The button instance.
        """
        reset_options = ['Reset all paystubs and finances', 'Reset all bills and utilities']

        # Create a popup for reset options
        option_popup = Popup(title='Reset Options', size_hint=(0.6, 0.4))
        option_layout = BoxLayout(orientation='vertical', spacing=10)

        for option in reset_options:
            button = Button(text=option, font_name='Roboto', on_press=lambda x, opt=option: self.confirm_reset(opt, option_popup))
            option_layout.add_widget(button)

        option_popup.content = option_layout
        option_popup.open()

    def confirm_reset(self, option, option_popup):
        """
        Display a confirmation popup for resetting financial data.

        Args:
            option (str): The selected reset option.
            option_popup (Popup): The reset options popup.
        """
        # Create a popup for confirmation
        confirm_popup = Popup(title='Confirm Reset', size_hint=(0.6, 0.4))
        confirm_layout = BoxLayout(orientation='vertical', spacing=10)

        confirm_label = Label(text=f"Are you sure you want to {option.lower()}?\nThis action cannot be undone.", font_name='Roboto')
        confirm_layout.add_widget(confirm_label)

        button_layout = BoxLayout(spacing=10)
        yes_button = Button(text='Yes', font_name='Roboto', on_press=lambda x: self.perform_reset(option, confirm_popup, option_popup))
        no_button = Button(text='No', font_name='Roboto', on_press=confirm_popup.dismiss)
        button_layout.add_widget(yes_button)
        button_layout.add_widget(no_button)
        confirm_layout.add_widget(button_layout)

        confirm_popup.content = confirm_layout
        confirm_popup.open()

    def perform_reset(self, option, confirm_popup, option_popup):
        """
        Perform the selected reset action and clear the corresponding JSON stores.

        Args:
            option (str): The selected reset option.
            confirm_popup (Popup): The confirmation popup.
            option_popup (Popup): The reset options popup.
        """
        if option == 'Reset all paystubs and finances':
            JsonStore('paystub.json').clear()
            JsonStore('finance.json').clear()
        elif option == 'Reset all bills and utilities':
            JsonStore('bills.json').clear()
            JsonStore('utility.json').clear()

        confirm_popup.dismiss()
        option_popup.dismiss()

    def _update_rect(self, instance, value):
        """
        Update the position and size of the background rectangle.

        Args:
            instance (Widget): The widget instance.
            value (list): The size or position value.
        """
        self.rect.pos = instance.pos
        self.rect.size = instance.size