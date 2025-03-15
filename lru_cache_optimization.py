import random
import time
from functools import lru_cache

# --- Параметри ---
N = 100_000  # Розмір масиву
Q = 50_000   # Кількість запитів
CACHE_SIZE = 1000  # Максимальний розмір кешу

# --- Генерація масиву ---
array = [random.randint(1, 100) for _ in range(N)]
array_storage = {}  # Зберігає стан масиву для кешу

# --- Функції без кешу ---
def range_sum_no_cache(L, R):
    return sum(array[L:R + 1])

def update_no_cache(index, value):
    array[index] = value

# --- Функції з кешем ---
@lru_cache(maxsize=CACHE_SIZE)
def cached_range_sum(array_id, L, R):
    global array_storage
    return sum(array_storage[array_id][L:R + 1])

def range_sum_with_cache(L, R):
    global array_storage
    array_id = id(array)
    if array_id not in array_storage:
        array_storage[array_id] = array
    return cached_range_sum(array_id, L, R)

def update_with_cache(index, value):
    global array_storage
    array[index] = value
    array_id = id(array)
    if array_id in array_storage:
        cached_range_sum.cache_clear()
        array_storage[array_id] = array

# --- Генерація тестових запитів ---
queries = []
for _ in range(Q):
    query_type = random.choice(["Range", "Update"])
    if query_type == "Range":
        L = random.randint(0, N - 1)
        R = random.randint(L, N - 1)
        queries.append((query_type, L, R))
    else:
        index = random.randint(0, N - 1)
        value = random.randint(1, 100)
        queries.append((query_type, index, value))

# --- Тест без кешу ---
start_time = time.time()
for query in queries:
    if query[0] == "Range":
        range_sum_no_cache(query[1], query[2])
    else:
        update_no_cache(query[1], query[2])
time_no_cache = time.time() - start_time

# --- Тест з кешем ---
start_time = time.time()
for query in queries:
    if query[0] == "Range":
        range_sum_with_cache(query[1], query[2])
    else:
        update_with_cache(query[1], query[2])
time_with_cache = time.time() - start_time

# --- Вивід результатів ---
print(f"Час виконання без кешування: {time_no_cache:.2f} секунд")
print(f"Час виконання з LRU-кешем: {time_with_cache:.2f} секунд")