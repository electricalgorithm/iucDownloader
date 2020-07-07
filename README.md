# iucDownloader
İstanbul Üniversitesi - Cerrahpaşa Döküman İndirme/Bulma Programı

Program Python ile yazılmıştır, tarafımca belirli aralıktaki ders kodları denenmiş ve kodda görünen klasörler oluşturulmuştur. Hangi dersin dökümanları olduğunu
isterseniz oradan bakaabilirsiniz. Ancak OBS sistemi tarafından verilen linkler geçerliliğini yitirmektedir - yani dersi indirmeden önce yeniden program üzerinden
ders dökümanlarını istemeniz gerekmektedir.

Program 
```bash
python3 iucDownloader.py
```
şeklinde çalışıtırılır. Bayraklama sistemi yoktur, yaparsanız çok şükela olur.

## Ders Kodları
İstediğiniz bölümün dersini alabilir ve dökümanlarını indirebilirsiniz. Bölümlerin ders kodlarını bulmak için ebs.istanbulc.edu.tr adresine girin ve herhangi bir
fakültedeki herhangi bir bölümün sayfasına erişin. Bu sayfada ders programı kısmına gelin ve müfredatın açıldığını gördüğünüzden emin olun.

Açılan müfredatta istediğiniz derse tıklayın. Ben örnek için Mühendislik Fakültesi'ndeki Jeoloji Mühendisliği'nin Zemin Mekaniği dersini seçiyorum. Tıkladığınızda
açılan sayfanın bağlantısı şu tarz olacaktır:
```
https://ebs.istanbulc.edu.tr/home/izlence/?id=668809&bid=1205
```
Buradaki id=XXXXXXX kısmındaki XXXXXX, her zaman 6 basamaklı bir sayıdır ve bizim ders kodumuzdur. bid=YYYYYY yazan kısım ise bölümün kodudur ve programın çalışması
için önemli değildir, program kendi o kodu bulur.

## Program neden indirmiyor da internet sayfası oluşturuyor?
Programın indirmemesinin sebebi, benim bunu becerememem. Programın kodunu incelediğinde göreceksinzi ki linke kadar her şeyi buluyor ve üstelik bunu JSON olarak
depoluyor. Requests kütüphanesi ile neler neler denedim, bir türlü indiremedim. Sorun indirmek için öncelikle kullanıcı girişi yapmamızın gerekliliği, eğer 
çözebilirseniz -ki kullanıcı girişini session olarak yaparak hem cookieleri de saklayabilirsiniz, sormamıza gerek kalmaz- kullanıcı dostu bir program hazırlanmış
ve en büyük katkıyı siz yapmış olursunuz.

HTML olarak depo etmek ise bana çok makul göründü, tahminen HTML'i açacağınız tarayıcı hali hazırda OBS'ye giriş yapmış tarayıcı olacağı için linke direk basarak
indirebileceksiniz. Daha öncede söylediğim gibi **linkler bir süre sonra zaman aşımına uğruyor, dersin dökümanlarını indirecekseniz çok bekletmeden indirin.**

## Ahlaki ve Hukuki Boyut
Açıkçası hukuki boyutundan bihaberim. Bu bir güvenlik zaafiyeti olarak değerlendirilebilir mi, emin değilim. Bu metni yazmamdan ertesi gün hem rektörlüğe hem bilgi
işlem'e hem de bilgisayar mühendisliği bölümüne bu durumu ve kaynak kodu göndereceğim - belki bilgisar mühendisliği bölümüne geçrirler beni süpriz olarak :D) 
Eğer isterlerse bu GitHub reposunu da anında kaldıracağım, burada yanlış anlaşılma olmasın. Akademik etik anlamıda bu durumu doğru bulmuyorum. Yani hazırlanmış (
veya bazı hocaların da dökümanlarını görüdüğümüz üzere çalıntı) belgeler o dersin hocasına aittir, izinsiz indirmek doğru olmaz. Bunun bilincinde programı 
kullanmalısınız. Ben sadece kodunu yazdım ve gösterdim açığı, dosyaları indirmek sizin sorumluluğunuzdadır.

## Acı Gerçek
Acı gerçek şu ki, bazı bölümlerin COVID19 sürecinde nasıl rezalet bir eğitim aldığının göstergesi oldu bu olay. Hakkını vermek gerek, en çok dökümana sahip bölüm
benim de bölümüm olan EEM bölümüydü - tıp, veterinerlik dışında sanırım. Ayrıca da şunu belirtmeliyim, eğer dersin dökümanları yoksa bir diğer ihtimal MERGEN BTK'da
öğrencilere eğitim vermeleri olabilir.
