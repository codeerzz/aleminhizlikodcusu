# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 18:17:55 2020

@author: yAquila
"""

import twint
import telepot
bot = telepot.Bot("946004533:AAHnEullMC2g_ZuGa7Az1YFakE9-b5rHuFs")
guncelleme = bot.getUpdates()
##print(guncelleme[0])
marmara_chat_id = "@marmara_bolgesi_deprem_bilgi"
ege_chat_id = "@ege_bolgesi_deprem_bilgi"
dogu_anadolu_chat_id = "@dogu_anadolu_deprem_bilgi"
karadeniz_chat_id = "@karadeniz_deprem_bilgi"

##bot.sendMessage(chat_id,"ben depremmbot")

import re
import pandas as pd
import datetime
import time


bolgeler_dict = {"Marmara" : "Marmara, Yunanistan, Bulgaristan Edirne, Kırklareli, Tekirdağ, İstanbul, Kocaeli, Yalova, Sakarya, Bilecik, Bursa, Balıkesir, Çanakkale".lower() ,
                 "Ege" : "Ege, Akdeniz, İzmir, Manisa, Aydın, Denizli, Kütahya, Afyonkarahisar, Uşak, Muğla".lower() ,
                 "Karadeniz" : "Karadeniz, İç Anadolu, Gürcistan, Rize, Trabzon, Artvin, Sinop, Tokat, Çorum, Amasya, Samsun, Zonguldak, Bolu, Düzce, Karabük, Bartın, Kastamonu, Bayburt, Giresun, Gümüşhane, Ordu".lower() ,
                 "Dogu Anadolu" : "Doğu Anadolu, Güneydoğu Anadolu, Suriye,Irak, Ermenistan, İran, Ağrı, Ardahan, Bingöl, Bitlis, Elazığ, Erzincan, Erzurum, Hakkari, Iğdır, Kars, Malatya, Muş, Tunceli, Van, Şırnak".lower()} 
gonderilecek_bolge = "Marmara"

def eski_veri_silme():
    cols = ",".join(df.columns)
    file = open("deprem.csv","w+")
    file.write(cols+"\n")
    file.close()
##    file2 = open("deprem_temiz.txt","w")
##    file2.write("")
##    file2.close()
    
def arama():
    c = twint.Config()
    c.Username = "Kandilli_info"
    c.Search = "#DEPREM"
    c.Limit = 20
    c.Hide_output = True
    c.Format = ": Date: {date}  |  Tweet: {tweet}"
    c.Since = "{}-{}-{}".format(dattime.year, dattime.month, dattime.day)
    c.Store_csv = True
    c.Output = "deprem.csv"
    twint.run.Search(c)

def konum_bul(i):
    a = re.search("DEPREM",df.iloc[i,10])
    ind1 = (list(a.span()))[1]+1
    b = re.search("https", df.iloc[i,10])
    ind2 = (list(b.span()))[0]-1
    konum = (df.iloc[i,10])[ind1:ind2]
    return konum.lower()

def tarih_ve_saat_bulma(i):
    a = re.search("{}".format(dattime.day),df.iloc[i,10])
    ind1 = (list(a.span()))[0]
    b = re.search("TSİ", df.iloc[i,10])
    ind2 = (list(b.span()))[1]-4
    tarih_ve_saat = (df.iloc[i,10])[ind1:ind2]
    return tarih_ve_saat

def buyukluk_bulma(i):
    a = re.search("Büyüklük: ",df.iloc[0,10])
    ind1 = (list(a.span()))[0]
    b = re.search("Derinlik", df.iloc[0,10])
    ind2 = (list(b.span()))[0]-1
    buyukluk = (df.iloc[0,10])[ind1:ind2]
    return buyukluk

def derinlik_bulma(i):
    a = re.search("Derinlik: ",df.iloc[i,10])
    ind1 = (list(a.span()))[0]
    b = re.search("km", df.iloc[i,10])
    ind2 = (list(b.span()))[1]
    derinlik = (df.iloc[i,10])[ind1:ind2]
    return derinlik

def bilgi():
    icindeki = open("deprem_temiz.txt","r").read()
    eski_veri_silme()
    arama()
    df = pd.read_csv("deprem.csv")
##    print(df.iloc[0,10])
    aynisi = 0
    
    if icindeki!="":print("Yeni tweet gelmedi, eski tweet:\n "+icindeki)
    if icindeki=="Konum: {}\nTarih: {}\n{}\n{}\n".format(konum_bul(0),
                                                        tarih_ve_saat_bulma(0),
                                                        buyukluk_bulma(0),
                                                        derinlik_bulma(0)):
        aynisi = 1
    if aynisi != 1:
        file2 = open("deprem_temiz.txt","w")
        file2.write("Konum: {}\nTarih: {}\n{}\n{}\n".format(konum_bul(0),
                                                            tarih_ve_saat_bulma(0),
                                                            buyukluk_bulma(0),
                                                            derinlik_bulma(0)))
        file2.close()
    return aynisi
dattime = datetime.datetime.now()
arama()
df = pd.read_csv("deprem.csv")
depremTemizTxt = open("deprem_temiz.txt","w")
depremTemizTxt.close()

while True:
    dattime = datetime.datetime.now()
    
    aynisi = 0
    aynisi = bilgi()

    for bolge in bolgeler_dict.keys():
        for il in bolgeler_dict[bolge].split(", "):
            if len(re.findall(il,konum_bul(0))) != 0:
                gonderilecek_bolge = bolge
                break
    if aynisi !=1:
        if gonderilecek_bolge == "Marmara":
            bot.sendMessage(marmara_chat_id,"Konum: {}\nTarih: {}\n{}\n{}\n".format(konum_bul(0),
                                                                tarih_ve_saat_bulma(0),
                                                                buyukluk_bulma(0),
                                                                derinlik_bulma(0)))
        elif gonderilecek_bolge == "Ege":
            bot.sendMessage(ege_chat_id,"Konum: {}\nTarih: {}\n{}\n{}\n".format(konum_bul(0),
                                                                tarih_ve_saat_bulma(0),
                                                                buyukluk_bulma(0),
                                                                derinlik_bulma(0)))
        elif gonderilecek_bolge == "Dogu Anadolu":
            bot.sendMessage(dogu_anadolu_chat_id,"Konum: {}\nTarih: {}\n{}\n{}\n".format(konum_bul(0),
                                                                tarih_ve_saat_bulma(0),
                                                                buyukluk_bulma(0),
                                                                derinlik_bulma(0)))

        elif gonderilecek_bolge == "Karadeniz":
            bot.sendMessage(karadeniz_chat_id,"Konum: {}\nTarih: {}\n{}\n{}\n".format(konum_bul(0),
                                                                tarih_ve_saat_bulma(0),
                                                                buyukluk_bulma(0),
                                                                derinlik_bulma(0)))
##    else: bot.sendMessage(marmara_chat_id,"1 dk doldu yeni mesaj yok")
    time.sleep(60)
