class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __str__(self):
        return f" '{self.name}' exp_day: {self.sell_in} qu: {self.quality} {'Expired!' if self.sell_in == 0 else ''}"


class NewItem(Item):
    """
    Наследуемся от первоначального класса Item
    """
    def __init__(self, name, sell_in, quality, update_func):
        super().__init__(name, sell_in, quality)
        self.__update_func = update_func  # метод расчета качества

    def update_quality(self):
        self.sell_in, self.quality = self.__update_func(self.sell_in, self.quality)
        # Второй вариант решения проблемы легендарных товаров:
        # if self.__update_func == Store.calc_method_quality_stable:
        #     # для товаров с легендарным методом расчета качества
        #     self.quality = Store.STABLE_QUALITY
        # else:
        #     self.sell_in, self.quality = self.__update_func(self.sell_in, self.quality)


class Store(list):
    """
    Класс описывающий магазин
    """
    MIN_QUALITY = 0  # минимальное значение качества товара
    MAX_QUALITY = 50  # максимальное значение качества товара
    STABLE_QUALITY = 80  # качество для легендарных товаров

    def __init__(self, name):
        super().__init__()
        self.name = name  # название магазина

    def update_quality(self):
        """
        Обновление качества каждого товара в магазине
        :return: None
        """
        for item in self:
            item.update_quality()

    def show_store(self):
        """
        Вывод на консоль содержимого магазина
        :return: None
        """
        for item in self:
            print(item)

    @staticmethod
    def day_check(day):
        """
        Проверка дня на валидность
        :param day: int
        :return: int - целое положительное число
        """
        return day if day > 0 else 0

    @staticmethod
    def quality_check(quality):
        """
        Проверка значения качества на валидность
        :param quality: int
        :return: int
        """
        if quality < Store.MIN_QUALITY:
            return Store.MIN_QUALITY
        elif quality in range(Store.MIN_QUALITY, Store.MAX_QUALITY + 1):
            return quality
        else:
            return Store.MAX_QUALITY

    @staticmethod
    def calc_method_quality_default(day, quality):
        """
        Способ расчета качества - стандартный
        :param day: int - день
        :param quality: int - качество
        :return: tuple(int, int) - новые значения дня и качества
        """
        quality -= 1 if day > 0 else 2  # качество убывает в 2 раза быстрее при истечении срока хранения
        day -= 1  # уменьшаем на 1 день
        return Store.day_check(day), Store.quality_check(quality)

    @staticmethod
    def calc_method_quality_increase(day, quality):
        """
        Способ расчета качества - качество растет до максимума с увеличением сроков хранения товара
        :param day: int - день
        :param quality: int - качество
        :return: tuple(int, int) - новые значения дня и качества
        """
        quality += 1
        day -= 1
        return Store.day_check(day), Store.quality_check(quality)

    @staticmethod
    def calc_method_quality_stable(day, quality):
        """
        Легендарный метод расчета качества
        Способ расчета качества - неизменное качество и неограниченный срок хранения товара
        :param day: int - день
        :param quality: int - качество
        :return: tuple(int, int) - новые значения дня и качества
        """
        return Store.day_check(day), Store.STABLE_QUALITY

    @staticmethod
    def calc_method_default_fast(day, quality):
        """
        Способ расчета качества - качество уменьшается в 2 раза быстрее с увеличением срока хранения товара
        :param day: int - день
        :param quality: int - качество
        :return: tuple(int, int) - новые значения дня и качества
        """
        quality -= 2 if day > 0 else 4  # в 2 раза быстрее
        day -= 1
        return Store.day_check(day), Store.quality_check(quality)


if __name__ == '__main__':
    store = Store("Wonder store")
    store.append(NewItem("Default item", 10, 40, Store.calc_method_quality_default))
    store.append(NewItem("Aged Brie", 10, 40, Store.calc_method_quality_increase))
    store.append(NewItem("Sulfuras", 10, 80, Store.calc_method_quality_stable))
    store.append(NewItem("Conjured", 10, 40, Store.calc_method_default_fast))

    for d in range(20):
        print(f">>>> day: {d}:")
        store.update_quality()
        store.show_store()
