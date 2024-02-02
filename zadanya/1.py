#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dataclasses import dataclass
import xml.etree.ElementTree as ET


@dataclass
class Money:
    rubles: int = 0
    kopecks: int = 0

    def read(self) -> None:
        self.rubles, self.kopecks = map(int, input("Введите количество рублей и копеек через пробел: ").split())

    def display(self) -> None:
        print(f"{self.rubles} руб. {self.kopecks:02d} коп.")

    def add(self, other: 'Money') -> 'Money':
        total_kopecks = self.rubles * 100 + self.kopecks + other.rubles * 100 + other.kopecks
        return Money(*divmod(total_kopecks, 100))

    def subtract(self, other: 'Money') -> 'Money':
        total_kopecks = self.rubles * 100 + self.kopecks - (other.rubles * 100 + other.kopecks)
        return Money(*divmod(total_kopecks, 100))

    def divide_sum(self, num: float) -> 'Money':
        total_kopecks = (self.rubles * 100 + self.kopecks) / num
        return Money(*divmod(int(total_kopecks), 100))

    def multiply_by_number(self, num: float) -> 'Money':
        total_kopecks = (self.rubles * 100 + self.kopecks) * num
        return Money(*divmod(int(total_kopecks), 100))

    def compare(self, other: 'Money') -> bool:
        return self.rubles == other.rubles and self.kopecks == other.kopecks

    def is_less_than(self, other: 'Money') -> bool:
        return (self.rubles * 100 + self.kopecks) < (other.rubles * 100 + other.kopecks)

    def to_xml_element(self) -> ET.Element:
        money_element = ET.Element('Money')
        ET.SubElement(money_element, 'Rubles').text = str(self.rubles)
        ET.SubElement(money_element, 'Kopecks').text = str(self.kopecks)
        return money_element

    @classmethod
    def from_xml_element(cls, element: ET.Element) -> 'Money':
        rubles = int(element.find('Rubles').text)
        kopecks = int(element.find('Kopecks').text)
        return cls(rubles, kopecks)


if __name__ == '__main__':
    money1 = Money()
    money1.read()
    money1.display()

    money2 = Money()
    money2.read()
    money2.display()

    sum_result = money1.add(money2)
    print("Сумма:")
    sum_result.display()

    diff_result = money1.subtract(money2)
    print("Разность:")
    diff_result.display()

    divide_sum_num = float(input("Введите число для деления суммы: "))
    div_sum_result = money1.divide_sum(divide_sum_num)
    print("Деление суммы на число:")
    div_sum_result.display()

    multiply_by_num = float(input("Введите число для умножения: "))
    mul_result = money1.multiply_by_number(multiply_by_num)
    print("Умножение на число:")
    mul_result.display()

    comparison_result = money1.compare(money2)
    print(f"Сравнение: {comparison_result}")

    comparison_result_lt = money1.is_less_than(money2)
    print(f"Сравнение меньше: {comparison_result_lt}")

    # Сохранение в XML
    money1_element = money1.to_xml_element()
    tree = ET.ElementTree(money1_element)
    tree.write('money_data.xml')

    # Загрузка из XML
    loaded_tree = ET.parse('money_data.xml')
    loaded_money_element = loaded_tree.getroot()
    loaded_money = Money.from_xml_element(loaded_money_element)
    print("Данные, загруженные из XML:")
    loaded_money.display()
