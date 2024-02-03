# setup environments
import os 
if not os.path.exists("flash-attention"):
    os.system("./setup.sh")

import gradio as gr
from lmdeploy import turbomind as tm
from modelscope.hub.snapshot_download import snapshot_download


MD5 = {
    "pytorch_model-00001-of-00008.bin": "3aa96b2686c72ce5c1c12dbb251f52c8",
    "pytorch_model-00002-of-00008.bin": "3135f7626e19827b319f8448f0e7f63a",
    "pytorch_model-00003-of-00008.bin": "cd23c24fe5fb2f990ac5a078e787615d",
    "pytorch_model-00004-of-00008.bin": "7b13e0526772b65a43b64e36fe28055f",
    "pytorch_model-00005-of-00008.bin": "dc8d33d528a3c3f3609f55f53d82e9b6",
    "pytorch_model-00006-of-00008.bin": "ca37e9e409abc7bd0298ebd537075e4b",
    "pytorch_model-00007-of-00008.bin": "b64fde4eabb90252ca8981cc6d71b617",
    "pytorch_model-00008-of-00008.bin": "bba8111f1beb1e7d8115c0871c9bbd8d"
}

PROMPT_TEMPLATE = """
<|System|>:你是中学历史学习助手，内在是InternLM-7B大模型。你的开发者是安泓郡。开发你的目的是为了提升中学生对历史学科的学习效果。你将对中学历史知识点做详细、耐心、充分的解答。
<|User|>:{}
<|Bot|>:"""
    

def download_model():
    model_dir = snapshot_download(
        'CoderAN/InternHistory-TurboMind-W4A16', 
        cache_dir='model/internlm-chat-7b-history', 
    )
    return model_dir


def api(question: str, chat_history: list=[]):
    if question == None or len(question) < 1:
        return "", chat_history
    try:
        prompt = PROMPT_TEMPLATE.format(question)
        input_ids = tm_model.tokenizer.encode(prompt)
        for outputs in generator.stream_infer(session_id=0, input_ids=[input_ids]):
            res, tokens = outputs[0]
        response = tm_model.tokenizer.decode(res.tolist())
        chat_history.append((question, response))
        return "", chat_history
    except Exception as e:
        return e, chat_history


if __name__ == "__main__":
    os.environ["no_proxy"] = "localhost,127.0.0.1,::1"
    model_path = download_model()

    tm_model = tm.TurboMind.from_pretrained(model_path)
    generator = tm_model.create_instance()

    block = gr.Blocks()
    with block as demo:
        with gr.Row(equal_height=True):   
            with gr.Column(scale=15):
                # 展示的页面标题
                gr.Markdown("""<h1><center>InternHistory</center></h1>
                    <center>中学历史学习助手</center>
                    """)

        with gr.Row():
            with gr.Column(scale=4):
                # 创建一个聊天机器人对象
                chatbot = gr.Chatbot(height=450, show_copy_button=True)
                # 创建一个文本框组件，用于输入 prompt。
                msg = gr.Textbox(label="Prompt/问题")

                with gr.Row():
                    # 创建提交按钮。
                    db_wo_his_btn = gr.Button("Chat")
                with gr.Row():
                    # 创建一个清除按钮，用于清除聊天机器人组件的内容。
                    clear = gr.ClearButton(
                        components=[chatbot], value="Clear console")
                    
            # 设置按钮的点击事件。当点击时，调用上面定义的 qa_chain_self_answer 函数，并传入用户的消息和聊天历史记录，然后更新文本框和聊天机器人组件。
            db_wo_his_btn.click(api, inputs=[
                                msg, chatbot], outputs=[msg, chatbot])

        gr.Markdown("""提醒：<br>
        1. 初始化数据库时间可能较长，请耐心等待。
        2. 使用中如果出现异常，将会在文本输入框进行展示，请不要惊慌。 <br>
        """)
    gr.close_all()
    # 直接启动
    demo.launch()
