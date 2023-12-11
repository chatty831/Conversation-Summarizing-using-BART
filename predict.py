def predict(prompt,tokenizer, model):
    inputs = tokenizer(prompt, return_tensors='pt')

    summary_ids = model.generate(inputs["input_ids"], num_beams=2, max_length=128)

    output_sent = tokenizer.batch_decode(summary_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]

    return output_sent

