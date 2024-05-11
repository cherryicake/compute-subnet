import requests
import runpod
import compute
import json
from neurons.Validator.pow import run_validator_pow
from compute import serverless_worker
import time
import concurrent.futures

difficulty_list = [7,8,9,10]
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
    password, hash, salt, mode, chars, mask = run_validator_pow(length)
    response = serverless_worker.hashcat(
        endpoint=endpoint,
        challenge_difficulty=length,
        miner_incentive=0.00401,
        _hash=hash,
        salt=salt,
        mode=mode,
        chars=chars,
        mask=mask
    )
    print(f"密码:::::{password}")
    return response

def serverless_benchmark():
    benchmarks = []

    for endpoint_dict in serverless_worker.endpoints:
        for difficulty in difficulty_list:
            response = runpod_worker(endpoint=endpoint_dict['endpoint'], length=difficulty)
            response['gpu'] = endpoint_dict['gpu']
            response['difficulty'] = difficulty
            print(response)
            benchmarks.append(response)
            time.sleep(5)
    
    return benchmarks

def serverless_benchmark_parallel():
    benchmarks = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        for _ in range(10):
            for endpoint_dict in serverless_worker.endpoints:
                for difficulty in difficulty_list:
                    # 每次提交两个任务给线程池
                    future_results = [executor.submit(runpod_worker, endpoint=endpoint_dict['endpoint'], length=difficulty) for _ in range(2)]
                    # 等待获取结果
                    for future in concurrent.futures.as_completed(future_results):
                        try:
                            response = future.result()
                            response['gpu'] = endpoint_dict['gpu']
                            response['difficulty'] = difficulty
                            print(response)
                            benchmarks.append(response)
                        except Exception as e:
                            print(f"An error occurred: {e}")
    return benchmarks
if __name__ == "__main__":
    # 本地测试
    # print(local_worker(12))
    
    # serverless 单任务串行测试
    # benchmarks = serverless_benchmark()
    # serverless 多任务并行测试
    benchmarks = serverless_benchmark_parallel()

    # 将对象数组写入 JSON 文件
    with open("benchmarks.json", "w") as json_file:
        json.dump(benchmarks, json_file, indent=4)