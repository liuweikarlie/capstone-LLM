
#step 1
git clone https://github.com/ggerganov/llama.cpp.git

# step 2
cd llama.cpp

#step 3
pip install -r requirements.txt

# Step 4 -if you use CUDA
make LLAMA_CUBLAS=1

# Step 4 - if you use cpu
make

# step 5 - convert model to gguf format
python ./convert.py <your_model_path> — outfile <output_name>.gguf


./quantize <model_output_in_step2>.gguf <output_file_name>.gguf Q4_K


./main -m <model_name>.gguf --interactive
#or
./main -m <model_name>.gguf --color -f prompts/alpaca.txt -ins -c 2048 --temp 0.2 -n 256 --repeat_penalty 1.3


./server -m <your_model>.gguf -ngl 100
