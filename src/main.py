"""
Main entry point for the application.

This module sets up the Kivy application, creates the screen manager, and adds the necessary pages.
"""

import kivy

kivy.require('2.3.0')

from front_page import FrontPage
from ui_page import UIPage
from aps_page import APSPage
from vcf_page import VCFPage
from ad_page import ADPage
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager


class MyApp(App):
    """
    Main application class.

    This class inherits from the Kivy App class and defines the application's build method.
    """

    def build(self):
        """
        Build the application.

        This method is called when the application starts. It creates a screen manager and adds the necessary pages.

        Returns:
            ScreenManager: The screen manager containing the application's pages.
        """
        sm = ScreenManager()
        sm.add_widget(FrontPage(name='front'))
        sm.add_widget(UIPage(name='UI page'))
        sm.add_widget(APSPage(name='APS page'))
        sm.add_widget(VCFPage(name='VCF page'))
        sm.add_widget(ADPage(name='AD page'))
        return sm


if __name__ == '__main__':
    """
    Run the application.

    This block is executed when the script is run directly (not imported as a module).
    It creates an instance of the MyApp class and runs it.
    """
    MyApp().run()