import json
# from transformers import T5Tokenizer, T5ForConditionalGeneration
from transformers import T5TokenizerFast, T5ForConditionalGeneration
import sys

def infer(input_text: str, model_dir: str = "outputs"):
    model_dir = str(model_dir).strip()  # Ensure it's a valid string
    print(f"Loading model from: {model_dir}")
    tokenizer = T5TokenizerFast.from_pretrained(model_dir)
    model     = T5ForConditionalGeneration.from_pretrained(model_dir)

    prompt = "convert to json: " + input_text
    print("Using prompt:", prompt)

    inputs  = tokenizer(prompt, return_tensors="pt", truncation=True)
    outputs = model.generate(**inputs, max_length=512)
    result  = tokenizer.decode(outputs[0], skip_special_tokens=True)

    print("Raw model output:", result)
    try:
        parsed = json.loads(result)
        print(json.dumps(parsed, indent=2, ensure_ascii=False))
    except json.JSONDecodeError:
        print("Failed to parse JSON:\n", result)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python inference.py '<text input>' [model_dir]")
    else:
        text = sys.argv[1]
        print(f"Input text: {text}")
        model_dir = sys.argv[2] if len(sys.argv) > 2 else "outputs"
        print(f"Using model directory: {model_dir}")
        infer(text, model_dir)
