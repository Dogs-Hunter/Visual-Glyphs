# from_image.py
import argparse
import getpass
from pathlib import Path
from PIL import Image
from encryption import decrypt_with_password
from compression import decompress_protobuf
from grid_codec import grid_to_binary
from visualization import image_to_grid
from converter import protobuf_to_json

def main():
    parser = argparse.ArgumentParser(description="Декодирование данных из защищённого изображения")
    parser.add_argument("input", help="Путь к data_visual.png")
    parser.add_argument("-o", "--output", default="restored.json")
    parser.add_argument("-p", "--password", help="Пароль (если не указан, будет запрошен скрыто)")
    args = parser.parse_args()

    password = args.password or getpass.getpass("🔑 Введите пароль для расшифровки: ")
    if not password.strip():
        print("❌ Пароль не может быть пустым.")
        return

    img = Image.open(args.input)
    grid = image_to_grid(img)
    encrypted = grid_to_binary(grid)
    compressed = decrypt_with_password(encrypted, password)
    pb_bytes = decompress_protobuf(compressed)
    json_str = protobuf_to_json(pb_bytes)
    Path(args.output).write_text(json_str, encoding="utf-8")
    print(f"✅ Данные восстановлены: {args.output}")

if __name__ == "__main__":
    main()