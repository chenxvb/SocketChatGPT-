import os
import openai
import json
from pickle import load, dump
from transformers import GPT2TokenizerFast
# openai.organization = "org-zBCuK7fVD9owyNsJUyVBRRuE"

with open('config.json', 'r') as f:
    BotConfig = json.load(f)

if BotConfig['openai_proxy']['http'] != '' and BotConfig['openai_proxy']['https'] != '':
    openai.proxy = {
        "http": BotConfig['openai_proxy']['http'],
        "https": BotConfig['openai_proxy']['https'] ,
    }

defaultApiKey =  BotConfig["defaultApiKey"]

config = {
    'default': {
        'preset': '',
        'api_key': '',
        'enable_context': True,
        'context': '',
        'openai': {
            'model': 'text-davinci-003',
            'temperature': 0.9,
            'max_tokens': 3000,
            'top_p': 1,
            'echo': False,
            'presence_penalty': 0,
            'frequency_penalty': 0,
        }
    }
}
tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")

if os.path.exists('config'):
    for file in os.listdir('config'):
        with open(f'config/{file}', 'rb') as f:
            config[file.replace('.pickle', '')] = load(f)
else:
    os.mkdir('config')

def newConfig(id):
    config[id] = config['default'].copy()
    saveConfig(id)

def checkConfig(id):
    if id not in config:
        newConfig(id)
        saveConfig(id)

def saveConfig(id):
    with open(f'config/{id}.pickle', 'wb') as f:
        dump(config[id], f)

def getConfig(id):
    checkConfig(id)
    return config[id]

def setConfig(id, conf):
    checkConfig(id)
    config[id] = conf;
    saveConfig(id)

def setPreset(id, preset):
    checkConfig(id)
    config[id]['preset'] = preset
    saveConfig(id)

def setApiKey(id, api_key):
    checkConfig(id)
    config[id]['api_key'] = api_key
    saveConfig(id)
    
def setEnableContext(id, enable_context):
    checkConfig(id)
    config[id]['enable_context'] = enable_context
    saveConfig(id)

def setMaxTokens(id, max_tokens):
    checkConfig(id)
    config[id]['openai']['max_tokens'] = max(min(max_tokens, 4096),4)
    saveConfig(id)

def clear(id):
    checkConfig(id)
    config[id]['context'] = ''
    config[id]['preset'] = ''
    saveConfig(id)

def get_chat(prompt,group_config):
    try:
        openai.api_key = group_config['api_key'] or defaultApiKey
        resp = openai.Completion.create(**group_config['openai'],prompt=prompt)
        resp = resp['choices'][0]['text']
    except openai.OpenAIError as e:
        resp = str(e)
    return resp

def chat(id, prompt):
    group_config = getConfig(id)
    # 加载上下文
    if group_config['enable_context']:
        group_context = group_config['context']
    else:
        group_context = ''

    # 计算可发送的 token 数量
    token_limit = 4096 - group_config['openai']['max_tokens'] - len(tokenizer.encode(group_config["preset"])) - 3
    group_context = f'{group_context}Q:{prompt}\nA:'
    ids = tokenizer.encode(group_context)
    tokens = tokenizer.decode(ids[-token_limit:])
    # 计算可发送的字符数量
    char_limit = len(''.join(tokens))
    group_context = group_context[-char_limit:]
    # 从最早的提问开始截取
    pos = group_context.find('Q:')
    group_context = group_context[pos:]
    # 加载预设
    query = f'{group_config["preset"]}\n\n{group_context}'
    print(f'>>>{query}')
    resp = get_chat(query,group_config)
    resp = resp.strip()
    # 更新上下文
    if group_config['enable_context']:
        group_config['context'] = f'{group_context}{resp}\n\n'
    else:
        group_config['context'] = ''
    print(f'<<<{resp}')
    saveConfig(id)
    return resp

if __name__ == '__main__':
    while True:
        prompt = input('>>>')
        chat('test',prompt)
