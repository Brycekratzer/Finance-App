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
from kivy.garden.graph import Graph, LinePlot
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
        top_box = BoxLayout(orientation='vertical', size_hint=(1, None), height=50)

        back_button = Button(
            text='Home',
            background_normal='',
            background_color=(0, 0, 1, 1),
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
            Color(0.1, 0.1, 0.1, 1)  # Darker background color for add bill panel
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
            background_color=(0, 0, 1, 1),
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
            background_color=(0, 0, 1, 1),
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
            Color(20/255, 38/255, 81/255, 1) # Dark blue background color
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
        self.current_bills_box.clear_widgets()
        for bill_name in self.store.keys():
            bill_amount = self.store.get(bill_name)['amount']
            bill_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=100, padding=30)
            with bill_box.canvas.before:
                Color(0, 0, 0.3, 1)  # Lighter dark blue color for content box
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
                background_color=(1, 0, 0, 1),
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
        
        # Files for Storing Paystub and distribution
        self.paystub_store = JsonStore('paystub.json')
        self.distribution_store = JsonStore('distribution.json')
        
        # Main layout
        layout = GridLayout(cols=1, spacing=20, padding=30)
        
        top_box = BoxLayout(orientation='vertical', size_hint=(1, None), height=50)
        back_button = Button(
            text='Home',
            background_normal='',
            background_color=(0, 0, 1, 1),
            color=(1, 1, 1, 1),
            font_size=18,
            font_name='Roboto',
            size_hint=(0.09, 1),
            on_press=self.go_back
        )
        top_box.add_widget(back_button)
        layout.add_widget(top_box)
        
        paystub_label = Label(text='Past Pay Stubs', size_hint=(1, None), height=50, font_size=40, font_name='Roboto', bold=True)
        layout.add_widget(paystub_label)
        
        # Subbox storing each past paystubs
        paystub_scroll = ScrollView(size_hint=(1, 0.3))
        self.paystub_box = GridLayout(cols=1, spacing=5, size_hint_y=None)
        self.paystub_box.bind(minimum_height=self.paystub_box.setter('height'))
        paystub_scroll.add_widget(self.paystub_box)
        layout.add_widget(paystub_scroll)
        
        add_paystub_label = Label(text='Add Pay Stub', size_hint=(1, None), height=50, font_size=40, font_name='Roboto', bold=True)
        layout.add_widget(add_paystub_label)
        
        # Adding Paystubs Layout
        paystub_input_layout = GridLayout(cols=1, spacing=10, size_hint=(1, None), height=200, padding=20)
        paystub_amount_input = TextInput(multiline=False, hint_text='Enter pay stub amount', font_name='Roboto', size_hint=(1, None), height=50)
        paystub_input_layout.add_widget(paystub_amount_input)
        
        add_paystub_button = Button(
            text='Add Pay Stub',
            background_normal='',
            background_color=(0, 0, 1, 1),
            color=(1, 1, 1, 1),
            font_size=24,
            font_name='Roboto',
            size_hint=(1, None),
            height=50,
            on_press=lambda x: self.add_paystub(paystub_amount_input.text)
        )
        paystub_input_layout.add_widget(add_paystub_button)
        
        adjust_distribution_button = Button(
            text='Adjust Distribution',
            background_normal='',
            background_color=(0, 0, 1, 1),
            color=(1, 1, 1, 1),
            font_size=24,
            font_name='Roboto',
            size_hint=(1, None),
            height=50,
            on_press=self.go_to_adjust_distribution
        )
        paystub_input_layout.add_widget(adjust_distribution_button)
        
        layout.add_widget(paystub_input_layout)
        
        self.add_widget(layout)
        self.load_paystubs()
        
        with self.canvas.before:
            Color(20/255, 38/255, 81/255, 1) # Dark blue background color
            self.rect = Rectangle(size=self.size, pos=self.pos)
        
        self.bind(size=self._update_rect, pos=self._update_rect)
               
    def _update_rect(self, instance, value):
        instance.rect.pos = instance.pos
        instance.rect.size = instance.size
    
    def load_paystubs(self):
        self.paystub_box.clear_widgets()
        for paystub_date in self.paystub_store.keys():
            paystub_amount = self.paystub_store.get(paystub_date)['amount']
            paystub_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, padding=10)
            with paystub_box.canvas.before:
                Color(0, 0, 0.3, 1)  # Lighter dark blue color for content box
                paystub_box.rect = Rectangle(size=paystub_box.size, pos=paystub_box.pos)
            paystub_box.bind(size=self._update_paystub_rect, pos=self._update_paystub_rect)
            
            paystub_label = Label(text=f"Date: {paystub_date}, Amount: ${paystub_amount}", font_name='Roboto')
            paystub_box.add_widget(paystub_label)
            
            self.paystub_box.add_widget(paystub_box)
    
    def _update_paystub_rect(self, instance, value):
        instance.rect.pos = instance.pos
        instance.rect.size = instance.size
    
    def add_paystub(self, paystub_amount):
        if paystub_amount:
            confirm_popup = Popup(title='Confirm', size_hint=(0.5, 0.3))
            confirm_layout = BoxLayout(orientation='vertical', spacing=10)
            confirm_label = Label(text=f"Is the pay stub amount of ${paystub_amount} correct?\n *You can not delete a paystub*", font_name='Roboto')
            confirm_layout.add_widget(confirm_label)
            
            button_layout = BoxLayout(spacing=10)
            yes_button = Button(text='Yes', font_name='Roboto', on_press=lambda x: self.save_paystub(paystub_amount, confirm_popup))
            no_button = Button(text='No', font_name='Roboto', on_press=confirm_popup.dismiss)
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
        self.calculate_distribution(paystub_date, float(paystub_amount))

    def calculate_distribution(self, paystub_date, paystub_amount):
        bills_store = JsonStore('bills.json')
        utility_store = JsonStore('utility.json')
        
        # Calculates Total Bills based on bi-weekly pay
        total_bills = 0
        utility_bills = 0
        for bill_name in bills_store.keys():
            total_bills += float(bills_store.get(bill_name)['amount'])
        
        if utility_store.exists('utility'):
            utility_bills += float(utility_store.get('utility')['amount'])
            utility_bills * 1.15 # Accounts for fluctuating utilites
            total_bills += utility_bills
        
        total_bills = total_bills/2        
        remaining_income = paystub_amount - total_bills
        
        distribution = self.get_distribution()
        total_proportion = sum(distribution.values())
        
        categories = ['Debt', 'Savings', 'Leisure', 'Food']
        for category in categories:
            amount = (distribution[category] / total_proportion) * remaining_income
            self.update_finance(paystub_date, category, amount)

    
    def get_distribution(self):
        if not self.distribution_store.exists('distribution'):
            # Default distribution
            self.distribution_store.put('distribution', Debt=8, Savings=9, Leisure=2, Food=5)
        
        return self.distribution_store.get('distribution')
    
    def update_finance(self, paystub_date, category, amount):
        finance_store = JsonStore('finance.json')
        if finance_store.exists(paystub_date):
            paystub_data = finance_store.get(paystub_date)
            paystub_data[category] = paystub_data.get(category, 0) + amount
            finance_store.put(paystub_date, **paystub_data)
        else:
            finance_store.put(paystub_date, **{category: amount})
    
    def go_to_adjust_distribution(self, instance):
        self.manager.current = 'AJ page'

    def go_back(self, instance):
        self.manager.current = 'front'

# Allows user to view there current finances, such as how much money they have earned, and where it has gone
class VCFPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.finance_store = JsonStore('finance.json')
        self.paystub_store = JsonStore('paystub.json')
        
        layout = GridLayout(cols=1, spacing=20, padding=30)
        
        top_box = BoxLayout(orientation='vertical', size_hint=(1, None), height=50)
        back_button = Button(
            text='Home',
            background_normal='',
            background_color=(0, 0, 1, 1),
            color=(1, 1, 1, 1),
            font_size=18,
            font_name='Roboto',
            size_hint=(0.09, 1),
            on_press=self.go_back
        )
        top_box.add_widget(back_button)
        layout.add_widget(top_box)
        
        current_finances_label = Label(text='Current Finances', size_hint=(1, None), height=50, font_size=40, font_name='Roboto', bold=True)
        layout.add_widget(current_finances_label)
        
        self.distribution_table = GridLayout(cols=2, spacing=10, size_hint=(1, None), height=200)
        layout.add_widget(self.distribution_table)
        
        graph_label = Label(text='Paystub Distribution Over Time', size_hint=(1, None), height=50, font_size=30, font_name='Roboto', bold=True)
        layout.add_widget(graph_label)
        
        self.graph = Graph(xlabel='Date', ylabel='Amount', x_ticks_minor=5, x_ticks_major=25, y_ticks_major=50, y_grid_label=True, x_grid_label=True, padding=5, x_grid=True, y_grid=True, xmin=0, xmax=100, ymin=0, ymax=1000)
        layout.add_widget(self.graph)
        
        total_money_label = Label(text='Total Money Earned: $0', size_hint=(1, None), height=50, font_size=30, font_name='Roboto', bold=True)
        layout.add_widget(total_money_label)
        
        self.add_widget(layout)
        self.load_distribution()
        self.load_graph()
        self.calculate_total_money(total_money_label)
        
        with self.canvas.before:
            Color(20/255, 38/255, 81/255, 1) # Dark blue background color
            self.rect = Rectangle(size=self.size, pos=self.pos)
        
        self.bind(size=self._update_rect, pos=self._update_rect)
    
    def _update_rect(self, instance, value):
        instance.rect.pos = instance.pos
        instance.rect.size = instance.size
    
    def load_distribution(self):
        self.distribution_table.clear_widgets()
        latest_paystub_date = self.get_latest_paystub_date()
        if latest_paystub_date:
            distribution = self.finance_store.get(latest_paystub_date)
            for category, amount in distribution.items():
                category_label = Label(text=category, font_name='Roboto')
                amount_label = Label(text=f'${amount:.2f}', font_name='Roboto')
                self.distribution_table.add_widget(category_label)
                self.distribution_table.add_widget(amount_label)
        else:
            no_data_label = Label(text='No paystub data available', font_name='Roboto')
            self.distribution_table.add_widget(no_data_label)
    
    def get_latest_paystub_date(self):
        paystub_dates = list(self.paystub_store.keys())
        if paystub_dates:
            return max(paystub_dates)
        else:
            return None
    
    def load_graph(self):
        self.graph.clear_plot()
        paystub_dates = list(self.paystub_store.keys())
        paystub_dates.sort(reverse=True)
        paystub_dates = paystub_dates[:6]  # Get the last 6 paystubs
        
        for paystub_date in paystub_dates:
            distribution = self.finance_store.get(paystub_date)
            total_amount = sum(distribution.values())
            plot = LinePlot(color=[1, 1, 0, 1])
            plot.points = [(paystub_date, total_amount)]
            self.graph.add_plot(plot)
        
        self.graph.xmin = 0
        self.graph.xmax = len(paystub_dates)
        self.graph.x_ticks_major = 1
        self.graph.x_labels = paystub_dates
        self.graph.x_label_texture_size = (50, None)
        
        self.graph.ymin = 0
        self.graph.ymax = max(sum(self.finance_store.get(date).values()) for date in paystub_dates) * 1.1
    
    def calculate_total_money(self, total_money_label):
        total_money = sum(sum(self.finance_store.get(date).values()) for date in self.paystub_store.keys())
        total_money_label.text = f'Total Money Earned: ${total_money:.2f}'
    
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