


from pathlib import Path
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from api import *
import seaborn as sns
from matplotlib.pyplot import pie, axis, show
import plotly.express as px
from PIL import Image
import requests
import json
 
st.image("t.png")
db = Dbconnect()
req = f'select * from librarydb.library'
db.dbcursor.execute(req)
results = db.dbcursor.fetchall()
columns = ["id","titles","notations","prices","availability"]
df = pd.DataFrame(results,columns=columns)
df["titles"]=df["titles"].astype(str)
df["notations"]=df["notations"].astype(str)
df["availability"]=df["availability"].astype(str)
df.set_index("id",inplace = True)
# df
# st.write(df.dtypes)
# db.close_db()


def main():
    st.title("mon premier streamlit")
    if st.button('Say hello'):
          st.write('Why hello there')
    else:
          st.write('Goodbye')
    menu = ["Read","insert","update","Delete","view","about"]
    choice = st.sidebar.selectbox("Menu",menu)
   
    if choice == "Read":
          # aff = df.to_string(index=False)
          if st.checkbox('Show raw data'):
               st.subheader('Raw data')
               load_state = st.text('Loading Data..')
               st.write(df)
               load_state.text('Loading Completed!')
          valuet = st.text_input("Search this value")
          search_choice= st.radio("Field to search by",df.columns)
          if st.button("Search"):
               if search_choice == "titles":
                    df[df["titles"]==valuet]
               elif search_choice == "notations":
                    df[df["notations"]==valuet]
               elif search_choice == "prices":
                    df[df["prices"]==valuet]
               elif search_choice == "availability":
                    df[df["availability"]==valuet]
                    
    elif choice == "insert":
         with st.form("my_form"):
               title = st.text_input('Movie title')
               notations = st.text_input('notations title')
               prices = st.text_input('prices title')
               stock = st.text_input(' availability')
               submit = st.form_submit_button("INSERT")
               def insertPage():
                    st.title("Add Book")
                    di = {"id": 1000,"titles":title,"notations":notations,"prices":prices,"availability":stock}
                    if submit:
                         requests.post("http://127.0.0.1:5000/record/{_id}",json=di)
                         st.write('lid est bien ajoute')
         st.session_state.runpage = insertPage()

     
    elif choice == "update":
         valuet = st.text_input("Search this value")
         search_choice= st.radio("Field to search by",df.columns)
         if st.button("Search"):
               if search_choice == "titles":
                    df[df["titles"]==valuet]
                    res = df[df["titles"]==valuet]#.to_dict('records')[0]
               elif search_choice == "notations":
                    df[df["notations"]==valuet]
                    res = df[df["notations"]==valuet]#.to_dict('records')[0]
               elif search_choice == "prices":
                    df[df["prices"]==valuet]
                    res = df[df["prices"]==valuet]#.to_dict('records')[0]
               elif search_choice == "availability":
                    df[df["availability"]==valuet]
                    res = df[df["availability"]==valuet]#.to_dict('records')[0]

               def updatePage():
                    st.title("update Book")
                    dii = {"id": _id,"titles":title_d,"notations":notations_d,"prices":prices_d,"availability":stock_d}
                    requests.put(f"http://127.0.0.1:5000/record/{_id}",json=dii)
                    st.write('librairie est mis a jour')

               with st.form("my_form1"):
                    # st.help(st.text_input('Movie title', res["titles"].values))
                    _id = st.text_input('ID title', res.index.values[0])
                    title_d = st.text_input('Movie title', res["titles"].values.astype(str)[0])
                    notations_d = st.text_input('Notations title', res["notations"].values.astype(str)[0])
                    prices_d = st.text_input('Prices title', res["prices"].values[0])
                    stock_d = st.text_input(' Availability', res["availability"].values.astype(str)[0])
                    update = st.form_submit_button("Update")
                    # res=res.astype(str)
                    # st.text(res.dtypes) 
                    #Steamlit changes strings to objects because of a bug in this version
                    if update:
                         updatePage()
               
               
     #     st.session_state.runpage = updatePage()
    elif choice == "Delete":
        st.session_state.runpage = DeletePage()
    elif choice == "view":
          fig = plt.figure(figsize=(20,10))
          sums = df.groupby("notations").sum()["prices"]
          axis('equal');
          pie(sums, labels=sums.index,autopct = "%1f%%" );
          fig = plt.gcf()
          fig.set_size_inches(30,12)
          sns.set(font_scale = 2)
          st.write(fig)
          st.subheader("view Items")
          st.write(fig)

         # Bar chart to show the Top 10 Crimes using plotly
          st.subheader(" Top 10 Crimes ")
          grp_data = df.copy()
          grp_data['PRICE'] = 1
          k = pd.DataFrame(grp_data.groupby(['notations'], sort=False)['prices'].count().rename_axis(["Type of book"]).nlargest(10))
          Crime = pd.Series(k.index[:])
          Count = list(k['prices'][:])
          Crime_Count = pd.DataFrame(list(zip(Crime, Count)),
                                        columns=['notation', 'price'])
          fig = px.bar(Crime_Count, x='notation', y='price', color='price',
                         labels={'book': 'book notation', 'Count': 'book price'})
          st.plotly_chart(fig)

          fig, ax = plt.subplots()
          df.hist(
                    bins=8,
                    column="prices",
                    grid=False,
                    figsize=(8, 8),
                    color="#86bf91",
                    zorder=2,
                    rwidth=0.9,
                    ax=ax,
                    )
          st.write(fig)
    else:
        #st.subheader("about")
        ab= HelloWorld.apropos(HelloWorld)
        ab



def DeletePage():
     st.title("Add Book")
     id = st.text_input("L'id du la tuple que tu veux supprimer") 
     if st.button("Delete ce tuple"):
          HelloWorld.delete(HelloWorld, id)
          # requests.delete()
          st.write('lid est bien suprimer')

          
if __name__ == '__main__':
    main()


