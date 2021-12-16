'''
Aplikasi Analisis Statistik Minyak Mentah 

Data diperoleh melalui CSV dan JSON
Referensi API Streamlit: https://docs.streamlit.io/library/api-reference
'''

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import json
from matplotlib import cm

############### title ###############
st.set_page_config(layout="wide")  # this needs to be the first Streamlit command called
st.title("Statistik Jumlah Penumpang TransJakarta Tahun 2019")
st.markdown("*Sumber data berasal dari [Jakarta Open Data](https://data.jakarta.go.id/dataset/data-jumlah-penumpang-trans-jakarta-tahun-2019-kpi)*")
############### title ###############)

with open ("kode_negara_lengkap.json") as f:
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
        return kode_negara

#No 1 Grafik Produksi Minyak Negara N
negara = 'AUS' #selectbox sidebar
tahun = range(1970,2015)
bar_data = df[(df.tahun == tahun) & (df.kode_negara == negara)]
x = df[df['kode_negara']==negara].tahun
y = df[df['kode_negara']==negara].produksi

fig1,ax1 = plt.subplots()
ax1.set_xlabel("Tahun")
ax1.set_ylabel("Jumlah Produksi")
ax1.bar(x,y)        

#No 2 B besar Negara pada Tahun T
Bbesar = 10 #slider
year = 2015 #slider pisan

promax = df[df.tahun == year].produksi.sort_values(ascending=False)[:Bbesar].values
fig2,ax2 = plt.subplots()

for prod in promax:
    kode_max = df[(df.tahun == year) & (df.produksi == prod)].kode_negara.item()
    nama_max = nama_negara(kode_max)
    ax2.barh(nama_max, prod)

plt.title(f"Top {Bbesar} negara produksi terbesar pada tahun {year}")
plt.show()
#no 3 B-Besar Negara dengan Produksi Terbesar Kumulatif
Bbesar = 12 #slider

x = df.groupby(['kode_negara']).sum().sort_values(by='produksi', ascending = False).produksi[:Bbesar].index
y = df.groupby(['kode_negara']).sum().sort_values(by='produksi', ascending = False).produksi[:Bbesar]

fig3,ax3 = plt.subplots()
ax3.bar(x,y)