from openai import OpenAI
import pandas
import threading
import os
from retrying import retry


deepseek = {
    "api_key": "", # your key of deepseek
    "base_url": "", # your url of deepseek
    "name": "deepseek-v3"
}
qwen = {
    "api_key": "", # your key of qwen
    "base_url": "", # your url of qwen
    "name": "qwen-plus-latest"
}
gpt = {
    "api_key": "", # your key of gpt-4
    "base_url": "", # your url of gpt-4
    "name": "gpt-4"
}
claude = {
    "api_key": "", # your key of claude-3-5-sonnet
    "base_url": "", # your url of claude-3-5-sonnet
    "name": "claude-3-5-sonnet"
}
gemini = {
    "api_key": "", # your key of gemini-2
    "base_url": "", # your url of gemini-2
    "name": "gemini-2"
}
@retry(stop_max_attempt_number=6, wait_fixed=5000)
def get_response(prompt, m):
    client = OpenAI(api_key=m["api_key"], base_url=m["base_url"])
    response = client.chat.completions.create(
        model=m["name"],
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        stream = False
    )
    return response.choices[0].message.content

def multi_thread(prompt_df, model_name):
    row_num = len(prompt_df)
    threads = []
    for i in range(10):
        num = row_num // 10
        y = row_num % 10
        start = 0
        end = 0
        if i < y:
            start = i * (num + 1)
            end = start + num + 1
        else:
            start = (num + 1) * y + (i - y) * num
            end = start + num
        threads.append(threading.Thread(target=send_requests, args=(prompt_df, int(start), int(end), model_name)))
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

def send_requests(prompt_df, start, end, model_name):
    i = start
    while i < end:
        row = prompt_df.iloc[i]
        print("now is " + str(row["index"]))
        
        user_prompt = row["prompt"]
        try:
            response = get_response(user_prompt, model_name)
            prompt_df.at[i, "response"] = response
        except Exception as e:
            print(f"{model_name['name']} {i} Failed after retries: {e}")
        i += 1
        
def run():
    model_list = [deepseek, qwen, gpt, claude, gemini]
    for model in model_list:
        print(f"now is {model['name']}")
        path = f"result/{model['name']}"
        try:
            os.makedirs(path)
        except FileExistsError:
            pass
        
        prompt_df = pandas.read_json("data/T2C.json")
        multi_thread(prompt_df, model)
        prompt_df.to_json(f"{path}/code_generation_response.json", orient='records', indent=4)

        prompt_df = pandas.read_json("data/funtion_level_completion.json")
        multi_thread(prompt_df, model)
        prompt_df.to_json(f"{path}/funtion_level_completion_repsonse.json", orient='records', indent=4)

        prompt_df = pandas.read_json("data/block_level_completion.json")
        multi_thread(prompt_df, model)
        prompt_df.to_json(f"{path}/block_level_completion_response.json", orient='records', indent=4)
    

if __name__ == "__main__":
    run()
    
    