import os
import asyncio

from openai import AsyncOpenAI

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

asyncSemaphore = asyncio.Semaphore(2)

SEMAPHORE_TIMEOUT = 8
OPENAI_API_TIMEOUT = 60

# AsyncOpenAI Client
client = AsyncOpenAI(
    api_key=OPENAI_API_KEY,
)


async def create_response(text: str):
    instructions = (
        f'Always start your reply with phrase "I am Fatherrunner. *Katana swing sound*".'
        f'Translate the whole phrase into the language you are responding in, if needed. For russian translate the word "Fatherrunner" as "Фазерраннер"'
    )

    try:
        # print('Process started')
        await asyncio.wait_for(asyncSemaphore.acquire(), timeout=SEMAPHORE_TIMEOUT)
    except asyncio.TimeoutError:
        # print('I am busy')
        raise TimeoutError('One at a time.')

    try:
        # print('Try 1 passed')
        try:
            print('Try 2 passed')
            response = await client.responses.create(
                model='gpt-5-nano',
                instructions=instructions,
                input=text,
            )
        except asyncio.TimeoutError:
            # print('I am busy')
            raise TimeoutError('I am busy rn, little boy.')

        # print(response.output_text)
        return response.output_text

    finally:
        asyncSemaphore.release()
