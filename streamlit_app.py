import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError



fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")


my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

streamlit.title('The new healthy restaurant!')

streamlit.header('Menu')

streamlit.text('🥣 Food!')
streamlit.header('🍞 Breakfast Menu')
streamlit.text('🥑 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(my_fruit_list)

streamlit.header("Fruityvice Fruit Advice!")

def fet_fruityvice_data(fruit):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit)
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normalized

try:
  fruit_choice = streamlit.text_input('Select fruit to information')
  if not fruit_choice:
    streamlit.error("Select a fruit")
  else:
    streamlit.dataframe(fet_fruityvice_data(fruit_choice))
    
except URLError as e:
  streamlit.error()

#fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
#streamlit.write('The user entered ', fruit_choice)


# write your own comment -what does the next line do? 
#fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# write your own comment - what does this do?
#streamlit.dataframe(fruityvice_normalized)

#streamlit.stop
streamlit.header("The Fruit List Contains")

def get_fruit_load_list():
  with my_cur = my_cnx.cursor():
  my_cur.execute("SELECT * from fruit_load_list")
  my_data_rows = my_cur.fetchall()

if streamlit.button('Get fruit Load List'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_rows = get_fruit_load_list()
  streamlit.dataframe(my_data_rows)

fruit_add = streamlit.text_input('What fruit would you to add?','')
streamlit.write('The added ', fruit_add)
#my_cur.execute("insert into fruit_load_list values ('from streamlit')")
