# generate_raw.py
import argparse
import json
import random
import string
from pathlib import Path

def _generate_record(idx: int) -> dict:
    """Генерирует одну запись, строго соответствующую схеме Ser из serialization.proto"""
    titles = ["Настройка сервера", "Бэкап БД", "Обновление API", "Логи деплоя", "Ключ доступа", "Миграция данных"]
    descs = ["Первичная конфигурация", "Ежедневный снапшот", "Патч безопасности", "Сбор метрик", "Ротация секретов", "Тестовая нагрузка"]
    domains = ["@corp.com", "@dev.io", "@secure.net", "@cloud.org"]

    return {
        "record_id": 1000 + idx,
        "title": f"{random.choice(titles)} #{idx+1}",
        "description": f"{random.choice(descs)} для задачи {idx+1}",
        "login": f"user_{idx:03d}{random.choice(domains)}",
        "password": ''.join(random.choices(string.ascii_letters + string.digits + "!@#$%", k=14))
    }

def main():
    parser = argparse.ArgumentParser(description="Генерация raw.json с заданным количеством записей")
    parser.add_argument("count", type=int, help="Количество записей для генерации (например, 100)")
    parser.add_argument("-o", "--output", type=str, default="raw.json", help="Имя выходного файла (по умолчанию: raw.json)")
    args = parser.parse_args()

    if args.count < 1:
        parser.error("Количество записей должно быть больше 0.")

    data = {"records": [_generate_record(i) for i in range(args.count)]}
    output_path = Path(args.output)
    output_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"✅ Сгенерировано {args.count} записей -> {output_path.name} ({output_path.stat().st_size:,} байт)")

if __name__ == "__main__":
    main()