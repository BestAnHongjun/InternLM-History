# setup environments
import os 
if not os.path.exists("flash-attention"):
    os.system("./setup.sh")

import gradio as gr
from openxlab.model import download
    

def download_model():
    download(model_repo='Coder-AN/InternLM-History', output='model/internlm-chat-7b-history')


def greet(name):
    return "您的输入是：" + name + "。这只是一个测试Demo，项目仍在开发中。"


if __name__ == "__main__":
    os.environ["no_proxy"] = "localhost,127.0.0.1,::1"
    download_model()
    iface = gr.Interface(fn=greet, inputs="text", outputs="text")
    iface.launch(share=True)
