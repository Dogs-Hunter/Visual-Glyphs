import os
import math
from typing import List

# --- Внутренние утилиты для работы с битами ---
def _bytes_to_bits(data: bytes) -> List[int]:
    """Конвертирует байты в список битов [0, 1] (MSB first)."""
    return [(byte >> i) & 1 for byte in data for i in range(7, -1, -1)]

def _bits_to_bytes(bits: List[int]) -> bytes:
    """Конвертирует список битов обратно в байты."""
    if len(bits) % 8 != 0:
        bits = bits + [0] * (8 - len(bits) % 8)
    
    result = bytearray()
    for i in range(0, len(bits), 8):
        byte = 0
        for j in range(8):
            byte = (byte << 1) | bits[i + j]
        result.append(byte)
    return bytes(result)

def _random_bits(n: int) -> List[int]:
    """Генерирует n криптографически случайных битов."""
    if n == 0:
        return []
    bytes_needed = (n + 7) // 8
    rand_bytes = os.urandom(bytes_needed)
    return _bytes_to_bits(rand_bytes)[:n]

HEADER_BITS = 32
CHAR_MAP = {0: '/', 1: '\\'}
REV_MAP = {'/': 0, '\\': 1}


def binary_to_grid(data: bytes) -> str:
    """
    Бинарные данные → Геометрический квадрат/прямоугольник
    1. Добавляет 4-байтовый заголовок с длиной исходных данных
    2. Дополняет криптографическим паддингом до ближайшего полного квадрата битов
    3. Мапит биты в '/' и '\' и возвращает строку-сетку
    """
    if not isinstance(data, bytes):
        raise TypeError("Ожидается тип bytes")
    if len(data) > (2**32 - 1):
        raise ValueError("Данные превышают лимит 4 ГБ")

    # 1. Заголовок + данные
    header = len(data).to_bytes(4, byteorder='big')
    payload_bits = _bytes_to_bits(header + data)
    
    # 2. Расчёт полного квадрата и паддинга
    total_bits = len(payload_bits)
    side = math.isqrt(total_bits)
    if side * side < total_bits:
        side += 1
    target_bits = side * side
    
    padding = _random_bits(target_bits - total_bits)
    all_bits = payload_bits + padding

    # 3. Маппинг и формирование сетки
    char_str = ''.join(CHAR_MAP[b] for b in all_bits)
    lines = [char_str[i:i+side] for i in range(0, target_bits, side)]
    return '\n'.join(lines)


def grid_to_binary(grid: str) -> bytes:
    """
    Геометрический квадрат/прямоугольник → Исходные бинарные данные
    Игнорирует паддинг, извлекает длину из заголовка и возвращает оригинал
    """
    clean = grid.replace('\n', '').replace(' ', '').replace('\r', '')
    if not clean:
        raise ValueError("Пустая сетка")
        
    bits = [REV_MAP[c] for c in clean]
    
    # 1. Читаем длину из первых 32 битов
    data_len_bits = bits[:HEADER_BITS]
    data_len = 0
    for b in data_len_bits:
        data_len = (data_len << 1) | b
        
    # 2. Извлекаем полезные данные
    data_bits = bits[HEADER_BITS : HEADER_BITS + data_len * 8]
    if len(data_bits) < data_len * 8:
        raise RuntimeError("Некорректная сетка: недостаточно битов для заявленной длины")
        
    return _bits_to_bytes(data_bits)