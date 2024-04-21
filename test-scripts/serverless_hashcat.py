import requests
import runpod
import compute
from neurons.Validator.pow import run_validator_pow


endpoints = []


def local_worker(input_data):
    endpoint = "http://localhost:8000/runsync"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer XXXXXXXXXXXXX",
    }

    response = requests.post(endpoint, json=input_data, headers=headers)
    return response.json()


def spawn_pow(length: int = compute.pow_min_difficulty):
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
    return input_data, password


if __name__ == "__main__":
    for _ in range(5):
        input_data, password = spawn_pow()
        print(local_worker(input_data))
        print(password)
