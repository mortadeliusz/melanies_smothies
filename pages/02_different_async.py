import streamlit as st
import asyncio
import time

tasks = []

async def call_api(search_phrase: str):
    # Your API call logic here
    return '{"name":"my fake JSON", "age":27}'

async def upload_to_s3(json_str: str):
    # Your S3 upload logic here
    await asyncio.sleep(10)
    st.toast("File uploaded to S3")

async def process_search(search_phrase: str):
    task_id = str(time.time())
    tasks.append(task_id)
    json_result = await call_api(search_phrase)
    await upload_to_s3(json_result)
    tasks.remove(task_id)

if st.button("Submit"):
    search_phrase = st.text_input("Search Phrase")
    if search_phrase:
        asyncio.create_task(process_search(search_phrase))

# Background process to monitor tasks
async def background_task():
    while True:
        if tasks:
            task_id = tasks[0]
            await process_search(task_id)
        await asyncio.sleep(1)  # Check for new tasks every second

asyncio.create_task(background_task())