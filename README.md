
#  Sürücüsüz Metro Simülasyonu (Rota Optimizasyonu)
Bu projede Graf veri yapısını kullanarak metro ağını modelleme BFS (Breadth-First Search) algoritması ile en az aktarmalı rotayı bulma A* algoritması ile en hızlı rotayı bulma Gerçek dünya problemlerini algoritmik düşünce ile çözme yer almaktadır.
İçerisinde 3 farklı örnek yer almaktadır.
# BFS (Breadth-First Search / Genişlik Öncelikli Arama)
Graf veya ağaç yapısında, aynı seviyedeki tüm düğümleri genişleterek arama yapar.
## Çalışma Prensibi:
FIFO (First In First Out / İlk Giren İlk Çıkar) mantığıyla çalışan kuyruk (queue) kullanır
İlk önce başlangıç düğümünü, sonra onun komşularını ve ardından onların komşularını ziyaret eder
## Avantajları:
En kısa yolu garanti eder
Sonsuz döngüye girme riski düşüktür
## Dezavantajları:
Çözüm bulunana kadar genişlemeye devam ettiği için daha fazla bellek kullanabilir
En kötü durumda en uzun süreyi alabilir
## Örnek Kullanım:
En kısa yol problemleri
Sosyal ağ analizinde en yakın bağlantıları bulmak
# A* Algoritması
A* araması, açgözlü en iyi-öncelikli aramanın geliştirilmiş bir versiyonudur. Sadece hedefe olan sezgisel maliyeti h(n) değil, aynı zamanda başlangıçtan şu anki düğüme kadar olan gerçek maliyet g(n) de dikkate alır.
Formül:
f(n)=g(n)+h(n)
Burada:
f(n) → Tahmini toplam maliyet g(n) → Başlangıç düğümünden mevcut düğüme kadar kat edilen gerçek yol maliyeti h(n) → Hedefe olan sezgisel (heuristik) maliyet Çalışma Prensibi:

Algoritma, iki maliyeti de göz önünde bulundurarak en düşük toplam maliyetli yolu seçer.
Yanıltıcı sezgisellerin etkisini azaltır ve gereksiz yere uzun yolları tercih etmekten kaçınır. Gerektiğinde önceki seçimlerine dönüp daha iyi alternatifleri değerlendirebilir.
A* aramasının verimli olması için sezgisel maliyeti veren fonksiyon h(n):
Kabul edilebilir olmalıdır → Gerçek maliyeti asla aşmamalıdır. Tutarlı olmalıdır → Bir düğümün sezgisel maliyeti, komşu düğümün sezgisel maliyeti ile bu iki düğüm arasındaki gerçek geçiş maliyetinin toplamından daha büyük olmamalıdır.
## Avantajları:
En iyi çözümü garanti eder (eğer sezgisel fonksiyon doğruysa). Bilgisiz aramalara göre daha verimlidir.
## Dezavantajları:
Yanlış sezgisellerle yavaşlayabilir. Hafıza kullanımı yüksektir, büyük problemler için maliyetli olabilir. A* araması, doğru bir sezgisel fonksiyon ile kullanıldığında en iyi çözümü en verimli şekilde bulabilen güçlü bir algoritmadır.


