import streamlit as st
import asyncio
from snowflake.snowpark.functions import col
import time

cnx=st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"),col("SEARCH_ON"))

async def fake_fetch_data(sleeptime:int = 5):
    await asyncio.sleep(sleeptime)
    return "this is not really data - but here you go"

async def submit_order(ingredients: str, name_on_smoothie:str):
    time.sleep(60)
    my_insert_stmt = f"""insert into smoothies.public.orders(ingredients,name_on_order)
                    values ('{ingredients}','{name_on_smoothie}')"""
    session.sql(my_insert_stmt).collect()
        
st.write("# This is an async page")
name_on_smoothie=st.text_input("Name on smoothie.")
ingredients_list = st.multiselect("select up to 5 ingredients",my_dataframe,max_selections=5)
if ingredients_list:
    ingredients_string = ",".join(fruit for fruit in ingredients_list)       
    time_to_insert=st.button("Submit Order")
    if time_to_insert:
        with st.spinner("creating order..."):
            asyncio.run(submit_order(ingredients_string,name_on_smoothie))
            st.success(f'Your Smoothie is ordered, {name_on_smoothie}!', icon="✅")
