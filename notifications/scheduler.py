import asyncio
import random


async def faulty_server(el):
    if random.random() < 0.5:
        print('pass')
        return True
    else:
        print('fail')
        return False


async def scheduler():
    stack = [1, 2, 3]
    while stack:
        i = random.randint(0, len(stack)-1)
        if faulty_server(stack[i]):
            del stack[i]

if __name__ == "__main__":
    asyncio.run(scheduler())
