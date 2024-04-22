import requests
import runpod
import compute
import json
from neurons.Validator.pow import run_validator_pow
from compute import serverless_worker

difficulty_list = [7,8,9,10,11,12]
def local_worker(length: int = compute.pow_min_difficulty):
    password, hash, salt, mode, chars, mask = run_validator_pow(length)
    input_data = {
        "input": {
            "_hash": hash,
            "salt": salt,
            "mode": mode,
            "chars": chars,
            "mask": mask,
            "hashcat_workload_profile": compute.miner_hashcat_workload_profile,
            "hashcat_extended_options": compute.miner_hashcat_extended_options,
        }
    }
    print(input_data)
    endpoint = "http://localhost:8000/runsync"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer XXXXXXXXXXXXX",
    }

    response = requests.post(endpoint, json=input_data, headers=headers)
    return response.json()

def runpod_worker(endpoint: runpod.Endpoint, length: int = compute.pow_min_difficulty):
    _, hash, salt, mode, chars, mask = run_validator_pow(length)
    response = serverless_worker.hashcat(
        endpoint=endpoint,
        _hash=hash,
        salt=salt,
        mode=mode,
        chars=chars,
        mask=mask
    )
    return response

def serverless_benchmark():
    benchmarks = []

    for endpoint_dict in serverless_worker.endpoints:
        for difficulty in difficulty_list:
            response = runpod_worker(endpoint=endpoint_dict['endpoint'], length=difficulty)
            response['gpu'] = endpoint_dict['gpu']
            response['difficulty'] = difficulty
            benchmarks.append(response)
    
    return benchmarks


if __name__ == "__main__":
    # print(local_worker(12))
    benchmarks = serverless_benchmark()
    # 将对象数组写入 JSON 文件
    with open("benchmarks.json", "w") as json_file:
        json.dump(benchmarks, json_file, indent=4)
