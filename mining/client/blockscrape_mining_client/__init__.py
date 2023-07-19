import argparse
import asyncio
from functools import reduce
from json import JSONDecoder, JSONEncoder

import blockscrape_mining_server.abstract_api
import httpx

parser = argparse.ArgumentParser()
parser.add_argument("--mining_server_url", type=str, default="localhost")
parsed_args = parser.parse_args()
mining_server_url: str = parsed_args.mining_server_url
async def scrape(request):
    httpx.request()


async def return_result(result):
    await sio.emit(event="scrape_result", data=JSONEncoder().encode(result))


async def get_and_run_task_bundle():
    task_bundle_obj = await blockscrape_mining_server.abstract_api.request_task_bundle()
    tasks = await asyncio.gather(*
                                 [return_result(scrape(task)) for task in task_bundle_obj]
                                 )
