# pip install zstandard

import zstandard as zstd

def compress_protobuf(pb_data: bytes, level: int = 22) -> bytes:
    """Сжимает бинарные данные Protobuf. level=19 (быстрее) или 22 (максимальное сжатие)"""
    if not pb_data:
        raise ValueError("Входные данные Protobuf не должны быть пустыми")
    if level not in (19, 22):
        raise ValueError("Параметр level должен быть строго 19 или 22")
    
    compressor = zstd.ZstdCompressor(level=level)
    return compressor.compress(pb_data)

def decompress_protobuf(compressed_data: bytes) -> bytes:
    """Разжимает данные обратно в исходный бинарный формат Protobuf"""
    if not compressed_data:
        raise ValueError("Входные сжатые данные не должны быть пустыми")
        
    decompressor = zstd.ZstdDecompressor()
    return decompressor.decompress(compressed_data)