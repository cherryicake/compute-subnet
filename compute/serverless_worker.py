import runpod
import compute
import os
import time
import shlex
import bittensor as bt
import requests

runpod.api_key = "XDYRIUTAAZFT88TC8VGQL3TPPIFG3C5CK0RPI72M"

endpoints = [
    # {
    #     "endpoint": runpod.Endpoint("t7e3xyfi6wasnb"),
    #     "max_challenge_difficulty": 9, # 当前Serverless硬件适合处理的最大任务难度
    #     "gpu": "A4500",
    # },
    # {
    #     "endpoint": runpod.Endpoint("7tdpqcwi8grfm4"),
    #     "max_challenge_difficulty": 12,
    #     "gpu": "4090",
    # },
    # {
    #     "endpoint": runpod.Endpoint("n6ac67bq451dt5"),
    #     "max_challenge_difficulty": 12,
    #     "gpu": "H100",
    # }
    {
        "endpoint": "https://vvx8gw6m9uz7q7-8000.proxy.runpod.net/hashcat",
        "max_challenge_difficulty": 12,
        "gpu": "4090*5"
    }
]

def hashcat(
    endpoint: runpod.Endpoint | str,
    _hash: str,
    salt: str,
    mode: str,
    chars: str,
    mask: str,
    timeout: int = compute.pow_timeout,
    hashcat_path: str = compute.miner_hashcat_location,
    hashcat_workload_profile: str = compute.miner_hashcat_workload_profile,
    hashcat_extended_options: str = compute.miner_hashcat_extended_options,
):
    response = {}
    try:
        command = [
            hashcat_path,
            f"{_hash}:{salt}",
            "-a",
            "3",
            "-D",
            "2",
            "-m",
            mode,
            "-1",
            str(chars),
            mask,
            "-w",
            hashcat_workload_profile,
            hashcat_extended_options,
        ]
        command_str = " ".join(shlex.quote(arg) for arg in command)
        bt.logging.info(f"command_str🟠: {command_str}")

        start_time = time.time()

        input_data = {
                    "input": {
                        "_hash": _hash,
                        "salt": salt,
                        "mode": mode,
                        "chars": chars,
                        "mask": mask,
                        "timeout": timeout,
                        "hashcat_workload_profile": hashcat_workload_profile,
                        "hashcat_extended_options": hashcat_extended_options,
                    }
                }

        if isinstance(endpoint, runpod.Endpoint):
            response = endpoint.run_sync(
                request_input=input_data,
                timeout=timeout,
            )
        else:
            response = requests.post(url=endpoint, json=input_data)
            if response.status_code == 200:
                response = response.json()
            else:
                response = {"error": f"requests error code: {response.status_code}"}
    except Exception as e:
        bt.logging.exception(e)
        response['code'] = 400
        response['error'] = str(e)
    response['run_sync_time'] = time.time() - start_time
    return response
