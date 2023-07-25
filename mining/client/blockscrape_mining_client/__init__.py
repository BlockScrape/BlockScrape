import argparse
import asyncio
from functools import reduce
from json import JSONDecoder, JSONEncoder

import blockscrape_mining_server.abstract_api
import httpx

from mining.server.blockscrape_mining_server import TaskResultSchema, TaskSchema
from mining.server.blockscrape_mining_server.abstract_api import register_result

parser = argparse.ArgumentParser()
parser.add_argument("--mining_server_url", type=str, default="localhost")
parsed_args = parser.parse_args()
mining_server_url: str = parsed_args.mining_server_url


async def scrape(task: TaskSchema) -> TaskResultSchema:
    async with httpx.AsyncClient() as client:
        res: httpx.Response = await client.request(method=task.method.value,
                                                   url=task.url,
                                                   params=task.params,
                                                   headers=task.headers,
                                                   content=task.content,
                                                   data=task.data,
                                                   files=task.files,
                                                   json=task.json,
                                                   cookies=task.cookies,
                                                   )
        return TaskResultSchema(task_id=task.id,
                                headers=res.headers,
                                content=res.content,
                                encoding=res.encoding,
                                status=res.status_code,
                                elapsed=res.elapsed,
                                )


async def get_and_run_task_bundle():
    task_bundle_obj = await blockscrape_mining_server.abstract_api.request_task_bundle()
    tasks = await asyncio.gather(*
                                 [register_result(scrape(task)) for task in task_bundle_obj]
                                 )
