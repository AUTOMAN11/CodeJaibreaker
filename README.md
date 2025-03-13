# CodeJailbreaker
![overview](./fig/overview.png)

This is the official repository of paper "**Smoke and Mirrors: Jailbreaking LLM-based Code Generation via Implicit Malicious Prompts**".

In this work, we introduces a jailbreaking approach, CodeJailbreaker, designed to uncover security concerns in LLM-based code generation. The basic observation is that existing security mechanisms for LLMs are built through the instruction-following paradigm, where malicious intent is explicitly articulated within the instruction of the prompt. Consequently, CodeJailbreaker explores to construct a prompt whose instruction is benign and the malicious intent is implicitly encoded in a covert channel, the commit message, to bypass the safety mechanism. Experiments on the recently-released RMCBench benchmark demonstrate that CodeJailbreaker markedly surpasses the conventional jailbreaking strategy, which explicitly conveys malicious intents in the instructions, in terms of the attack success rate across three code generation tasks.

## Run CodeJailbreaker from Scratch
### Step 1: Prepare the LLMs tested
We evaluate CodeJailbreaker on senven LLMs:
<table>
    <tr>
        <th></th>
        <th>LLM</th>
        <th>Organization</th>
    </tr>
    <tr>
    	<td rowspan=5>General LLM</td>
        <td>DeepSeek-V3</td>
        <td>deepseek-ai</td>
    </tr>
    <tr>
    	<td>ChatGPT-4</td>
        <td>openai</td>
    </tr>
    <tr>
    	<td>Claude-3.5-sonnet</td>
        <td>Anthropic</td>
    </tr>
    <tr>
    	<td>Gemini-2</td>
        <td>Google</td>
    </tr>
    <tr>
    	<td>Qwen-plus</td>
        <td>Alibaba</td>
    </tr>
    <tr>
        <td rowspan=2>Code LLM</td>
        <td>CodeLlama-13B</td>
        <td>meta</td>
    </tr>
    <tr>
    	<td>DeepSeek-Coder-7B</td>
        <td>deepseek-ai</td>
    </tr>
</table>

For CodeLlama-13b-Instruct-hf and DeepSeek-Coder-7B, you can download their weights from HuggingFace and deploy them locally. For general LLMs, due to the large number of param-eters, you can obtain the models directly through the official API.

### Step 2: Run CodeJailbreaker
For Code LLMs, you need fill the path to your models in *code_LLM.py*, then you can run with:
> python code_LLM.py

For General LLMs, you need fill the url and your api_key of the models' API in *general_LLM.py*, then you can run with:
> python general_LLM.py

### Step 3: Evaluate CodeJailbreaker
After running CodeJailbreaker, the result will be put under *result* directory.

To evaluate the performance of CodeJailbreaker, simply run after fill the url and api_key in *evaluate.py*:
> python evaluate.py