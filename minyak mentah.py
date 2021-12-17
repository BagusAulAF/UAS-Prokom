'''
Aplikasi Analisis Statistik Minyak Mentah 

Data diperoleh melalui CSV dan JSON
Referensi API Streamlit: https://docs.streamlit.io/library/api-reference
'''
import numpy as np
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import json

st.cache()
##Bagus Aulia Ahmad Fahrezi
##NIM: 12220108
############### title ###############
st.set_page_config(layout="wide")  # this needs to be the first Streamlit command called
st.title("Statistik Produksi Minyak Mentah Dunia")
st.markdown("*Sumber data berasal dari file CSV dan JSON yang telah saya unggah pada GitHub")
############### title ###############)

with open ('kode_negara_lengkap.json') as f:
    data_json = json.load(f)

df = pd.read_csv('produksi_minyak_mentah.csv')

daftar_negara = df.kode_negara.unique()
dict_negara = dict()
for name in data_json:
    if name['alpha-3'] in daftar_negara:
        dict_negara.update({name['alpha-3']:name['name']})

def nama_negara(kode_negara):
    if kode_negara in dict_negara:
        return dict_negara[kode_negara]
    else:
        return ("N/A")
## Sidebar
st.sidebar.subheader("Pengaturan konfigurasi tampilan")
list_negara = df.kode_negara.unique()
pilih_negara = st.sidebar.selectbox("Pilih negara", list_negara)

Bbesar = st.sidebar.number_input("Jumlah baris dalam tabel yang ditampilkan", min_value=1, max_value=None, value=10)

tahun = st.sidebar.slider("Pilih tahun", min_value=1970,max_value=2015,value=None)

############### sidebar ###############


#No 1 Grafik Produksi Minyak Negara N
st.subheader("Grafik Produksi Minyak Suatu Negara")
bar_data = df[(df.tahun == tahun) & (df.kode_negara == pilih_negara)]
x = df[df['kode_negara']==pilih_negara].tahun
y = df[df['kode_negara']==pilih_negara].produksi

fig1,ax1 = plt.subplots()
ax1.set_xlabel("Tahun")
ax1.set_ylabel("Jumlah Produksi")
ax1.bar(x,y)

plt.title(f'Grafik Produksi {nama_negara(pilih_negara)} dari Tahun ke Tahun')
st.pyplot(fig1)        

#No 2 B besar Negara pada Tahun T
st.subheader('Diagram Negara dengan Produksi Terbesar')
promax = df[df.tahun == tahun].produksi.sort_values(ascending=False)[:Bbesar].values
fig2,ax2 = plt.subplots()

for prod in promax:
    kode_max = df[(df.tahun == tahun) & (df.produksi == prod)].kode_negara.item()
    nama_max = nama_negara(kode_max)
    ax2.barh(nama_max, prod)

plt.title(f"Top {Bbesar} negara produksi terbesar pada tahun {tahun}")
st.pyplot(fig2)

#no 3 B-Besar Negara dengan Produksi Terbesar Kumulatif
st.subheader("Negara Produksi Terbesar Kumulatif")

x = df.groupby(['kode_negara']).sum().sort_values(by='produksi', ascending = False).produksi[:Bbesar].index
y = df.groupby(['kode_negara']).sum().sort_values(by='produksi', ascending = False).produksi[:Bbesar]

fig3,ax3 = plt.subplots()
ax3.bar(x,y)
st.pyplot(fig3)