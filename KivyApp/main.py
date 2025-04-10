from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.card import MDCard
from kivy.core.window import Window

Window.size = (360, 640)

class ABSRApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.accent_palette = "Lime"
        self.theme_cls.theme_style = "Dark"

        screen = MDScreen()
        layout = MDBoxLayout(orientation="vertical", spacing=20, padding=20)

        toolbar = MDTopAppBar(
            title="ABSR",
            elevation=10,
            md_bg_color=self.theme_cls.primary_color,
            left_action_items=[["menu", lambda x: print("Menu pressed")]],
        )
        screen.add_widget(toolbar)

        welcome_card = MDCard(
            orientation="vertical",
            size_hint=(0.95, None),
            height="200dp",
            padding="24dp",
            pos_hint={"center_x": 0.5},
            md_bg_color=self.theme_cls.bg_dark,
            shadow_softness=5,
            shadow_offset=(0, 2),
            line_color=(0.3, 0.3, 0.3, 0.2),
        )

        welcome_label = MDLabel(
            text="Welcome to [b]ABSR[/b]\n[i]The most advanced business rating system ever created![/i]",
            halign="center",
            theme_text_color="Custom",
            text_color=self.theme_cls.primary_light,
            markup=True,
            font_style="H6",
        )

        start_button = MDRaisedButton(
            text="Get Started",
            pos_hint={"center_x": 0.5},
            md_bg_color=self.theme_cls.accent_color,
            on_release=lambda x: print("Getting Started..."),
        )

        welcome_card.add_widget(welcome_label)
        welcome_card.add_widget(start_button)

        layout.add_widget(welcome_card)
        screen.add_widget(layout)
        return screen

if __name__ == "__main__":
    ABSRApp().run()
