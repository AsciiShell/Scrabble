import time
from threading import Thread

from scrabblelib import *


class Player:
    """Абстрактный класс игрока"""
    lastID = 0

    def __init__(self, name, t, rid=None, dif=None, ip=None):
        """Создает нового игрока с указанным именем"""
        self.name = name
        self.type = t
        self.id = Player.lastID
        Player.lastID += 1
        self.rid = rid
        self.dif = dif
        self.ip = ip


class TurnStruct:
    def __init__(self, add_letters, letters=None, pass_letters=None):
        if add_letters:
            self.isChanged = True
            if letters is None:
                warnings.warn("Letters is None")
            self.letters = letters
            self.pass_letters = []
        else:
            self.isChanged = False
            if pass_letters is None:
                warnings.warn("Pass letters is None")
            self.pass_letters = pass_letters
            self.letters = []


class GamePlayer(Player):
    def __init__(self, name, game, rid=None, dif=None, ip=None):
        self.score = 0
        self.game = game
        self.letters = []
        self.isTurn = False
        self.timeout = 0
        self.input = None
        self.result = None
        super().__init__(name, None, rid, dif, ip)

    def turn_end(self):
        """Срабатывает при завершении хода любого игрока. Перерисовка"""
        pass

    def my_turn(self):
        """Предупреждает игрока о начале его хода. Активирует игровой интерфейс"""
        pass

    def action(self):
        """Посылает игроку команду на начало действий и ожидает прекращения"""
        self.isTurn = True
        self.timeout = GameConfig.turnTime
        self.result = None
        self.my_turn()
        while self.isTurn:
            time.sleep(1)
            self.timeout -= 1
            if self.timeout <= 0:
                self.isTurn = False
        # TODO ошибка состояния гонки
        self.isTurn = False
        if self.result is None:
            return TurnStruct(False, [], [])
        else:
            return self.result

    def check_turn(self, turn):
        """Проверяет правильность ввода новых букв"""
        self.game.matrix.reject_temp()
        for _ in turn:
            self.game.matrix.newkoord.append([_.y, _.x])
            self.game.matrix.newletters.append(_.letter)
        return self.game.matrix.serch()

    def accept_turn(self, turn):
        """Проверяет правильность ввода новых букв и завершает ход"""
        if turn.isChanged:
            res = self.check_turn(turn.letters)
            if res.result:
                for i in turn.letters:
                    self.game.matrix.Mainmap[i.x][i.y] = i.letter
                    self.letters.remove(i.letter)
                self.score += res.score
                self.result = turn
                # Останавливает ход
                self.isTurn = False
                return Message(True, str(res.score))
            else:
                return Message(False, res.msg)
        else:
            for i in turn.pass_letters:
                self.letters.remove(i)
            self.result = turn
            self.isTurn = False

            return Message(True, "Пропуск")


class PlayerLocal(GamePlayer):
    def my_turn(self):
        # TODO andrsolo21 перерисовываем интерфес
        # мб эту функцию переопределить в Form.py?
        pass

    def turn_end(self):
        # TODO andrsolo21 перерисовываем интерфес
        # мб эту функцию переопределить в Form.py?
        pass


class PlayerBot(GamePlayer):
    class PosStruct:
        def __init__(self, arr, score):
            self.letters = arr
            self.score = score

    def __init__(self, name, game):
        self.botEnable = True
        self.thread = Thread(target=self._daemon)
        super().__init__(name, game)
        self.thread.start()

    def __del__(self):
        self.botEnable = False
        self.thread.join(1)

    @staticmethod
    def _is_replaceable(a, b):
        return b == '' or a == b

    def _available(self, word, ind):
        res = []
        for i in range(len(self.game.matrix.Mainmap)):
            for j in range(len(self.game.matrix.Mainmap[0])):
                if self.game.matrix.Mainmap[i][j] == word[ind]:
                    # Проверка по горизонтали
                    let = self.letters.copy()
                    turn = []
                    if (j - ind - 1 < 0 or self.game.matrix.Mainmap[i][j - ind - 1] == '') and \
                            (j - ind + len(word) >= len(self.game.matrix.Mainmap[0]) or self.game.matrix.Mainmap[i][
                                j - ind + len(word)] == ''):
                        for x in range(len(word)):
                            if not 0 <= j - ind + x < len(self.game.matrix.Mainmap):
                                break
                            if self.game.matrix.Mainmap[i][j - ind + x] != word[x]:
                                if self.game.matrix.Mainmap[i][j - ind + x] != '':
                                    break
                                elif word[x] in let:
                                    turn.append(Point(i, j - ind + x, word[x]))
                                    let.remove(word[x])
                                else:
                                    break
                        else:
                            # TODO asciishell переделать под новый алгоритм
                            check = self.check_turn(turn)
                            if check.result:
                                res.append(self.PosStruct(turn, check.score))
                    # Проверка по вертикали
                    let = self.letters.copy()
                    if (i - ind - 1 < 0 or self.game.matrix.Mainmap[i - ind - 1][j] == '') and \
                            (i - ind + len(word) >= len(self.game.matrix.Mainmap) or
                             self.game.matrix.Mainmap[i - ind + len(word)][j] == ''):
                        for x in range(len(word)):
                            if not 0 <= i - ind + x < len(self.game.matrix.Mainmap):
                                break
                            if self.game.matrix.Mainmap[i - ind + x][j] != word[x]:
                                if self.game.matrix.Mainmap[i - ind + x][j] != '':
                                    break
                                elif word[x] in let:
                                    turn.append(Point(i - ind + x, j, word[x]))
                                    let.remove(word[x])
                                else:
                                    break
                        else:
                            # TODO asciishell переделать под новый алгоритм
                            check = self.check_turn(turn)
                            if check.result:
                                res.append(self.PosStruct(turn, check.score))
        return res

    def cpu(self):
        """Вычисляет информацию для хода"""
        letters = ""
        for i in self.game.matrix.Mainmap:
            for j in i:
                if letters.count(j) == 0:
                    letters += j
        for i in self.letters:
            if letters.count(i) == 0:
                letters += i
        words = self.game.dict.prepare(letters)
        res = []
        for word in words:
            for char in range(len(word)):
                temp = self._available(word, char)
                if temp:
                    res += temp
                    break  # SOME optimize

        if res:
            max_score = 0
            for i in range(len(res)):
                if res[i].score > res[max_score].score:
                    max_score = i
            print(res[max_score].score)
            for x in range(len(self.game.matrix.Mainmap)):
                for y in range(len(self.game.matrix.Mainmap[0])):
                    for let in res[max_score].letters:
                        if let.x == x and let.y == y:
                            print(let.letter, end='\t')
                            break
                    else:
                        print(self.game.matrix.Mainmap[x][y], end='\t')
                print()
            print('\n---------\n')
            self.accept_turn(TurnStruct(True, res[max_score].letters))
        else:
            # Reject all letters
            self.accept_turn(TurnStruct(False, pass_letters=self.letters))

    def _daemon(self):
        """Демон бота"""
        while self.botEnable:
            if self.isTurn:
                self.cpu()
            time.sleep(1)


class GameServerPrepare:
    """Основной класс игры"""

    def create_game_async(self):
        """Асинхронный метод для ожидания информации"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(("", 8383))
        server_id = rand(8)
        while self.gamePrepare:
            data, address = sock.recvfrom(1024)
            data = convert_type(data)
            if data["action"] == "getStatus":
                send_broadcast({"game": [value.__dict__ for key, value in self.players.items()], "queue": self.queue,
                                "id": server_id})
            elif data["action"] == "connectGame":
                for i in self.queue:
                    if i['rid'] == data['rid']:
                        break
                else:
                    self.queue.append({"ip": address, "name": data["name"], "rid": data["rid"], "add": False})
            elif data["action"] == 'continue':
                pass
            else:
                warnings.warn("Неизвестное действие " + data["action"])
            print(data)
        sock.close()

    def create_game(self, player_name):
        """Создает игру с указанными параметрами"""
        self.gamePrepare = True
        self.players = {}
        self.queue = []
        me = Player(player_name, "local")
        self.players[me.id] = me
        self.gamePrepareThread = Thread(target=self.create_game_async)
        self.gamePrepareThread.start()

    def get_status(self):
        if self.gamePrepare:
            return {"game": self.players, "queue": self.queue}
        else:
            return False

    def add_player(self, t, rid=None):
        if not self.gamePrepare:
            return Message(False, 'Игра не находится в процессе подготовки')
        if len(self.players) >= 4:
            return Message(False, 'Достаточно игроков')
        if t == 'bot':
            p = Player('BOT_' + str(random.randint(1000, 9999)), 'bot')
            self.players[p.id] = p
        elif t == 'net':
            for i in self.queue:
                if i['rid'] == rid:
                    for key, value in self.players.items():
                        if rid == value.rid:
                            return Message(False, "Игрок {} не найден ".format(str(rid)))
                    p = Player(i['name'], 'net', rid, ip=i['ip'])
                    self.players[p.id] = p
                    i["add"] = True
                    break
            else:
                return Message(False, "Игрок {} не найден ".format(str(rid)))
        else:
            return Message(False, 'Неизвестный тип ' + t)
        return Message(True)

    def delete_player(self, rid):
        if self.gamePrepare:
            return Message(False, 'Игра не находится в процессе подготовки')
        for i in self.players:
            if i.rid == rid:
                del self.players[i]
                break
        else:
            for i in self.queue:
                if i['rid'] == rid:
                    self.queue.remove(i)
                    break
            else:
                return Message(False, "Игрок {} не найден ".format(str(rid)))
        return Message(True)

    def start_game(self):
        self.gamePrepare = False
        send_broadcast({'action': 'continue'}, 8383)
        self.gamePrepareThread.join(1)

    def __init__(self):
        self.players = {}
        self.queue = []
        self.gamePrepare = False
        self.gamePrepareThread = Thread()
        self.dict = GameDictionary()


class GameServer:
    def __init__(self, players):
        self.players = []
        for player in players:
            if player.type == "local":
                self.players.append(PlayerLocal(player.name, self))
            elif player.type == "bot":
                self.players.append(PlayerBot(player.name, self))
            else:
                warnings.warn("Тип не найден" + player.type)
        self.playStatus = True
        self.alphabet = ""
        self.matrix = Matrix()
        self.dict = GameDictionary()
        for key, value in GameConfig.letters.items():
            self.alphabet += key * value["count"]
        self.thread = Thread(target=self._game_loop)
        self.thread.start()

    def _give_letter(self, player):
        """Выдает игроку недостающие фишки"""
        while len(player.letters) < GameConfig.startCount and len(self.alphabet) > 0:
            i = self.alphabet[random.randrange(len(self.alphabet))]
            player.letters.append(i)
            self.alphabet = self.alphabet.replace(i, "", 1)

    def _game_loop(self):
        while self.playStatus:
            for player in self.players:
                self._give_letter(player)
                result = player.action()
                print("Игрок {} закончил ход {}. Набрал {} очков".format(player.name,
                                                                         "Активно" if result.isChanged else "Пассивно",
                                                                         player.score))
                print("Осталось в руке {} букв. В мешке - {} букв".format(str(len(player.letters)),
                                                                          str(len(self.alphabet))))
                if result:
                    # TODO Какая то обработка резульатата и измененние значений
                    pass
                for i in self.players:
                    i.turn_end()


# send_broadcast({'action': 'connectGame', 'rid': 'qwмty', 'name': 'BOSS'}, 8383)


if __name__ == '__main__':
    game_server = GameServer([Player("BOT", "bot")])
    game_server.matrix.Mainmap[7][7] = "П"
    game_server.matrix.Mainmap[7][8] = "Р"
    game_server.matrix.Mainmap[7][9] = "И"
    game_server.matrix.Mainmap[7][10] = "В"
    game_server.matrix.Mainmap[7][11] = "Е"
    # game_server.players[0].letters = ["Т"]
