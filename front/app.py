import tensorflow as tf
import streamlit as st
from streamlit_elements import elements, mui, html
from streamlit_elements import media
import streamlit_elements as elem
import time
import requests
from foodE.registery import model_load
from foodE.model import pred
from foodE.streamlit_outils import new_ID
from foodE.streamlit_outils import exist_ID
from foodE.streamlit_outils import ID_update_height
from foodE.streamlit_outils import ID_update_weigth
from foodE.streamlit_outils import ID_update_weigth_height
from foodE.streamlit_outils import ID_read
import numpy as np
from PIL import Image
import os
from google.cloud import bigquery
import datetime
import plotly.express as px
import pandas as pd
import json


#Function
def calc_objectif(weigth,height,age,genre:str):
    """Calculate the portion of macronutriment based on height,weight,age and genre \n
    Return protein,fat,carbs,obj"""
    if genre == "M":
        calories = 88.362 + 13.397*weigth + 4.799*height - 5.677*age
        protein = 1.7*weigth
        fat = (calories*0.2)/9
        carbs = ((protein*4)+(fat*9))/4
        obj = calories *1.2
    else:
        calories = 447.593 + 9.247*weigth + 3.098*height - 4.330*age
        protein = 1.7*weigth
        fat = (calories*0.2)/9
        carbs = ((protein*4)+(fat*9))/4
        obj = calories *1.2
    return protein,fat,carbs,obj


#Instanciate client for bigquery
client = bigquery.Client()

# Create a sidebar with navigation links
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Personal information",  "Camera", "Page 2", "Journal"])

# Use the page variable to determine which page to display
if page == "Personal information":
    st.title("Personal information")

    with st.form(key='my_data_1'):
        t1, _, _ = st.columns(3)
        with t1 :
            user_ID = st.number_input(label='Enter your User ID please : ', value = 1)

        submit_button = st.form_submit_button(label='Submit')
        # Verifier si l'ID Exist
        exist_id = exist_ID(user_ID)[0]['f0_']

    #Logic for existing User
    if exist_id :
        id_read = ID_read(user_ID)[0]
        st.write("<center>Welcome</center>",unsafe_allow_html=True)
        st.write(f"<center>L'ID numéro {user_ID} est bien present dans notre base des données</center>"\
                ,unsafe_allow_html=True)

        #Get objectives data
        query = f"SELECT * from foode-376420.foodE.objectif WHERE UserID = {user_ID}"
        query_job = client.query(query)
        rows_raw = query_job.result()
        rows = [dict(row) for row in rows_raw]

        #Daily objectives display
        st.write("<center style = 'font-size:35px;'>Daily Objectives</center>",unsafe_allow_html=True)
        c1,c2 = st.columns(2)

        #Display pie chart for macronutriment
        data = pd.DataFrame({
            'Macronutrient': ['Protein', 'Carbs', 'Fat'],
            'Grams': [rows[0]["Protein"],rows[0]["Carbs"], rows[0]["Fat"]]
})
        pie = px.pie(data,values='Grams',color_discrete_sequence=["#167d09","#2e76e8","#ad0a0a"],hole=0.4,\
            labels=["protein","carbs","fat"],names=["protein","carbs","fat"])
        c2.plotly_chart(pie,use_container_width=500)

        #Display frame of objectives

        c1.markdown(f"""
        <div style="position: absolute; top: 150px; left: 5px;">
        🔥 {rows[0]["Calories"]} calories <br>
        🥚 {rows[0]["Protein"]}g proteins <br>
        🍞 {rows[0]["Carbs"]}g carbs <br>
        🥑 {rows[0]["Fat"]}g fat</div>
        """, unsafe_allow_html=True)
        #st.write(respons

        #Form to change weight
        form = st.form(key='my_data')
        c1,_ = form.columns(2)
        weigth = c1.slider(label='Change your weigth (kg) : ', min_value=40, max_value=150)
        submit_button = c1.form_submit_button(label='Submit')

        #Update Bigquery tables with new weight
        if submit_button:
            #Update weight in personnal info
            weight_query = f"UPDATE `foode-376420.foodE.ID_info` SET Weigth = {weigth} WHERE UserID={user_ID}"
            query_job = client.query(weight_query)
            rows_raw = query_job.result()

            #Change objective
            protein,fat,carbs,obj = calc_objectif(weigth,id_read["Height"],id_read["Age"],id_read["Genre"])
            objectif_query= f"UPDATE foode-376420.foodE.objectif\
                SET Protein = {round(protein,1)},Carbs = {round(carbs,1)}\
                    ,Fat = {round(fat,1)},Calories = {round(obj,1)}\
                WHERE UserID = {user_ID}"
            query_job = client.query(objectif_query)
            query_job.result()

            #Reload page, to show pie chart with new value
            st.experimental_rerun()


    #Logic to write a new ID in database
    else:
        st.write(f"L'user ID n'existe pas dans notre base. S'il vous plaît creez un nouveau utilisateur en renseignant les informations ci-dessous:")

        with st.form(key='my_data_2'):

            c1, c2 = st.columns(2)
            with c1:
                genre = st.selectbox("Genre : ", ["M", "F"])
                height = st.slider(label='Enter your height (cm) please : ', min_value=100, max_value=220)
            with c2:
                age = st.number_input(label='Age : ', value = 15)
                weigth = st.slider(label='Enter your weigth (kg) please : ', min_value=40, max_value=150)

            submit_button_2 = st.form_submit_button(label='Submit')

        if submit_button_2 :
            new_ID(user_ID, height, weigth, age, genre)

            #Calcul d'objectif
            protein,fat,carbs,obj = calc_objectif(weigth,height,age,genre)
            # if genre == "M":
            #     calories = 88.362 + 13.397*weigth + 4.799*height - 5.677*age
            #     protein = 1.7*weigth
            #     fat = (calories*0.2)/9
            #     carbs = ((protein*4)+(fat*9))/4
            #     obj = calories *1.2
            # else:
            #     calories = 447.593 + 9.247*weigth + 3.098*height - 4.330*age
            #     protein = 1.7*weigth
            #     fat = (calories*0.2)/9
            #     carbs = ((protein*4)+(fat*9))/4
            #     obj = calories *1.2

            #Pushing queries to BQ
            obj_update =   f"INSERT INTO `foode-376420.foodE.objectif` (UserID, Protein, Carbs, Fat, Calories)\
                VALUES ({round(user_ID,1)}, {round(protein,1)}, {round(carbs,1)}, {round(fat,1)}, {round(obj,1)})"
            query_job = client.query(obj_update)
            rows_raw = query_job.result()

            #Reload page to show pie chart after creating the new user
            st.experimental_rerun()


        # tester le fonctionnement de value
        # test = f'Heigth : {height}, weigth = {weigth}, user = {user_ID}'
        # st.write(test)






# Enregistrer données dans la table ID_heigth_weigth
# 1 creer fichier secrets.toml
# 2 ajouter dans .gitignore
# 3 ajouter secrets dans streamlit
# cf : https://docs.streamlit.io/knowledge-base/tutorials/databases/bigquery
# Si problemes de syncro : sudo hwclock -s
# Attention, dossier .streamlit (le deplacer ?)
# Age / Gere


if page == "Camera":
    st.title("Camera")
    img_file_buffer = st.camera_input("Take a picture")

    with st.spinner("Wait for it..."):
        time.sleep(2.5)
        if img_file_buffer:
            # Change image to the correct size
            img = Image.open(img_file_buffer)
            img_height = int(os.environ.get('IMG_HEIGHT'))
            img_width = int(os.environ.get('IMG_WIDTH'))
        # st.write(img_width)
            img = img.resize((img_height,img_width))
            #st.write(type(img))

            # Transform img to np.array
            img_array = np.array(img)
            #st.write(img_array.shape)

            # Make a json with a list
            jayson = {"img": img_array.tolist() }

            # Post request to API
            headers = {'Content-Type': 'application/json'}
            response = requests.post("http://localhost:8000/predict", headers = headers, json=jayson)

            if response.status_code == 200:
                st.balloons()
                response_list = json.loads(response.content.decode('utf-8'))
                body_list = [item['body'] for item in response_list]

                # st.write(f"Per 100g your {body_list[0]} meal contains: {body_list[1]} calories, {body_list[2]} carbs,\
                #    {body_list[3]} fat, {body_list[4]} proteins")

                st.markdown(f"""
                                ## 🍽️ : {body_list[0]}

                                #### **Per 100g** :

                                🔥 {body_list[1]} calories

                                🥚 {body_list[4]}g proteins

                                🍞 {body_list[2]}g carbs

                                🥑 {body_list[3]}g fat

                            """)
                #st.write(response.content)
            else:
                st.markdown("**Oops**, something went wrong 😓 Please try again.")
                print(response.status_code, response.content)




if page == "Page 2":
    img_file_buffer = st.file_uploader("Food image to predict your Calories", type=None, accept_multiple_files=False, key=None, help=None, on_change=None,disabled=False, label_visibility="visible")
    if img_file_buffer:
        st.image(img_file_buffer)
        # Change image to the correct size
        img = Image.open(img_file_buffer)
        img_height = int(os.environ.get('IMG_HEIGHT'))
        img_width = int(os.environ.get('IMG_WIDTH'))
    # st.write(img_width)
        img = img.resize((img_height,img_width))
        #st.write(type(img))

        # Transform img to np.array
        img_array = np.array(img)
        #st.write(img_array.shape)

        # Make a json with a list
        jayson = {"img": img_array.tolist() }

        # Post request to API
        headers = {'Content-Type': 'application/json'}
        response = requests.post("http://localhost:8000/predict", headers = headers, json=jayson)

        if response.status_code == 200:
            st.balloons()
            response_list = json.loads(response.content.decode('utf-8'))
            body_list = [item['body'] for item in response_list]

            # st.write(f"Per 100g your {body_list[0]} meal contains: {body_list[1]} calories, {body_list[2]} carbs,\
            #    {body_list[3]} fat, {body_list[4]} proteins")

            st.markdown(f"""
                            ## 🍽️ : {body_list[0]}

                            #### **Per 100g** :

                            🔥 {body_list[1]} calories

                            🥚 {body_list[4]}g proteins

                            🍞 {body_list[2]}g carbs

                            🥑 {body_list[3]}g fat

                        """)
            #st.write(response.content)
        else:
            st.markdown("**Oops**, something went wrong 😓 Please try again.")
            print(response.status_code, response.content)
if page == "Journal":

    # select = st.sidebar.selectbox('Select a State',["France"])

    # if select:

    #     progress_text = "Proteine"
    #     my_bar = st.progress(70, text=progress_text)
    from google.cloud import bigquery
    import datetime
    import streamlit as st

    userid = 1

    d = st.date_input(
        "Date",
        datetime.date(2023, 2, 18))
    st.write('Date selected:', d)

    client = bigquery.Client()

    # DAILY OBJ
    st.header("Daily")
    st.progress(80, text="🔥 Calories")
    st.progress(70, text="🥚 Protein")
    st.progress(60, text="🍞 Carbs")
    st.progress(50, text="🥑 Fat")

    # WEEKLY EVOLUTION
    st.header("Weekly")
    cal_sevendays = f"""
        SELECT Date, SUM(Calories) AS Calories
        FROM `foode-376420.foodE.macro`
        WHERE UserID = {userid} AND Date BETWEEN DATE_SUB('{d}', INTERVAL 7 DAY) AND '{d}'
        GROUP BY Date
     """


    st.write("Objectif calorique sur les 7 derniers jours")

    st.area_chart(data = client.query(cal_sevendays).to_dataframe(), x='Date') # AJOUTER UNE LIGNE OBJ

    nutri_sevendays = f"""
        SELECT Date, SUM(Protein)*20/100 AS Protein , SUM(Carbs)/100 AS Carbs , SUM(Fat)*20/100 AS Fat
        FROM `foode-376420.foodE.macro`
        WHERE UserID = {userid} AND Date BETWEEN DATE_SUB('{d}', INTERVAL 7 DAY) AND '{d}'
        GROUP BY Date
     """

    st.write("Objectif nutritionnel sur les 7 derniers jours")

    st.line_chart(data = client.query(nutri_sevendays).to_dataframe(), x='Date') # AJOUTER UNE LIGNE OBJ

    # https://docs.streamlit.io/library/api-reference/charts/st.altair_chart ?

    # DATABASE
    st.header("Database")
    query = f"""
        SELECT *
        FROM `foode-376420.foodE.macro`
        WHERE Date = '{d}' AND UserID = {userid}
     """
    st.write(query)
    results = client.query(query)
    results = results.to_dataframe()
    st.write(results)

    ## AAGRID TO EDIT? https://streamlit-aggrid.readthedocs.io/en/docs/AgGrid.html
