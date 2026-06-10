import random
from PIL import Image, ImageDraw

# Отключаем искусственный лимит Pillow на количество пикселей
Image.MAX_IMAGE_PIXELS = None

CELL_SIZE = 10
LINE_COLOR = (255, 255, 255)  # Белые линии
THRESHOLD = 200               # Порог: пиксели > 200 считаются линией

def _safe_color() -> tuple:
    """Генерирует цвет, гарантированно далёкий от белого (макс 180 по каналу)."""
    return tuple(random.randint(20, 180) for _ in range(3))

def grid_to_image(grid_str: str) -> Image.Image:
    """Сетка символов → Изображение с белым паттерном на случайном тёмном фоне."""
    lines = [line.strip() for line in grid_str.strip().split('\n') if line.strip()]
    if not lines:
        raise ValueError("Пустая сетка")

    rows = len(lines)
    cols = max(len(row) for row in lines)
    pat_w = cols * CELL_SIZE
    pat_h = rows * CELL_SIZE

    # ✅ Холст теперь строго равен размеру паттерна (отступы убраны)
    canvas_w, canvas_h = pat_w, pat_h

    # 1️⃣ Слой паттерна: RGBA с прозрачным фоном и белыми линиями
    pat_img = Image.new("RGBA", (pat_w, pat_h), (0, 0, 0, 0))
    pat_draw = ImageDraw.Draw(pat_img)
    for r, row in enumerate(lines):
        for c, ch in enumerate(row):
            x0, y0 = c * CELL_SIZE, r * CELL_SIZE
            if ch == '/':
                pat_draw.line([(x0, y0 + CELL_SIZE - 1), (x0 + CELL_SIZE - 1, y0)], fill=LINE_COLOR, width=1)
            elif ch == '\\':
                pat_draw.line([(x0, y0), (x0 + CELL_SIZE - 1, y0 + CELL_SIZE - 1)], fill=LINE_COLOR, width=1)

    # 2️⃣ Слой фона: строго без белых/светлых оттенков, заполняет весь холст
    bg_img = Image.new("RGB", (canvas_w, canvas_h), _safe_color())
    bg_draw = ImageDraw.Draw(bg_img)

    for _ in range(80):
        shape = random.choice(['circle', 'polygon', 'line'])
        color = _safe_color()
        if shape == 'circle':
            r = random.randint(5, min(canvas_w, canvas_h) // 6)
            x, y = random.randint(0, canvas_w - r*2), random.randint(0, canvas_h - r*2)
            bg_draw.ellipse([x, y, x + r*2, y + r*2], fill=color)
        elif shape == 'polygon':
            pts = [(random.randint(0, canvas_w), random.randint(0, canvas_h)) for _ in range(random.randint(3, 5))]
            bg_draw.polygon(pts, fill=color)
        else:
            x1, y1 = random.randint(0, canvas_w), random.randint(0, canvas_h)
            x2, y2 = random.randint(0, canvas_w), random.randint(0, canvas_h)
            bg_draw.line([(x1, y1), (x2, y2)], fill=color, width=random.randint(1, 4))

    # 3️⃣ Композит: паттерн накладывается поверх фона, фон не смешивается с линиями
    bg_img.paste(pat_img, (0, 0), mask=pat_img)
    return bg_img


def image_to_grid(img: Image.Image) -> str:
    """Изображение → Сетка символов (обратное декодирование белых линий)."""
    canvas_w, canvas_h = img.size
    # Округляем до кратного CELL_SIZE на случай артефактов кропа
    pat_w = (canvas_w // CELL_SIZE) * CELL_SIZE
    pat_h = (canvas_h // CELL_SIZE) * CELL_SIZE

    # Вырезаем рабочую область и переводим в оттенки серого
    pat_img = img.crop((0, 0, pat_w, pat_h)).convert("L")
    pix = pat_img.load()

    rows = pat_h // CELL_SIZE
    cols = pat_w // CELL_SIZE
    grid = []

    for r in range(rows):
        row_chars = []
        for c in range(cols):
            x0, y0 = c * CELL_SIZE, r * CELL_SIZE
            # Проверяем диагональные пиксели на наличие БЕЛОГО цвета (> THRESHOLD)
            tl = pix[x0 + 2, y0 + 2] > THRESHOLD or pix[x0 + 7, y0 + 7] > THRESHOLD  # \
            bl = pix[x0 + 2, y0 + 7] > THRESHOLD or pix[x0 + 7, y0 + 2] > THRESHOLD  # /

            if bl and not tl:
                row_chars.append('/')
            elif tl and not bl:
                row_chars.append('\\')
            else:
                # Fallback: считаем яркие пиксели на диагоналях
                d1 = sum(pix[x0 + i, y0 + i] > THRESHOLD for i in range(10))
                d2 = sum(pix[x0 + i, y0 + 9 - i] > THRESHOLD for i in range(10))
                row_chars.append('\\' if d1 > d2 else '/')
        grid.append(''.join(row_chars))
    return '\n'.join(grid)