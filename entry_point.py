from pathlib import Path
from PIL import Image  # ✅ ИСПРАВЛЕНИЕ: Добавлен импорт Image

from converter import json_to_protobuf, protobuf_to_json
from compression import compress_protobuf, decompress_protobuf
from encryption import generate_key, encrypt_bytes, decrypt_bytes
from grid_codec import binary_to_grid, grid_to_binary
from visualization import grid_to_image, image_to_grid

def main():
    print("🚀 Запуск пайплайна конвертации...")

    # 1. Генерация и конвертация
    raw_json_path = Path("raw.json")
    if not raw_json_path.exists():
        print("❌ Файл raw.json не найден!")
        return

    pb_bytes = json_to_protobuf(raw_json_path)
    print(f"✅ JSON → Protobuf ({len(pb_bytes)} байт)")

    # 2. Сжатие и шифрование
    aes_key = generate_key()
    compressed = compress_protobuf(pb_bytes, level=22)
    encrypted = encrypt_bytes(compressed, aes_key)
    print(f"🔒 Сжатие + Шифрование ({len(encrypted)} байт)")

    # 3. Визуализация
    grid_str = binary_to_grid(encrypted)
    final_img = grid_to_image(grid_str)
    final_img.save("data_visual.png")
    print(f"🖼️ Изображение сохранено: {final_img.size[0]}x{final_img.size[1]} px")

    # 4. Обратная конвертация
    loaded_img = Image.open("data_visual.png")
    recovered_grid = image_to_grid(loaded_img)
    decrypted_bytes = grid_to_binary(recovered_grid)
    decrypted = decrypt_bytes(decrypted_bytes, aes_key)
    decompressed = decompress_protobuf(decrypted)
    final_json = protobuf_to_json(decompressed)

    print("\n✅ Данные успешно восстановлены из изображения!")
    # print(final_json) # Раскомментируйте, чтобы увидеть JSON

if __name__ == "__main__":
    main()