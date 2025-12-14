#bikesharing_analysis
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import numpy as np
from babel.numbers import format_currency
sns.set(style='dark')

#MENYIAPKAN DATAFRAME
def create_daily_sharing_df(df):
    daily_sharing_df = df.resample(rule='D', on='dteday').agg({
        "cnt": "sum",
        "casual": "sum",
        "registered": "sum"
    })
    daily_sharing_df = daily_sharing_df.reset_index()
    
    return daily_sharing_df

def create_total_sharing_bike_df(df):
    total_sharing_bike_df = df.groupby("hr").cnt.sum().sort_values(ascending=False).reset_index()

    return total_sharing_bike_df

def create_byday_df(df):
    byday_df = df.groupby(by="weekday").cnt.sum().reset_index()
    byday_df.rename(columns={
        "cnt": "count",
    }, inplace=True)
    byday_df['weekday'] = pd.Categorical(byday_df['weekday'].map({0: 'Minggu',1: 'Senin', 2: 'Selasa', 3: 'Rabu', 4: 'Kamis', 5: 'Jumat', 6: 'Sabtu'}), ordered=True)

    return byday_df

def create_byhour_df(df):
    byhour_df = df.groupby(by="hr").cnt.sum().reset_index()
    byhour_df.rename(columns={
        "cnt": "count"
    }, inplace=True)

    return byhour_df

def create_byyear_df(df):
    byyear_df = df.groupby(by="yr").cnt.sum().reset_index()
    byyear_df.rename(columns={
        "cnt": "count"
    }, inplace=True)

    byyear_df['yr'] = pd.Categorical(byyear_df['yr'].map({0: 'Tahun 2011', 1: 'Tahun 2012'}), ordered=True)

    return byyear_df

def create_by_season_df(df):
    byseason_df = df.groupby(by="season").cnt.sum().reset_index()
    byseason_df.rename(columns={
        "cnt": "count"
    }, inplace=True)

    byseason_df['season'] = pd.Categorical(byseason_df['season'].map({1: 'Musim Semi',2: 'Musim Panas', 3: 'Musim Gugur', 4: 'Musim Dingin'}), ordered=True)

    return byseason_df

def create_by_weather_df(df):
    byweather_df = df.groupby(by="weathersit").cnt.sum().reset_index()
    byweather_df.rename(columns={
        "cnt": "count"
    }, inplace=True)

    byweather_df['weathersit'] = pd.Categorical(byweather_df['weathersit'].map({1: 'Cerah',2: 'Kabut', 3: 'Salju Ringan', 4: 'Hujan Lebat'}), ordered=True)

    return byweather_df

def create_workingday_df(df):
    byworkingday_df = df.groupby(by="workingday").cnt.sum().reset_index()
    byworkingday_df.rename(columns={
        "cnt": "count"
    }, inplace=True)

    byworkingday_df['workingday'] = pd.Categorical(byworkingday_df['workingday'].map({0: 'Weekend/Holiday', 1: 'Bukan Weekend/Holiday'}), ordered=True)

    return byworkingday_df

def create_bytemp_df(df):
    bytemp_df = df.groupby(by="dteday").agg({"temp":"mean"})
    return bytemp_df

def create_bywindspeed_df(df):
    bywindspeed_df = df.groupby(by="dteday").agg({"windspeed":"mean"})
    return bywindspeed_df

def create_rfm_df(df):
    rfm_df = df.groupby(by="instant", as_index=False).agg({
    "dteday": ["max","nunique"], #mengambil tanggal order terakhir
    "cnt": "sum"
    })
    rfm_df.columns = ["instant", "max_order_timestamp", "frequency", "monetary"]
    
    rfm_df["max_order_timestamp"] = rfm_df["max_order_timestamp"].dt.date
    recent_date = df["dteday"].dt.date.max()
    rfm_df["recency"] = rfm_df["max_order_timestamp"].apply(lambda x: (recent_date - x).days)
    rfm_df.drop("max_order_timestamp", axis=1, inplace=True)
    
    return rfm_df

def create_user_segment_df(df):
    rfm_df = df.groupby(by="instant", as_index=False).agg({
    "dteday": ["max","nunique"], #mengambil tanggal order terakhir
    "cnt": "sum"
    })
    rfm_df.columns = ["instant", "max_order_timestamp", "frequency", "monetary"]
    
    rfm_df["max_order_timestamp"] = rfm_df["max_order_timestamp"].dt.date
    recent_date = df["dteday"].dt.date.max()
    rfm_df["recency"] = rfm_df["max_order_timestamp"].apply(lambda x: (recent_date - x).days)
    rfm_df.drop("max_order_timestamp", axis=1, inplace=True)

    rfm_df['r_rank'] = rfm_df['recency'].rank(ascending=False)
    rfm_df['f_rank'] = rfm_df['frequency'].rank(ascending=True)
    rfm_df['m_rank'] = rfm_df['monetary'].rank(ascending=True)

    # normalizing the rank of the customers
    rfm_df['r_rank_norm'] = (rfm_df['r_rank']/rfm_df['r_rank'].max())*100
    rfm_df['f_rank_norm'] = (rfm_df['f_rank']/rfm_df['f_rank'].max())*100
    rfm_df['m_rank_norm'] = (rfm_df['m_rank']/rfm_df['m_rank'].max())*100

    rfm_df['RFM_score'] = 0.15*rfm_df['r_rank_norm']+0.28 * \
    rfm_df['f_rank_norm']+0.57*rfm_df['m_rank_norm']
    rfm_df['RFM_score'] *= 0.05
    rfm_df = rfm_df.round(2)

    rfm_df["user_segment"] = np.where(
        rfm_df['RFM_score'] > 4.5, "Top user", (np.where(
            rfm_df['RFM_score'] > 4, "High value user",(np.where(
                rfm_df['RFM_score'] > 3, "Medium value user", np.where(
                    rfm_df['RFM_score'] > 1.6, 'Low value user', 'lost user'))))))


    user_segment_df = rfm_df.groupby(by="user_segment", as_index=False).instant.nunique()
    user_segment_df['user_segment'] = pd.Categorical(user_segment_df['user_segment'], [
    "lost user", "Low value user", "Medium value user",
    "High value user", "Top user"])

    return user_segment_df


day_df = pd.read_csv("data/data_day.csv")
hour_df = pd.read_csv("data/data_hours.csv")

day_df["dteday"] = pd.to_datetime(day_df["dteday"])
hour_df["dteday"] = pd.to_datetime(hour_df["dteday"])

min_date = hour_df["dteday"].min()
max_date = hour_df["dteday"].max()

with st.sidebar:
    st.image("https://raw.githubusercontent.com/andizabrina21/bike_sharing_db/main/images/bikepic.jpg", caption="Pic From Google")
    ':bike:'':bike:'':bike:'':bike:'':bike:'':bike:'':bike:'':bike:'':bike:'':bike:'':bike:'':bike:'':bike:'
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = hour_df[(hour_df["dteday"] >= str(start_date)) & 
                (hour_df["dteday"] <= str(end_date))]

daily_sharing_df = create_daily_sharing_df(main_df)
bytemp_df = create_bytemp_df(main_df)
bywindspeed_df = create_bywindspeed_df(main_df)
total_sharing_bike_df = create_total_sharing_bike_df(main_df)
byday_df = create_byday_df(main_df)
byhour_df = create_byhour_df(main_df)
byyear_df = create_byyear_df(main_df)
byseason_df = create_by_season_df(main_df)
byweather_df = create_by_weather_df(main_df)
byworkingday_df = create_workingday_df(main_df)
rfm_df = create_rfm_df(main_df)
user_segment_df = create_user_segment_df(main_df)

with st.sidebar:
    col1, col2 = st.columns(2)
    with col1:
        rounded_mean_temp = round(bytemp_df['temp'].mean(), 2)
        st.metric(label="Avg Temperature", value=f"{rounded_mean_temp}°C")
    with col2:
        rounded_mean_wind = round(bywindspeed_df['windspeed'].mean(), 2)
        st.metric(label="Avg Windspeed", value=f"{rounded_mean_wind}knot")
    st.caption('The values of temp are divided to 41 (max) and the values of windspeed are divided to 67 (max)')

#MELENGKAPI DASHBOARD DGN VISUALISASI DATA
st.header('Bike Sharing Dashboard :bike:')

st.subheader('Daily Sharing')

col1, col2, col3 = st.columns(3)

with col1:
    total_sharing = daily_sharing_df.cnt.sum()
    st.metric("Total Sharing", value=total_sharing)

with col2:
    total_casual = daily_sharing_df.casual.sum()
    st.metric("Total Casual", value=total_casual)

with col3:
    total_registered = daily_sharing_df.registered.sum()
    st.metric("Total Registered", value=total_registered)

with st.expander("See explanation"):
    st.write(
        "Total Sharing merupakan total pengguna bike-sharing."
    )
    st.write(
        "Total Casual merupakan total pengguna biasa bike-sharing."
    )
    st.write(
        "Total Registered merupakan total pengguna terdaftar bike-sharing"
    )

st.subheader("Waktu Paling Ramai dan Sepi Pengguna Bike Sharing")
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(24, 6))

#colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

sns.barplot(x="cnt", y="hr", data=total_sharing_bike_df, order=total_sharing_bike_df.sort_values(by="cnt", ascending=False).hr.head(5), palette="crest", ax=ax[0], orient="y")
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title("Waktu Paling Ramai", loc="center", fontsize=18)

sns.barplot(x="cnt", y="hr", data=total_sharing_bike_df, order=total_sharing_bike_df.sort_values(by="cnt", ascending=True).hr.head(5), palette="crest", ax=ax[1], orient="y")
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Waktu Paling Sepi", loc="center", fontsize=18)

st.pyplot(fig)

st.subheader("Tren Jumlah Pengguna Bike-Sharing Per-Hari dan Per-Jam")
col1, col2 = st.columns(2)
with col1:
    fig, ax = plt.subplots(figsize=(20, 10))
    ax.plot(
        byday_df["weekday"],
        byday_df["count"],
        marker='o',
        markersize=10,
        linewidth=5,
        color="#72BCD4",
    )
    ax.set_title("Tren Jumlah Pengguna Per-Hari", loc="center", fontsize=25)
    ax.set_ylabel("Jumlah Pengguna", fontsize=20)
    ax.tick_params(axis='y', labelsize=20)
    ax.tick_params(axis='x', labelsize=20)
    st.pyplot(fig)

with col2:
    fig, ax = plt.subplots(figsize=(20, 10))
    plt.plot(
        byhour_df['hr'],
        byhour_df["count"],
        marker='o',
        markersize=10,
        linewidth=5,
        color="#72BCD4",
    )
    plt.title("Tren Jumlah Pengguna Per-Jam")
    plt.ylabel("Jumlah Pengguna", fontsize=20)

    plt.xticks(range(24), labels=[f"{i:02d}:00" for i in range(24)], rotation=45)
    plt.tight_layout()
    st.pyplot(fig)

st.subheader("Jumlah Pengguna Bike-Sharing Per-Tahun")
fig, ax = plt.subplots(figsize=(10, 5))
colors = ["#72BCD4","#D3D3D3"]
sns.barplot(
    y="count",
    x="yr",
    data=byyear_df,
    order=byyear_df.sort_values(by="count", ascending=False).yr,
    palette=colors
)
ax.set_ylabel("Jumlah Pengguna")
ax.tick_params(labelsize=12)
st.pyplot(fig)

st.subheader("Pengaruh Musim dan Cuaca Terhadap Jumlah Pengguna Bike-Sharing")
col1, col2 = st.columns(2)
with col1:
    fig, ax = plt.subplots(figsize=(10, 5))
    colors=["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
    sns.barplot(
        y="count",
        x="season",
        data = byseason_df,
        order = byseason_df.sort_values(by="count", ascending=False).season,
        palette=colors,
        ax=ax
    )
    ax.set_ylabel("Jumlah Pengguna")
    ax.tick_params(labelsize=12)
    st.pyplot(fig)

with col2:
    fig, ax = plt.subplots(figsize=(10, 5))
    colors=["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
    sns.barplot(
        y="count",
        x="weathersit",
        data = byweather_df, 
        order = byweather_df.sort_values(by="count", ascending=False).weathersit,
        palette=colors,
        ax=ax
    )
    ax.set_ylabel("Jumlah Pengguna")
    ax.tick_params(labelsize=12)
    st.pyplot(fig)

st.subheader("Pengaruh Weekend/Holiday Terhadap Jumlah Pengguna Bike-Sharing")
fig, ax = plt.subplots(figsize=(10, 5))
colors = ["#72BCD4", "#D3D3D3"]
sns.barplot(
    y="count",
    x="workingday",
    data=byworkingday_df,
    order=byworkingday_df.sort_values(by="count", ascending=False).workingday,
    palette=colors,
    ax=ax
)
#ax.set_title("Jumlah Penyewa Sepeda Setiap Musim", loc="center", fontsize=15)
ax.set_ylabel("Jumlah Pengguna")
ax.tick_params(labelsize=12)
st.pyplot(fig)

st.subheader("Pengguna Terbaik Berdasarkan Parameter RFM")
col1, col2, col3 = st.columns(3)
with col1:
    avg_recency = round(rfm_df.recency.mean(), 1)
    st.metric("Average Recency (hours)", value=avg_recency)
 
with col2:
    avg_frequency = round(rfm_df.frequency.mean(), 2)
    st.metric("Average Frequency", value=avg_frequency)
 
with col3:
    avg_frequency = round(rfm_df.monetary.mean(),3) 
    st.metric("Average Monetary", value=avg_frequency)

fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(30, 6))

colors = ["#72BCD4", "#72BCD4", "#72BCD4", "#72BCD4", "#72BCD4"]

sns.barplot(y="recency", x="instant", data=rfm_df.sort_values(by="recency", ascending=True).head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title("By Recency (hours)", loc="center", fontsize=18)
ax[0].tick_params(axis ='x', labelsize=15)

sns.barplot(y="frequency", x="instant", data=rfm_df.sort_values(by="frequency", ascending=False).head(5), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].set_title("By Frequency", loc="center", fontsize=18)
ax[1].tick_params(axis='x', labelsize=15)

sns.barplot(y="monetary", x="instant", data=rfm_df.sort_values(by="monetary", ascending=False).head(5), palette=colors, ax=ax[2])
ax[2].set_ylabel(None)
ax[2].set_xlabel(None)
ax[2].set_title("By Monetary", loc="center", fontsize=18)
ax[2].tick_params(axis='x', labelsize=15)
 
st.pyplot(fig)

st.subheader("Jumlah Pengguna Pada Setiap Segmentasi Pengguna Berdasarkan RFM SCORE")
fig, ax = plt.subplots(figsize=(10, 5))
colors_ = ["#72BCD4", "#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

sns.barplot(
    x="instant",
    y="user_segment",
    data=user_segment_df,
    order=user_segment_df.sort_values(by="user_segment", ascending=False).user_segment,
    palette=colors_
)
ax.set_title("Number of User for Each Segment", loc="center", fontsize=15)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='y', labelsize=12)
st.pyplot(fig)
