import os
from datasets import load_dataset, DatasetDict
from transformers import T5Tokenizer, T5ForConditionalGeneration, Trainer, TrainingArguments


def train_model(
    data_path: str,
    model_name: str = "t5-small",
    output_dir: str = "outputs",
    epochs: int = 3,
    train_batch_size: int = 4,
    eval_batch_size: int = 4
):
    # Load and split dataset
    ds = load_dataset("json", data_files={"data": data_path}, split="data")
    ds = ds.train_test_split(test_size=0.1)
    datasets = DatasetDict({"train": ds["train"], "validation": ds["test"]})

    # Tokenizer and model
    tokenizer = T5Tokenizer.from_pretrained(model_name)
    model = T5ForConditionalGeneration.from_pretrained(model_name)

    def preprocess(examples):
        inputs = ["convert to json: " + txt for txt in examples["input"]]
        model_inputs = tokenizer(inputs, max_length=512, truncation=True, padding="max_length")

        with tokenizer.as_target_tokenizer():
            labels = tokenizer(examples["target"], max_length=512, truncation=True, padding="max_length")
        model_inputs["labels"] = labels["input_ids"]
        return model_inputs

    tokenized = datasets.map(preprocess, batched=True, remove_columns=["input", "target"])

    args = TrainingArguments(
        output_dir=output_dir,
        num_train_epochs=epochs,
        per_device_train_batch_size=train_batch_size,
        per_device_eval_batch_size=eval_batch_size,
        do_eval=True,
        eval_steps=100,
        save_steps=100,
        logging_steps=50,
        overwrite_output_dir=True
    )
    trainer = Trainer(
        model=model,
        args=args,
        train_dataset=tokenized["train"],
        eval_dataset=tokenized["validation"]
    )
    trainer.train()
    trainer.save_model(output_dir)
    tokenizer.save_pretrained(output_dir)
    print(f"Model and tokenizer saved to {output_dir}")


if __name__ == "__main__":
    os.makedirs("outputs", exist_ok=True)
    train_model(data_path="./data/processed/train_all.jsonl")
