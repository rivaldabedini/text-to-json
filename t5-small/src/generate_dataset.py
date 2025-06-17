# Script to generate synthetic dataset matching sample structure.
import random
import json
import os

def generate_synthetic(output_path: str, num_samples: int = 100):
    versions = [
        "English Standard Version®", "King James Version", 
        "New International Version", "Revised Standard Version"
    ]
    descriptions = [
        "Creation and early events", "Historical accounts", 
        "Philosophical discussions", "Mythical tales"
    ]
    lorem = [
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
        "Vivamus lacinia odio vitae vestibulum vestibulum.",
        "Cras vehicula, mi eget feugiat fermentum, purus eros fermentum nisl, at aliquam nunc nisl quis leo.",
        "Sed ut perspiciatis unde omnis iste natus error sit voluptatem.",
        "But I must explain to you how all this mistaken idea of denouncing pleasure."
    ]
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        for i in range(num_samples):
            version = random.choice(versions)
            release_date = f"2025-06-{random.randint(1, 30):02d}"
            name = f"Sample Book {i+1}"
            content_desc = random.choice(descriptions)
            date_modified = f"2025-07-{random.randint(1, 30):02d}"
            
            toc_items = []
            content_items = []
            num_chapters = random.randint(3, 5)
            for idx in range(1, num_chapters + 1):
                toc_items.append({"index": idx, "title": f"Chapter {idx}"})
                content_items.append({"type": "header", "text": f"Chapter {idx}", "chapter": idx})
                body_text = random.choice(lorem)
                content_items.append({"type": "body", "text": body_text})

            record = {
                "version": version,
                "release_date": release_date,
                "name": name,
                "content_description": content_desc,
                "date_modified": date_modified,
                "table_of_contents": {
                    "label": "Table of Contents",
                    "items": toc_items
                },
                "content": content_items
            }
            text_input = " ".join(item["text"] for item in content_items if item["type"] == "body")
            entry = {"input": text_input, "target": json.dumps(record, ensure_ascii=False)}
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    print(f"Synthetic dataset written to {output_path}")

if __name__ == "__main__":
    generate_synthetic(output_path="./data/processed/synthetic.jsonl", num_samples=100)
