import streamlit as st
import streamlit.components.v1 as components  
from content_based_filtering import content_recommendation
from scipy.sparse import load_npz
import pandas as pd

# load the data
cleaned_data_path = "data/cleaned_data.csv"
songs_data = pd.read_csv(cleaned_data_path)

# load the transformed data
transformed_data_path = "data/transformed_data.npz"
transformed_data = load_npz(transformed_data_path)

# Title
st.title('Welcome to the Spotify Song Recommender!')

# Subheader
st.write('### Enter the name of a song and the recommender will suggest similar songs 🎵🎧')

# Text Input
song_name = st.text_input('Enter a song name:')
st.write('You entered:', song_name)

# artist name
artist_name = st.text_input('Enter the artist name:')
st.write('You entered:', artist_name)

# lowercase the input
song_name = song_name.lower()
artist_name = artist_name.lower()

# k recommendations
k = st.selectbox(
    'How many recommendations do you want?',
    [5, 10, 15, 20],
    index=1
)


# Button
if st.button('Get Recommendations'):

    if ((songs_data["name"] == song_name) &
        (songs_data['artist'] == artist_name)).any():

        st.write(
            'Recommendations for',
            f"**{song_name.title()}** by **{artist_name.title()}**"
        )

        recommendations = content_recommendation(
            song_name=song_name,
            artist_name=artist_name,
            songs_data=songs_data,
            transformed_data=transformed_data,
            k=k
        )


        # Display Recommendations
        for ind, recommendation in recommendations.iterrows():
            
            # Variables ka naam thoda change kiya taaki upar wale input se clash na ho
            rec_song_name = recommendation['name'].title()
            rec_artist_name = recommendation['artist'].title()

            if ind == 0:
                st.markdown("## Currently Playing")
                st.markdown(
                    f"#### **{rec_song_name}** by **{rec_artist_name}**"
                )
                st.audio(recommendation['spotify_preview_url'])
                st.write('---')

            elif ind == 1:
                st.markdown("### Next Up 🎵")
                st.markdown(
                    f"#### {ind}. **{rec_song_name}** by **{rec_artist_name}**"
                )
                st.audio(recommendation['spotify_preview_url'])
                st.write('---')

            else:
                st.markdown(
                    f"#### {ind}. **{rec_song_name}** by **{rec_artist_name}**"
                )
                st.audio(recommendation['spotify_preview_url'])
                st.write('---')
                
       

        js_code = """
        <script>
        const audios = window.parent.document.querySelectorAll('audio');
        audios.forEach(audio => {
            audio.addEventListener('play', function() {
                audios.forEach(a => {
                    if (a !== audio) a.pause();
                });
            });
        });
        </script>
        """
        components.html(js_code, height=0)

    else:
        st.write(
            f"Sorry, we couldn't find {song_name} "
            "in our database. Please try another song."
        )
