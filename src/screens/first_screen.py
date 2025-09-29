#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 29 18:27:29 2025

@author: ann
"""

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.switch import Switch
from kivy.core.window import Window
from kivy.storage.jsonstore import JsonStore
from kivy.clock import Clock

import re

class FirstLaunchScreen(Screen):
    def __init__(self, **kwargs):  # ⚠️ ИСПРАВЬ: было (self, kwargs)
        super().__init__(**kwargs)
        self.store = JsonStore('user.json')
        self.build_ui()
    
    def build_ui(self):
        root = BoxLayout(orientation="vertical", padding=20, spacing=15)  # ⚠️ ИСПРАВЬ: было "spacting"
        
        root.add_widget(Label(text='Добро пожаловать', font_size='24sp', size_hint_y=None, height=40))

        # --- Имя ---
        root.add_widget(Label(text='Имя', size_hint_y=None, height=30))
        self.name_inp = TextInput(multiline=False, size_hint_y=None, height=40, write_tab=False)
        self.name_inp.bind(text=self.validate)
        root.add_widget(self.name_inp)

        # --- Телефон ---
        root.add_widget(Label(text='Телефон', size_hint_y=None, height=30))
        self.phone_inp = TextInput(multiline=False, size_hint_y=None, height=40, input_filter=self.phone_filter, write_tab=False)
        self.phone_inp.bind(text=self.validate)
        root.add_widget(self.phone_inp)

        # --- Будильники ---
        root.add_widget(Label(text='Будильники', size_hint_y=None, height=30))
        alarms = [('Утро 06:30', 'morning'), ('День 12:30', 'day'), ('Вечер 21:30', 'evening')]
        self.switches = {}
        for txt, key in alarms:
            box = BoxLayout(size_hint_y=None, height=30)
            box.add_widget(Label(text=txt))
            sw = Switch(active=True)
            self.switches[key] = sw
            box.add_widget(sw)
            root.add_widget(box)

        # --- Кнопка ---
        self.save_btn = Button(text='Сохранить и начать', size_hint_y=None, height=50, disabled=True)
        self.save_btn.bind(on_release=self.save_and_go)
        root.add_widget(self.save_btn)

        self.add_widget(root)

    def phone_filter(self, text, from_undo=False):
        # разрешаем только цифры, максимум 10
        return re.sub(r'[^0-9]', '', text)[:10]

    def validate(self, *a):
        # кнопка активна, если имя не пустое и телефон = 10 цифр
        name_ok = bool(self.name_inp.text.strip())
        phone_ok = len(self.phone_inp.text) == 10
        self.save_btn.disabled = not (name_ok and phone_ok)

    def save_and_go(self, btn):
        self.store.put('user',
                       name=self.name_inp.text.strip(),
                       phone=self.phone_inp.text,
                       morning=self.switches['morning'].active,
                       day=self.switches['day'].active,
                       evening=self.switches['evening'].active)
        # переход на основной экран
        self.manager.current = 'morning'  # ⚠️ ИСПРАВЬ: было switch_to