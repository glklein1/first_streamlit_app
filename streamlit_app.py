import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My Mom\'s New Healthy Diner')

streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🍓Make Your Own Smoothie 🥝🍍')

# import pandas
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

#Let's put a pick list here so customers can pick what fruit they want in their smoothie
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Banana','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# display the table on the page
# This was the original line for the full tablestreamlit.dataframe(my_fruit_list)
# being replaced with this
streamlit.dataframe(fruits_to_show)

# create repeatable code block (called a function)
def get_fruityvice_data(this_fruit_choice):
      fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
      fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
      return fruityvice_normalized    

#New Section to display FruityVice API Response
streamlit.header('Fruityvice Fruit Advice!')
try:
    fruit_choice = streamlit.text_input('What fruit would you like information about?')
    if not fruit_choice:
      streamlit.error("Please select a fruit to get more information.")
    else:
        back_from_function = get_fruity_vice_data(fruit_choice)
        streamlit.dataframe(back_from_function)
    
#    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
#      fruityvice_normalized = pandas.json_normalized(fruityvice_response.json())
#      streamlit.dataframe(fruityvice_normalized)
      
# except URLError as e:
#  streamlit.error()

# streamlit.write('The user entered ', fruit_choice)

# import requests
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)
#streamlit.text(fruityvice_response.json()) #Just writes the data to the screen

# take the json version of the data and normalize it
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
#output it to the screen as a table
streamlit.dataframe(fruityvice_normalized)

#don't run anything past here while we troubleshoot
streamlit.stop()

# import snowflake.connector

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * FROM FRUIT_LOAD_LIST")
my_data_rows = my_cur.fetchall()
streamlit.header("The Fruit Load List contains:")
streamlit.dataframe(my_data_rows)

# Allow end user to add fruit to the list
add_my_fruit = streamlit.text_input('What fruit would you like to add?', '')
streamlit.write('Thanks for adding ', add_my_fruit)

#This will not work correctly, but just go with it for now
my_cur.execute("insert into fruit_load_list values ('from streamlit')")
