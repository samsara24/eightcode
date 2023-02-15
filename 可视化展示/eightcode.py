import numpy as np
import copy
import math


def get_reverse(pre):
    inverse = 0
    global width
    for i in range(1, width ** 2):
        for j in range(i):
            try:
                if pre[i] != 0 and pre[j] != 0 and pre[i] > pre[j]:
                    inverse = inverse + 1
            except:
                pass
    return inverse


def is_reverse(pre, final):
    global width
    if width % 2 == 1:
        preCode = get_reverse(pre)
        finalCode = get_reverse(final)
        return preCode % 2 == finalCode % 2
    else:
        preCode = get_reverse(pre)
        pre_zero_index = pre.index(0) + 1
        pre_row = math.ceil(pre_zero_index / width)
        finalCode = get_reverse(final)
        final_zero_index = final.index(0)
        final_row = math.ceil(final_zero_index / width)
        if abs(pre_row-final_row) % 2 == 0:
            return preCode % 2 == finalCode % 2
        else:
            return preCode % 2 != finalCode % 2


width = 3


class Node:
    def __init__(self, data, level, parent, score):
        self.data = data
        self.level = level
        self.parent = parent
        self.score = score


class EightCode:
    global width

    def __init__(self, initial, goals, typeScout):
        # 一维变二维
        self.initial = Node(np.reshape(initial, (width, width)), 0, "None", 0)
        self.goals = Node(np.reshape(goals, (width, width)), 0, "None", 0)

        # 初始化初始节点估价数值
        self.scout = typeScout
        self.__inspiration_score(self.initial, self.goals)

        # 初始化open和close
        self.open_ = [self.initial]
        self.close_ = []
        self.lists = []

    # 估价函数
    def __inspiration_score(self, node, goals):
        # d(n)
        a = node.level
        # w(n)
        b = 0
        if (self.scout == 1):
            # 所需移动距离
            for i in range(width ** 2):
                position = np.where(node.data == i)
                x = position[0]
                y = position[1]
                position1 = np.where(goals.data == i)
                x1 = position1[0]
                y1 = position1[1]
                b = b + abs(x-x1) + abs(y-y1)
            node.score = a + b
            return node
        elif (self.scout == 2):
            # 位置不同
            b = np.count_nonzero(node.data-goals.data)
            node.score = a+b
            return node
        elif (self.scout == 3):
            for i in range(width ** 2):
                position = np.where(node.data == i)
                x = position[0]
                y = position[1]
                position1 = np.where(goals.data == i)
                x1 = position1[0]
                y1 = position1[1]
                b = b + abs(x-x1) + abs(y-y1)
            flatter = node.data.reshape(1, width ** 2)
            node.score = a + b + 3 * get_reverse(flatter)
            return node
        elif (self.scout == 4):
            # 宽度优先
            node.score = a
            return node
        elif (self.scout == 5):
            # 深度优先
            b = np.count_nonzero(node.data-goals.data)
            node.score = b
            return node

    # 展示数据函数
    def __show_data(self, a):
        self.lists.append(np.reshape(a.data, (1, width ** 2))[0])
        for i in a.data:
            print(i)

    def view_array(self, a):
        newArray = np.reshape(a.data, (1, width ** 2))[0]
        return newArray
    # 移动函数

    def __move(self, n, position, row, col):
        if position == "left":
            n[row, col], n[row, col-1] = n[row, col-1], n[row, col]
        elif position == "right":
            n[row, col], n[row, col+1] = n[row, col+1], n[row, col]
        elif position == "up":
            n[row, col], n[row-1, col] = n[row-1, col], n[row, col]
        elif position == "down":
            n[row, col], n[row+1, col] = n[row+1, col], n[row, col]
        return n

    def __exist_both(self, move_result, close, open_):
        for i in range(len(close)):
            if (move_result == close[i].data).all():
                return True
        for i in range(len(open_)):
            if (move_result == open_[i].data).all():
                return True
        return False

    def __exists_open(self, move_result, open_):
        if len(open_) == 0:
            return False
        for i in range(len(open_)):
            if (move_result == open_[i].data).all():
                return open_[i]
        return False

    def __exists_close(self, move_result, close):
        if len(close) == 0:
            return False
        for i in range(len(close)):
            if (move_result == close[i].data).all():
                return close[i]
        return False

    def __sort_by_score(self, arr):
        n = len(arr)
        for i in range(n):
            for j in range(0, n-i-1):
                if arr[j].score > arr[j+1].score:
                    arr[j], arr[j+1] = arr[j+1], arr[j]
        return arr

    def find_path(self):
        # 遍历次数
        flag = 0
        while self.open_:
            flag = flag + 1
            direction = ['up', 'down', 'right', 'left']
            # 从open表中删除第一个状态并放入close表中
            first_state = self.open_.pop(0)
            self.close_.append(first_state)
            # 如果n为目标状态则返回求解路径

            if (first_state.data == self.goals.data).all():
                # 匹配成功
                resultList = []
                resultList.append(first_state)
                while first_state.parent != "None":
                    resultList.append(first_state.parent)
                    first_state = first_state.parent
                for j in range(len(resultList)):
                    print(str(j)+"——>")
                    result = resultList.pop(-1)
                    self.__show_data(result)
                return True

            position = np.where(first_state.data == 0)

            i = position[0]
            j = position[1]
            length_down = first_state.data.shape[0]
            length_right = first_state.data.shape[1]

            # 操作算子更新
            if i == 0:
                direction.remove("up")
            if j == 0:
                direction.remove("left")
            if i == length_down-1:
                direction.remove("down")
            if j == length_right-1:
                direction.remove("right")

            # 找到子状态
            for p in range(len(direction)):
                first_copy = copy.deepcopy(first_state)
                move_result = self.__move(first_copy.data, direction[p], i, j)
                # 判断是否存在于open\close表
                if (self.__exist_both(move_result, self.close_, self.open_)):
                    # 比较self.score和原有的score
                    if (self.__exists_open(move_result, self.open_) != False):
                        old = self.__exists_open(
                            move_result, self.open_)  # 原有的
                        score_t = self.__inspiration_score(
                            Node(move_result, first_state.level+1, first_state, 0), self.goals)
                        if (score_t.score < old.score):
                            old.score = score_t.score
                            old.parent = score_t.parent
                    if (self.__exists_close(move_result, self.close_) != False):
                        old = self.__exists_close(move_result, self.close_)
                        score_t = self.__inspiration_score(
                            Node(move_result, first_state.level+1, first_state, 0), self.goals)
                        if (score_t.score < old.score):
                            self.close_.remove(old)
                            self.open_.append(old)
                            old.score = score_t.score
                            old.parent = score_t.parent
                else:
                    # 评估节点
                    score_t = self.__inspiration_score(
                        Node(move_result, first_state.level+1, first_state, 0), self.goals)

                    self.open_.append(score_t)
            # open表排序
            self.open_ = self.__sort_by_score(self.open_)
