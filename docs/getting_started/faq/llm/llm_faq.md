LLM USE FAQ
==================================
##### Q1:how to use openai chatgpt service
change your LLM_MODEL in `.env`
````shell
LLM_MODEL=proxyllm
````

set your OPENAPI KEY

````shell
PROXY_API_KEY={your-openai-sk}
PROXY_SERVER_URL=https://api.openai.com/v1/chat/completions
````

make sure your openapi API_KEY is available

##### Q2 What difference between `python dbgpt_server --light` and `python dbgpt_server`
```{note}
* `python dbgpt_server --light` dbgpt_server does not start the llm service. Users can deploy the llm service separately by using `python llmserver`, and dbgpt_server accesses the llm service through set the LLM_SERVER environment variable in .env. The purpose is to allow for the separate deployment of dbgpt's backend service and llm service.

* `python dbgpt_server` dbgpt_server service and the llm service are deployed on the same instance. when dbgpt_server starts the service, it also starts the llm service at the same time.

```

```{tip}
If you want to access an external LLM service(deployed by DB-GPT), you need to

1.set the variables LLM_MODEL=YOUR_MODEL_NAME, MODEL_SERVER=YOUR_MODEL_SERVER（eg:http://localhost:5000） in the .env file.

2.execute dbgpt_server.py in light mode

python pilot/server/dbgpt_server.py --light

```


##### Q3 How to use MultiGPUs

DB-GPT will use all available gpu by default. And you can modify the setting `CUDA_VISIBLE_DEVICES=0,1` in `.env` file
to use the specific gpu IDs.

Optionally, you can also specify the gpu ID to use before the starting command, as shown below:

````shell
# Specify 1 gpu
CUDA_VISIBLE_DEVICES=0 python3 pilot/server/dbgpt_server.py

# Specify 4 gpus
CUDA_VISIBLE_DEVICES=3,4,5,6 python3 pilot/server/dbgpt_server.py
````

You can modify the setting `MAX_GPU_MEMORY=xxGib` in `.env` file to configure the maximum memory used by each GPU.

##### Q4 Not Enough Memory

DB-GPT supported 8-bit quantization and 4-bit quantization.

You can modify the setting `QUANTIZE_8bit=True` or `QUANTIZE_4bit=True` in `.env` file to use quantization(8-bit quantization is enabled by default).

Llama-2-70b with 8-bit quantization can run with 80 GB of VRAM, and 4-bit quantization can run with 48 GB of VRAM.

Note: you need to install the latest dependencies according to [requirements.txt](https://github.com/eosphoros-ai/DB-GPT/blob/main/requirements.txt).

##### Q5 How to Add LLM Service dynamic local mode

Now DB-GPT through multi-llm service switch, so how to add llm service dynamic,

```commandline
dbgpt model start --model_name ${your_model_name} --model_path ${your_model_path}

chatglm2-6b
eg: dbgpt model start --model_name chatglm2-6b --model_path /root/DB-GPT/models/chatglm2-6b

chatgpt
eg: dbgpt model start --model_name chatgpt_proxyllm --model_path chatgpt_proxyllm --proxy_api_key ${OPENAI_KEY} --proxy_server_url {OPENAI_URL}
```
##### Q6 How to Add LLM Service dynamic in remote mode
If you  deploy llm service in remote machine instance, and you want to add model service to dbgpt server to manage

use dbgpt start worker and set --controller_addr.

```commandline
eg: dbgpt start worker --model_name vicuna-13b-v1.5 \
--model_path /app/models/vicuna-13b-v1.5 \
--port 8002 \
--controller_addr http://127.0.0.1:8000

```

##### Q7 dbgpt command not found

```commandline
pip install -e "pip install -e ".[default]"
```

##### Q8 When starting the worker_manager on a cloud server and registering it with the controller, it is noticed that the worker's exposed IP is a private IP instead of a public IP, which leads to the inability to access the service.

```commandline

--worker_register_host  public_ip     The ip address of current worker to register
                                to ModelController. If None, the address is
                                  automatically determined
```


