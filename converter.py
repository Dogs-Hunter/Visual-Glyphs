# pip install protobuf

import json
from pathlib import Path
from google.protobuf.json_format import MessageToJson, Parse, ParseError
from serialization_pb2 import SerPaswd

def json_to_protobuf(input_data, output_pb=None) -> bytes:
    """Конвертирует JSON-файл в бинарный формат Protobuf"""
    if isinstance(input_data, dict):
        json_str = json.dumps(input_data, ensure_ascii=False)
    elif isinstance(input_data, (str, Path)):
        json_str = Path(input_data).read_text(encoding="utf-8")
    else:
        raise TypeError("input_data должен быть dict, str или Path")

    msg = SerPaswd()
    try:
        Parse(json_str, msg, ignore_unknown_fields=True)
    except ParseError as e:
        raise ValueError(f"JSON не соответствует схеме .proto: {e}") from e

    binary_data = msg.SerializeToString()
    if output_pb:
        Path(output_pb).write_bytes(binary_data)
    return binary_data

def protobuf_to_json(input_data, output_json=None) -> str:
    """Конвертирует бинарный Protobuf в JSON-строку"""
    if isinstance(input_data, bytes):
        binary_data = input_data
    elif isinstance(input_data, (str, Path)):
        binary_data = Path(input_data).read_bytes()
    else:
        raise TypeError("input_data должен быть bytes, str или Path")

    msg = SerPaswd()
    msg.ParseFromString(binary_data)

    json_str = MessageToJson(msg, indent=2, ensure_ascii=False)
    if output_json:
        Path(output_json).write_text(json_str, encoding="utf-8")
    return json_str