import runpod
import os

runpod.api_key = os.getenv("RUNPOD_API_KEY")

endpoint = runpod.Endpoint("YOUR_ENDPOINT_ID")


def hashcat(uid, ):
    run_request = endpoint.run_sync(
            {
                "input": {
                    "prompt": "Hello, world!",
                }
            },
            timeout=30,
        )
