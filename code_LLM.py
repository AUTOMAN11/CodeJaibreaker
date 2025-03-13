from transformers import pipeline, AutoTokenizer
import torch
import pandas
import os
from datasets import Dataset


model_list = [
    {
        "id":1,
        "path":"", # your path
        "LLM_name":"CodeLlama-13b-Instruct-hf"
    },
    {
        "id":2,
        "path":"", # your path
        "LLM_name":"deepseek-coder-7b-instruct-v1.5"
    }
]




def model_init(model_id):
    pipe = pipeline(
        "text-generation",
        model=model_id,
        model_kwargs={"torch_dtype": torch.bfloat16},
        device_map="cuda:0",
    )
    return pipe

def prompt_init(input):
    prompt = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": input},
    ]
    return prompt

def get_response_dataset(pipe, dataset, tokenizer, model_name):
    
    terminators = tokenizer.eos_token_id
    if model_name == "Meta-Llama-3-8B-Instruct":
        terminators = [
            pipe.tokenizer.eos_token_id,
            pipe.tokenizer.convert_tokens_to_ids("<|eot_id|>")
        ]
    
    response = pipe(
        dataset['prompt'],
        do_sample=True,
        top_k=10,
        top_p=0.9,
        temperature = 0.75,
        num_return_sequences=1,
        eos_token_id=terminators,
        max_new_tokens=4096, 
    )
    content = []
    for i, res in enumerate(response):
        assitant = res[0]["generated_text"]
        if type(assitant) == list:
            content.append(assitant[-1]['content'])
        else:
            print(f"type error in {model_name} {i}")
    return content

def run(prompt_df, dataset, model_name, pipe, tokenizer, task):
    print(f"now is {model_name} {task}")
    response = get_response_dataset(pipe, dataset, tokenizer, model_name)
    prompt_df["response"] = response
    path = f"result/{model_name}"
    try:
        os.makedirs(path) 
    except FileExistsError:
        pass
    prompt_df.to_json(f"{path}/{task}_response.json", orient='records', indent=4)

def get_dataset(df):
    cols = df['prompt'].tolist()
    prompts = []
    for col in cols:
        prompt = prompt_init(col)
        prompts.append(prompt)
    dataset = Dataset.from_dict({'prompt': prompts})
    return dataset
    
def test_run_dataset():
    
    for i in range(0, 2):
        model = model_list[i]
        pipe = model_init(model["path"])
        tokenizer = AutoTokenizer.from_pretrained(model["path"])
        
        model_name = model["LLM_name"]
        prompt_df = pandas.read_json("data/T2C.json")
        dataset = get_dataset(prompt_df)
        run(prompt_df, dataset, model_name, pipe, tokenizer, "code_generation")

        prompt_df = pandas.read_json("data/funtion_level_completion.json")
        dataset = get_dataset(prompt_df)
        run(prompt_df, dataset, model_name, pipe, tokenizer, "function_level_completion")

        prompt_df = pandas.read_json("data/block_level_completion.json")
        dataset = get_dataset(prompt_df)
        run(prompt_df, dataset, model_name, pipe, tokenizer, "block_level_completion")



if __name__ == "__main__":
    test_run_dataset()