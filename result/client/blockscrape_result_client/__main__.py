import argparse
import asyncio
from json import JSONEncoder, JSONDecoder

import socketio

from schema import TaskResultSchema

parser = argparse.ArgumentParser()
parser.add_argument("--result_server_url", type=str, default="localhost")
parser.add_argument("--output_dir", type=str, required=True)
parser.add_argument("--job_id", type=str, required=True)
parsed_args = parser.parse_args()
mining_server_url: str = parsed_args.result_server_url
output_dir: str = parsed_args.output_dir

sio = socketio.Client(logger=True, engineio_logger=True)


@sio.event
def connect():
    sio.emit("set_job", parsed_args.job_id)
    print("set job_id to: ", parsed_args.job_id)


@sio.on("task_result")
def compute_task_bundle(data):
    # write result to file
    print("got result: ")
    print(data)
    parsed_data = JSONDecoder().decode(data)
    parsed_data = [TaskResultSchema.model_validate(task_res) for task_res in parsed_data]
    for task_res in parsed_data:
        with open(f"{output_dir}/{str(task_res.time)}", "w") as f:
            f.write(task_res.model_dump_json())


if __name__ == "__main__":
    try:
        sio.connect(mining_server_url)
    except KeyboardInterrupt:
        print("exiting")
