# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.header(":blue[Choose the fruits you want in your custom smoothie.]")
    
name_on_smoothie=st.text_input("Name on smoothie.")
st.write(name_on_smoothie)

cnx=st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME","SEARCH_ON"))
# st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect("select up to 5 ingredients",my_dataframe,max_selections=5)
# temp part
# fv_df = st.dataframe(data=fruityvice_response.json(),use_container_width = True )
# end of temp part
if ingredients_list:
    ingredients_string=''
    for fruit in ingredients_list:
        ingredients_string+=fruit+' '
        st.subheader(f'{fruit} Nutrion Information.')
        fruityvice_response = requests.get(f'https://fruityvice.com/api/fruit/{fruit}')
        fv_df = st.dataframe(data=fruityvice_response.json(),use_container_width = True )
        
    my_insert_stmt = f"""insert into smoothies.public.orders(ingredients,name_on_order)
                        values ('{ingredients_string}','{name_on_smoothie}')"""


    time_to_insert=st.button("Submit Order")
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f'Your Smoothie is ordered, {name_on_smoothie}!', icon="✅")