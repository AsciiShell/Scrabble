import os
import warnings
from typing import List, Dict, Union


class GameConfig:
    """Конфигурация игры"""
    map: List[List[int]] = \
        [[4, 0, 0, 1, 0, 0, 0, 4, 0, 0, 0, 1, 0, 0, 4],
         [0, 2, 0, 0, 0, 3, 0, 0, 0, 3, 0, 0, 0, 2, 0],
         [0, 0, 2, 0, 0, 0, 1, 0, 1, 0, 0, 0, 2, 0, 0],
         [1, 0, 0, 2, 0, 0, 0, 1, 0, 0, 0, 2, 0, 0, 1],
         [0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0],
         [0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0],
         [0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0],
         [4, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 4],
         [0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0],
         [0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0],
         [0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0],
         [1, 0, 0, 2, 0, 0, 0, 1, 0, 0, 0, 2, 0, 0, 1],
         [0, 0, 2, 0, 0, 0, 1, 0, 1, 0, 0, 0, 2, 0, 0],
         [0, 2, 0, 0, 0, 3, 0, 0, 0, 3, 0, 0, 0, 2, 0],
         [4, 0, 0, 1, 0, 0, 0, 4, 0, 0, 0, 1, 0, 0, 4]]
    """Карта поля"""
    letters: Dict[str, Dict[str, int]] = \
        {'А': {'count': 10, 'price': 1},
         'Б': {'count': 3, 'price': 3},
         'В': {'count': 5, 'price': 2},
         'Г': {'count': 3, 'price': 3},
         'Д': {'count': 5, 'price': 2},
         'Е': {'count': 9, 'price': 1},
         'Ж': {'count': 2, 'price': 5},
         'З': {'count': 2, 'price': 5},
         'И': {'count': 8, 'price': 1},
         'Й': {'count': 4, 'price': 2},
         'К': {'count': 6, 'price': 2},
         'Л': {'count': 4, 'price': 2},
         'М': {'count': 5, 'price': 2},
         'Н': {'count': 8, 'price': 1},
         'О': {'count': 10, 'price': 1},
         'П': {'count': 6, 'price': 2},
         'Р': {'count': 6, 'price': 2},
         'С': {'count': 6, 'price': 2},
         'Т': {'count': 5, 'price': 2},
         'У': {'count': 3, 'price': 3},
         'Ф': {'count': 1, 'price': 10},
         'Х': {'count': 2, 'price': 5},
         'Ц': {'count': 1, 'price': 10},
         'Ч': {'count': 2, 'price': 5},
         'Ш': {'count': 1, 'price': 10},
         'Щ': {'count': 1, 'price': 10},
         'Ъ': {'count': 1, 'price': 10},
         'Ы': {'count': 2, 'price': 5},
         'Ь': {'count': 2, 'price': 5},
         'Э': {'count': 1, 'price': 10},
         'Ю': {'count': 1, 'price': 10},
         'Я': {'count': 3, 'price': 3},
         '*': {'count': 0, 'price': None}}
    """Список всех букв с ценой и количеством"""
    startCount: int = 10
    """Начальное число фишек"""
    fullBonus: int = 15
    """Бонус за полное использование фишек"""
    skipEnd: int = 2
    """Количество пропусков для завершения игры"""
    turnTime: int = 120
    """Время хода"""


class Point:
    """Класс ячейки поля"""
    info: List[Dict[str, Union[str, int]]] = \
        [{'color': 'white', 'multi': 'letter', 'value': 1},
         {'color': 'green', 'multi': 'letter', 'value': 2},
         {'color': 'blue', 'multi': 'word', 'value': 2},
         {'color': 'yellow', 'multi': 'letter', 'value': 3},
         {'color': 'red', 'multi': 'word', 'value': 3}, ]

    @property
    def get_info(self) -> Dict[str, Union[str, int]]:
        """Возвращает информацию о текущей точке

        :rtype: Dict[str, Union[str, int]]
        """
        return self.info[self.t]

    @property
    def get_score(self) -> int:
        """Возвращает стоимость буквы на поле

        :rtype: int
        """
        if self.multi == "letter":
            return GameConfig.letters[self.letter]['price'] * self.value
        else:
            return GameConfig.letters[self.letter]['price']

    @property
    def get_multi(self) -> int:
        """

        :return: Множитель слова
        :rtype: int
        """
        if self.multi == "letter":
            return 1
        else:
            return self.value

    def __init__(self, x: int, y: int, letter: str) -> None:
        """Создает букву по указанным координатам

        :param x: Х координата
        :type x: int

        :param y: У координата
        :type y: int

        :param letter: Буква
        :type letter: str
        """
        self.x = x
        self.y = y
        self.letter = letter

        try:
            self.t = GameConfig.map[x][y]
        except Exception:
            print("Error")
        self.color = Point.info[self.t]["color"]
        self.multi = Point.info[self.t]["multi"]
        self.value = Point.info[self.t]["value"]


class Message:
    """Класс возвращаемых сообщений"""

    def __init__(self, res: bool = False, msg: str = "") -> None:
        """

        :param res: Статус операции
        :type res: int

        :param msg: Сообщение
        :type msg: str
        """
        self.res = res
        self.msg = msg


class MatrixResult:
    """Результат проверки матрицы"""

    def __init__(self, stat: bool, score: int = 0, words: List[str] = None, errmsg: str = "") -> None:
        """

        :param stat: Результат проверки
        :type stat: bool

        :param score: Сумма очков
        :type score: int

        :param words: Список найденных или ошибочных слов
        :type words: List[str]

        :param errmsg: Сообщение об ошибке
        :type errmsg: str
        """
        self.score = score
        self.result = stat
        if stat:
            if words is None:
                warnings.warn("Слова не найдены")
            self.words = words
        else:
            self.msg = errmsg
            self.wordsError = words


class Matrix:
    """Класс игрового поля"""

    # TODO andrsolo21 создай/укажи 2 метода и назови их красиво
    # первый принимает массив новых букв
    # возвращает структуру состоящую из
    #     a)успеха,
    #     b)суммы очков,
    #     c)найденные слова,
    #     или
    #     d)список ошибок (клетка занята), слово не существует в словаре
    #
    #     ошибки больше нужны для человека
    # второй принимает все то же самое,
    # вызывает первую функцию а затем, в случае успеха, фиксирует изменения
    # По идее все методы есть, их надо красиво скомпоновать
    # те сделать newkoord и newletters локальными, убрать обращение к ним извне и передавать как параметр
    #
    # P.S.
    # TODO думаю словарь хранить тоже в матрице, так как там он и обрабатывается. Как думаешь?
    # TODO P.P.S в этом файле ошибки только в этом классе
    def add_temporary(self, arr):
        """Добавляет несколько элементов во временную матрицу"""
        if type(arr) is list:
            self.temp.extend(arr)
        elif type(arr) is int:
            self.temp.append(arr)
        else:
            raise Exception('Wrong type' + str(arr))

    def accept_temp(self):
        """Принимает временные изменения"""
        for i in self.temp:
            self.map[i.x][i.y] = i
        self.reject_temp()

    def reject_temp(self):
        """Отклоняет временные изменения"""
        self.newkoord = []
        self.newletters = []
        self.tempmap = [["" for i in range(15)] for j in range(15)]
        self.matrvalid = [[0 for i in range(15)] for j in range(15)]

    def check_temp(self):
        """Возвращает True, если временная матрица правильная"""
        # TODO andrsolo21
        return True

    def _prov(self, x, y, napr):
        """проверяет, наличие слова в этой ячейке (начало слова)"""
        flag = 0
        if napr == 2 and y != 14:
            if y != 0:
                if (self.map[y - 1][x] == '') and (self.map[y + 1][x] != ''):
                    flag = 1
            else:
                if self.map[y + 1][x] != '':
                    flag = 1
        if napr == 1 and x != 14:
            if x != 0:
                if self.map[y][x - 1] == '' and self.map[y][x + 1] != '':
                    flag = 1
            else:
                if self.map[y][x + 1] != '':
                    flag = 1
        if flag == 1:
            return self._schit(x, y, napr)
        else:
            return ['', 0, 0]

    def _schit(self, x, y, napr):
        """считывает слово"""
        s = ''
        newword = 0
        score = 0
        multisc = 1
        if napr == 2:
            a = 1
            while a != 0:
                koord = [x, y]
                if koord in self.newkoord:
                    newword = 1
                point = Point(x, y, self.map[y][x])
                score += point.score
                multisc *= point.value
                s = s + self.map[y][x]
                if y == 14:
                    a = 0
                else:
                    if self.map[y + 1][x] == '':
                        a = 0
                y = y + 1
        else:
            a = 1
            while a != 0:
                koord = [x, y]
                if koord in self.newkoord:
                    newword = 1
                point = Point(x, y, self.map[y][x])
                score += point.score
                multisc *= point.value
                s = s + self.map[y][x]
                if x == 14:
                    a = 0
                else:
                    if self.map[y][x + 1] == '':
                        a = 0
                x = x + 1
        return [s, newword, score * multisc]

    def pasteletters(self):
        """вставляет буквы в матрицу"""
        self.tempmap = [_.copy() for _ in self.Mainmap]
        for i in range(len(self.newkoord)):
            self.tempmap[self.newkoord[i][1]][self.newkoord[i][0]] = self.newletters[i]

    def serch(self):
        """ищет слова в матрице
        основная функция"""
        # движение по оси x = 1
        # движение по оси y = 2
        outx = []
        outy = []
        self.tempmap = [["" for i in range(15)] for j in range(15)]
        self.matrvalid = [[0 for i in range(15)] for j in range(15)]
        score = 0
        self._ChekKoord()
        self.pasteletters()
        undefined = []
        if self.ValidationKoord():
            self.map = [_.copy() for _ in self.tempmap]
            for i in range(len(self.map)):
                for j in range(len(self.map[i])):
                    if self.map[i][j] != '':

                        slx = self._prov(j, i, 1)

                        sly = self._prov(j, i, 2)

                        if slx[1] == 1:
                            # проверка слова на наличие в словаре
                            if slx[0] not in self.dict.dict:
                                undefined.append(slx[0])
                            else:
                                outx.append(slx[0])
                            try:
                                score += slx[2]
                            except Exception as e:
                                print(e)
                        if sly[1] == 1:
                            # проверка слова на наличие в словаре
                            if sly[0] not in self.dict.dict:
                                undefined.append(sly[0])
                            else:
                                outy.append(sly[0])
                            try:
                                score += sly[2]
                            except Exception as e:
                                print(e)
            # if not sys.argv[0].endswith("server_old.py"):
            #     print('поиск закончен')
            if len(undefined) == 0:
                # if not sys.argv[0].endswith("server_old.py"):
                #     print('ok')
                return MatrixResult(True, score, outx + outy)
            else:
                # if not sys.argv[0].endswith("server_old.py"):
                #     print('нопознанные слова')
                self.map = [_.copy() for _ in self.Mainmap]
                return MatrixResult(False, 1, undefined, 'нопознанные слова')

        else:
            # print('неправильное заполнение матрицы1')
            return MatrixResult(False, 2, outx + outy, 'неправильное заполнение матрицы')

    def get(self, y, x):
        """Возвращает точку по адресу"""
        return self.map[y][x]

    def _ChekKoord(self):
        a = []
        b = []
        for i in range(len(self.newkoord)):
            if self.newkoord[i][1] != None and self.newkoord[i][0] != None:
                a.append(self.newkoord[i])
                b.append(self.newletters[i])
        self.newkoord = a
        self.newletters = b

    def _ValidationCheck(self, koord):
        # poisk sverhy
        if self.matrvalid[koord[0]][koord[1]] == 0:
            self.count += 1
            self.matrvalid[koord[0]][koord[1]] += 1
            if koord[0] != 0:
                if self.tempmap[koord[0] - 1][koord[1]] != "":
                    self._ValidationCheck([koord[0] - 1, koord[1]])
            # poisk sleva
            if koord[1] != 0:
                if self.tempmap[koord[0]][koord[1] - 1] != "":
                    self._ValidationCheck([koord[0], koord[1] - 1])
            # poisk vnizy
            if koord[0] != 14:
                if self.tempmap[koord[0] + 1][koord[1]] != "":
                    self._ValidationCheck([koord[0] + 1, koord[1]])
            # poisk sprava
            if koord[1] != 14:
                if self.tempmap[koord[0]][koord[1] + 1] != "":
                    self._ValidationCheck([koord[0], koord[1] + 1])

    def ValidationKoord(self):
        self.count = 0
        if self.tempmap[self.FirstFish[0]][self.FirstFish[1]] != '':
            self._ValidationCheck(self.FirstFish)
            # if not sys.argv[0].endswith("server_old.py"):
            #     print('нашел ' + str(self.count) + ' букв')
            for i in range(15):
                for j in range(15):
                    if self.tempmap[i][j] != '':
                        self.count -= 1
            # if not sys.argv[0].endswith("server_old.py"):
            #     print('проверил, осталось: ' + str(self.count) + ' букв')
            if self.count == 0:
                return True
            else:
                return False
        else:
            return False

    def SaveChangesMatr(self):
        self.Mainmap = [_.copy() for _ in self.map]
        self.reject_temp()

    def __init__(self):
        """Создает новую игровую карту"""
        self.Mainmap = [["" for i in range(15)] for j in range(15)]
        self.map = [["" for i in range(15)] for j in range(15)]
        self.tempmap = [["" for i in range(15)] for j in range(15)]
        self.newkoord = []
        self.newletters = []
        self.matrvalid = [[0 for i in range(15)] for j in range(15)]
        self.dict = GameDictionary()
        self.FirstFish = [7, 7]


class GameDictionary:
    """Словарь слов игры"""
    filename = "dictionary"
    """Имя файла словаря"""
    filetemp = "dictionarytemp"
    """Имя файла пользовательского словаря"""

    def append(self, item: str) -> None:
        """
        Добавляет новое слово в словарь

        :param item: Слово
        :type item: str
        """
        self.dict.append(item)
        with open(self.filetemp, "a", encoding="utf-8") as f:
            f.write(item + "\n")

    def prepare(self, alphabet: str) -> List[str]:
        """Подготавливает словарь для дальнейшей обработки

        :param alphabet: Список доступных букв
        :type alphabet: str

        :return: Список слов
        :rtype: List[str]
        """
        alphabet = alphabet.upper()
        if '*' in alphabet:
            star = alphabet.count("*")
        else:
            star = 0
        if len(alphabet) >= 32:
            return self.dict

        temp_dict = []
        for i in self.dict:
            loc_star = star
            for j in i:
                if alphabet.count(j) == 0:
                    if loc_star == 0:
                        break
                    else:
                        loc_star -= 1
            else:
                temp_dict.append(i)
        return temp_dict

    def __init__(self, test_mode: bool = False) -> None:
        """Инициализирует словарь начальным списком слов

        :param test_mode: Указывает на процесс тестирования словаря
        :type test_mode: bool
        """
        if not os.path.exists(self.filetemp):
            with open(self.filetemp, 'w'): pass
        with open(self.filename, "r", encoding="utf-8") as f:
            self.dict = f.read().upper().split("\n")
        if not test_mode:
            with open(self.filetemp, "r", encoding="utf-8") as f:
                temp = f.read().upper()
                if temp != "":
                    self.dict += temp.split("\n")


a = GameDictionary()
a.append("Asd")
