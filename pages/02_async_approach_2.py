import streamlit as st
import asyncio

async def fetch_data():
    await asyncio.sleep(10)
    return "this is not really data - but here you go"

async def main():
    st.write("#This is an async page")
    data = await fetch_data()
    st.write(data)

if __name__ == '__main__':
    asyncio.run(main())