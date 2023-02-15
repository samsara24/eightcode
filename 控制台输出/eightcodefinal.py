import os
import time
import numpy as np
import copy
import math
import psutil


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


class NumberCode:
    global width

    def __init__(self, initial, target, typeScout):
        # 一维变二维
        self.initial = Node(np.reshape(initial, (width, width)), 0, "None", 0)
        self.target = Node(np.reshape(target, (width, width)), 0, "None", 0)

        # 初始化open和closed
        self.open = [self.initial]
        self.closed_ = []

        # 初始化估价函数类型和初始节点的估价数值
        self.scout = typeScout
        self.inspiration_score(self.initial, self.target)



    # 估价函数
    def inspiration_score(self, node, target):
        a = node.level # g(x)
        b = 0 # h(x)
        if self.scout == 1:
            # 所需移动距离
            for i in range(width ** 2):
                position = np.where(node.data == i)
                x = position[0]
                y = position[1]
                position1 = np.where(target.data == i)
                x1 = position1[0]
                y1 = position1[1]
                b = b + abs(x-x1) + abs(y-y1)
            node.score = a + b
            return node
        elif self.scout == 2:
            # 位置不同
            b = np.count_nonzero(node.data-target.data)
            node.score = a+b
            return node
        elif self.scout == 3:
            # 位置不同 + 3倍逆序数
            b = np.count_nonzero(node.data-target.data)
            flatter = node.data.reshape(1, width ** 2)
            node.score = a + b + 3 * get_reverse(flatter)
            return node
        elif self.scout == 4:
            # 宽度优先
            node.score = a
            return node
        elif self.scout == 5:
            # 深度优先
            b = np.count_nonzero(node.data-target.data)
            node.score = a + 100 * b
            return node

    # 展示数据函数
    def show_data(self, ans):
        for i in ans.data:
            print(i)

    def view_array(self, ans):
        newArray = np.reshape(ans.data, (1, width ** 2))[0]
        return newArray
    
    # 模拟移动

    def move(self, n, position, row, col):
        if position == "up":
            n[row, col], n[row-1, col] = n[row-1, col], n[row, col]
        elif position == "down":
            n[row, col], n[row+1, col] = n[row+1, col], n[row, col]
        elif position == "left":
            n[row, col], n[row, col-1] = n[row, col-1], n[row, col]
        elif position == "right":
            n[row, col], n[row, col+1] = n[row, col+1], n[row, col]
        return n

    def exist_both(self, move_result, closed, open):
        for i in range(len(closed)):
            if (move_result == closed[i].data).all():
                return True
        for i in range(len(open)):
            if (move_result == open[i].data).all():
                return True
        return False

    def exist_open(self, move_result, open):
        if len(open) == 0:
            return False
        for i in range(len(open)):
            if (move_result == open[i].data).all():
                return open[i]
        return False

    def exist_closed(self, move_result, closed):
        if len(closed) == 0:
            return False
        for i in range(len(closed)):
            if (move_result == closed[i].data).all():
                return closed[i]
        return False

    def sort_by_score(self, arr):
        n = len(arr)
        for i in range(n):
            for j in range(0, n-i-1):
                if arr[j].score > arr[j+1].score:
                    arr[j], arr[j+1] = arr[j+1], arr[j]
        return arr

    def find_path(self):
        # 遍历次数
        flag = 0
        while self.open:
            flag = flag + 1
            direction = ['up', 'down', 'right', 'left']
            # 从open表中删除第一个状态并放入closed表中
            first_state = self.open.pop(0)
            self.closed_.append(first_state)
            # 如果n为目标状态则返回求解路径
            if (first_state.data == self.target.data).all():
                # 匹配成功
                resultList = []
                resultList.append(first_state)
                print("搜索完成，搜索路径如下：")
                while first_state.parent != "None":
                    resultList.append(first_state.parent)
                    first_state = first_state.parent
                for j in range(len(resultList)):
                    print(str(j)+"——>")
                    result = resultList.pop(-1)
                    self.show_data(result)
                print(
                    "----------------------------------结束搜索-----------------------------------")
                return True

            position = np.where(first_state.data == 0)
            i = position[0]
            j = position[1]
            length_down = first_state.data.shape[0]
            length_right = first_state.data.shape[1]

            # 操作算子更新
            if i == 0:
                direction.remove("up")
            if i == length_down-1:
                direction.remove("down")
            if j == 0:
                direction.remove("left")
            if j == length_right-1:
                direction.remove("right")

            # 没有子状态
            if len(direction) == 0:
                continue

            # 遍历子状态
            for p in range(len(direction)):
                first_copy = copy.deepcopy(first_state)
                move_result = self.move(first_copy.data, direction[p], i, j)
                # 判断是否存在于open\closed表
                if self.exist_both(move_result, self.closed_, self.open):
                    # 比较self.score和原有的score
                    if self.exist_open(move_result, self.open) != False:
                        old = self.exist_open(
                            move_result, self.open)  # 原有的
                        score_t = self.inspiration_score(
                            Node(move_result, first_state.level+1, first_state, 0), self.target)
                        if score_t.score < old.score:
                            old.score = score_t.score
                            old.parent = score_t.parent
                    if self.exist_closed(move_result, self.closed_) != False:
                        old = self.exist_closed(move_result, self.closed_)
                        score_t = self.inspiration_score(
                            Node(move_result, first_state.level+1, first_state, 0), self.target)
                        if score_t.score < old.score:
                            # closed->open
                            self.closed_.remove(old)
                            self.open.append(old)
                            old.score = score_t.score
                            old.parent = score_t.parent
                else:
                    # 评估节点
                    score_t = self.inspiration_score(
                        Node(move_result, first_state.level+1, first_state, 0), self.target)
                    # 加入open表
                    self.open.append(score_t)
            # open表排序
            self.open = self.sort_by_score(self.open)

            print("第"+str(flag)+"次移动后的结果为：", first_state.data, sep='\n')
            print("当前所在搜索树的层数为", first_state.level)
            print("此时估价函数值为", first_state.score)


# 初始化状态
a = [1, 2, 8, 0, 6, 3, 7, 5, 4]
b = [1, 2, 3, 8, 0, 4, 7, 6, 5]
c = [5, 1, 2, 4, 9, 6, 3, 8, 13, 15, 10, 11, 14, 0, 7, 12]
d = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0]
typeMode = eval(input("请选择八数码或十五数码"))
if (typeMode == 8):
    width = int(math.sqrt(len(a)))
    typeScout = eval(input("请选择估价函数"))
    ans = NumberCode(a, b, typeScout=typeScout)
    judge = is_reverse(a, b)
else:
    width = int(math.sqrt(len(c)))
    typeScout = eval(input("请选择估价函数"))
    ans = NumberCode(c, d, typeScout=typeScout)
    judge = is_reverse(c, d)
if (not judge):
    if width == 3:
        print("不存在八数码解")
    else:
        print("不存在十五数码解")
else:
    start = time.perf_counter()
    ans.find_path()
    end = time.perf_counter()
    print(u'当前进程的内存使用：%.4f MB' %
          (psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024))
    print('运行时间 : %.4f 秒' % (end-start))
