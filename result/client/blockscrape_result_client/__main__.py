import argparse
import asyncio
from json import JSONEncoder, JSONDecoder
from datetime import datetime
import socketio

from schema import TaskResultSchema

parser = argparse.ArgumentParser()
parser.add_argument("--result_server_url", type=str, default="http://localhost:8000")
parser.add_argument("--output_dir", type=str, default="output")
parser.add_argument("--job_id", type=str, default="978fdba9-9225-4a80-8b60-347b7a7d1385")
parser.add_argument("--server_path", type=str, default="")
parsed_args = parser.parse_args()
mining_server_url: str = parsed_args.result_server_url
output_dir: str = parsed_args.output_dir
server_path: str = parsed_args.server_path

sio = socketio.Client()


@sio.event
def connect():
    sio.emit("set_job", parsed_args.job_id)
    print("set job_id to: ", parsed_args.job_id)


@sio.on("task_result")
def compute_task_bundle(data):
    # write result to file
    parsed_data = TaskResultSchema.model_validate(data)
    print("got result: ")
    print(parsed_data)
    output_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    with open(f"./{output_dir}/{output_str}.txt", "w") as f:
        f.write(parsed_data.model_dump_json())


if __name__ == "__main__":
    try:
        sio.connect(mining_server_url, socketio_path=server_path)
    except KeyboardInterrupt:
        print("exiting")
