# Script to prepare paired dataset from raw text and JSON examples.
import os
import json
from pathlib import Path

def prepare_dataset(raw_txt_dir: str, raw_json_dir: str, output_path: str):
    """
    Reads .txt and corresponding .json files, pairs them, and writes to a JSONL dataset.
    raw_txt_dir: directory containing .txt files
    raw_json_dir: directory containing .json files (same base filenames)
    output_path: path to output .jsonl
    """
    txt_paths = sorted(Path(raw_txt_dir).glob("*.txt"))
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as fout:
        for txt_path in txt_paths:
            base = txt_path.stem
            json_path = Path(raw_json_dir) / f"{base}.json"
            if not json_path.exists():
                print(f"Warning: JSON file not found for {base}")
                continue

            # Load input text
            text = txt_path.read_text(encoding='utf-8').strip()
            # Load and serialize JSON
            obj = json.loads(json_path.read_text(encoding='utf-8'))
            tgt = json.dumps(obj, ensure_ascii=False)

            entry = {"input": text, "target": tgt}
            fout.write(json.dumps(entry, ensure_ascii=False) + "\n")

    print(f"Dataset written to {output_path}")

if __name__ == "__main__":
    # Example usage
    prepare_dataset(
        raw_txt_dir="./data/raw/txt",
        raw_json_dir="./data/raw/json",
        output_path="./data/processed/dataset.jsonl"
    )