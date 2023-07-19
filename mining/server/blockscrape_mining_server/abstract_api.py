from json import JSONDecoder
from typing import List
import httpx

from mining.server.blockscrape_mining_server import TaskSchema, TaskResultSchema


async def request_task_bundle(address: str = "localhost", number_of_tasks: int = 10) -> List[TaskSchema]:
    with httpx.AsyncClient() as client:
        response = JSONDecoder().decode(await client.post(address + "/task_bundle"))
    tasks: List[TaskSchema] = [TaskSchema.model_validate(x) for x in response]
    return tasks


async def register_result(List[TaskResultSchema]):
    pass
