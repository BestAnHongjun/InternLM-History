pip install ninja
pip install packaging
pip install python-docx
pip install tqdm
pip install openxlab
pip install torch==2.0.1
pip install xtuner[deepspeed]
pip install gradio==3.18.0

# MAX_JOBS=4 pip install flash-attn --no-build-isolation
git clone https://gitee.com/an_hongjun/flash-attention.git
cd flash-attention
MAX_JOBS=8 python setup.py install
cd ..

pip install lmdeploy[all]==v0.1.0
