import streamlit as st
import pandas as pd
import numpy as np
from scipy.sparse import load_npz
from numpy import load
from sklearn.metrics.pairwise import cosine_similarity

# -------------------------------------------------------------------
# Collaborative Filtering Logic
# -------------------------------------------------------------------
def collaborative_recommendation(song_name, artist_name, track_ids, songs_data, interaction_matrix, k=5):
    # lowercase the song name
    song_name = song_name.lower()
    
    # lowercase the artist name
    artist_name = artist_name.lower()
    
    # fetch the row from songs data
    song_row = songs_data.loc[(songs_data["name"] == song_name) & (songs_data["artist"] == artist_name)]
    
    # track_id of input song
    input_track_id = song_row['track_id'].values.item()
   
    # index value of track_id
    ind = np.where(track_ids == input_track_id)[0].item()
    
    # fetch the input vector
    input_array = interaction_matrix[ind]
    
    # get similarity scores
    similarity_scores = cosine_similarity(input_array, interaction_matrix)
    
    # index values of recommendations
    recommendation_indices = np.argsort(similarity_scores.ravel())[-k-1:][::-1]
    
    # get top k recommendations
    recommendation_track_ids = track_ids[recommendation_indices]
    
    # get top scores
    top_scores = np.sort(similarity_scores.ravel())[-k-1:][::-1]
    
    # get the songs from data and print
    scores_df = pd.DataFrame({"track_id":recommendation_track_ids.tolist(),
                            "score":top_scores})
    
    top_k_songs = (
                songs_data
                .loc[songs_data["track_id"].isin(recommendation_track_ids)]
                .merge(scores_df,on="track_id")
                .sort_values(by="score",ascending=False)
                .drop(columns=["track_id","score"])
                .reset_index(drop=True)
                )
    
    return top_k_songs

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
st.write('### Enter the name of a song and the recommender will suggest similar songs 🎵🎧')

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
k = st.selectbox('How many recommendations do you want?', [5,10,15,20], index=1)

st.write("---")
st.write("### Collaborative Filtering Active")

# Button
if st.button('Get Recommendations'):
    # Verify the song exists in our collaborative filtering dataset
    if ((filtered_data["name"] == song_name) & (filtered_data['artist'] == artist_name)).any():
        st.write('Recommendations for', f"**{song_name.title()}** by **{artist_name.title()}**")
        
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
                st.markdown(f"#### **{rec_song_name}** by **{rec_artist_name}**")
                st.audio(recommendation['spotify_preview_url'])
                st.write('---')
            elif ind == 1:   
                st.markdown("### Next Up 🎵")
                st.markdown(f"#### {ind}. **{rec_song_name}** by **{rec_artist_name}**")
                st.audio(recommendation['spotify_preview_url'])
                st.write('---')
            else:
                st.markdown(f"#### {ind}. **{rec_song_name}** by **{rec_artist_name}**")
                st.audio(recommendation['spotify_preview_url'])
                st.write('---')
    else:
        st.error(f"Sorry, we couldn't find '{song_name.title()}' by '{artist_name.title()}' in our user listening history database. Please try another song.")
