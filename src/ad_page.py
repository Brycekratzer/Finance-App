import kivy

kivy.require('2.3.0')

from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle
from kivy.storage.jsonstore import JsonStore
from kivy.uix.popup import Popup


class DistributionPopup(Popup):
    """
    Distribution popup class.

    This class represents the popup window for editing the distribution settings.
    """

    def __init__(self, category, current_value, save_callback, **kwargs):
        """
        Initialize the DistributionPopup.

        Args:
            category (str): The category being edited.
            current_value (int): The current value of the category.
            save_callback (function): The callback function to save the edited value.
            **kwargs: Additional keyword arguments.
        """
        super().__init__(**kwargs)
        self.category = category
        self.save_callback = save_callback
        self.size_hint = (0.4, 0.4)  # Set the size of the popup to 40% of the screen size
        self.background_color = (0, 24/255, 44/255, 0.9)  # Set the background color with transparency
        self.title = f"Adjust {category}"

        layout = BoxLayout(orientation='vertical', spacing=10, padding=20)

        category_label = Label(text=category, font_size=24, font_name='Roboto', size_hint=(1, None), height=50)
        layout.add_widget(category_label)

        self.input_field = TextInput(text=str(current_value), multiline=False, font_size=20, font_name='Roboto', size_hint=(1, None), height=50)
        layout.add_widget(self.input_field)

        button_box = BoxLayout(orientation='horizontal', spacing=10, size_hint=(1, None), height=50)

        save_button = Button(
            text='Save',
            background_normal='',
            background_color=(14/255, 40/255, 62/255, 1),
            color=(1, 1, 1, 1),
            font_size=18,
            font_name='Roboto',
            on_press=self.save_changes
        )
        button_box.add_widget(save_button)

        discard_button = Button(
            text='Discard',
            background_normal='',
            background_color=(14/255, 40/255, 62/255, 1),
            color=(1, 1, 1, 1),
            font_size=18,
            font_name='Roboto',
            on_press=self.discard_changes
        )
        button_box.add_widget(discard_button)

        layout.add_widget(button_box)

        self.content = layout

    def save_changes(self, instance):
        """
        Save the edited distribution value.

        Args:
            instance (Button): The button instance.
        """
        new_value = int(self.input_field.text)
        self.save_callback(self.category, new_value)
        self.dismiss()

    def discard_changes(self, instance):
        """
        Discard the changes and close the popup.

        Args:
            instance (Button): The button instance.
        """
        self.dismiss()


class ADPage(Screen):
    """
    Adjust Distribution (AD) page class.

    This class represents the AD page of the application, where users can view and edit the distribution
    settings for managing their finances.
    """

    def __init__(self, **kwargs):
        """
        Initialize the ADPage.

        This method sets up the user interface layout, including the current distribution display,
        edit distribution functionality, and loading the existing distribution settings from the JSON store.
        """
        super().__init__(**kwargs)
        self.distribution_store = JsonStore('distribution.json')

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

        current_distribution_label = Label(text='Current Distribution', size_hint=(1, None), height=50, font_size=40, font_name='Roboto', bold=True)
        layout.add_widget(current_distribution_label)

        self.distribution_box = GridLayout(cols=2, spacing=10, size_hint_y=None, height=300)
        self.distribution_box.bind(minimum_height=self.distribution_box.setter('height'))

        self.category_labels = {}
        categories = ['Debt', 'Savings', 'Leisure', 'Food']
        for category in categories:
            category_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=150, padding=10)
            with category_box.canvas.before:
                Color(14/255, 40/255, 62/255, 1)
                category_box.rect = Rectangle(size=category_box.size, pos=category_box.pos)
            category_box.bind(size=self._update_distribution_rect, pos=self._update_distribution_rect)

            category_label = Label(text=category, font_name='Roboto', size_hint=(0.7, 1))
            self.category_labels[category] = category_label
            category_box.add_widget(category_label)
            
            button_size_layout = BoxLayout(orientation='vertical', size_hint=(0.3, 1))
            button_size_layout.add_widget(Widget(size_hint_y=.25))
            
            edit_button = Button(
                text='Edit',
                background_normal='',
                background_color=(0, 24/255, 44/255, 1),
                color=(1, 1, 1, 1),
                font_size=18,
                font_name='Roboto',
                size_hint=(0.75, 1),
                on_press=lambda instance, category=category: self.show_edit_popup(category)
            )
            button_size_layout.add_widget(edit_button)
            button_size_layout.add_widget(Widget(size_hint_y=.25))
            category_box.add_widget(button_size_layout)

            self.distribution_box.add_widget(category_box)

        layout.add_widget(self.distribution_box)

        revert_button = Button(
            text='Revert to Recommended',
            background_normal='',
            background_color=(14/255, 40/255, 62/255, 1),
            color=(1, 1, 1, 1),
            font_size=18,
            font_name='Roboto',
            size_hint=(1, None),
            height=50,
            on_press=self.revert_to_recommended
        )
        layout.add_widget(revert_button)

        note_label = Label(text='Note: Distribution takes effect after the next paystub is added.', size_hint=(1, None), height=10, font_size=14, font_name='Roboto')
        scale_label = Label(text='\n\n\n\n\n\n\nAggressive Spending: 7-10\n\nModerate Spending: 4-6\n\nLight Spending: 1-3\n\nNo Spending: 0', size_hint=(1, None), pos_hint={'center_x': .5, 'center_y': .35}, font_size=45, font_name='Roboto')
        layout.add_widget(note_label)
        layout.add_widget(scale_label)

        self.add_widget(layout)

        with self.canvas.before:
            Color(0, 24/255, 44/255, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self._update_rect, pos=self._update_rect)

        self.load_distribution()

    def _update_rect(self, instance, value):
        """
        Update the position and size of the background rectangle.

        Args:
            instance (Widget): The widget instance.
            value (list): The size or position value.
        """
        instance.rect.pos = instance.pos
        instance.rect.size = instance.size

    def _update_distribution_rect(self, instance, value):
        """
        Update the position and size of the distribution category rectangles.

        Args:
            instance (Widget): The widget instance.
            value (list): The size or position value.
        """
        instance.rect.pos = instance.pos
        instance.rect.size = instance.size

    def load_distribution(self):
        """Load the distribution settings from the JSON store and display them."""
        if self.distribution_store.exists('distribution'):
            distribution = self.distribution_store.get('distribution')
            for category, value in distribution.items():
                self.category_labels[category].text = f"{category}: {value}"
        else:
            # Set default distribution if it doesn't exist
            default_distribution = {'Debt': 8, 'Savings': 9, 'Leisure': 2, 'Food': 5}
            self.distribution_store.put('distribution', **default_distribution)
            self.load_distribution()

    def show_edit_popup(self, category):
        """
        Show the edit popup for modifying the distribution value of a specific category.

        Args:
            category (str): The category to be edited.
        """
        current_value = self.distribution_store.get('distribution')[category]
        popup = DistributionPopup(category, current_value, self.save_distribution)
        popup.open()

    def save_distribution(self, category, value):
        """
        Save the edited distribution value for a specific category.

        Args:
            category (str): The category being edited.
            value (int): The new value for the category.
        """
        distribution = self.distribution_store.get('distribution')
        distribution[category] = value
        self.distribution_store.put('distribution', **distribution)
        self.load_distribution()

    def revert_to_recommended(self, instance):
        """
        Revert the distribution settings to the recommended values.

        Args:
            instance (Button): The button instance.
        """
        recommended_distribution = {'Debt': 8, 'Savings': 9, 'Leisure': 2, 'Food': 5}
        self.distribution_store.put('distribution', **recommended_distribution)
        self.load_distribution()

    def go_back(self, instance):
        """
        Navigate back to the front page.

        Args:
            instance (Button): The button instance.
        """
        self.manager.current = 'front'

    def on_enter(self):
        """Refresh the distribution settings when the page is entered."""
        self.load_distribution()