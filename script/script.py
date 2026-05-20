#!/usr/bin/env python3

import argparse
import binascii
import glob
import os
import sys


def file_info(path):
    try:
        with open(path, "rb") as f:
            data = f.read()

        size = len(data)
        crc = binascii.crc32(data) & 0xFFFFFFFF

        print(f"Arquivo : {path}")
        print(f"Tamanho : {size}")
        print(f"CRC32   : {crc:08X}")
        print("-" * 60)

    except Exception as e:
        print(f"ERRO: {path}: {e}", file=sys.stderr)


def expand_paths(patterns):
    files = []

    for pattern in patterns:
        # Expande curingas (*.mp3, *.bin, etc.)
        matches = glob.glob(pattern, recursive=True)

        if not matches:
            matches = [pattern]

        for item in matches:
            if os.path.isdir(item):
                for root, _, filenames in os.walk(item):
                    for filename in filenames:
                        files.append(os.path.join(root, filename))
            elif os.path.isfile(item):
                files.append(item)

    # Remove duplicados preservando ordem
    return list(dict.fromkeys(files))


def main():
    parser = argparse.ArgumentParser(
        description="Mostra tamanho e CRC32 de arquivos"
    )
    parser.add_argument(
        "files",
        nargs="+",
        help='Arquivos, diretórios ou padrões (*.mp3, ., *.bin, etc.)'
    )

    args = parser.parse_args()

    files = expand_paths(args.files)

    if not files:
        print("Nenhum arquivo encontrado.", file=sys.stderr)
        return 1

    for file in files:
        file_info(file)

    return 0


if __name__ == "__main__":
    sys.exit(main())