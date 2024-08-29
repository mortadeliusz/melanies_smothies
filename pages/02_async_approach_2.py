import streamlit as st
import asyncio

async def fake_fetch_data(sleeptime:int = 5):
    await asyncio.sleep(sleeptime)
    return "this is not really data - but here you go"

async def main():
    ingredients ='mango, jerry'
    name_on_smoothie="macias"
    cnx=st.connection("snowflake")
    session = cnx.session()
    st.write("# This is an async page")
    with st.spinner("creating order..."):
        await fake_fetch_data()
        my_insert_stmt = f"""insert into smoothies.public.orders(ingredients,name_on_order)
                    values ('{ingredients}','{name_on_smoothie}')"""
        session.sql(my_insert_stmt).collect()
        st.success("The order should be right there now.")
        

if __name__ == '__main__':
    asyncio.run(main())