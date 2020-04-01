import transformers
import torch
from transformers import GPT2Tokenizer, GPT2LMHeadModel
import random
from transformers import AutoModel, AutoTokenizer, AutoModelWithLMHead
import os
import json




def load_model(model_dir=None):
    """Loads the saved GPT2 model from disk if the directory exists.
    Otherwise it will download the model and tokenizer from hugging face.  
    Returns 
    a tuple consisting of `(model,tokenizer)`
    """    

    if model_dir is None:
        model_dir = 'models/'
        if not os.path.isdir(model_dir):
            tokenizer = AutoTokenizer.from_pretrained("cpierse/gpt2_film_scripts")
            model = AutoModelWithLMHead.from_pretrained("cpierse/gpt2_film_scripts")
            return model, tokenizer

    tokenizer = GPT2Tokenizer.from_pretrained(model_dir)
    model = GPT2LMHeadModel.from_pretrained(model_dir)
    return model, tokenizer


def generate(model, tokenizer, input_text=None, num_samples=1, max_length=1000):
    model.eval()
    
    if input_text:
        input_ids = tokenizer.encode(input_text, return_tensors='pt')
        output = model.generate(
            input_ids= input_ids,
            do_sample=True,   
            top_k=50, 
            max_length = max_length,
            top_p=0.95, 
            num_return_sequences= num_samples
        )
    else:
        output = model.generate(
            bos_token_id=random.randint(1,50000),
            do_sample=True,   
            top_k=50, 
            max_length = max_length,
            top_p=0.95, 
            num_return_sequences=num_samples

        )


    decoded_output = []
    for sample in output:
        decoded_output.append(tokenizer.decode(
            sample, skip_special_tokens=True))

    return decoded_output

def update_index():
    "Updates samples index from which tweets are being generated"
    with open('counter.json', 'r+') as f:
        data = json.load(f)
        data['last_index'] = data['last_index'] + 1 # <--- add `id` value.
        f.seek(0)        # <--- should reset file position to the beginning.
        json.dump(data, f, indent=4)
        f.truncate()     # remove remaining part
        
def get_start_index():
    "Gets the current index of generated samples"
    with open('counter.json', 'r') as f:
        data = json.load(f)
        index = data['last_index'] # <--- add `id` value.
        return index




# if __name__ ==  "__main__":
#     model, tokenizer = load_model()
#     samples = generate(model, tokenizer, max_length=100,num_samples=1)
#     for sample in samples:
#         print(sample)

