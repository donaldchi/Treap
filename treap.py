"""
部分木を持たないバージョン
こちらに参照に作成
https://www.techiedelight.com/implementation-treap-data-structure-cpp-java-insert-search-delete/
"""

from random import randrange


class TreapNode:
    def __init__(self, key, priority=1000000, left=None, right=None):
        self.key = key
        # self.priority = randrange(priority)
        self.priority = priority
        self.left = left
        self.right = right


def rorate_left(root):
    # rootと右子ノードを回転し
    # rootを子ノードの左子ノードにつける
    # rootの左子ノードはそのまま移動後のrootの左子ノードになる
    R = root.right
    X = root.right.left

    # 回転
    R.left = root
    root.right = X

    return R


def rorate_right(root):
    # rootと左子ノードを回転し
    # rootを子ノードの左子ノードにつける
    L = root.left
    Y = root.left.right

    # 回転
    L.right = root
    root.left = Y

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
        root.left = insert_node(root.left, key, priority)

        # 2分ヒープ条件を満たない場合回転が発生
        if root.left and root.left.priority > root.priority:
            root = rorate_right(root)
    else:
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
    -
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
    # 見つからなかった場合は??
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


if __name__ == "__main__":
    length = 5
    keys = [randrange(100) for _ in range(length)]
    priorities = [randrange(100) for _ in range(length)]

    root = None
    for key, priority in zip(keys, priorities):
        root = insert_node(root, key, priority)

    print(keys)
    print(priorities)
    print_treap(root)

    # print(search_node(root, 10))
    # print(search_node(root, 9))
    # print(search_node(root, 100))

    # print('print deleted treap')
    # print_treap(delete_node(root, 220))

    print_pretty_treap(root, 0)
