# -*- coding: utf-8 -*-
"""Merveİntepe_MetroSimulation.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1DEmE5J1foXPB9xyJ38F3oqALno6tN4da

# Sürücüsüz Metro Simülasyonu (Rota Optimizasyonu)
Bu projede
Graf veri yapısını kullanarak metro ağını modelleme
BFS (Breadth-First Search) algoritması ile en az aktarmalı rotayı bulma
A* algoritması ile en hızlı rotayı bulma
Gerçek dünya problemlerini algoritmik düşünce ile çözme
yer almaktadır.

#BFS (Breadth-First Search / Genişlik Öncelikli Arama)
Graf veya ağaç yapısında, aynı seviyedeki tüm düğümleri genişleterek arama yapar.

##Çalışma Prensibi:

FIFO (First In First Out / İlk Giren İlk Çıkar) mantığıyla çalışan kuyruk (queue) kullanır
İlk önce başlangıç düğümünü, sonra onun komşularını ve ardından onların komşularını ziyaret eder
##Avantajları:

En kısa yolu garanti eder
Sonsuz döngüye girme riski düşüktür
##Dezavantajları:

Çözüm bulunana kadar genişlemeye devam ettiği için daha fazla bellek kullanabilir
En kötü durumda en uzun süreyi alabilir
##Örnek Kullanım:

En kısa yol problemleri
Sosyal ağ analizinde en yakın bağlantıları bulmak

#A* Algoritması
A* araması, açgözlü en iyi-öncelikli aramanın geliştirilmiş bir versiyonudur. Sadece hedefe olan sezgisel maliyeti h(n) değil, aynı zamanda başlangıçtan şu anki düğüme kadar olan gerçek maliyet g(n) de dikkate alır.
##Formül:

f(n)=g(n)+h(n)

Burada:

f(n) → Tahmini toplam maliyet
g(n) → Başlangıç düğümünden mevcut düğüme kadar kat edilen gerçek yol maliyeti
h(n) → Hedefe olan sezgisel (heuristik) maliyet
Çalışma Prensibi:

Algoritma, iki maliyeti de göz önünde bulundurarak en düşük toplam maliyetli yolu seçer.

Yanıltıcı sezgisellerin etkisini azaltır ve gereksiz yere uzun yolları tercih etmekten kaçınır. Gerektiğinde önceki seçimlerine dönüp daha iyi alternatifleri değerlendirebilir.

A* aramasının verimli olması için sezgisel maliyeti veren fonksiyon h(n):

Kabul edilebilir olmalıdır → Gerçek maliyeti asla aşmamalıdır.
Tutarlı olmalıdır → Bir düğümün sezgisel maliyeti, komşu düğümün sezgisel maliyeti ile bu iki düğüm arasındaki gerçek geçiş maliyetinin toplamından daha büyük olmamalıdır.
##Avantajları:

En iyi çözümü garanti eder (eğer sezgisel fonksiyon doğruysa).
Bilgisiz aramalara göre daha verimlidir.
##Dezavantajları:

Yanlış sezgisellerle yavaşlayabilir.
Hafıza kullanımı yüksektir, büyük problemler için maliyetli olabilir.
A* araması, doğru bir sezgisel fonksiyon ile kullanıldığında en iyi çözümü en verimli şekilde bulabilen güçlü bir algoritmadır.
"""

!pip install networkx

"""#BFS ve A* kodlarını içeren kodlar"""

from collections import defaultdict, deque
import heapq
from typing import Dict, List, Set, Tuple, Optional

import networkx as nx  # networkx modülünü import et
import matplotlib.pyplot as plt  # matplotlib modülünü import et

class Istasyon:
    def __init__(self, idx: str, ad: str, hat: str):
        self.idx = idx
        self.ad = ad
        self.hat = hat
        self.komsular: List[Tuple['Istasyon', int]] = []  # (istasyon, süre) tuple'ları

    def komsu_ekle(self, istasyon: 'Istasyon', sure: int):
        self.komsular.append((istasyon, sure))

     # Add the __lt__ method for comparison
    def __lt__(self, other):
        # Compare based on station index (idx)
        return self.idx < other.idx

class MetroAgi:
    def __init__(self):
        self.istasyonlar: Dict[str, Istasyon] = {}
        self.hatlar: Dict[str, List[Istasyon]] = defaultdict(list)

    def istasyon_ekle(self, idx: str, ad: str, hat: str) -> None:
        if id not in self.istasyonlar:
            istasyon = Istasyon(idx, ad, hat)
            self.istasyonlar[idx] = istasyon
            self.hatlar[hat].append(istasyon)

    def baglanti_ekle(self, istasyon1_id: str, istasyon2_id: str, sure: int) -> None:
        istasyon1 = self.istasyonlar[istasyon1_id]
        istasyon2 = self.istasyonlar[istasyon2_id]
        istasyon1.komsu_ekle(istasyon2, sure)
        istasyon2.komsu_ekle(istasyon1, sure)

    def en_az_aktarma_bul(self, baslangic_id: str, hedef_id: str) -> Optional[List[Istasyon]]:
        if baslangic_id not in self.istasyonlar or hedef_id not in self.istasyonlar:
          return None

        baslangic = self.istasyonlar[baslangic_id]
        hedef = self.istasyonlar[hedef_id]
        kuyruk = deque([(baslangic, [baslangic])])  # (current_station, path_so_far)
        ziyaret_edildi = set()

        while kuyruk:
            mevcut, yol = kuyruk.popleft()  # Kuyruktan istasyonu çıkar
            if mevcut in ziyaret_edildi:
                continue

            ziyaret_edildi.add(mevcut)  # İstasyonu ziyaret edilmiş olarak işaretle

            # Hedef istasyon bulunursa, yolu döndür
            if mevcut == hedef:
                return yol

            # Komşu istasyonları keşfet
            for komsu, _ in mevcut.komsular:
                if komsu not in ziyaret_edildi:
                    kuyruk.append((komsu, yol + [komsu]))  # Kuyruğa ekle

        return None  # Rota bulunamazsa



    def en_hizli_rota_bul(self, baslangic_id: str, hedef_id: str) -> Optional[Tuple[List[Istasyon], int]]:
        if baslangic_id not in self.istasyonlar or hedef_id not in self.istasyonlar:
           return None

        baslangic = self.istasyonlar[baslangic_id]
        hedef = self.istasyonlar[hedef_id]
        pq = [(0, baslangic, [baslangic])]
        ziyaret_edildi = set()

        while pq:
            toplam_sure, mevcut, yol = heapq.heappop(pq)  # En düşük süreye sahip olanı çıkar

            if mevcut in ziyaret_edildi:
                continue

            ziyaret_edildi.add(mevcut)  # Ziyaret edilen istasyonları işaretle

            # Hedef istasyona ulaşıldıysa rotayı ve toplam süreyi döndür
            if mevcut == hedef:
                return (yol, toplam_sure)

            # Komşuları keşfet ve öncelik kuyruğuna ekle
            for komsu, sure in mevcut.komsular:
                if komsu not in ziyaret_edildi:
                    heapq.heappush(pq, (toplam_sure + sure, komsu, yol + [komsu]))

        return None  # Hiçbir rota bulunamadıysa

"""#görselleştirmek için"""

import matplotlib.pyplot as plt
import networkx as nx

def metro_agini_gorsellestir(metro_agi):
    # Yeni bir Graph oluştur
    G = nx.Graph()

    # İstasyonları ekle
    for istasyon_id, istasyon in metro_agi.istasyonlar.items():
        G.add_node(istasyon_id, label=istasyon.ad, hat=istasyon.hat)

    # Bağlantıları ekle
    for istasyon_id, istasyon in metro_agi.istasyonlar.items():
        for komsu, sure in istasyon.komsular:
            G.add_edge(istasyon_id, komsu.idx, weight=sure)

    # Grafiği çiz
    pos = nx.spring_layout(G)  # Düğüm yerleşimi
    edge_labels = nx.get_edge_attributes(G, 'weight')  # Kenar ağırlıkları (süre)
    node_labels = nx.get_node_attributes(G, 'label')  # Düğüm isimleri

    plt.figure(figsize=(10, 8))
    nx.draw(G, pos, with_labels=False, node_color='lightblue', node_size=2000, font_size=10, font_weight='bold')
    nx.draw_networkx_labels(G, pos, labels=node_labels, font_size=10)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red')

    plt.title("Metro Ağı Görselleştirmesi")
    plt.show()

# Örnek Kullanım
if __name__ == "__main__":
    metro = MetroAgi()

    # İstasyonlar ekleme
    # Kırmızı Hat
    metro.istasyon_ekle("K1", "Kızılay", "Kırmızı Hat")
    metro.istasyon_ekle("K2", "Ulus", "Kırmızı Hat")
    metro.istasyon_ekle("K3", "Demetevler", "Kırmızı Hat")
    metro.istasyon_ekle("K4", "OSB", "Kırmızı Hat")

    # Mavi Hat
    metro.istasyon_ekle("M1", "AŞTİ", "Mavi Hat")
    metro.istasyon_ekle("M2", "Kızılay", "Mavi Hat")  # Aktarma noktası
    metro.istasyon_ekle("M3", "Sıhhiye", "Mavi Hat")
    metro.istasyon_ekle("M4", "Gar", "Mavi Hat")

    # Turuncu Hat
    metro.istasyon_ekle("T1", "Batıkent", "Turuncu Hat")
    metro.istasyon_ekle("T2", "Demetevler", "Turuncu Hat")  # Aktarma noktası
    metro.istasyon_ekle("T3", "Gar", "Turuncu Hat")  # Aktarma noktası
    metro.istasyon_ekle("T4", "Keçiören", "Turuncu Hat")

    # Bağlantılar ekleme
    # Kırmızı Hat bağlantıları
    metro.baglanti_ekle("K1", "K2", 4)  # Kızılay -> Ulus
    metro.baglanti_ekle("K2", "K3", 6)  # Ulus -> Demetevler
    metro.baglanti_ekle("K3", "K4", 8)  # Demetevler -> OSB

    # Mavi Hat bağlantıları
    metro.baglanti_ekle("M1", "M2", 5)  # AŞTİ -> Kızılay
    metro.baglanti_ekle("M2", "M3", 3)  # Kızılay -> Sıhhiye
    metro.baglanti_ekle("M3", "M4", 4)  # Sıhhiye -> Gar

    # Turuncu Hat bağlantıları
    metro.baglanti_ekle("T1", "T2", 7)  # Batıkent -> Demetevler
    metro.baglanti_ekle("T2", "T3", 9)  # Demetevler -> Gar
    metro.baglanti_ekle("T3", "T4", 5)  # Gar -> Keçiören

    # Hat aktarma bağlantıları (aynı istasyon farklı hatlar)
    metro.baglanti_ekle("K1", "M2", 2)  # Kızılay aktarma
    metro.baglanti_ekle("K3", "T2", 3)  # Demetevler aktarma
    metro.baglanti_ekle("M4", "T3", 2)  # Gar aktarma

    # Test senaryoları
    print("\n=== Test Senaryoları ===")

    # Senaryo 1: AŞTİ'den OSB'ye
    print("\n1. AŞTİ'den OSB'ye:")
    rota = metro.en_az_aktarma_bul("M1", "K4")
    if rota:
        print("En az aktarmalı rota:", " -> ".join(i.ad for i in rota))

    sonuc = metro.en_hizli_rota_bul("M1", "K4")
    if sonuc:
        rota, sure = sonuc
        print(f"En hızlı rota ({sure} dakika):", " -> ".join(i.ad for i in rota))

    # Senaryo 2: Batıkent'ten Keçiören'e
    print("\n2. Batıkent'ten Keçiören'e:")
    rota = metro.en_az_aktarma_bul("T1", "T4")
    if rota:
        print("En az aktarmalı rota:", " -> ".join(i.ad for i in rota))

    sonuc = metro.en_hizli_rota_bul("T1", "T4")
    if sonuc:
        rota, sure = sonuc
        print(f"En hızlı rota ({sure} dakika):", " -> ".join(i.ad for i in rota))

    # Senaryo 3: Keçiören'den AŞTİ'ye
    print("\n3. Keçiören'den AŞTİ'ye:")
    rota = metro.en_az_aktarma_bul("T4", "M1")
    if rota:
        print("En az aktarmalı rota:", " -> ".join(i.ad for i in rota))

    sonuc = metro.en_hizli_rota_bul("T4", "M1")
    if sonuc:
        rota, sure = sonuc
        print(f"En hızlı rota ({sure} dakika):", " -> ".join(i.ad for i in rota))

metro_agini_gorsellestir(metro)

"""#Örnek 1
istasyon ıd sini bu kodda farklı yaptığımda, zaten yazdığım hedef istasyonun sonucu vermiş okuyor. Bu yüzden ortak adı olan istasyonda aynı ıd kullandım.
"""

# bir metro hattında iki farlı aktarma noktası ile gidilmek istenilen yere gidilebiliyor olsun.

#metro ağı aluştur
if __name__ == "__main__":

      metro1=MetroAgi()

      #istasyon ekle,(ıd, isim, hat)
      metro1.istasyon_ekle("A1", "istasyon A1", "H1")
      metro1.istasyon_ekle("A2", "istasyon A2", "H2")
      metro1.istasyon_ekle("A3", "istasyon A3", "H1-H2 Aktarma")# birinci aktarma yeri
      metro1.istasyon_ekle("A4","istasyon A4","H1-H3") # ikinci aktarma yeri
      metro1.istasyon_ekle("X", "İstasyon X", "H2")
      metro1.istasyon_ekle("C1","istasyon C1","H3")
      metro1.istasyon_ekle("X","istasyon X","H3")


      #bağlantı ekle (istasyon1, istasyon2, sure)

      metro1.baglanti_ekle("A1", "A2", 7)
      metro1.baglanti_ekle("A2", "A3", 8)
      metro1.baglanti_ekle("A3","A4",2)
      metro1.baglanti_ekle("A4", "C1", 7)
      metro1.baglanti_ekle("C1","X",5)
      metro1.baglanti_ekle("A3", "X", 15)


      # En az aktarma ile yol bulmayı test et
      rota = metro1.en_az_aktarma_bul("A1", "X")
      if rota:
          print("istasyon A1'den istasyon X'e rota:", " -> ".join(i.ad for i in rota))
      else:
          print("Rota bulunamadı.")

      # En hızlı rota
      sonuc = metro1.en_hizli_rota_bul("A1", "X")
      if sonuc:
          rota, sure = sonuc
          print(f"En hızlı rota ({sure} dakika):", " -> ".join(i.ad for i in rota))

metro_agini_gorsellestir(metro1)

"""#örnek 1 için yorum
en_az_aktarmalı ve en_hızlı_rota için istenilen sonucu verdi.

# örnek 2-istanbul
  istasyon ıd ve süreler gerçek değildir
"""

#varmak istenilen durak  ıd kısmını farklı istasyonlarda aynı yazdım.
if __name__ == "__main__":

        metro_ist=MetroAgi()

        #istasyon ekle

        #M2 hattı
        metro_ist.istasyon_ekle("A1", "yenikapı", "M2") #M2-Ma aktarma noktası
        metro_ist.istasyon_ekle("A2", "vezneciler-istanbul ü.", "M2")
        metro_ist.istasyon_ekle("A3", "haliç", "M2")
        metro_ist.istasyon_ekle("A4", "şişhane", "M2")
        metro_ist.istasyon_ekle("A5", "taksim", "M2")
        metro_ist.istasyon_ekle("A6","osmanbey","M2")
        metro_ist.istasyon_ekle("A7","şişli-mecidiyeköy","M2")#M2-MB aktarma noktası
        #marmaray
        metro_ist.istasyon_ekle("B1","yenikapı","Ma") #Ma-M2 aktarma noktası
        metro_ist.istasyon_ekle("B2","sirkeci","Ma")
        metro_ist.istasyon_ekle("B3","üsküdar","Ma")
        metro_ist.istasyon_ekle("B4","ayrılık çeşmesi","Ma")# Ma-M4 aktarma noktası
        #metrobüs hattı
        metro_ist.istasyon_ekle("C1","şişli-mecidiyeköy","MB")#MB-M2 aktarma noktas
        metro_ist.istasyon_ekle("C2","zincirlikuyu","MB")
        metro_ist.istasyon_ekle("C3","şehitler köprüsü","MB")
        metro_ist.istasyon_ekle("C4","burhaniye","MB")
        metro_ist.istasyon_ekle("C5","altunizade","MB")
        metro_ist.istasyon_ekle("C6","acıbadem","MB")
        metro_ist.istasyon_ekle("C7","ünalan/uzunçayır","MB")#MB-M4 aktarma noktası
        #M4 hattı
        metro_ist.istasyon_ekle("D1","ayrılık çeşmesi","M4")#M4-Ma aktarma noktası
        metro_ist.istasyon_ekle("D2","acıbadem","M4")
        metro_ist.istasyon_ekle("D3","ünalan/uzunçayır","M4")#M4-MB aktarma noktası


        #bağlantı ekleme
        metro_ist.baglanti_ekle("A1", "A2",6)
        metro_ist.baglanti_ekle("A2", "A3",6)
        metro_ist.baglanti_ekle("A3", "A4",4)
        metro_ist.baglanti_ekle("A4", "A5",4)
        metro_ist.baglanti_ekle("A5", "A6",6)
        metro_ist.baglanti_ekle("A6", "A7",6)


        metro_ist.baglanti_ekle("B1", "B2",6)
        metro_ist.baglanti_ekle("B2", "B3",8)
        metro_ist.baglanti_ekle("B3", "B4",10)

        metro_ist.baglanti_ekle("C1", "C2",6)
        metro_ist.baglanti_ekle("C2", "C3",10)
        metro_ist.baglanti_ekle("C3", "C4",8)
        metro_ist.baglanti_ekle("C4", "C5",4)
        metro_ist.baglanti_ekle("C5", "C6",4)
        metro_ist.baglanti_ekle("C6", "C7",6)

        metro_ist.baglanti_ekle("D1", "D2",2)
        metro_ist.baglanti_ekle("D2", "D3",4)

        metro_ist.baglanti_ekle("A1", "B1",1)
        metro_ist.baglanti_ekle("B4","D1",1)
        metro_ist.baglanti_ekle("C7","D3",1)
        metro_ist.baglanti_ekle("A7","C1",1)


        print("\n.haliç'den ünalan/uzunçayır'a")
        # Haliç/ünalan-uzunçayır
        rota = metro_ist.en_az_aktarma_bul("A3", "C7")
        if rota:
            print("haliç'den ünalan/uzunçayır'a rota:", " -> ".join(i.ad for i in rota))
        else:
            print("Rota bulunamadı.")

        sonuc = metro_ist.en_hizli_rota_bul("A3", "C7")
        if sonuc:
            rota, sure = sonuc
            print(f"En hızlı rota ({sure} dakika):", " -> ".join(i.ad for i in rota))

        print("\n. zincirlikuyu dan taksim'e: ")
        #
        rota = metro_ist.en_az_aktarma_bul("C2", "A5")
        if rota:
            print("zincirlikuyu'dan taksim ' e rota:", " -> ".join(i.ad for i in rota))
        else:
            print("Rota bulunamadı.")

        sonuc = metro_ist.en_hizli_rota_bul("C2", "A5")
        if sonuc:
            rota, sure = sonuc
            print(f"En hızlı rota ({sure} dakika):", " -> ".join(i.ad for i in rota))

        print("\n. taksim den ünalan/uzunçayır'a: ")

        rota = metro_ist.en_az_aktarma_bul("A5", "D3")
        if rota:
            print("zincirlikuyu'dan taksim ' e rota:", " -> ".join(i.ad for i in rota))
        else:
            print("Rota bulunamadı.")

        sonuc = metro_ist.en_hizli_rota_bul("A5", "D3")
        if sonuc:
            rota, sure = sonuc
            print(f"En hızlı rota ({sure} dakika):", " -> ".join(i.ad for i in rota))

"""#örnek 2 için yorum
haliç ten ünalan/uzunçayır a gitme yönü- ##en_az_akatarmalı rota için M2 ve MB hatlarını seçerek ilerlemesini beklerken, M2, Ma ve M4 hatlarını seçerek ilerledi. ##En_hızlı_rota için ise yine istenilenin tersi şekilde sonuç verdi.
"""

metro_agini_gorsellestir(metro_ist)