import api
import socket
import re
import sys
import select
import _thread
from json import loads, load

with open('config.json', 'r') as f:
    BotConfig = load(f)

ListenSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ListenSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
ListenSocket.bind((BotConfig['bind_ip'], BotConfig['port']))
ListenSocket.listen(100)

def json_check(msg): 
    for i in range(len(msg)):
        if msg[i] == "{" and msg[-1] == "}":
            return loads(msg[i:])
    return None

def rev_main():  # Each new connection will have a new thread 

    inputs = [ListenSocket, sys.stdin]
    running = True
    
    while True:
        readable, writeable, exceptional = select.select(inputs, [], [])
        for sock in readable:
            if sock == ListenSocket:
                c, addr = sock.accept()
                inputs.append(c)
            else:
                _thread.start_new_thread(chat_main, (sock, 'ok'))
                inputs.pop()

def chat_main(sock, qwq):

    Request = sock.recv(50000).decode('utf-8', "ignore")
    rev = json_check(Request.strip('\n'))

    while True:
        if rev == None:
            break

        try:
            msg = rev['message']
            id = str(rev['group_id'])

            if ' ' in msg:
                if re.match(r"/.*? ", msg) != None:
                    index = re.match(r"/(.*?)[ $]", msg).group(1)
                else:
                    break
            else:
                index = msg[1:]

            if index == 'chat':
                rep = chat_msg(msg, id)
            
            elif index == 'clear':
                rep = clear_msg(msg, id)

            elif index == 'get':
                rep = get_msg(msg, id)
                
            elif index == 'set':
                rep = set_msg(msg, id)
                
            elif index == 'reset':
                rep = reset_msg(msg, id)

            elif index == 'preset':
                rep = preset_msg(msg, id)
                
            elif index == 'key':
                rep = key_msg(msg, id)
                
            elif index == 'mem':
                rep = mem_msg(msg, id)
                
            elif index == 'help':
                rep = help_msg(msg, id)
            
            else:
                rep = '指令错误'
            
        except:
            rep = '执行出错，请联系机器人管理员'

        print(rep)
        sock.send(rep.encode())
        break

            

    sock.close()


def chat_msg(msg:str, id:str):
    msg = msg[6:]
    res = api.chat(id, msg)
    return res


def key_msg(msg:str, id:str):
    if msg == '/key':
        return(id, '请输入 API Key')
    else:
        id = id
        msg = msg[5:]
        api.setApiKey(id, msg)
        return '已设置 API Key'


def mem_msg(msg:str, id: str):
    if msg == '/mem':
        return '请输入长度上限'
    else:
        id = id
        msg = msg[5:]
        return '已修改长度上限'
        print(int(msg))
        api.setMaxTokens(id, int(msg))


def set_msg(msg: str, id: str):
    if msg == '/set':
        return '请输入config'
    else:
        id = id
        msg = msg[5:]
        msg_par = ''
        for i in msg:
            if i == '"':
                msg_par += "'"
            elif i == "'":
                msg_par += '"'
            else:
                msg_par += i
        msg_par = msg_par.replace("True", "true")
        msg_par = msg_par.replace("False", "false")
        api.setConfig(id, dict(loads(msg_par)))
        return '已设置config'


def preset_msg(msg: str, id: str):
    if msg == '/preset':
        return '请输入预设内容'
    else:
        msg = msg.replace('/preset', '')
        api.setPreset(id, msg)
        return '已设置预设内容'


def reset_msg(msg: str, id:str):
    api.newConfig(id)
    return '已重置'


def get_msg(msg: str, id: str):
    res = str(api.getConfig(id))
    return res


def clear_msg(msg: str, id: str):
    api.clear(id)
    return '已重置对话'


def help_msg(msg: str, id: str):
    return                         '''\
OPQChatBot-GPT 指令列表
/chat   ：生成对话
/clear  ：重置对话
/get    ：查看配置
/set    ：设置配置（直接传入get的返回值即可）
/reset  ：重置配置
/preset ：修改预设
/key    ：设置 OpenAI API Key
/mem    ：设置记忆长度，范围为 4~4096
/help   ：查看帮助
仓库地址 : 未开放
Fork 源 : https://github.com/timlzh/OPQChatBot-GPT
配置参考 : https://beta.openai.com/docs/api-reference/completions/create
'''


if __name__ == "__main__":
    print('Chat Start!')
    
    while True:
        rev_main() 