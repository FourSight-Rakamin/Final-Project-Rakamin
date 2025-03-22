import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data hasil clustering
df = pd.read_excel("Hasil Clustering KMeans.xlsx")  # Pastikan file ini adalah hasil dari K-Means

# Streamlit UI
st.title("🏡 Airbnb Recommendation System")
st.subheader("Find your perfect Airbnb property based on your preferences!")

col1, col2, col3 = st.columns([1, 2, 1])  # Membuat 3 kolom, kolom tengah lebih besar
with col2:  # Menempatkan gambar di kolom tengah
    st.image("Logo Kelompok Foursight .jpg", caption="Createrd by : Foursight", width=200)


# Checkbox untuk menampilkan data mentah
if st.checkbox("Show raw data"):
    st.write(df.head())

# Mapping angka cluster ke nama unik
cluster_names = {
    0: "🏠 Budget Stay",         # Properti ekonomis, harga murah
    1: "🏡 Comfort Living",      # Properti harga menengah, nyaman
    2: "🌟 Luxury Retreat",      # Properti mewah dengan fasilitas lengkap
    3: "🌍 Traveler’s Choice"    # Properti populer dengan rating tinggi
}

# Ganti angka cluster dengan nama
df["cluster_name"] = df["cluster"].map(cluster_names)

# Dropdown untuk memilih cluster tertentu
cluster_option = st.selectbox("Select Cluster", sorted(df["cluster_name"].unique()))

# Membuat 4 kolom untuk filter agar tampilan lebih rapi
col1, col2, col3, col4 = st.columns(4)

# Pastikan kolom 'price' dalam format numerik
df["price"] = df["price"].astype(str)  # Pastikan semua dalam bentuk string
df["price"] = df["price"].str.replace("[$,]", "", regex=True)  # Hapus simbol $ dan koma
df["price"] = pd.to_numeric(df["price"])  # Konversi ke numerik

# Input filter dalam kolom masing-masing
with col1:
    price_range = st.slider("Price Range", int(df["price"].min()), int(df["price"].max()), (50, 200))

with col2:
    rating_range = st.slider("Review Scores", int(df["review_scores_rating"].min()), 
                             int(df["review_scores_rating"].max()), (80, 100))

with col3:
    num_bedrooms = st.number_input("Min Bedrooms", min_value=0, max_value=int(df["bedrooms"].max()), value=1, step=1)

with col4:
    num_bathrooms = st.number_input("Min Bathrooms", min_value=0, max_value=int(df["bathrooms"].max()), value=1, step=1)


# Filter data berdasarkan input pengguna
filtered_df = df[(df["cluster_name"] == cluster_option) & 
                 (df["price"] >= price_range[0]) & (df["price"] <= price_range[1]) &
                 (df["review_scores_rating"] >= rating_range[0]) & (df["review_scores_rating"] <= rating_range[1]) &
                 (df["bedrooms"] >= num_bedrooms) &
                 (df["bathrooms"] >= num_bathrooms)]

cols = st.columns(3)  # Buat 3 kolom sejajar

for index, row in filtered_df.iterrows():
    with cols[index % 3]:  # Memasukkan gambar ke dalam kolom secara bergantian
        st.image(row["picture_url"], caption=row["name"], width=100)
        st.write(f"💰 ${row['price']}")

st.write(f"Showing {len(filtered_df)} properties matching your criteria:")
st.write(filtered_df[["name","room_type", "price","picture_url", "review_scores_rating", "bedrooms", "bathrooms", "listing_url"]])



# Scatter plot Harga vs. Rating dengan warna berdasarkan cluster
st.subheader("📊 Price vs. Review Scores Rating (Clustered)")
fig, ax = plt.subplots(figsize=(8,6))
sns.scatterplot(x=df["price"], y=df["review_scores_rating"], hue=df["cluster_name"], palette="coolwarm", ax=ax)
ax.set_xlabel("Price")
ax.set_ylabel("Review Scores Rating")
st.pyplot(fig)

# Pie Chart distribusi tipe kamar dalam cluster yang dipilih
st.subheader("🏠 Room Type Distribution in Selected Cluster")
fig, ax = plt.subplots()
filtered_df["room_type"].value_counts().plot.pie(autopct="%1.1f%%", startangle=140, cmap="coolwarm", ax=ax)
st.pyplot(fig)

