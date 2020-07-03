from random import randrange
import time
from datetime import datetime


class TreapNode:
    def __init__(self, key, priority=1000000, left=None, right=None):
        self.key = key
        # self.priority = randrange(priority)
        self.priority = priority
        self.left = left
        self.right = right
        self.right_size = 0
        self.left_size = 0


def rorate_left(root):
    # rootと右子ノードを回転し
    # rootを子ノードの左子ノードにつける
    # rootの左子ノードはそのまま移動後のrootの左子ノードになる
    R = root.right
    X = root.right.left

    # 回転
    R.left = root
    root.right = X

    R.left.right_size = R.left_size
    R.left_size += root.left_size + 1
    return R


def rorate_right(root):
    # rootと左子ノードを回転し
    # rootを子ノードの左子ノードにつける
    L = root.left
    Y = root.left.right

    # 回転
    L.right = root
    root.left = Y

    L.right.left_size = L.right_size
    L.right_size += root.right_size + 1
    return L


def insert_node(root, key, priority):
    """再帰的に挿入できるポイントを調べ
    回転により木構造の変更を行う
    挿入が適切場所 (以下条件を満たす場所)
    - treap nodeのkeyが2分木になっていないだめ
    - 親ノードの優先度はいつも子ノードより大きい
    """

    # 空の木である場合
    if root is None:
        return TreapNode(key, priority)

    if key < root.key:
        root.left_size += 1
        root.left = insert_node(root.left, key, priority)

        # 2分ヒープ条件を満たない場合回転が発生
        if root.left and root.left.priority > root.priority:
            root = rorate_right(root)
    else:
        root.right_size += 1
        root.right = insert_node(root.right, key, priority)

        # 2分ヒープ条件を満たない場合回転が発生
        if root.right and root.right.priority > root.priority:
            root = rorate_left(root)
    return root


def search_node(root, key):
    # keyによる2分探索のみ
    if root is None:
        return False

    if root.key == key:
        return True

    if key < root.key:
        return search_node(root.left, key)
    else:
        return search_node(root.right, key)


def print_treap(root):
    if root:
        print('root')
        print(root.key)
        print(root.priority)
    if root.right:
        print('right')
        print(root.right.key)
        print(root.right.priority)
    if root.left:
        print('left')
        print(root.left.key)
        print(root.left.priority)


def delete_node(root, key):
    """
    考えられるケース
    - 削除対象ノードが葉ノードの場合、葉を削除するだけで終わり
    - 片方の子ノードしか持たない場合ノードを削除して、自分の子ノードは自分の親ノードに付ければ良い
    - 両方の子ノードを持つ場合、rootが葉になるまで回転を繰り返す

    削除したいノードが見つからなかった場合は木をそのまま返す
    """

    if root is None:
        return None

    if key < root.key:
        root.left = delete_node(root.left, key)
    elif key > root.key:
        root.right = delete_node(root.right, key)
    else:
        # keyが見つかった場合
        if root.left is None and root.right is None:
            root = None
        elif root.left and root.right:
            if root.left.priority < root.right.priority:
                root = rotate_left(root)

                root.left = delete_node(root.left, key)
            else:
                root = rorate_right(root)
                root.right = delete_node(root.right, key)
        else:
            # 片方の子ノードしか持たない場合
            # ノードを削除して、自分の子ノードは自分の親ノードに付ければ良い
            child = root.left if root.left else root.right
            root = child
    return root


def print_pretty_treap(root, space):
    height = 10

    # Base case
    if root is None:
        return

    # increase distance between levels
    space += height

    # print right child first
    print_pretty_treap(root.right, space)

    # print current node after padding with spaces
    for i in range(height, space):
        print(' ', end='')

    print((root.key, root.priority))

    # print left child
    print_pretty_treap(root.left, space)


def print_pretty_treap_childsize(root, space):
    height = 10

    # Base case
    if root is None:
        return

    # increase distance between levels
    space += height

    # print right child first
    print_pretty_treap_childsize(root.right, space)

    # print current node after padding with spaces
    for i in range(height, space):
        print(' ', end='')

    print((root.key, root.priority, root.left_size, root.right_size))

    # print left child
    print_pretty_treap_childsize(root.left, space)


def search_ith_node(root, i, delta_num=0):
    if (root.left_size + delta_num + 1) < i:
        delta_num += root.left_size + 1
        root = root.right
        return search_ith_node(root, i, delta_num)
    elif (root.left_size + delta_num + 1) > i:
        root = root.left
        return search_ith_node(root, i, delta_num)
    elif (root.left_size + delta_num + 1) == i:
        return root.key


if __name__ == "__main__":
    start_time = datetime.now()
    import random
    keys = random.sample([v for v in range(100)], 10)
    priorities = random.sample([v for v in range(100)], 10)

    root = None
    for key, priority in zip(keys, priorities):
        root = insert_node(root, key, priority)
    end_time = datetime.now()
    print('{}ms'.format((end_time-start_time).microseconds/1000))

    print(keys)
    print(priorities)
    # print_treap(root)

    # print(search_node(root, 10))
    # print(search_node(root, 9))
    # print(search_node(root, 100))

    # print('print deleted treap')
    # print_treap(delete_node(root, 220))

    # print_pretty_treap(root, 0)

    # print('================================================================================================')

    # print_pretty_treap_childsize(root, 0)

    # i番目に小さいデータ
    value = search_ith_node(root, 3)
    print('third value: ', value)

    value = search_ith_node(root, 7)
    print('third value: ', value)

    print('sorted keys : ', sorted(keys))
