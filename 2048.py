#! /usr/bin/python3
# coding=utf8

import curses
from random import randrange, choice
from collections import defaultdict

# 用户所能执行的 六 种操作
actions = ['Up', 'Left', 'Down', 'Right', 'Restart', 'Exit']

# 用户常见的输入，不区分大小写
letter_codes = [ord(ch) for ch in 'WASDRQwasdrq']  # ord 函数以字符作为参数，返回其对应的 ascii 或 unicode 值

# 将用户输入与行为相关联
action_dict = dict(zip(letter_codes, actions * 2))  # zip 函数将前后两个可迭代对象依次配对，若数量不一致，则抛出一场

'''
    处理游戏的主逻辑我们使用有限状态机
    2048游戏很容易拆成几个状态的转换
    
    status 存储当前的状态， status_actions 字典变量作为状态转换的规则， key 为状态， value 为返回下一个状态的函数
    
    以下是状态转换图
    Init: init()
        Game
    Game: game()
        Game
        Win
        GameOver
        Exit
    Win: lambda: not_game('Win')
        Init
        Exit
    GameOver: lambda: not_game('GameOver')
        Init
        Exit
    Exit: 退出循环
    
    状态机会不断循环，知道触发退出操作达到 Exit 状态为止
'''


# 用户输入处理， 阻塞 + 循环 ，直到获取有效输入才返回对应行为
def get_user_action(keyboard):
    char = 'N'
    while char not in action_dict:
        char = keyboard.getch()
    a = action_dict[char]
    return action_dict[char]


# 矩阵转置和矩阵逆转能减少重复代码
# 只需实现一个方向的操作使用转置和逆转能够实现其他方向的操作
def transpose(field):
    # 使用 拆包， zip 和 列表生成式实现一行矩阵转置
    return [list(row) for row in zip(*field)]


def invert(field):
    # 使用列表生成式 一行实现矩阵逆转，左右反转，步长值为 -1 反转列表
    return [row[::-1] for row in field]


class GameField(object):
    def __init__(self, height=4, width=4, win=2048):
        self.height = height  # 高
        self.width = width  # 宽
        self.win_value = win  # 过关分数
        self.score = 0  # 当前分数
        self.highScore = 0  # 历史最高分
        self.reset()  # 重置棋盘

    # 在场地为 0 的地方随机生成一个 2 或 4
    def spawn(self):
        new_element = 4 if randrange(100) > 89 else 2
        # choice 从可迭代对象中随机返回一个元素
        (i, j) = choice([(i, j) for i in range(self.width) for j in range(self.height) if self.field[i][j] == 0])
        self.field[i][j] = new_element

    def reset(self):
        if self.score > self.highScore:
            self.highScore = self.score
        self.score = 0
        # 重置矩阵
        self.field = [[0 for i in range(self.width)] for j in range(self.height)]
        self.spawn()
        self.spawn()

    def move(self, direction):

        def move_row_left(row):
            # 将非 0 元素挤到一起
            def tighten(row):
                new_row = [i for i in row if i != 0]
                new_row += [0 for i in range(len(row) - len(new_row))]
                return new_row

            def merge(row):
                pair = False
                new_row = []
                for i in range(len(row)):
                    if pair:
                        new_row.append(row[i] * 2)
                        self.score += row[i] * 2
                        pair = False
                    else:
                        if i + 1 < len(row) and row[i] == row[i + 1]:
                            pair = True  # 找到一对可以相加的，记下标记
                            new_row.append(0)  # 因为两个元素合并会留下一个空位
                        else:
                            new_row.append(row[i])
                assert len(new_row) == len(row)
                return new_row

            # 先挤到一起再合并再挤到一起
            return tighten(merge(tighten(row)))

        moves = {}
        moves['Left'] = lambda field: [move_row_left(row) for row in field]
        # 因为move_row_left向左合并，所以反转field后需要将结果再次反转
        moves['Right'] = lambda field: invert(moves['Left'](invert(field)))
        moves['Up'] = lambda field: transpose(moves['Left'](transpose(field)))
        moves['Down'] = lambda field: transpose(moves['Right'](transpose(field)))

        if direction in moves:
            if self.move_is_possible(direction):
                self.field = moves[direction](self.field)
                self.spawn()
                return True
        else:
            return False

    def move_is_possible(self, direction):
        def move_left_movable(row):
            def change(i):
                if row[i] == 0 and row[i + 1] != 0:  # 可以移动
                    return True
                if row[i] != 0 and row[i] == row[i + 1]:  # 可以合并
                    return True
                return False

            return any(change(i) for i in range(len(row) - 1))

        check = {}
        check['Left'] = lambda field: any(move_left_movable(row) for row in field)
        check['Right'] = lambda field: check['Left'](invert(field))
        check['Up'] = lambda field: check['Left'](transpose(field))
        check['Down'] = lambda field: check['Right'](transpose(field))

        if direction in check:
            return check[direction](self.field)
        else:
            return False

    def is_win(self):
        # any 函数检查可迭代对象是否全空或全假，当全假或全空时返回False，其他情况返回True
        return any(any(i >= self.win_value for i in row) for row in self.field)

    def is_gameover(self):
        return not any(self.move_is_possible(move) for move in actions)

    def draw(self, screen):
        help_string1 = '(W)Up, (S)Down, (A)Left, (D)Right'
        help_string2 = '        (R)Reset (Q)Exit'
        gameover_string = '         Game Over'
        win_string = '              You Win'

        def cast(string):
            screen.addstr(string + '\n')

        # 水平分割线
        def draw_hor_separator():
            line = '+' + ('+-------' * self.width + '+')[1:]
            separator = defaultdict(lambda: line)
            if not hasattr(draw_hor_separator, 'counter'):
                draw_hor_separator.counter = 0
            cast(separator[draw_hor_separator.counter])
            draw_hor_separator.counter += 1

        def draw_row(row):
            cast(''.join('|{: 5} '.format(num) if num > 0 else '|    ' for num in row) + '|')

        screen.clear()
        cast('SCORE: ' + str(self.score))

        if self.highScore != 0:
            cast('HIGHSCORE: ' + str(self.highScore))
        for row in self.field:
            draw_hor_separator()
            draw_row(row)

        draw_hor_separator()

        if self.is_win():
            cast(win_string)
        else:
            if self.is_gameover():
                cast(gameover_string)
            else:
                cast(help_string1)

        cast(help_string2)


def main(stdscr):
    def init():
        # 重置棋盘
        game_field.reset()
        return 'Game'

    def not_game(state):
        # 不在游戏中的状态，GameOver 或 Win
        game_field.draw(stdscr)
        # 读取用户输入到 action ，判断重启还是结束游戏
        action = get_user_action(stdscr)
        # defaultdict 参数表示属性的初始值，这里 lambda : state 表示 F() = state ，表示属性值为当前状态
        responses = defaultdict(lambda: state)  # 默认是当前状态，没有行为就会一直循环
        # 表示重置和退出的状态机
        responses['Restart'], responses['Exit'] = 'Init', 'Exit'
        return responses[action]

    def game():
        # 画出当前棋盘的状态
        game_field.draw(stdscr)
        # 读取输入到action
        action = get_user_action(stdscr)

        if action == 'Init':
            return 'Init'
        if action == 'Exit':
            return 'Exit'
        if game_field.move(action):
            if game_field.is_win():
                return 'Win'
            if game_field.is_gameover():
                return 'Gameover'
        # 当没有输入的时候要保持在 Game 状态，无此语句则返回 None
        return 'Game'

    state_actions = {
        'Init': init,
        'Win': lambda: not_game('Win'),
        'Gameover': lambda: not_game('Gameover'),
        'Game': game
    }

    curses.use_default_colors()
    game_field = GameField(win=32)

    state = 'Init'

    while state != 'Exit':
        state = state_actions[state]()


curses.wrapper(main)
