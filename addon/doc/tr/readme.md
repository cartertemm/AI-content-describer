# NVDA için Yapay Zeka İçerik Betimleyici

Bu eklenti, görseller ve diğer görsel olarak erişilemeyen içerikler için ayrıntılı betimlemeler elde etmeyi mümkün kılar.  

GPT-4 büyük dil modelinin çok modlu yeteneklerinden yararlanarak sınıfının en iyisi içerik açıklamaları sunmayı hedefliyoruz. Temel model hakkında daha fazla bilgi için [GPT-V4](https://openai.com/research/gpt-4v-system-card) adresine bakın.

## Özellikler

* Odak nesnesini, gezgin nesnesini veya tüm ekranı betimleme
* İster bir e-postadaki resim, ister Windows Explorer'daki bir yol olsun, panoya kopyalanan herhangi bir resmi betimleme
* PNG (.png), JPEG (.jpeg ve .jpg), WEBP (.webp) ve animasyonsuz GIF (.gif) dahil çok çeşitli formatları destekler
* API kotasını korumak için isteğe bağlı olarak yanıtları önbelleğe alır
* Gelişmiş kullanım için bilgileri ihtiyaçlara göre uyarlamak amacıyla istemi ve jeton sayısını özelleştirebilme

## Kullanım örneği:

Bu projenin arkasında birkaç temel motivasyon vardı.

NVDA, oyunun kurallarını değiştiren kutudan çıkar çıkmaz optik karakter tanıma (OCR) gerçekleştirme yeteneğine sahiptir. Bir görüntüden veya PDF belgesinden metin çıkarmaya çalışıyorsanız, aradığınız şey budur.

Ancak OCR yalnızca *metin olabilecek* verileri analiz edebilir. Bu görüntülerde aktarılan bağlamı, nesneleri ve ilişkileri dikkate alma konusunda yetersiz kalıyor. Ve internet onlarla dolu. Logolar, portreler, memler, simgeler, çizelgeler, diyagramlar, çubuk/çizgi grafikler... Adını siz koyun. Bunlar her yerdedir ve genellikle ekran okuyucu kullanıcılarının yorumlayabileceği bir formatta değildir.
Yakın zamana kadar, alternatif metin açıklamaları sunan içerik yazarlarına sarsılmaz bir güven vardı. Bu hala bir zorunluluk olsa da, yüksek kalite standardının kural değil istisna olduğu gerçeğini değiştirmek zordur.

Şimdi, olasılıklar neredeyse sonsuzdur. Şunları yapabilirsiniz:

* Başkalarını eğitirken simgelerin yerleşimini anlamak için masaüstünü veya belirli bir pencereyi görselleştirin
* Sesin yetersiz veya kullanılamadığı durumlarda oyunların, sanal makinelerin vb. durumu hakkında ayrıntılı bilgi alın
* Bir grafikte neyin görüntülendiğini bulma
* Ekran görüntülerinin gizemini aydınlatın
* Video kaydetmeden veya çevrimiçi toplantılara katılmadan önce yüzünüzün kameraya net bir şekilde baktığından emin olun

## Başlarken

[Eklentinin en son sürümünü bu bağlantıdan indirin](https://github.com/cartertemm/AI-content-describer/releases/latest/). NVDA'nın kurulu olduğu bir bilgisayardaki dosyaya tıklayın, ardından OpenAI'den bir API anahtarı almak için aşağıdaki talimatları izleyin:

1. https://platform.openai.com/account/api-keys adresine gidin.
2. Henüz bir hesabınız yoksa bir tane oluşturun. Eğer varsa, giriş yapın.
3. API anahtarları sayfasında yeni bir gizli anahtar oluşturmak için tıklayın. Panonuza kopyalayın.
4. Hesaba en az 1$ yatırın
5. NVDA ayarları iletişim kutusunda Yapay Zeka İçerik Betimleyici kategorisine ilerleyin, ardından API anahtarı alanına girin ve az önce oluşturduğunuz anahtarı buraya yapıştırın.

Bu yazının yazıldığı sırada OpenAI, yeni geliştirici hesaplarına üç ay boyunca kullanılabilecek krediler veriyor ve sonrasında bu krediler kayboluyor.

Bu sürenin ardından kredi satın almanız gerekecektir. Tipik kullanım asla ayda 5,00 doları aşmamalıdır. Referans olması açısından, bu eklentinin orijinal sürümü bir doların biraz altında bir fiyata geliştirildi. Kotanızı almak için OpenAI hesabınıza giriş yapıp "kullanım" seçeneğine tıklamanız her zaman mümkündür.

## Kullanma

Üç kısayol tuşu varsayılan olarak tanımlanmıştır

* NVDA+shift+i: Geçerli odağın mı, gezgin nesnesinin mi yoksa tüm ekranın mı Yapay zeka  ile betimleneceğini soran bir menü açar.
* NVDA+shift+u: Mevcut gezgin nesnesinin içeriğini yapay zeka kullanarak betimler.
* NVDA+shift+y: Yapay zekayı kullanarak panodaki görüntüyü (veya görüntünün dosya yolunu) betimler.

Tanımlanmayan iki hareket:

* Şu anda odaklanılan öğenin içeriğini yapay zeka kullanarak betimler.
* Bir ekran görüntüsü alır ve ardından yapay zekayı kullanarak betimler.

Bunları istediğiniz zaman girdi hareketleri iletişim kutusundan özelleştirmekten çekinmeyin.

## Eklentiyi oluşturma

Eklenti paketini kaynaktan oluşturmak için ihtiyacınız olacaklar:
* Python dağıtımı (3.7 veya üzeri önerilir). Windows Yükleyicileri için [Python Web Sitesini](https://www.python.org) kontrol edin. Şu anda NVDA kaynak kodunun ve içerdiği üçüncü taraf modüllerin hazırlanmasının Python 3.7'nin 32 bit sürümünü gerektirdiğini lütfen unutmayın.
* Scons - [Web sitesi](https://www.scons.org/) - sürüm 4.3.0 veya üzeri. PIP aracılığıyla kurabilirsiniz. 'pip kurulum ekleri'
* Markdown 3.3.0 veya üzeri. 'pip kurulum işaretlemesi'

Ardından tercih ettiğiniz terminali açın:
```
git clone https://github.com/cartertemm/AI-content-describer.git
scons
```

'scons' komutunun yürütülmesi tamamlandıktan sonra, yayınlanmaya hazır bir *.nvda-addon dosyası görmelisiniz.

## Katkılar

Hepsi çok takdir edilmektedir.
Bir sorun mu buldunuz? Sorunu [sorun izleyiciye](https://github.com/cartertemm/AI-content-describer/issues) gönderin
Yeni bir özellik öneriniz mi var? Bunun için de bir Bilet oluşturun, uygulamaya geçirme konusunu konuşabiliriz. İlgili sorunları olmayan çekme istekleri incelenecek, ancak özellikle yeni düzeltmenin veya işlevselliğin farklı çalışması gerektiğine karar verirsem muhtemelen herkes için daha fazla zaman alacaktır.

Çeviriler açık kollarla karşılanır.
Github'ınız yoksa veya kullanmamayı tercih ediyorsanız, [bana bir e-posta gönderebilirsiniz](mailto:cartertemm@gmail.com) - cartertemm (at) gmail (dot) com.
Destek için teşekkürler!