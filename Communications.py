import sqlite3
import tkinter as tk
import tkinter.ttk as ttk

class InvalidTariffError(Exception):
    def __init__(self, tariff):
        self.tariff = tariff
        super().__init__(f"Invalid tariff: {tariff}")

class TelephoneCommunications:
    def __init__(self, *users):
        self.users = users

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            for user in self.users:
                if callable(user):
                    user(*args, **kwargs)
            return result
        return wrapper

from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class Tariff:
    name: str
    price: int

    def __str__(self):
        return f"{self.name} - {self.price} RUB"

class OperatorInterface(ABC):
    @abstractmethod
    def display_operator_details(self):
        pass

    @abstractmethod
    def pick_tariff(self, tariff_input: int):
        pass

class BaseOperator(OperatorInterface):
    def __init__(self, name, speed, quality, tariffs):
        self.name = name
        self.speed = speed
        self.quality = quality
        self.tariffs = [Tariff(f"Тариф {i}", price) for i, price in enumerate(tariffs, start=1)]

    def display_operator_details(self):
        print(f"Выбранный оператор: {self.name}")
        print(f"Скорость соединения: {self.speed}")
        print(f"Качество связи: {self.quality}")
        print(f"Тарифы: {', '.join(map(str, self.tariffs))} RUB")

    def pick_tariff(self, tariff_input: int):
        if tariff_input in [tariff.price for tariff in self.tariffs]:
            print(f"Тариф за {tariff_input} RUB оформлен. Спасибо, что пользуетесь нами!")
        else:
            raise InvalidTariffError(tariff_input)

class MegafonOperator(BaseOperator):
    def __init__(self):
        super().__init__('Megafon', 'отличная', 'замечательное', [200, 400, 700])

class MTSOperator(BaseOperator):
    def __init__(self):
        super().__init__('MTS', 'высокая', 'хорошее', [299, 499, 899])

class Tele2Operator(BaseOperator):
    def __init__(self):
        super().__init__('Tele2', 'низкая', 'удовлетворительное', [249, 419, 719])

class YotaOperator(BaseOperator):
    def __init__(self):
        super().__init__('Yota', 'очень низкая', 'плохое', [350, 550, 850])

from typing import TypeVar, Generic

T = TypeVar('T', bound='BaseOperator')

class GenericOperator(Generic[T]):
    def __init__(self, operator: T):
        self.operator = operator

    def display_operator_details(self):
        self.operator.display_operator_details()

    def pick_tariff(self, tariff_input: int) -> None:
        self.operator.pick_tariff(tariff_input)

class Network:
    def __init__(self):
        self.operators = {
            'MEGAFON': MegafonOperator(),
            'MTS': MTSOperator(),
            'TELE2': Tele2Operator(),
            'YOTA': YotaOperator(),
        }

    def __del__(self):
        print("Сеть мобильных операторов удалена.")

    def select_operator(self, operator_name):
        return self.operators.get(operator_name.upper())

    def call_check_work(self, func_name, operator):
        def call_check():
            self.check_work()
        return call_check


    def check_work(self):
        print("Количество оформленных тарифов:", self.tariffs_count)

def main():
    network = Network()

    def show_operators():
        operator_names = [op.name for op in network.operators.values()]
        operator_text = "\n".join(operator_names)
        operator_label = tk.Label(root, text=operator_text, wraplength=480)
        operator_label.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

    def show_tariffs():
        tariff_text = ""
        for op in network.operators.values():
            tariff_text += f"{op.name}:\n"
            for tariff in op.tariffs:
                tariff_text += f"  - {tariff.name} ({tariff.price} RUB)\n"
        tariff_label = tk.Label(root, text=tariff_text, wraplength=480)
        tariff_label.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

    def show_about():
        about_window = tk.Toplevel(root)
        about_window.title("О нас")
        about_label = tk.Label(about_window, text="Здесь будет информация о нас")
        about_label.pack()

    root = tk.Tk()
    root.title("Коммуникации.Арх")
    root.geometry("500x500")
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - 500) // 2
    y = (screen_height - 500) // 2

    root.geometry(f"+{x}+{y}")

    for c in range(2):
        root.columnconfigure(index=c, weight=1)
    for r in range(3):
        root.rowconfigure(index=r, weight=1)

    btn1 = ttk.Button(text="Ознакомиться с операторами", command=show_operators)
    btn1.grid(row=0, column=0, columnspan=2, ipadx=70, ipady=6, padx=5, pady=5)

    btn3 = ttk.Button(text="Выбрать тариф подключения", command=show_tariffs)
    btn3.grid(row=1, column=0, ipadx=6, ipady=6, padx=5, pady=5)

    btn4 = ttk.Button(text="Подробнее о компании", command=show_about)
    btn4.grid(row=1, column=1, ipadx=6, ipady=6, padx=5, pady=5)

    root.mainloop()

if __name__ == '__main__':
    main()