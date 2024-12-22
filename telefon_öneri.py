import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors
import tkinter as tk
from tkinter import ttk, messagebox

# Veri Yükleme
dosya_yolu = 'C:/Users/aygun/Desktop/telefon_öneri_sistemi/phones_data.csv'
df = pd.read_csv(dosya_yolu)

# Gerekli sütunları seç
df = df[['brand_name', 'model_name', 'os', 'popularity', 'best_price', 'screen_size', 'sellers_amount']]
df.dropna(inplace=True)

# Özellik Seçimi ve Standardizasyon
#Fiyat verileri StandardScaler kullanılarak ölçeklendirilir.sıfır ortalama ve birim standart sapmaya uyarlanır (z-skor standardizasyonu).
X = df[['best_price']].values
olcekleyici = StandardScaler()
X_olcekli = olcekleyici.fit_transform(X)

# Model Eğitimi (KNN) mesafe için öklid yöntemini seçtim
knn = NearestNeighbors(n_neighbors=10, metric='euclidean')
knn.fit(X_olcekli)


# Arayüz Tasarımı
def telefon_oner():
    try:
        butce = float(giris_butce.get())
        butce_olcekli = olcekleyici.transform([[butce]])
        mesafeler, indeksler = knn.kneighbors(butce_olcekli)

        # Önerilen Telefonlar
        onerilen_telefonlar = []
        for idx in indeksler[0]:
            telefon = df.iloc[idx]
            onerilen_telefonlar.append(telefon)

        onerilen_telefonlar = sorted(onerilen_telefonlar, key=lambda x: x['popularity'], reverse=True)

        # Sonuçları Gösterme
        for item in agac.get_children():
            agac.delete(item)
        for telefon in onerilen_telefonlar:
            agac.insert('', 'end', values=(telefon['brand_name'], telefon['model_name'], telefon['best_price'],
                                           telefon['popularity'], telefon['screen_size'], telefon['sellers_amount']))
    except ValueError:
        messagebox.showerror("Hata", "Lütfen geçerli bir bütçe girin.")


pencere = tk.Tk()
pencere.title("Telefon Öneri Sistemi")

# Bütçe Girişi
cerceve = tk.Frame(pencere)
cerceve.pack(pady=10)
tk.Label(cerceve, text="Telefon için bütçenizi girin:").pack(side=tk.LEFT)
giris_butce = tk.Entry(cerceve)
giris_butce.pack(side=tk.LEFT, padx=5)
tk.Button(cerceve, text="Önerileri Göster", command=telefon_oner).pack(side=tk.LEFT)

# Sonuç Tablosu
sutunlar = ('brand_name', 'model_name', 'best_price', 'popularity', 'screen_size', 'sellers_amount')
agac = ttk.Treeview(pencere, columns=sutunlar, show='headings')
agac.heading('brand_name', text='Marka')
agac.heading('model_name', text='Model')
agac.heading('best_price', text='Fiyat')
agac.heading('popularity', text='Popülerlik')
agac.heading('screen_size', text='Ekran (inç)')
agac.heading('sellers_amount', text='Satıcı Sayısı')
agac.pack(pady=20)

pencere.mainloop()
