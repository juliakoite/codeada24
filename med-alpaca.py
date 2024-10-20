import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

# Load the slow tokenizer and model
tokenizer = AutoTokenizer.from_pretrained("medalpaca/medalpaca-7b", use_fast=False)
pl = pipeline("text-generation", model="medalpaca/medalpaca-7b", tokenizer=tokenizer)
question = "Can you explain this medical charge on my medical bill? Here is the charge: CHEST PHYSIO SUBSQ"
context = "You are an AI Medical Assistant trained on a vast dataset of health information. Please be thorough and provide an informative answer. If you don't know the answer to a specific medical inquiry, advise seeking professional help."
answer = pl(f"Context: {context}\n\nQuestion: {question}\n\nAnswer: ",
max_new_tokens=200)
print(answer)
