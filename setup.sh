pip install ninja
pip install packaging
pip install python-docx
pip install tqdm
pip install openxlab
pip install torch==2.0.1
pip install xtuner[deepspeed]

# MAX_JOBS=4 pip install flash-attn --no-build-isolation
git clone https://gitee.com/an_hongjun/flash-attention.git
cd flash-attention
MAX_JOBS=4 python setup.py install
cd ..

pip install lmdeploy[all]==v0.1.0
pip install gradio==4.15.0
