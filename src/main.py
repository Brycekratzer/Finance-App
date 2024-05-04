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

#Delete after done developing app
from kivy.lang import Builder
from kivy.clock import Clock

class FrontPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(Label(text='Welcome to BBFM', pos_hint={'center_x': 0.5, 'center_y': 0.90}))
        
        # Initalizing buttons for front page
        
        # User input button 
        UIbutton = Button(
            text='Add/Edit Poop',
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
        
        layout = GridLayout(cols=1, spacing=10, padding=20)
        
        current_bills_label = Label(text='Current Bills', size_hint=(1, None), height=30)
        layout.add_widget(current_bills_label)
        
        scroll_view = ScrollView(size_hint=(1, 0.6))
        self.current_bills_box = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.current_bills_box.bind(minimum_height=self.current_bills_box.setter('height'))
        scroll_view.add_widget(self.current_bills_box)
        layout.add_widget(scroll_view)
        
        add_bill_label = Label(text='Add/Edit Bills', size_hint=(1, None), height=30)  # Label for add/edit bills section
        layout.add_widget(add_bill_label)  # Add the add/edit bills label to the layout
        
        bill_input_layout = GridLayout(cols=2, spacing=10, size_hint=(1, None), height=50)  # Create a GridLayout for bill input fields
        
        bill_name_input = TextInput(multiline=False, hint_text='Bill name', size_hint=(None, None), size=(200, 30))  # TextInput for bill name
        bill_input_layout.add_widget(bill_name_input)  # Add the bill name input to the bill input layout
        
        bill_amount_input = TextInput(multiline=False, hint_text='USD Amount', size_hint=(None, None), size=(200, 30))  # TextInput for bill amount
        bill_input_layout.add_widget(bill_amount_input)  # Add the bill amount input to the bill input layout
        
        layout.add_widget(bill_input_layout)  # Add the bill input layout to the main layout
        
        add_button = Button(text='Add Bill', size_hint=(None, None), size=(100, 30), on_press=lambda x: self.add_update_bill(bill_name_input.text, bill_amount_input.text))  # Button to add/update a bill
        layout.add_widget(add_button)  # Add the add button to the layout
        
        back_button = Button(text='Go Home', size_hint=(None, None), size=(100, 30), on_press=self.go_back)  # Button to go back to the home screen
        layout.add_widget(back_button)  # Add the back button to the layout
        
        self.add_widget(layout)  # Add the main layout to the UIPage screen
        self.load_bills()  # Load the existing bills from storage
        
        
        self.add_widget(layout)
        self.load_bills()
        
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
            bill_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, padding=10)
            with bill_box.canvas.before:
                Color(0, 0, 0.3, 1)  # Lighter dark blue color for content box
                bill_box.rect = Rectangle(size=bill_box.size, pos=bill_box.pos)
            bill_box.bind(size=self._update_bill_rect, pos=self._update_bill_rect)
            
            bill_info = BoxLayout(orientation='horizontal', size_hint=(0.8, 1))
            bill_name_label = Label(text=f"{bill_name}", size_hint=(0.8, 1))
            bill_info.add_widget(bill_name_label)
            bill_amount_label = Label(text=f"${bill_amount}", size_hint=(0.2, 1))
            bill_info.add_widget(bill_amount_label)
            bill_box.add_widget(bill_info)
            
            edit_button = Button(text='Edit', size_hint=(0.2, 1), on_press=lambda x, bill=bill_name: self.show_edit_bill(bill))
            bill_box.add_widget(edit_button)
            
            self.current_bills_box.add_widget(bill_box)
    
    def show_edit_bill(self, bill_name):
        # Implement the logic to display the text boxes for editing the selected bill
        pass
    
    def _update_bill_rect(self, instance, value):
        instance.rect.pos = instance.pos
        instance.rect.size = instance.size
    
    def go_back(self, instance):
        self.manager.current = 'front'
       
# Grabs users pay stub, assumes it is a by monthy pay stub, then properly distributes the pay stub to each category
class APSPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(Label(text='Add Pay Stub', pos_hint={'center_x': .5, 'center_y': .9}))
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
        self.add_widget(Label(text='Adjust Funding', pos_hint={'center_x': .5, 'center_y': .9}))
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