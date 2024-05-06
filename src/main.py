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
from kivy.graphics import Color, Rectangle
from kivy.storage.jsonstore import JsonStore
from datetime import datetime
from kivy.uix.popup import Popup
class FrontPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(Label(text='Welcome to BBFM', pos_hint={'center_x': 0.5, 'center_y': 0.90}))
        
        # Initalizing buttons for front page
        
        # User input button 
        UIbutton = Button(
            text='Add/Edit Bills',
            background_color=(0, 0, 1, 1),
            color=(1, 1, 1, 1),
            font_size=24,
            font_name='Arial',
            size_hint=(0.2, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.80},
            on_press=self.go_to_UI_page
        )
        
        # Add pay stub button
        APSbutton = Button(
            text='Add pay stub',
            background_color=(0, 0, 1, 1),
            color=(1, 1, 1, 1),
            font_size=24,
            font_name='Arial',
            size_hint=(0.2, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.60},
            on_press=self.go_to_APS_page
        )
        
        # View current finances button
        VCFbutton = Button(
            text='Current Finances',
            background_color=(0, 0, 1, 1),
            color=(1, 1, 1, 1),
            font_size=24,
            font_name='Arial',
            size_hint=(0.2, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.40},
            on_press=self.go_to_VCF_page
        )
        
        # Adjust distrubtions for each category
        AJbutton = Button(
            text='Adjust Distrubtions',
            background_color=(0, 0, 1, 1),
            color=(1, 1, 1, 1),
            font_size=24,
            font_name='Arial',
            size_hint=(0.2, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.20},
            on_press=self.go_to_AJ_page
        )
        
        self.add_widget(VCFbutton)
        self.add_widget(APSbutton)
        self.add_widget(UIbutton)
        self.add_widget(AJbutton)
        
    def go_to_UI_page(self, instance):
        self.manager.current = 'UI page'
    
    def go_to_APS_page(self, instance):
        self.manager.current = 'APS page'
        
    def go_to_VCF_page(self, instance):
        self.manager.current = 'VCF page'
    
    def go_to_AJ_page(self, instance):
        self.manager.current = 'AJ page'

# Grabs user bills such as car payments, rent or mortgage, gas bills, etc
class UIPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.store = JsonStore('bills.json')
        self.utility_store = JsonStore('utility.json')
        
        # Set up main layout and top back button box
        layout = GridLayout(cols=1, spacing=20, padding=30)
        top_box = BoxLayout(orientation='vertical', size_hint=(.045,.035))

        back_button = Button(
            text='Home',
            background_color=(0, 0, 1, 1),
            color=(1, 1, 1, 1),
            font_size=18,
            font_name='Arial',
            size_hint=(0.09, 0.07),
            on_press=self.go_back
        )
        top_box.add_widget(back_button)
        layout.add_widget(top_box)
        
        # Set up display for current bills
        current_bills_label = Label(text='Current Bills', size_hint=(1, None), height=30, font_size=40)
        layout.add_widget(current_bills_label)
        
        scroll_view = ScrollView(size_hint=(1, 0.3))
        self.current_bills_box = GridLayout(cols=1, spacing=5, size_hint_y=None)
        self.current_bills_box.bind(minimum_height=self.current_bills_box.setter('height'))
        scroll_view.add_widget(self.current_bills_box)
        layout.add_widget(scroll_view)
        
        add_bill_label = Label(text='Add/Edit Bills', size_hint=(1, None), height=30, font_size=40)
        layout.add_widget(add_bill_label)
        
        # Sets up input text boxes in own grid layout
        add_edit_layout = GridLayout(cols=2, spacing=10, size_hint=(1, None), size_hint_y=.3, padding=10) # Main Layout that stores both utility and adding bills 
        add_bill_panel = GridLayout(cols=1, padding=5) # Adding bills panel
        utility_bill_panel = GridLayout(cols=1, padding=5) # Adding utilites panel
        
        add_bill_sub_label = Label(
            text='Input Bills', 
            height=30, 
            font_size=30,
            size_hint=(0.25, 0.05), 
            pos_hint={'x': 0.03, 'y': 0.35} 
        )
        self.add_widget(add_bill_sub_label)
        
        bill_name_input = TextInput(
            multiline=False, 
            hint_text='Bill name', 
            size_hint=(0.25, 0.05), 
            pos_hint={'x': 0.03, 'y': 0.25}  
        )
        self.add_widget(bill_name_input)
        
        bill_amount_input = TextInput(
            multiline=False, 
            hint_text='USD Amount',
            size_hint=(0.25, 0.05),
            pos_hint={'x': 0.03, 'y': 0.15} 
        )
        self.add_widget(bill_amount_input)
        
        # Adds buttons to bottom of bill input 
        add_button = Button(
            text='Add Bill',
            background_color=(0, 0, 1, 1),
            font_size=24,
            font_name='Arial',
            size_hint=(.15,.10),
            pos_hint={'x': 0.30, 'center_y': 0.22},
            on_press=lambda x: self.add_update_bill(bill_name_input.text, bill_amount_input.text)
        )
        self.add_widget(add_button)
        
        # Set up utility panel
        utility_label = Label(
            text='Monthly Utility (Average)', 
            height=30, 
            font_size=30,
            size_hint=(0.25, 0.05), 
            pos_hint={'x': 0.61, 'y': 0.35} 
        )
        self.add_widget(utility_label)
    
        self.utility_display = Label(
            text='', 
            size_hint=(.20, 0.05),
            size=(100, 30),
            pos_hint={'x': 0.63, 'y': 0.30}
        )
        self.add_widget(self.utility_display)
        self.load_utility()
        
        utility_input = TextInput(
            multiline=False, 
            hint_text='Enter utility amount',
            size_hint=(0.25, 0.05), 
            pos_hint={'x': 0.60, 'y': 0.25}  
        )
        self.add_widget(utility_input)
        
        utility_button = Button(
            text='Update Utility',
            background_color=(0, 0, 1, 1),
            color=(1, 1, 1, 1),
            font_size=20,
            size_hint=(.15,.10),
            pos_hint={'x': .65, 'y': .13},
            on_press=lambda x: self.update_utility(utility_input.text)
        )
        self.add_widget(utility_button)
        
        add_edit_layout.add_widget(add_bill_panel)
        add_edit_layout.add_widget(utility_bill_panel)
        layout.add_widget(add_edit_layout) 
        
        self.add_widget(layout)
        self.load_bills()
        self.load_utility()

        with self.canvas.before:
            Color(0, 0, 0.2, 1)  # Dark blue background color
            self.rect = Rectangle(size=self.size, pos=self.pos)
        
        self.bind(size=self._update_rect, pos=self._update_rect)
               
    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
            
    def add_update_bill(self, bill_name, bill_amount):
        if bill_name and bill_amount:
            self.store.put(bill_name, amount=bill_amount)
            self.load_bills()
    
    def load_bills(self):
        self.current_bills_box.clear_widgets()
        for bill_name in self.store.keys():
            bill_amount = self.store.get(bill_name)['amount']
            bill_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=100, padding=30)
            with bill_box.canvas.before:
                Color(0, 0, 0.3, 1)  # Lighter dark blue color for content box
                bill_box.rect = Rectangle(size=bill_box.size, pos=bill_box.pos)
            bill_box.bind(size=self._update_bill_rect, pos=self._update_bill_rect)
            
            bill_info = BoxLayout(orientation='horizontal', size_hint=(0.6, 1))
            bill_name_label = Label(text=f"{bill_name}", size_hint=(0.8, 1))
            bill_info.add_widget(bill_name_label)
            bill_amount_label = Label(text=f"${bill_amount}", size_hint=(0.2, 1))
            bill_info.add_widget(bill_amount_label)
            bill_box.add_widget(bill_info)
            
            delete_button = Button(text='Delete', size_hint=(0.2, 1), font_size=14, on_press=lambda x, bill=bill_name: self.delete_bill(bill))
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
        if self.utility_store.exists('utility'):
            utility_amount = self.utility_store.get('utility')['amount']
            self.utility_display.text = f"Current Utility: ${utility_amount}"
        else:
            self.utility_display.text = "No utility set"
    
    def update_utility(self, utility_amount):
        if utility_amount:
            self.utility_store.put('utility', amount=utility_amount)
            self.load_utility()
       
# Grabs users pay stub, assumes it is a by monthy pay stub, then properly distributes the pay stub to each category
class APSPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.paystub_store = JsonStore('paystub.json')
        self.distribution_store = JsonStore('distribution.json')
        
        layout = GridLayout(cols=1, spacing=20, padding=30)
        
        self.add_widget(Label(text='Add Pay Stub', size_hint=(1, None), height=30, font_size=20))
        
        self.paystub_box = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.paystub_box.bind(minimum_height=self.paystub_box.setter('height'))
        
        paystub_scroll = ScrollView(size_hint=(1, 0.3))
        paystub_scroll.add_widget(self.paystub_box)
        layout.add_widget(paystub_scroll)
        
        paystub_input_layout = GridLayout(cols=2, spacing=10, size_hint_y=None, height=100)
        
        paystub_amount_input = TextInput(multiline=False, hint_text='Enter pay stub amount', size_hint=(0.8, None), height=40)
        paystub_input_layout.add_widget(paystub_amount_input)
        
        add_paystub_button = Button(
            text='Add Pay Stub',
            background_color=(0, 0, 1, 1),
            color=(1, 1, 1, 1),
            font_size=18,
            size_hint=(0.2, None),
            height=40,
            on_press=lambda x: self.add_paystub(paystub_amount_input.text)
        )
        paystub_input_layout.add_widget(add_paystub_button)
        
        adjust_distribution_button = Button(
            text='Adjust Distribution',
            background_color=(0, 0, 1, 1),
            color=(1, 1, 1, 1),
            font_size=18,
            size_hint=(0.4, None),
            height=40,
            on_press=self.go_to_adjust_distribution
        )
        paystub_input_layout.add_widget(adjust_distribution_button)
        
        layout.add_widget(paystub_input_layout)
        
        BackButton = Button(
            text='Go Home',
            background_color=(0, 0, 1, 1),
            color=(1, 1, 1, 1),
            font_size=24,
            font_name='Arial',
            size_hint=(0.2, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.10},
            on_press=self.go_back
        )
        layout.add_widget(BackButton)
        
        self.add_widget(layout)
        self.load_paystubs()

    def load_paystubs(self):
        self.paystub_box.clear_widgets()
        for paystub_date in self.paystub_store.keys():
            paystub_amount = self.paystub_store.get(paystub_date)['amount']
            paystub_label = Label(text=f"Date: {paystub_date}, Amount: ${paystub_amount}", size_hint_y=None, height=30)
            self.paystub_box.add_widget(paystub_label)
    
    def add_paystub(self, paystub_amount):
        if paystub_amount:
            confirm_popup = Popup(title='Confirm', size_hint=(0.5, 0.3))
            confirm_layout = BoxLayout(orientation='vertical', spacing=10)
            confirm_label = Label(text=f"Is the pay stub amount of ${paystub_amount} correct?")
            confirm_layout.add_widget(confirm_label)
            
            button_layout = BoxLayout(spacing=10)
            yes_button = Button(text='Yes', on_press=lambda x: self.save_paystub(paystub_amount, confirm_popup))
            no_button = Button(text='No', on_press=confirm_popup.dismiss)
            button_layout.add_widget(yes_button)
            button_layout.add_widget(no_button)
            confirm_layout.add_widget(button_layout)
            
            confirm_popup.content = confirm_layout
            confirm_popup.open()
    
    def save_paystub(self, paystub_amount, popup):
        paystub_date = datetime.now().strftime('%Y-%m-%d')
        self.paystub_store.put(paystub_date, amount=paystub_amount)
        self.load_paystubs()
        popup.dismiss()
        
        # Perform calculations and distribute the money
        self.calculate_distribution(float(paystub_amount))
    
    def calculate_distribution(self, paystub_amount):
        bills_store = JsonStore('bills.json')
        utility_store = JsonStore('utility.json')
        
        total_bills = 0
        for bill_name in bills_store.keys():
            total_bills += float(bills_store.get(bill_name)['amount'])
        
        if utility_store.exists('utility'):
            total_bills += float(utility_store.get('utility')['amount'])
        
        remaining_income = paystub_amount - total_bills
        
        distribution = self.get_distribution()
        total_proportion = sum(distribution.values())
        
        categories = ['Debt', 'Savings', 'Leisure', 'Food']
        for category in categories:
            amount = (distribution[category] / total_proportion) * remaining_income
            self.update_finance(category, amount)
    
    def get_distribution(self):
        if not self.distribution_store.exists('distribution'):
            # Default distribution
            self.distribution_store.put('distribution', Debt=5, Savings=5, Leisure=5, Food=5)
        
        return self.distribution_store.get('distribution')
    
    def update_finance(self, category, amount):
        finance_store = JsonStore('finance.json')
        if finance_store.exists(category):
            current_amount = float(finance_store.get(category)['amount'])
            finance_store.put(category, amount=current_amount + amount)
        else:
            finance_store.put(category, amount=amount)
    
    def go_to_adjust_distribution(self, instance):
        self.manager.current = 'AJ page'

    def go_back(self, instance):
        self.manager.current = 'front'

# Allows user to view there current finances, such as how much money they have earned, and where it has gone
class VCFPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(Label(text='View Finances', pos_hint={'center_x': .5, 'center_y': .9}))
        BackButton = Button(
            text='Go Home',
            background_color=(0, 0, 1, 1),
            color=(1, 1, 1, 1),
            font_size=24,
            font_name='Arial',
            size_hint=(0.2, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.10},
            on_press=self.go_back
        )
        self.add_widget(BackButton)

    def go_back(self, instance):
        self.manager.current = 'front'
        
class AJPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(Label(text='Adjust Funding Yo', pos_hint={'center_x': .5, 'center_y': .9}))
        BackButton = Button(
            text='Go Home',
            background_color=(0, 0, 1, 1),
            color=(1, 1, 1, 1),
            font_size=24,
            font_name='Arial',
            size_hint=(0.2, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.10},
            on_press=self.go_back
        )
        self.add_widget(BackButton)

    def go_back(self, instance):
        self.manager.current = 'front'

class MyApp(App):
    
    def build(self):
        sm = ScreenManager()
        sm.add_widget(FrontPage(name='front'))
        sm.add_widget(UIPage(name='UI page'))
        sm.add_widget(APSPage(name='APS page'))
        sm.add_widget(VCFPage(name='VCF page'))
        sm.add_widget(AJPage(name='AJ page'))
        return sm

if __name__ == '__main__':
    MyApp().run()