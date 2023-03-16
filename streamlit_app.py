import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

df = pd.read_csv('pet_food_customer_orders.csv')

X = df.drop('pet_food_tier', axis=1)
y = df['pet_food_tier']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

clf = DecisionTreeClassifier(random_state=42)

clf.fit(X_train, y_train)

y_pred = clf.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)


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
  with my_cnx.cursor() as my_cur:
    my_cur.execute("SELECT * from fruit_load_list")
    return my_cur.fetchall()

if streamlit.button('Get fruit Load List'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_rows = get_fruit_load_list()
  streamlit.dataframe(my_data_rows)

def insert_row_fruit(new_fruit):
  with my_cnx.cursor() as my_cur:
    my_cur.execute("insert into fruit_load_list values ('"+new_fruit+"')")
    return "Added: "+ new_fruit

fruit_add = streamlit.text_input('What fruit would you to add?','')
if streamlit.button('Add a new fruit'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  streamlit.text(insert_row_fruit(fruit_add))
#streamlit.write('The user added ', fruit_add)
#my_cur.execute("insert into fruit_load_list values ('from streamlit')")
