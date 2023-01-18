import streamlit as st 
import pandas as pd
import numpy as np
from PIL import Image
import time
import json
from streamlit_lottie import st_lottie
import requests
import random
from surprise import SVD
from surprise import Dataset
from surprise.model_selection import cross_validate
from surprise import Reader
from surprise.model_selection import KFold
from surprise import accuracy
from surprise.model_selection import cross_validate
from surprise import KNNWithZScore
from surprise import SVDpp
from collections import defaultdict


st.set_page_config(page_icon="🎓", page_title="Bibliobibuli")


url = 'https://drive.google.com/file/d/1oVxOIOQQ6jjKJvbCo2xxrYjeSIbW1O3e/view?usp=share_link' 
path = 'https://drive.google.com/uc?export=download&id='+url.split('/')[-2]
ratings = pd.read_csv(path)

url = 'https://drive.google.com/file/d/1Q4oXJU0pH0VxTRECaBsdg4ldAI0QTvxH/view?usp=share_link' 
path = 'https://drive.google.com/uc?export=download&id='+url.split('/')[-2]
books = pd.read_csv(path)


#audio_file = open(url_song,'rb')
#audio_byte = audio_file.read()
#st.audio(audio_byte, format='audio/ogg')

col1, col2, col3 = st.columns(3)
with col1:
    st.write('')
with col2:
    st.title(":red[_BIBLIOBIBULI_]")
with col3:
    st.write('')
    

#Lotti animation
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


Lotti = load_lottieurl('https://assets3.lottiefiles.com/packages/lf20_ad3uxjiv.json')
Page1 = load_lottieurl('https://assets3.lottiefiles.com/packages/lf20_1a8dx7zj.json')
Page2 = load_lottieurl('https://assets3.lottiefiles.com/private_files/lf30_htijkvxe.json')
Page3 = load_lottieurl('https://assets4.lottiefiles.com/packages/lf20_kq5rGs.json')
Page4 = load_lottieurl('https://assets4.lottiefiles.com/packages/lf20_arirrjzh.json')


st.sidebar.title('🎓 Navigation')
st.sidebar.write('🔽 Welcome To The Interactive Interface 🔽')
name = st.sidebar.text_input('Please Write Your Name :')
my_sld_val = st.sidebar.slider(f'How Many Books Do You Need **:blue[{name}]**',0,20)
options = st.sidebar.radio('Pages', options = ['🏡 Home','📚 Most Read','⭐ Best Rated','👍 Your Choice','🎁 Surprise Me !'])



def Ho():
    st_lottie(Lotti, height=700, width=700, key="try")
    st.header(':blue[Welcome to our Books Platform]') 
    st.header(':blue[We hope you gonna enjoy the Experience]')
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write('')
    with col2:
        st.write('')
    with col3:
        st.write(':green[©️ Made By Oussama Lajnef ©️]')



#Books cover by Lectures
ranking= pd.DataFrame(ratings.groupby('ISBN')['Book-Rating'].mean())
ranking['views'] = pd.DataFrame(ratings.groupby('ISBN')['User-ID'].count())
ranking = ranking.loc[ranking['views']>50]
ranking.sort_values('views',ascending=False).head()
Big = pd.merge(ranking,books,how='left', on= 'ISBN')
top_lecture = Big.sort_values('views',ascending=False).head(my_sld_val)
cover1 = list(top_lecture['Image-URL-L'])

#Books data frame table by Lectures
top_lecture = top_lecture[['ISBN','Book-Title','Book-Author','Year-Of-Publication','Book-Rating','views','Publisher']]
top_lecture = top_lecture.rename(columns={'Book-Rating':'Rating',
'views':'Lectures',
'rating':'Rating',
'Book-Title':'Title',
'Book-Author':'Author',
'Year-Of-Publication':'Publication Year'})
top_lecture.set_index('Title', inplace=True)




#Books cover by Ratings
ranking= pd.DataFrame(ratings.groupby('ISBN')['Book-Rating'].mean())
ranking['views'] = pd.DataFrame(ratings.groupby('ISBN')['User-ID'].count())
ranking = ranking.loc[ranking['views']>50]
ranking.sort_values('Book-Rating',ascending=False).head()
Big = pd.merge(ranking,books,how='left', on= 'ISBN')
top_rating = Big.sort_values('Book-Rating',ascending=False).head(my_sld_val)
cover2 = list(top_rating['Image-URL-L'])

#Books data frame table by Ratings
top_rating = top_rating[['ISBN','Book-Title','Book-Author','Year-Of-Publication','Book-Rating','views','Publisher']]
top_rating = top_rating.rename(columns={'Book-Rating':'Rating',
'views':'Lectures',
'rating':'Rating',
'Book-Title':'Title',
'Book-Author':'Author',
'Year-Of-Publication':'Publication Year'})
top_rating.set_index('Title', inplace=True)


#Books by choice
Real = pd.merge(books,ratings,how='inner', on= 'ISBN')
Liane =pd.DataFrame(Real['User-ID'].value_counts())
Liane = Liane.reset_index()
Liane.columns =["User-ID", "count_User-ID"]
Liane = Liane.loc[Liane['count_User-ID']>50]
fake = pd.merge(Real,Liane, how='right', on="User-ID")
Pitem = pd.pivot_table(data=fake, values='Book-Rating', index='User-ID', columns='ISBN')
Ranking= pd.DataFrame(ratings.groupby('ISBN')['Book-Rating'].mean())
Ranking['views'] = pd.DataFrame(ratings.groupby('ISBN')['User-ID'].count())
Ranking = Ranking.loc[Ranking['views']>50]
Ranking.sort_values('views',ascending=False).head()
Big = pd.merge(Ranking,books,how='left', on= 'ISBN')
Titles1 = list(Big['Book-Title'])
Titles1.insert(0,'')

    

#Function for lectures
def Lec():
    st.subheader('Recommended by Number of Lectures')
    st_lottie(Page1, height=400, width=400, key="try")
    st.subheader(':blue[“Good books do not give up all their secrets at once.”] \n:green[**― Stephen King**]')
    my_bar = st.progress(0)
    for percent_complete in range(100):
        time.sleep(0.1)
        my_bar.progress(percent_complete + 1)
    st.success('Done!')
    st.image(cover1)
    st.table(top_lecture)


#Function for rating
def Rat():
    st.subheader('Recommended by Ratings')
    st_lottie(Page2, height=400, width=400, key="try")
    st.subheader(':blue[“There is no friend as loyal as a book.”] \n:green[**― Ernest Hemingway**]')
    my_bar = st.progress(0)
    for percent_complete in range(100):
        time.sleep(0.1)
        my_bar.progress(percent_complete + 1)
    st.success('Done!')
    st.image(cover2)
    st.table(top_rating)



    #Function for choice
def Choi():
    st.subheader('Recommended by Choice')
    st_lottie(Page3, height=400, width=400, key="try")
    st.subheader(':blue[“Books are mirrors: you only see in them what you already have inside you.”] \n:green[**― Carlos Ruiz Zafón**]')
    book_choice = st.selectbox(f'What Book Did You Read Recently :red[{name}]?',options=Titles1)
    if book_choice == '':
      st.write('Please write or chose a Book')
    else:
      code = Big.loc[Big['Book-Title']== book_choice,'ISBN'].values[0] 
      Choice_Ratings = Pitem.loc[:,code]
      Choice_Ratings[Choice_Ratings>0]
      Similar_to_choice = Pitem.corrwith(Choice_Ratings)
      Corr_choice = pd.DataFrame(Similar_to_choice, columns=['PearsonR'])
      Corr_choice.dropna(inplace=True)
      Ranking= pd.DataFrame(ratings.groupby('ISBN')['Book-Rating'].mean())
      Ranking['Lectures'] = pd.DataFrame(ratings.groupby('ISBN')['User-ID'].count())
      Corr_choice_Final = Corr_choice.join(Ranking['Lectures'])
      Corr_choice_Final.drop(code, inplace=True)
      top = Corr_choice_Final[Corr_choice_Final['Lectures']>=10]
      top = Corr_choice_Final[Corr_choice_Final['PearsonR']==1].sort_values('Lectures', ascending=False).head(my_sld_val)
      Final = pd.merge(top,books,how='left', on='ISBN')
      cover3 = list(Final['Image-URL-L'])
      st.image(cover3)
      Final = Final[['Book-Title','Book-Author','Year-Of-Publication','Lectures','Publisher']]
      Final.set_index('Book-Title', inplace=True)
      st.table(Final)



#Function for rating
def Surp():
    st.subheader('Recommended by Surprise')
    st_lottie(Page4, height=400, width=400, key="try")
    st.subheader(':blue[“Books may well be the only true magic.”] \n:green[**― Alice Hoffman**]')
    if st.button('Surprise Me !'):
      surprise_me_Book = random.choice(Titles1[1:])
      code = Big.loc[Big['Book-Title']== surprise_me_Book,'ISBN'].values[0] 
      Choice_Ratings = Pitem.loc[:,code]
      Choice_Ratings[Choice_Ratings>0]
      Similar_to_choice = Pitem.corrwith(Choice_Ratings)
      Corr_choice = pd.DataFrame(Similar_to_choice, columns=['PearsonR'])
      Corr_choice.dropna(inplace=True)
      Ranking= pd.DataFrame(ratings.groupby('ISBN')['Book-Rating'].mean())
      Ranking['Lectures'] = pd.DataFrame(ratings.groupby('ISBN')['User-ID'].count())
      Corr_choice_Final = Corr_choice.join(Ranking['Lectures'])
      Corr_choice_Final.drop(code, inplace=True)
      top = Corr_choice_Final[Corr_choice_Final['Lectures']>=10]
      top = Corr_choice_Final[Corr_choice_Final['PearsonR']==1].sort_values('Lectures', ascending=False).head(my_sld_val)
      Final = pd.merge(top,books,how='left', on='ISBN')
      cover4 = list(Final['Image-URL-L'])
      st.image(cover4)
      Final = Final[['Book-Title','Book-Author','Year-Of-Publication','Lectures','Publisher']]
      Final.set_index('Book-Title', inplace=True)
      st.table(Final)
 
   
    
    #reader= Reader()
    #data = Dataset.load_from_df(fake[['User-ID','ISBN','Book-Rating']],reader)
    #trainset = data.build_full_trainset()
    #trainset.all_users()
    #testset= trainset.build_anti_testset()
    #kf = KFold(n_splits=3)
    #svd = SVD()
    #for trainset, testset in kf.split(data):   
        #cross_validate(svd, data, measures=['RMSE', 'MAE'], cv=3, verbose=True)
    #svd.fit(trainset)
    #predictions = svd.test(testset)
    #def get_top_p(predictions, p=10):
        #top_p = defaultdict(list)
        #for uid, iid, true_r, est, _ in predictions:
            #top_p[uid].append((iid, est))
        #for uid, user_ratings in top_p.items():
            #user_ratings.sort(key=lambda x: x[1], reverse=True)
            #top_p[uid] = user_ratings[:p]
        #return top_p
    #predict_dict = get_top_p(predictions, 10)
    #df = pd.DataFrame(predict_dict.items(), columns=['User-ID', 'est_score'])
    #user_ratings = pd.DataFrame (df.est_score[user_choice], columns = ['ISBN','est_score'])
    #End = user_ratings.merge(fake, how='left', on='ISBN').drop_duplicates('ISBN', keep='first').head(my_sld_val)
    #cover4 = list(End['Image-URL-L'])
    #st.image(cover4)
    #End = End[['Book-Title','Book-Author','Year-Of-Publication','Publisher']]
    #End.set_index('Book-Title', inplace=True)
    #st.table(End)
    
        


if options == '🏡 Home':
    Ho()
elif options == '📚 Most Read':
    Lec()
elif options == '⭐ Best Rated':
    Rat()
elif options == '👍 Your Choice':
    Choi()
elif options == '🎁 Surprise Me !':
    Surp()
