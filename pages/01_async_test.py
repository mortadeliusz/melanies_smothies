# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests
import pandas as pd
import asyncio



# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.header(":blue[Choose the fruits you want in your custom smoothie.]")
    
name_on_smoothie=st.text_input("Name on smoothie.")

cnx=st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"),col("SEARCH_ON"))
# st.dataframe(data=my_dataframe, use_container_width=True)
pd_df=my_dataframe.to_pandas()
# st.dataframe(pd_df)
# st.stop()


def submit_order(ingredients:str,name_on_smoothie:str):
    my_insert_stmt = f"""insert into smoothies.public.orders(ingredients,name_on_order)
                        values ('{ingredients}','{name_on_smoothie}')"""
    session.sql(my_insert_stmt).collect()
        
ingredients_list = st.multiselect("select up to 5 ingredients",my_dataframe,max_selections=5)


if ingredients_list:
    ingredients_string = ",".join(fruit for fruit in ingredients_list) 
    st.write(f'Ingredients str: #{ingredients_string}')      
    time_to_insert=st.button("Submit Order")
    if time_to_insert:
        submit_order(ingredients_string,name_on_smoothie)
        st.success(f'Your Smoothie is ordered, {name_on_smoothie}!', icon="✅")
