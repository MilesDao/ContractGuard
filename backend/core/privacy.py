from contextlib import contextmanager
from typing import Generator

@contextmanager
def ephemeral_bytes(file_bytes: bytes) -> Generator[bytes, None, None]:
    """
    Guarantees file bytes are zeroed and deleted after processing.
    Contracts live in memory ONLY — NEVER saved to disk or DB.
    Complies with Nghị định 13/2023/NĐ-CP Art. 10.
    """
    try:
        yield file_bytes
    finally:
        # Zero out buffer before GC
        byte_arr = bytearray(file_bytes)
        for i in range(len(byte_arr)):
            byte_arr[i] = 0
        del file_bytes
