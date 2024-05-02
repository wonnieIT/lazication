import openai
import streamlit as st
import random
from io import BytesIO
from PIL import Image
#import leafmap.foliumap as leafmap
from streamlit_image_select import image_select
from langchain_community.llms import Ollama
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
# from mitosheet.streamlit.v1 import spreadsheet
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
import state
import pandas as pd
import numpy as np

llm = Ollama(model="llama2")
conversation = ConversationChain(
    llm=llm,
    memory=ConversationBufferMemory(),
)



# Function to generate random travel photos using DALL-E
def generate_travel_photos(vibe):
    prompt = f"A vibrant and atmospheric travel photograph of travel sites. The image should evoke a sense of {vibe}"
    response = openai.Image.create(
        prompt=prompt,
        n=10,
        size="512x512"
    )

    travel_photos = []
    for image_data in response['data']:
        travel_photos.append(image_data['url'])
    return travel_photos

# Function to display random travel photos in select boxes
def display_travel_photos(travel_photos):
    random.shuffle(travel_photos)

    option = st.selectbox(
        "Select a travel destination",
        options=[""] + [st.image(photo, caption=None, width=200) for photo in travel_photos],
        format_func=lambda option: option if option else "Choose a destination",
    )

    if option:
        st.write(f"You selected: {option}")

def generate_travel_recommendations(starting_point, duration, budget, vibe):

    prompt = f"You are an awesome travel expert. Create a specific travel plan for {duration} days with a budget of {budget} and a {vibe} vibe. When choosing a travel site,  it could be domestic or international but it should connsider the fact that the the person is departing from {starting_point}, has budget limit of {budget} and the trip duration should be {duration} days. The oupput should be daily plan with hourly schedules including destinations, accommodations, activities, and restaurants. "
    print(prompt)
    answer = conversation(prompt)
    return answer['response']


def generate_packlist( ):
    prompt = f"Return a list of what to pack for the travel you suggested. It should be specific. For example, it should add charger based on the types of charger for that country and clothings based on the weather condition. Please return only the python list without any explanation"
    answer = conversation(prompt)
    return answer['response']



def generate_background_info(plans):
    prompt = f"Create 5 background information or historical backgrounds to know when traveling based on the plan you suggested. It will be good if you add photos "
    answer = conversation(prompt)
    return answer['response']


def main():

    st.title("Lazications")


    style = st.expander("여행 스타일 선택", expanded=True)
    final  = st.expander("여행 계획")
    preparation  = st.expander("여행 준비물 리스트")
    study  = st.expander("알아두면 좋을 배경 지식")
    pack_list = []
    with style:
        
        # try:
        #     loc_string = streamlit_geolocation()
        #     print(loc_string)
        # except:
        #     print("error")
        # if loc_string['latitude'] is not None:
        #     current_location = find_city(loc_string)
        #     starting_point = current_location

        starting_point =  st.text_input("From", "Seoul")
        
        # m = leafmap.Map(center=[40, -100], zoom=4)
        # cities = 'https://raw.githubusercontent.com/giswqs/leafmap/master/examples/data/world_cities.csv'
        # # countries = 'https://raw.githubusercontent.com/giswqs/leafmap/master/examples/data/countries.geojson'

        # # m.add_geojson(countries, layer_name='countries')
        # m.add_points_from_xy(
        #     cities,
        #     x="longitude",
        #     y="latitude",
        #     icon_names=['gear', 'map', 'leaf', 'globe'],
        #     spin=True,
        #     add_legend=True,
        # )

        # m.to_streamlit(height=300)

        vibe = st.multiselect(
                'Travel Keyword',
                ['Romantic', 'City', 'Nature','Relaxing', 'Adventurous', 'Luxurious', 'Cultural', 'Dynamic', 'Eye-opening', 'Enriching', 'Educational', 'Active'])
        
        
        col1, col2, col3, space, col4 = st.columns([5, 5, 5, 0.5, 5])
        with col1:
            heads = st.text_input("Travel Crew", "1")
        with col2:
            budget = st.text_input("Total Budget(KRW)", "1000000KRW")
        with col3:
            duration = st.number_input("Duration(days)", 3, step=1)

            
        with col4:
            st.write("\n")  # add spacing
            st.write("\n")  # add spacing
            if st.button("Start"):
                with st.spinner("Generating travel recommendations..."):
                    recommendations= generate_travel_recommendations(starting_point, duration, budget, vibe)
                    pack_list = generate_packlist()
                    #dataframe = pd.read_csv(csv_output)

                    # Display the dataframe in a Mito spreadsheet
                    #final_dfs, code = spreadsheet(dataframe)
                    final.markdown(f"## Plan")
                    final.write(recommendations) 
                    preparation.markdown(f"## Things to pack")
                    preparation.write(pack_list) 
                    #xfinal.write(final_dfs)
                    # for ele, key in enumerate(list(pack_list)):
                    #     preparation.checkbox(label=ele, key=key)
                    info = generate_background_info( recommendations )
                    study.write(info)



    # Generate initial travel photos
    #travel_photos = generate_travel_photos(vibe)

    # Display the travel photos in select boxes
    #travel_options = image_select(label = '어떤 여행지 사진이 가장 끌립니까?', images = travel_photos, index = 0, return_value = 'index')


    # https://leafmap.org/notebooks/02_using_basemaps/ 

    # Retry button to regenerate new photos
    # if st.button("Retry"):
    #     travel_photos = generate_travel_photos(vibe)
    #     with select_box_placeholder.container():
    #         display_travel_photos(travel_photos)
    # if st.button("Generate Recommendations"):
    #     with st.spinner("Generating travel recommendations..."):
    #         recommendations = generate_travel_recommendations(duration, budget, vibe)
    #         st.markdown(f"## Travel Recommendations\n\n{recommendations}")


if __name__ == "__main__":
    main()