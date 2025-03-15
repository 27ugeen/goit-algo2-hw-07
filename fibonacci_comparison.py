import time
import matplotlib.pyplot as plt
from functools import lru_cache

# Реалізація Splay Tree
class SplayNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None

class SplayTree:
    def __init__(self):
        self.root = None

    def _splay(self, root, key):
        if root is None or root.key == key:
            return root

        if key < root.key:
            if root.left is None:
                return root
            if key < root.left.key:
                root.left.left = self._splay(root.left.left, key)
                root = self._rotate_right(root)
            elif key > root.left.key:
                root.left.right = self._splay(root.left.right, key)
                if root.left.right is not None:
                    root.left = self._rotate_left(root.left)
            return self._rotate_right(root) if root.left is not None else root
        else:
            if root.right is None:
                return root
            if key > root.right.key:
                root.right.right = self._splay(root.right.right, key)
                root = self._rotate_left(root)
            elif key < root.right.key:
                root.right.left = self._splay(root.right.left, key)
                if root.right.left is not None:
                    root.right = self._rotate_right(root.right)
            return self._rotate_left(root) if root.right is not None else root

    def _rotate_left(self, root):
        temp = root.right
        root.right = temp.left
        temp.left = root
        return temp

    def _rotate_right(self, root):
        temp = root.left
        root.left = temp.right
        temp.right = root
        return temp

    def insert(self, key, value):
        if self.root is None:
            self.root = SplayNode(key, value)
            return
        self.root = self._splay(self.root, key)
        if self.root.key == key:
            self.root.value = value
            return
        new_node = SplayNode(key, value)
        if key < self.root.key:
            new_node.right = self.root
            new_node.left = self.root.left
            self.root.left = None
        else:
            new_node.left = self.root
            new_node.right = self.root.right
            self.root.right = None
        self.root = new_node

    def search(self, key):
        self.root = self._splay(self.root, key)
        return self.root.value if self.root and self.root.key == key else None

# Фібоначчі з LRU Cache
@lru_cache(maxsize=None)
def fibonacci_lru(n):
    if n <= 1:
        return n
    return fibonacci_lru(n - 1) + fibonacci_lru(n - 2)

# Фібоначчі з Splay Tree
def fibonacci_splay(n, tree):
    cached_value = tree.search(n)
    if cached_value is not None:
        return cached_value
    if n <= 1:
        result = n
    else:
        result = fibonacci_splay(n - 1, tree) + fibonacci_splay(n - 2, tree)
    tree.insert(n, result)
    return result

# Параметри тестування
fib_numbers = list(range(0, 950, 50))
lru_times = []
splay_times = []

# Вимірювання часу для LRU Cache
for n in fib_numbers:
    start_time = time.time()
    fibonacci_lru(n)
    lru_times.append((time.time() - start_time) / 10)

# Вимірювання часу для Splay Tree
for n in fib_numbers:
    splay_tree = SplayTree()
    start_time = time.time()
    fibonacci_splay(n, splay_tree)
    splay_times.append((time.time() - start_time) / 10)

# Виведення таблиці
print(f"{'n':<10}{'LRU Cache Time (s)':<25}{'Splay Tree Time (s)':<25}")
print("-" * 60)
for i in range(len(fib_numbers)):
    print(f"{fib_numbers[i]:<10}{lru_times[i]:<25.8f}{splay_times[i]:<25.8f}")

# Побудова графіка
plt.figure(figsize=(10, 6))
plt.plot(fib_numbers, lru_times, marker='o', linestyle='-', label="LRU Cache")
plt.plot(fib_numbers, splay_times, marker='x', linestyle='-', label="Splay Tree")

# Оформлення графіка
plt.xlabel("Число Фібоначчі (n)")
plt.ylabel("Середній час виконання (секунди)")
plt.title("Порівняння часу виконання для LRU Cache та Splay Tree")
plt.legend()
plt.grid(True)

# Збереження та показ
plt.savefig("fibonacci_comparison.png")
plt.show()