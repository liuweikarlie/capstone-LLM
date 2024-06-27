#!/bin/bash
# download ollama
# ensure download llama3 in ollama


ollama serve
litellm --model ollama_chat/llama3
python function_call_main.py

