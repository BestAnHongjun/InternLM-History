pip install ninja
pip install packaging
pip install python-docx
pip install tqdm
pip install openxlab==0.0.34
pip install torch==2.0.1
pip install xtuner[deepspeed]

# MAX_JOBS=4 pip install flash-attn --no-build-isolation
mkdir flash-attention
cd flash-attention
wget -N https://gitee.com/an_hongjun/flash-attention/releases/download/2.3.5/flash_attn-2.3.5%20cu117torch2.0cxx11abiTRUE-cp39-cp39-linux_x86_64.whl
mv "flash_attn-2.3.5 cu117torch2.0cxx11abiTRUE-cp39-cp39-linux_x86_64.whl" "flash_attn-2.3.5+cu117torch2.0cxx11abiTRUE-cp39-cp39-linux_x86_64.whl"
pip install "flash_attn-2.3.5+cu117torch2.0cxx11abiTRUE-cp39-cp39-linux_x86_64.whl"
cd ..
# git clone https://gitee.com/an_hongjun/flash-attention.git
# cd flash-attention
# MAX_JOBS=4 python setup.py install
# cd ..

pip install lmdeploy[all]==v0.1.0
pip install gradio==4.15.0
