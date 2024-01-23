import gradio as gr


def greet(name):
    return "您的输入是：" + name + "。这只是一个测试Demo，项目仍在开发中。"


iface = gr.Interface(fn=greet, inputs="text", outputs="text")
iface.launch()
