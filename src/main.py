from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from screens.first_launch import FirstLaunchScreen
from screens.morning import MorningScreen

class UtroApp(App):
    def build(self):
        try:
            print("=== Запуск приложения ===")
            sm = ScreenManager()
            
            # Сначала добавляем оба экрана
            sm.add_widget(FirstLaunchScreen(name='first'))
            sm.add_widget(MorningScreen(name='morning'))
            
            # Потом выбираем какой показывать
            if not self.user_exists():
                print("Пользователь не найден, показываем первый запуск")
                sm.current = 'first'
            else:
                print("Пользователь найден, показываем утренний экран")
                sm.current = 'morning'
                
            print("=== Приложение успешно построено ===")
            return sm
            
        except Exception as e:
            print(f"ОШИБКА в build: {e}")
            import traceback
            traceback.print_exc()
            raise

    def user_exists(self):
        try:
            from kivy.storage.jsonstore import JsonStore
            store = JsonStore('user.json')
            exists = store.exists('user')
            print(f"Проверка пользователя: {exists}")
            return exists
        except Exception as e:
            print(f"Ошибка при проверке пользователя: {e}")
            return False

if __name__ == '__main__':
    print("=== START APP ===")
    UtroApp().run()