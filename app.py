import streamlit as st
import streamlit.components.v1 as components  
import pandas as pd
import numpy as np
from scipy.sparse import load_npz
from numpy import load
from collaborative_filtering import collaborative_recommendation


# -------------------------------------------------------------------
# Load Required Data
# -------------------------------------------------------------------

# load the track ids
track_ids_path = "data/track_ids.npy"
track_ids = load(track_ids_path, allow_pickle=True)

# load the filtered songs data
filtered_data_path = "data/collab_filtered_data.csv"
filtered_data = pd.read_csv(filtered_data_path)

# load the interaction matrix
interaction_matrix_path = "data/interaction_matrix.npz"
interaction_matrix = load_npz(interaction_matrix_path)

# -------------------------------------------------------------------
# Streamlit App UI
# -------------------------------------------------------------------

# Title
st.title('Welcome to the Spotify Song Recommender!')

# Subheader
st.write(
    '### Enter the name of a song and the recommender '
    'will suggest similar songs 🎵🎧'
)

# Text Input
song_name = st.text_input('Enter a song name:')
st.write('You entered:', song_name)

# artist name
artist_name = st.text_input('Enter the artist name:')
st.write('You entered:', artist_name)

# lowercase the input for searching
song_name = song_name.lower()
artist_name = artist_name.lower()

# k recommendations
k = st.selectbox(
    'How many recommendations do you want?',
    [5, 10, 15, 20],
    index=1
)

st.write("---")
st.write("### Collaborative Filtering Active")

# Button
if st.button('Get Recommendations'):

    # Verify the song exists
    if (
        (filtered_data["name"] == song_name) &
        (filtered_data['artist'] == artist_name)
    ).any():

        st.write(
            'Recommendations for',
            f"**{song_name.title()}** by **{artist_name.title()}**"
        )

        # Get recommendations
        recommendations = collaborative_recommendation(
            song_name=song_name,
            artist_name=artist_name,
            track_ids=track_ids,
            songs_data=filtered_data,
            interaction_matrix=interaction_matrix,
            k=k
        )

        # Display Recommendations
        for ind, recommendation in recommendations.iterrows():

            rec_song_name = recommendation['name'].title()
            rec_artist_name = recommendation['artist'].title()

            if ind == 0:

                st.markdown("## Currently Playing")

                st.markdown(
                    f"#### **{rec_song_name}** "
                    f"by **{rec_artist_name}**"
                )

                st.audio(recommendation['spotify_preview_url'])
                st.write('---')

            elif ind == 1:

                st.markdown("### Next Up 🎵")

                st.markdown(
                    f"#### {ind}. "
                    f"**{rec_song_name}** "
                    f"by **{rec_artist_name}**"
                )

                st.audio(recommendation['spotify_preview_url'])
                st.write('---')

            else:

                st.markdown(
                    f"#### {ind}. "
                    f"**{rec_song_name}** "
                    f"by **{rec_artist_name}**"
                )

                st.audio(recommendation['spotify_preview_url'])
                st.write('---')

    else:

        st.error(
            f"Sorry, we couldn't find "
            f"'{song_name.title()}' by "
            f"'{artist_name.title()}' "
            "in our user listening history database. "
            "Please try another song."
        )


components.html(
    """
    <script>
    window.parent.document.addEventListener('play', function(e) {
        if (e.target.tagName === 'AUDIO') {
            window.parent.document.querySelectorAll('audio').forEach((audio) => {
                if (audio !== e.target) audio.pause();
            });
        }
    }, true);
    </script>
    """, 
    height=0
)
