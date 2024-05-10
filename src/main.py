import time
import kivy

kivy.require('2.3.0')  # replace with your current kivy version!

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle, Canvas
from kivy.storage.jsonstore import JsonStore
from datetime import datetime
from kivy.uix.popup import Popup
class FrontPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Initalizing buttons for front page
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
            text='Adjust Distrubtions',
            background_normal='',
            background_color=(14/255, 40/255, 62/255, 1),
            color=(1, 1, 1, 1),
            font_size=24,
            font_name='Arial',
            size_hint=(0.2, 0.1),
            pos_hint={'center_x': 0.65, 'center_y': 0.50},
            on_press=self.go_to_AD_page
        )
        
        # reset current finances button
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
        self.manager.current = 'UI page'
    
    def go_to_APS_page(self, instance):
        self.manager.current = 'APS page'
        
    def go_to_VCF_page(self, instance):
        self.manager.current = 'VCF page'
        
    def go_to_AD_page(self, instance):
        self.manager.current = 'AD page'
        
    def delete_current_finances(self, instance):
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
        if option == 'Reset all paystubs and finances':
            JsonStore('paystub.json').clear()
            JsonStore('finance.json').clear()
        elif option == 'Reset all bills and utilities':
            JsonStore('bills.json').clear()
            JsonStore('utility.json').clear()
        
        confirm_popup.dismiss()
        option_popup.dismiss()
    
    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
        

# Grabs user bills such as car payments, rent or mortgage, gas bills, etc
class UIPage(Screen):
    def __init__(self, **kwargs):
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
        
        add_bill_panel = GridLayout(cols=1, padding=20, spacing=10)  # Adding bills panel
        add_bill_panel_bg = Rectangle(size=add_bill_panel.size, pos=add_bill_panel.pos)
        add_bill_panel.bind(size=self._update_rect, pos=self._update_rect)
        with add_bill_panel.canvas.before:
            Color(0, 0.1, 0.1, 1)  # Darker background color for add bill panel
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
        
        utility_bill_panel = GridLayout(cols=1, padding=20, spacing=10)  # Adding utilities panel
        utility_bill_panel_bg = Rectangle(size=utility_bill_panel.size, pos=utility_bill_panel.pos)
        utility_bill_panel.bind(size=self._update_rect, pos=self._update_rect)
        with utility_bill_panel.canvas.before:
            Color(0.1, 0.1, 0.1, 1)  # Darker background color for utility panel
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
            Color(0, 24/255, 44/255, 1) # Dark blue background color
            self.rect = Rectangle(size=self.size, pos=self.pos)
        
        self.bind(size=self._update_rect, pos=self._update_rect)
               
    def _update_rect(self, instance, value):
        instance.rect.pos = instance.pos
        instance.rect.size = instance.size
            
    def add_update_bill(self, bill_name, bill_amount):
        if bill_name and bill_amount:
            self.store.put(bill_name, amount=bill_amount)
            self.load_bills()
    
    def load_bills(self):
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
        if self.store.exists(bill_name):
            self.store.delete(bill_name)
            self.load_bills()
    
    def _update_bill_rect(self, instance, value):
        instance.rect.pos = instance.pos
        instance.rect.size = instance.size
    
    def go_back(self, instance):
        self.manager.current = 'front'
    
    def load_utility(self):
        self.utility_store = JsonStore('utility.json')
        if self.utility_store.exists('utility'):
            utility_amount = self.utility_store.get('utility')['amount']
            self.utility_display.text = f"Current Utility: ${utility_amount}"
        else:
            self.utility_display.text = "No utility set"
    
    def update_utility(self, utility_amount):
        if utility_amount:
            self.utility_store.put('utility', amount=utility_amount)
            self.load_utility()
            
    def on_enter(self):
        self.load_utility()
        self.load_bills()
       
# Grabs users pay stub, assumes it is a by monthy pay stub, then properly distributes the pay stub to each category
class APSPage(Screen):
    def __init__(self, **kwargs):
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
            Color(0, 24/255, 44/255, 1) # Dark blue background color
            self.rect = Rectangle(size=self.size, pos=self.pos)
        
        self.bind(size=self._update_rect, pos=self._update_rect)
               
    def _update_rect(self, instance, value):
        """Update the position and size of the background rectangle."""
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
        """Update the position and size of the paystub content box rectangle."""
        instance.rect.pos = instance.pos
        instance.rect.size = instance.size
    
    def add_paystub(self, paystub_amount):
        """Add a new paystub with the specified amount."""
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
        """Save the paystub to the JSON store and perform distribution calculations."""
        paystub_date = datetime.now().strftime('%Y-%m-%d')
        self.paystub_store.put(paystub_date, amount=paystub_amount)
        self.load_paystubs()
        popup.dismiss()
        
        # Perform calculations and distribute the money
        self.calculate_distribution(paystub_date, float(paystub_amount))

    def calculate_distribution(self, paystub_date, paystub_amount):
        """Calculate the distribution of the paystub amount based on bills and distribution settings."""
        bills_store = JsonStore('bills.json')
        utility_store = JsonStore('utility.json')
        
        # Calculate Total Bills based on bi-weekly pay
        total_bills = 0
        utility_bills = 0
        
        # Iterate over the bills store and sum up the bill amounts
        for bill_name in bills_store.keys():
            total_bills += float(bills_store.get(bill_name)['amount'])
        
        # Check if utility bill exists and add it to the total bills
        if utility_store.exists('utility'):
            utility_bills += float(utility_store.get('utility')['amount'])
            utility_bills *= 1.15 # Account for fluctuating utilities
            total_bills += utility_bills
        
        # Divide the total bills by 2 to get the bi-weekly amount
        total_bills /= 2
        
        # Calculate the remaining income after deducting the bills
        remaining_income = paystub_amount - total_bills
        
        # Get the distribution settings and calculate the total proportion
        distribution = self.get_distribution()
        total_proportion = sum(distribution.values())
        
        # Distribute the remaining income based on the distribution settings
        categories = ['Debt', 'Savings', 'Leisure', 'Food']
        for category in categories:
            amount = (distribution[category] / total_proportion) * remaining_income
            self.update_finance(paystub_date, category, amount)
    
    def get_distribution(self):
        """Get the distribution settings from the JSON store or use default values."""
        if not self.distribution_store.exists('distribution'):
            # Set default distribution if not exists
            self.distribution_store.put('distribution', Debt=8, Savings=9, Leisure=2, Food=5)
        
        return self.distribution_store.get('distribution')
    
    def update_finance(self, paystub_date, category, amount):
        """Update the finance data in the JSON store with the distributed amount."""
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
        """Navigate back to the front page."""
        self.manager.current = 'front'
        
    def on_enter(self):
        self.load_paystubs()

# Allows user to view there current finances, such as how much money they have earned, and where it has gone
class VCFPage(Screen):
    def __init__(self, **kwargs):
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
        """
        instance.rect.pos = instance.pos
        instance.rect.size = instance.size
        
    def get_latest_paystub(self):
        """
        Return the date of the latest paystub in the JSON file, or None if no paystubs are available.
        """
        if len(self.finance_store.keys()) > 0:
            return sorted(self.finance_store.keys())[-1]
        else:
            return None
    
    def go_back(self, instance):
        """
        Navigate to the 'front' screen.
        """
        self.manager.current = 'front'
        
    def on_enter(self):
        """
        Reload the current and total distribution data when the screen is entered.
        """
        self.load_current_distribution()
        self.load_total_distribution()
        
class ADPage(Screen):
    def __init__(self, **kwargs):
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
        self.category_inputs = {}
        categories = ['Debt', 'Savings','Leisure', 'Food']
        for category in categories:
            category_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=150, padding=10)
            with category_box.canvas.before:
                Color(14/255, 40/255, 62/255, 1)
                category_box.rect = Rectangle(size=category_box.size, pos=category_box.pos)
            category_box.bind(size=self._update_distribution_rect, pos=self._update_distribution_rect)

            category_label = Label(text=category, font_name='Roboto', size_hint=(0.7, 1))
            self.category_labels[category] = category_label
            category_box.add_widget(category_label)

            category_input = TextInput(multiline=False, font_name='Roboto', size_hint=(0.3, 1), disabled=True)
            self.category_inputs[category] = category_input
            category_box.add_widget(category_input)

            self.distribution_box.add_widget(category_box)

        layout.add_widget(self.distribution_box)

        button_box = BoxLayout(orientation='horizontal', spacing=10, size_hint=(1, None), height=50)

        self.edit_button = Button(
            text='Edit Distribution',
            background_normal='',
            background_color=(14/255, 40/255, 62/255, 1),
            color=(1, 1, 1, 1),
            font_size=18,
            font_name='Roboto',
            on_press=self.toggle_edit_mode
        )
        button_box.add_widget(self.edit_button)

        revert_button = Button(
            text='Revert to Recommended',
            background_normal='',
            background_color=(14/255, 40/255, 62/255, 1),
            color=(1, 1, 1, 1),
            font_size=18,
            font_name='Roboto',
            on_press=self.revert_to_recommended
        )
        button_box.add_widget(revert_button)

        layout.add_widget(button_box)

        note_label = Label(text='Note: Distribution takes effect after the next paystub is added.', size_hint=(1, None), height=10, font_size=14, font_name='Roboto')
        Scale_label = Label(text='\n\n\n\n\n\n\nAggresive Spending: 7-10\n\nModerate Spending: 4-6\n\nLight Spending: 1-3\n\nNo Spending: 0', size_hint=(1, None), pos_hint={'center_x': .5, 'center_y': .35}, font_size=45, font_name='Roboto')
        layout.add_widget(note_label)
        layout.add_widget(Scale_label)

        self.add_widget(layout)

        with self.canvas.before:
            Color(0, 24/255, 44/255, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self._update_rect, pos=self._update_rect)

        self.edit_mode = False
        self.load_distribution()

    def _update_rect(self, instance, value):
        instance.rect.pos = instance.pos
        instance.rect.size = instance.size

    def _update_distribution_rect(self, instance, value):
        instance.rect.pos = instance.pos
        instance.rect.size = instance.size

    def load_distribution(self):
        if not self.distribution_store.exists('distribution'):
            self.distribution_store.put('distribution', Debt=8, Savings=9, Leisure=2, Food=5)

        distribution = self.distribution_store.get('distribution')
        for category, value in distribution.items():
            self.category_labels[category].text = f"{category}: {value}"
            self.category_inputs[category].text = str(value)

    def toggle_edit_mode(self, instance):
        self.edit_mode = not self.edit_mode
        if self.edit_mode:
            self.edit_button.text = 'Save Changes'
            for input_field in self.category_inputs.values():
                input_field.disabled = False
        else:
            self.edit_button.text = 'Edit Distribution'
            distribution = {}
            for category, input_field in self.category_inputs.items():
                value = int(input_field.text)
                distribution[category] = value
                self.category_labels[category].text = f"{category}: {value}"
                input_field.disabled = True
            self.distribution_store.put('distribution', **distribution)
            self.load_distribution()

    def revert_to_recommended(self, instance):
        recommended_distribution = {'Debt': 8, 'Savings': 9, 'Leisure': 2, 'Food': 5}
        self.distribution_store.put('distribution', **recommended_distribution)
        self.load_distribution()

    def go_back(self, instance):
        self.manager.current = 'front'

    def on_enter(self):
        self.load_distribution()
class MyApp(App):
    
    def build(self):
        sm = ScreenManager()
        sm.add_widget(FrontPage(name='front'))
        sm.add_widget(UIPage(name='UI page'))
        sm.add_widget(APSPage(name='APS page'))
        sm.add_widget(VCFPage(name='VCF page'))
        sm.add_widget(ADPage(name='AD page'))
        return sm
if __name__ == '__main__':
    MyApp().run()