class WrongInputError(Exception):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return 'Слишком мало параметров с --!'

    def __eq__(self, other):
        if isinstance(other, WrongInputError):
            return self.__str__() == other.__str__()
        return False


class WrongParameterNameError(Exception):
    def __init__(self, name):
        self.name = name
        super().__init__(self.name)

    def __str__(self):
        return f'Не существует параметра с именем {self.name}!'

    def __eq__(self, other):
        if isinstance(other, WrongParameterNameError):
            return self.__str__() == other.__str__()
        return False


class WrongCountParametersError(Exception):
    def __init__(self, count):
        self.count = count
        super().__init__(self.count)

    def __str__(self):
        return f'Слишком мало параметров: {self.count - 1}!'

    def __eq__(self, other):
        if isinstance(other, WrongCountParametersError):
            return self.__str__() == other.__str__()
        return False


class WrongFileError(Exception):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return 'Не получается открыть файл!'

    def __eq__(self, other):
        if isinstance(other, WrongFileError):
            return self.__str__() == other.__str__()
        return False


class WrongHtmlError(Exception):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return 'На странице нет логов!'

    def __eq__(self, other):
        if isinstance(other, WrongHtmlError):
            return self.__str__() == other.__str__()
        return False


class WrongPathError(Exception):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return 'Такого пути нет!'

    def __eq__(self, other):
        if isinstance(other, WrongPathError):
            return self.__str__() == other.__str__()
        return False
