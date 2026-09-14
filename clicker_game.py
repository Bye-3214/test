import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

class ClickerGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Кликер Игра")
        self.root.geometry("500x600")
        self.root.resizable(False, False)
        
        # Переменные игры
        self.score = 0
        self.click_power = 1
        self.auto_clickers = 0
        self.click_multiplier = 1
        
        # Загрузка сохранения
        self.load_game()
        
        # Создание интерфейса
        self.create_widgets()
        
        # Запуск авто-кликера
        self.auto_click()
    
    def create_widgets(self):
        # Главный фрейм
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Заголовок
        title_label = ttk.Label(main_frame, text="🎮 КЛИКЕР ИГРА 🎮", font=("Arial", 20, "bold"))
        title_label.pack(pady=10)
        
        # Счет
        self.score_label = ttk.Label(main_frame, text=f"Счет: {self.score}", font=("Arial", 24, "bold"), foreground="blue")
        self.score_label.pack(pady=20)
        
        # Кнопка клика
        self.click_button = tk.Button(main_frame, text="🖱️ КЛИК! 🖱️", font=("Arial", 18, "bold"), 
                                      bg="#4CAF50", fg="white", width=20, height=3,
                                      command=self.click, activebackground="#45a049")
        self.click_button.pack(pady=20)
        
        # Статистика
        stats_frame = ttk.LabelFrame(main_frame, text="Статистика", padding="10")
        stats_frame.pack(fill=tk.X, pady=10)
        
        self.power_label = ttk.Label(stats_frame, text=f"Сила клика: {self.click_power}")
        self.power_label.pack(anchor=tk.W)
        
        self.auto_label = ttk.Label(stats_frame, text=f"Авто-кликеры: {self.auto_clickers}")
        self.auto_label.pack(anchor=tk.W)
        
        self.multiplier_label = ttk.Label(stats_frame, text=f"Множитель: x{self.click_multiplier}")
        self.multiplier_label.pack(anchor=tk.W)
        
        # Магазин улучшений
        shop_frame = ttk.LabelFrame(main_frame, text="Магазин улучшений", padding="10")
        shop_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Улучшение силы клика
        click_upgrade_frame = ttk.Frame(shop_frame)
        click_upgrade_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(click_upgrade_frame, text="💪 Усилить клик (+1)").pack(side=tk.LEFT)
        self.click_upgrade_cost = max(10, int(self.click_power * 10))
        self.click_upgrade_btn = ttk.Button(click_upgrade_frame, text=f"Купить ({self.click_upgrade_cost})", 
                                           command=self.buy_click_upgrade)
        self.click_upgrade_btn.pack(side=tk.RIGHT)
        
        # Авто-кликер
        auto_clicker_frame = ttk.Frame(shop_frame)
        auto_clicker_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(auto_clicker_frame, text="🤖 Авто-кликер (+1/сек)").pack(side=tk.LEFT)
        self.auto_clicker_cost = max(50, int(self.auto_clickers * 50 + 50))
        self.auto_clicker_btn = ttk.Button(auto_clicker_frame, text=f"Купить ({self.auto_clicker_cost})", 
                                          command=self.buy_auto_clicker)
        self.auto_clicker_btn.pack(side=tk.RIGHT)
        
        # Множитель
        multiplier_frame = ttk.Frame(shop_frame)
        multiplier_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(multiplier_frame, text="⭐ Множитель (x2)").pack(side=tk.LEFT)
        self.multiplier_cost = max(200, int(self.click_multiplier * 200))
        self.multiplier_btn = ttk.Button(multiplier_frame, text=f"Купить ({self.multiplier_cost})", 
                                        command=self.buy_multiplier)
        self.multiplier_btn.pack(side=tk.RIGHT)
        
        # Кнопки управления
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(fill=tk.X, pady=10)
        
        save_btn = ttk.Button(control_frame, text="💾 Сохранить", command=self.save_game)
        save_btn.pack(side=tk.LEFT, padx=5)
        
        reset_btn = ttk.Button(control_frame, text="🔄 Сброс", command=self.reset_game)
        reset_btn.pack(side=tk.LEFT, padx=5)
        
        # Обновление интерфейса
        self.update_interface()
    
    def click(self):
        points_earned = self.click_power * self.click_multiplier
        self.score += points_earned
        self.update_interface()
        self.save_game()
    
    def buy_click_upgrade(self):
        cost = max(10, int(self.click_power * 10))
        if self.score >= cost:
            self.score -= cost
            self.click_power += 1
            self.click_upgrade_cost = max(10, int(self.click_power * 10))
            self.update_interface()
            self.save_game()
        else:
            messagebox.showinfo("Недостаточно средств", "Нужно больше очков!")
    
    def buy_auto_clicker(self):
        cost = max(50, int(self.auto_clickers * 50 + 50))
        if self.score >= cost:
            self.score -= cost
            self.auto_clickers += 1
            self.auto_clicker_cost = max(50, int(self.auto_clickers * 50 + 50))
            self.update_interface()
            self.save_game()
        else:
            messagebox.showinfo("Недостаточно средств", "Нужно больше очков!")
    
    def buy_multiplier(self):
        cost = max(200, int(self.click_multiplier * 200))
        if self.score >= cost:
            self.score -= cost
            self.click_multiplier *= 2
            self.multiplier_cost = max(200, int(self.click_multiplier * 200))
            self.update_interface()
            self.save_game()
        else:
            messagebox.showinfo("Недостаточно средств", "Нужно больше очков!")
    
    def auto_click(self):
        if self.auto_clickers > 0:
            points_earned = self.auto_clickers * self.click_power * self.click_multiplier
            self.score += points_earned
            self.update_interface()
            self.save_game()
        # Запуск через 1 секунду
        self.root.after(1000, self.auto_click)
    
    def update_interface(self):
        self.score_label.config(text=f"Счет: {self.score}")
        self.power_label.config(text=f"Сила клика: {self.click_power}")
        self.auto_label.config(text=f"Авто-кликеры: {self.auto_clickers}")
        self.multiplier_label.config(text=f"Множитель: x{self.click_multiplier}")
        
        # Обновление цен и кнопок
        click_cost = max(10, int(self.click_power * 10))
        self.click_upgrade_btn.config(text=f"Купить ({click_cost})")
        
        auto_cost = max(50, int(self.auto_clickers * 50 + 50))
        self.auto_clicker_btn.config(text=f"Купить ({auto_cost})")
        
        multi_cost = max(200, int(self.click_multiplier * 200))
        self.multiplier_btn.config(text=f"Купить ({multi_cost})")
    
    def save_game(self):
        game_data = {
            'score': self.score,
            'click_power': self.click_power,
            'auto_clickers': self.auto_clickers,
            'click_multiplier': self.click_multiplier
        }
        try:
            with open('clicker_save.json', 'w') as f:
                json.dump(game_data, f)
        except Exception as e:
            print(f"Ошибка сохранения: {e}")
    
    def load_game(self):
        try:
            if os.path.exists('clicker_save.json'):
                with open('clicker_save.json', 'r') as f:
                    game_data = json.load(f)
                    self.score = game_data.get('score', 0)
                    self.click_power = game_data.get('click_power', 1)
                    self.auto_clickers = game_data.get('auto_clickers', 0)
                    self.click_multiplier = game_data.get('click_multiplier', 1)
        except Exception as e:
            print(f"Ошибка загрузки: {e}")
    
    def reset_game(self):
        if messagebox.askyesno("Сброс игры", "Вы уверены, что хотите сбросить весь прогресс?"):
            self.score = 0
            self.click_power = 1
            self.auto_clickers = 0
            self.click_multiplier = 1
            self.update_interface()
            self.save_game()

if __name__ == "__main__":
    root = tk.Tk()
    game = ClickerGame(root)
    root.mainloop()
