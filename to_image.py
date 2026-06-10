# to_image.py
import argparse
import getpass
from pathlib import Path
from converter import json_to_protobuf
from compression import compress_protobuf
from encryption import encrypt_with_password
from grid_codec import binary_to_grid
from visualization import grid_to_image

def main():
    parser = argparse.ArgumentParser(description="Кодирование данных в защищённое изображение")
    parser.add_argument("input", help="Путь к raw.json или .pb")
    parser.add_argument("-o", "--output", default="data_visual.png")
    parser.add_argument("-p", "--password", help="Пароль (если не указан, будет запрошен скрыто)")
    args = parser.parse_args()

    password = args.password or getpass.getpass("🔑 Введите пароль для шифрования: ")
    if not password.strip():
        print("❌ Пароль не может быть пустым.")
        return

    inp = Path(args.input)
    pb_bytes = json_to_protobuf(inp) if inp.suffix == ".json" else inp.read_bytes()
    compressed = compress_protobuf(pb_bytes, level=22)
    encrypted = encrypt_with_password(compressed, password)
    grid = binary_to_grid(encrypted)
    img = grid_to_image(grid)
    img.save(args.output)
    print(f"✅ Изображение сохранено: {args.output}")

if __name__ == "__main__":
    main()