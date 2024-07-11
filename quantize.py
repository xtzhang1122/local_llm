"""
Adapted from M. Labonne's amazing notebook. Make sure to check out his work.

https://colab.research.google.com/drive/1pL8k7m04mgE5jo2NrjGi8atB0j_37aDD?usp=sharing

https://mlabonne.github.io/blog/posts/Quantize_Llama_2_models_using_ggml.html

"""

# What HuggingFace model do you want to quantize?
MODEL_ID = "mistralai/Mistral-7B-v0.1"

# What quantization methods do you want to use? M. Labonne recommends Q5_K_M. In my experience, Q4_0 also works well.
QUANTIZATION_METHODS = ["Q5_K_M"]


import subprocess

# Install llama.cpp
try:
    subprocess.run("git clone https://github.com/ggerganov/llama.cpp", shell=True, check=True)
except Exception as e:
    print(e)

try: 
    subprocess.run("cd llama.cpp && git pull && make clean && make", shell=True, check=True)
except Exception as e:
    print(e)

try:
    subprocess.run("pip install -r llama.cpp/requirements.txt", shell=True, check=True)
except Exception as e:
    print(e)


try:
    # Install git lfs https://docs.github.com/en/repositories/working-with-files/managing-large-files/installing-git-large-file-storage
    # Download model
    subprocess.run("git lfs install", shell=True, check=True)
    subprocess.run(f"git remote set-url origin https://xtzhang1122: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@huggingface.co/{MODEL_ID} && git pull origin", shell=True, check=True)
except Exception as e:
    print(e)

MODEL_NAME = MODEL_ID.split('/')[-1]

try:
    # Convert to fp16
    fp16 = f"{MODEL_NAME}/{MODEL_NAME.lower()}.fp16.bin"
    subprocess.run(f"python llama.cpp/examples/convert_legacy_llama.py {MODEL_NAME} --outtype f16 --outfile {fp16}", shell=True, check=True)
except Exception as e:
    print


for method in QUANTIZATION_METHODS:
    qtype = f"{MODEL_NAME}/{MODEL_NAME.lower()}.{method.upper()}.gguf"
    subprocess.run(f"/teamspace/studios/this_studio/local_llm/llama.cpp/examples/quantize/quantize {fp16} {qtype} {method}", shell=True, check=True)




