# NVDA için Yapay Zeka İçerik Betimleyici

Bu eklenti, görseller, kullanıcı arayüzü kontrolleri ve görsel olarak erişilemeyen diğer içerikler için ayrıntılı betimlemeler elde etmeyi mümkün kılar.

Gelişmiş yapay zeka modellerinin çok modlu yeteneklerinden ve bilgisayarlı görü algoritmalarından yararlanarak sınıfının en iyisi içerik betimlemeleri sunmayı ve genel olarak bağımsızlığı artırmayı hedefliyoruz. Temel modeller hakkında daha fazla bilgi için bu belgenin ilgili bölümüne bakın.

## Özellikler

* Odak nesnesini, gezgin nesnesini veya tüm ekranı betimleme ya da dahili kamerayla fotoğraf çekme
* İster bir e-postadaki resim, ister Windows Explorer'daki bir yol olsun, panoya kopyalanan herhangi bir resmi betimleme
* Odak nesnesinin, gezgin nesnesinin veya tüm ekranın görüntüsünü başka uygulamalara yapıştırmak üzere panoya kopyalama
* Bilgisayarlı görü algoritmalarıyla kullanıcının yüzünün kadrajın ortasında olup olmadığını bildirme (ücretli API erişimi gerektirmez)
* Erişilemeyebilecek görevler için desteklenen modellerle etkin uygulamayı fare ve klavye eylemleriyle kontrol etme
* Varsayılan olarak ücretsizdir, daha fazla model için isteğe bağlı olarak kendi API anahtarınızı ekleyebilirsiniz
* Birden çok sağlayıcıyı destekler (OpenAI'nin GPT'si ve ücretsiz Pollinations katmanı, Google'ın Gemini'si, Mistral Large 4, Anthropic'in Claude'u, xAI'nin Grok'u, Moonshot AI'nin Kimi'si, NVDA-CN üzerinden vivo BlueLM Vision, Datalab Chandra 2, Ollama, llama.cpp, LiteLLM Proxy ve Seer)
* PNG (.png), JPEG (.jpeg ve .jpg), WEBP (.webp) ve animasyonsuz GIF (.gif) dahil çok çeşitli formatları destekler
* API kotasını korumak için isteğe bağlı olarak yanıtları önbelleğe alır
* Gelişmiş kullanım için bilgileri ihtiyaçlara göre uyarlamak amacıyla istemi ve jeton sayısını özelleştirebilme
* Ek sorular sorma ve ek görseller iliştirme
* Yapılandırılmış bilgilere kolayca erişmek için Markdown işleme (yalnızca "Her sonucu göz atılabilir bir iletişim kutusunda aç" ayarını etkinleştirin ve isteminizin sonuna örneğin "Markdown ile yanıt ver" ekleyin)

## Kullanım örneği

Bu projenin arkasında birkaç temel motivasyon vardı.

NVDA, kutudan çıktığı haliyle optik karakter tanıma (OCR) gerçekleştirebilir ve bu oyunun kurallarını değiştiren bir özelliktir. Bir görüntüden veya PDF belgesinden metin çıkarmaya çalışıyorsanız, aradığınız şey budur.

Ancak OCR yalnızca *metin olabilecek* verileri analiz edebilir. Bu görüntülerde aktarılan bağlamı, nesneleri ve ilişkileri dikkate alma konusunda yetersiz kalıyor. Ve internet onlarla dolu. Logolar, portreler, memler, simgeler, çizelgeler, diyagramlar, çubuk/çizgi grafikler... Adını siz koyun. Bunlar her yerdedir ve genellikle ekran okuyucu kullanıcılarının yorumlayabileceği bir formatta değildir.
Yakın zamana kadar, alternatif metin açıklamaları sunan içerik yazarlarına sarsılmaz bir güven vardı. Bu hala bir zorunluluk olsa da, yüksek kalite standardının kural değil istisna olduğu gerçeğini değiştirmek zordur.

Şimdi, olasılıklar neredeyse sonsuzdur. Şunları yapabilirsiniz:

* Başkalarını eğitirken simgelerin yerleşimini anlamak için masaüstünü veya belirli bir pencereyi görselleştirin
* Sesin yetersiz veya kullanılamadığı durumlarda oyunların, sanal makinelerin vb. durumu hakkında ayrıntılı bilgi alın
* Bir grafikte neyin görüntülendiğini öğrenin
* Zoom veya Microsoft Teams'deki ekran görüntülerinin ve ekran paylaşımlarının gizemini aydınlatın
* Erişilemeyen bir uygulamayı kullanmak veya ön plandaki pencerede bir görevi tamamlamak için desteklenen bir modelden yardım isteyin
* Video kaydetmeden veya çevrimiçi toplantılara katılmadan önce yüzünüzün kameraya net bir şekilde baktığından ve arka planınızın profesyonel göründüğünden emin olun

## Modeller

* [Pollinations](https://pollinations.ai/): Pollinations.AI ekibi bu proje için cömertçe ücretsiz GPT4 erişimi sağlıyor, bu nedenle kullanıcıların kendi API anahtarlarını girmesi gerekmez. Hizmetin zaman zaman hatalı çalıştığı görülmüştür; bu projeden tam olarak yararlanmak için kendi anahtarlarınızı kullanmanızı önemle tavsiye ederiz.
* [OpenAI GPT modelleri](https://platform.openai.com/docs/models): Bir OpenAI API anahtarı gerektirir. GPT-5.4 ailesini (5.4 ve 5.4 mini), GPT-5.5 ailesini (5.5 ve 5.5 pro), GPT-6 ailesini (6 Astra ve 6 Luna) ve GPT-6.1 ailesini (6.1 Sol ve 6.1 Terra) içerir. Bilgisayar kontrolü GPT-5.4, GPT-5.5, GPT-6 ve GPT-6.1 aileleri tarafından desteklenir.
* [Google Gemini](https://deepmind.google/models/gemini/); 2.5 Flash, 2.5 Flash-Lite, 2.5 Pro, 3.1 Flash-Lite, 3.1 Pro Preview, 3.5 Flash, 3.5 Flash-Lite, 3.6 Flash, 3.7 Flash, 3.8 Flash, 4 Hydrogen, 4 Argon ve 4 Carbon modelleri dahil.
* [Anthropic Claude](https://docs.anthropic.com/claude/docs/vision); Claude 4.5 (Sonnet, Opus), 4.6 (Sonnet, Opus), 4.7 Opus, 4.8 Opus, 5 (Sonnet, Opus, Fable), 5.1 Fable, 5.2 Fable ve 5.5 (Haiku, Sonnet, Opus) dahil. Bunların hepsi bilgisayar kontrolünü destekler.
* [Mistral Large 4](https://docs.mistral.ai/models/mistral-large-4-0)
* [xAI Grok](https://docs.x.ai/developers/models); Grok 4.20 (akıl yürütmesiz), 4.3, 4.5, 4.6 ve 4.7 dahil.
* [Kimi](https://platform.kimi.ai/docs/guide/use-kimi-vision-model), Moonshot AI'nin çok modlu modelleri; Kimi K3 ve Kimi K2.6 dahil.
* vivo BlueLM Vision: vivo'nun ücretsiz bir NVDA-CN hesabıyla erişilen çok modlu modeli. Aşağıdaki kurulum bölümüne bakın.
* [Datalab Chandra 2](https://github.com/datalab-to/chandra): Datalab'ın karmaşık belge düzenleri, tablolar, formlar, el yazısı, grafikler ve matematik konusunda uzmanlaşmış, son teknoloji görü ve OCR modeli. Datalab'ın yönetilen bulut API'sini ([datalab.to](https://www.datalab.to) üzerinde) veya vLLM ile kendi sunucunuzda barındırılan kurulumları (`chandra_vllm` veya OpenAI uyumlu `/v1` uç noktalarıyla) destekler.
* [Ollama (kararsız)](https://ollama.com/)
* [llama.cpp (donanımınıza bağlı olarak son derece kararsız ve yavaş; llava-v1.5/1.6, BakLLaVA, Obsidian ve MobileVLM 1.7B/3B modelleriyle çalıştığı test edilmiştir)](https://github.com/ggerganov/llama.cpp)
* [LiteLLM Proxy](https://docs.litellm.ai/docs/proxy/quick_start): Birleşik bir proxy sunucusu üzerinden birden çok yapay zeka modeline erişin. Bir LiteLLM proxy sunucusu URL'si ve proxy yapılandırmanıza bağlı olarak isteğe bağlı bir API anahtarı gerektirir. Model yapılandırma iletişim kutusunda "LiteLLM Proxy" olarak görünür. Dinamik model seçimini ve ek soruları destekler. Tüm formatlarla uyumludur (PNG, JPEG, WEBP, GIF).
* [Seer](https://github.com/recursia-lab/Seer): PaliGemma2'yi Seer arka plan hizmeti üzerinden yerel olarak çalıştırır. API anahtarı veya internet bağlantısı gerekmez. Not: Bu yalnızca altyazı (başlık) üreten bir modeldir. İstemler ve ek sorular desteklenmez.

Bunların her birini çalıştırmak için aşağıdaki talimatları izleyin.

## Başlarken

Eklentinin en son sürümünü [bu bağlantıdan](https://github.com/cartertemm/AI-content-describer/releases/latest/) indirin. NVDA'nın kurulu olduğu bir bilgisayarda dosyaya tıklayın ve kurulumu yönergelere göre tamamlayın.

NVDA eklentiyle ilk kez başladığında bazı ek kütüphaneleri indirmek isteyip istemediğinizi sorar. Ayrıntılar için bu belgenin `Bağımlılıklar` bölümüne bakın.

2025.06.05 sürümünden itibaren, PollinationsAI topluluğunun cömertliği sayesinde GPT4 kullanımı ücretsizdir.

Ek modelleri keşfetmek için kaynağınız ve ilginiz varsa, her zaman kendi API anahtarınızı kullanabilir ve onların sunucularına giden istekleri azaltabilirsiniz. Yoksa doğrudan bu belgenin `kullanma` bölümüne geçebilirsiniz.

Desteklenen bir sağlayıcıdan API anahtarı almak için aşağıdaki talimatları izleyin.

### Hangi modeli kullanmalıyım?

Eskiden en ucuz ve en kaliteli seçenekler hakkında öneriler sunuyorduk, ancak alan o kadar hızlı değişiyor ki bunları güncel tutmak mümkün değil.

Kısaca, son teknoloji modellerin çoğu günlük kullanım durumlarının büyük kısmında doğru sonuç verecek düzeye ulaştı; bu yüzden aşina olduğunuz sağlayıcıyı seçin.

Çoğu kişi doğruluk ile maliyet arasında bir denge kurmak ister. [LLM arena sıralaması](https://lmarena.ai/leaderboard) (özellikle görü kategorisi) doğruluğu ölçer, [LLM fiyat hesaplayıcısı](https://www.llm-prices.com/) ise fiyatları gösterir.

Bilgisayar kontrolünü kullanmak istiyorsanız yukarıda listelenen desteklenen OpenAI veya Anthropic modellerinden birini seçin. Ücretsiz Pollinations erişimi görsel betimlemeleri için kullanışlıdır, ancak bilgisayar kontrolünü desteklemez.

### OpenAI'den API anahtarı alma:

1. [OpenAI'nin API anahtarı sayfasına](https://platform.openai.com/account/api-keys) gidin.
2. Henüz bir hesabınız yoksa bir tane oluşturun. Eğer varsa, giriş yapın.
3. API anahtarları sayfasında yeni bir gizli anahtar oluşturmak için tıklayın. Panonuza kopyalayın.
4. Hesaba en az 1$ yatırın
5. NVDA ayarları iletişim kutusunda Yapay Zeka İçerik Betimleyici kategorisine ilerleyin, ardından "modelleri yönet (alt+m)" seçeneğini seçin, sağlayıcı olarak OpenAI modellerinden herhangi birini (örneğin "GPT-6.1 Sol") seçin, Tab ile API anahtarı alanına gidin ve az önce oluşturduğunuz anahtarı buraya yapıştırın.

Bu yazının yazıldığı sırada OpenAI, yeni geliştirici hesaplarına üç ay boyunca kullanılabilecek krediler veriyor ve sonrasında bu krediler kayboluyor. Bu sürenin ardından kredi satın almanız gerekecektir. Tipik kullanım asla ayda 5,00 doları aşmamalıdır. Referans olması açısından, bu eklentinin orijinal sürümü bir doların biraz altında bir fiyata geliştirildi. Kotanızı görmek için OpenAI hesabınıza giriş yapıp "kullanım" seçeneğine tıklamanız her zaman mümkündür.

### Google'dan API anahtarı alma

1. Önce [Google Cloud konsoluna](https://console.cloud.google.com/projectcreate) giderek bir Google Workspace projesi oluşturmanız gerekir. Google hesabınızda oturum açtığınızdan emin olun.
2. "Gemini" veya "NVDA eklentisi" gibi dört ile otuz karakter arasında bir ad belirleyin
3. [Google AI Studio API anahtarları sayfasına](https://makersuite.google.com/app/apikey) gidin
4. "API anahtarı oluştur"a tıklayın
5. NVDA ayarları iletişim kutusunda Yapay Zeka İçerik Betimleyici kategorisine ilerleyin, ardından "modelleri yönet (alt+m)" seçeneğini seçin, sağlayıcı olarak "Google Gemini"yi seçin, Tab ile API anahtarı alanına gidin ve az önce oluşturduğunuz anahtarı buraya yapıştırın.

### Anthropic'ten API anahtarı alma

1. [Anthropic konsolunda](https://console.anthropic.com/login) oturum açın.
2. Profilinize ve ardından API keys'e tıklayın.
3. Create Key'e tıklayın.
4. Anahtar için "AIContentDescriber" gibi bir ad girin, ardından "Create Key"e tıklayın ve görüntülenen değeri kopyalayın. Bu değeri NVDA ayarları iletişim kutusunun Yapay Zeka İçerik Betimleyici kategorisinde, modelleri yönet -> herhangi bir Claude modeli (örneğin "Claude 5 Sonnet") altındaki API anahtarı alanına yapıştıracaksınız.
5. Henüz yapmadıysanız, [Anthropic planlar sayfasından](https://console.anthropic.com/settings/plans) en az 5$ değerinde kredi satın alın.

### Mistral'den API anahtarı alma

1. [MistralAI giriş sayfasına](https://auth.mistral.ai/ui/login) giderek bir MistralAI hesabında oturum açın veya hesap oluşturun.
2. İlk kez hesap oluşturuyor veya oturum açıyorsanız, istendiğinde bir ad girip şartlar ve koşulları kabul ederek bir çalışma alanı ekleyin.
3. Oturum açtıktan sonra menüden "API keys" seçeneğini seçin.
4. "Create a new key"e tıklayın ve anahtarı panonuza kopyalayın. Bu değeri NVDA ayarları iletişim kutusunun Yapay Zeka İçerik Betimleyici kategorisinde, modelleri yönet -> Mistral Large 4 altındaki API anahtarı alanına yapıştıracaksınız.
5. Gerekiyorsa hesaba bakiye yükleyin.

### Kimi'den (Moonshot AI) API anahtarı alma

1. [Kimi geliştirici platformunda](https://platform.kimi.ai/) oturum açın veya hesap oluşturun.
2. Oturum açtıktan sonra konsolun API anahtarları bölümünü açın ve yeni bir anahtar oluşturun.
3. Anahtarı panonuza kopyalayın. Bu değeri NVDA ayarları iletişim kutusunun Yapay Zeka İçerik Betimleyici kategorisinde, modelleri yönet -> Kimi K3 (veya başka bir Kimi modeli) altındaki API anahtarı alanına yapıştıracaksınız.
4. Gerekiyorsa hesaba bakiye yükleyin.


### VIVO BlueLM Vision modelini NVDA-CN üzerinden etkinleştirme

Bu hizmet, VIVO (vivo.com.cn) ile NVDA Çin Topluluğu (NVDACN) arasındaki bir ortaklık sayesinde ücretsiz olarak sunulmaktadır. Yüksek kaliteli çok modlu tanıma sağlar ve başta yeni başlayanlar olmak üzere tüm kullanıcılara önerilen modeldir.

Bu modeli kullanmak için yalnızca ücretsiz bir NVDA-CN hesabına ihtiyacınız vardır.

1.  Hesap oluşturun: NVDA-CN kayıt sayfasına gidin: [https://nvdacn.com/admin/register.php](https://nvdacn.com/admin/register.php).
    * **Not**: Sayfa şu anda Çincedir. Formu doldurmak için tarayıcınızın yerleşik çeviri özelliğini kullanmanızı öneririz.
    * Sizden bir kullanıcı adı, parola ve geçerli bir e-posta adresi istenecektir. Otomatik parola kurtarma henüz uygulanmadığından parolanızı güvenli bir yerde sakladığınızdan emin olun.
2.  E-postanızı doğrulayın: Gelen kutunuzda doğrulama e-postasını bulun ve hesabınızı etkinleştirmek için içindeki bağlantıya tıklayın.
3.  Eklentiyi yapılandırın:
    * NVDA ayarları iletişim kutusunu açın ve "Yapay Zeka İçerik Betimleyici" kategorisine gidin.
    * "Modelleri yönet" düğmesini seçin.
    * Sağlayıcılar listesinden "vivo BlueLM Vision (NVDA-CN)" seçeneğini seçin.
    * NVDA-CN kullanıcı adınızı ve parolanızı ilgili alanlara girin.
    * Kimlik bilgilerinizi kaydetmek için Tamam'a tıklayın.

Artık VIVO modelini kullanmaya hazırsınız. Hesapla ilgili sorunlar için NVDA-CN ekibine `support@nvdacn.com` adresinden ulaşabilirsiniz.


### Ollama'yı kurma

Bu, şu anda yerel kurulum için tercih edilen seçenektir.

Ollama entegrasyonu llama.cpp'ye göre daha kapsamlı test edilmiş olsa da bir API'yi çağırmaktan daha az kararlıdır ve bazı yapılandırmalarda, gerekli donanım özelliklerine sahip olmayan makinelerde çökmeye kadar varan tuhaf davranışlar gösterdiği bilinmektedir.
En azından, ilk kez denerken böyle bir durumla karşılaşma ihtimaline karşı devam etmeden önce tüm belgelerinizi ve önemli her şeyi kaydedin.

İşe, tercih ettiğiniz görü yetenekli modelle komut satırı arayüzü üzerinden etkileşim kurabildiğinizden emin olarak başlayın. Adımlar şunlardır:

1. [Ollama indirmeler](https://ollama.com/download) sayfasından Windows için Ollama kurulum dosyasını indirin.
2. Bu kurulum dosyasını çalıştırın. Makinenizin ihtiyaç duyacağı tüm bağımlılıkları kendisi indirecektir.
3. Kullanmak istediğiniz modeli bulun. Liste ollama.com -> models -> vision altında veya [doğrudan burada](https://ollama.com/search?c=vision) bulunabilir.
4. Bir komut istemi açıp `ollama run [model_name]` yazarak bu modeli indirin ve başlatın; elbette "[model_name]" yerine 3. adımda seçtiğiniz modeli yazın. Örneğin `ollama run llama3.2-vision`.
5. İşlem başarıyla tamamlandıysa, sorgular yazıp modelden yanıt alabileceğiniz etkileşimli bir kabuğa yerleştirilirsiniz; bunu yerel (ve sınırlı) bir ChatGPT gibi düşünebilirsiniz. Çalışıp çalışmadığını görmek için bir şey (herhangi bir şey) sorarak deneyin, ardından bu arayüzden çıkmak için "/bye" yazın.
6. Konsol pencerenize geri dönüp `ollama list` yazın. İlk sütunda "llama3.2-vision:latest" gibi bir ad göreceksiniz.
7. Yapay Zeka İçerik Betimleyici ayarları -> modelleri yönet -> Ollama'ya gidin. Model adı alanına bu değeri girin ve Tamam -> Tamam'a tıklayın. Her şey hazır! Model alt menüsünden Ollama'ya geçin; bir süre sonra çalışacaktır.

### llama.cpp'yi kurma

Bu sağlayıcı şu anda biraz hatalıdır ve sonuçlar kişiden kişiye değişebilir. Yalnızca yerel, kendi sunucusunda barındırılan modelleri çalıştırmaya ilgi duyan ve bunun için donanıma sahip ileri düzey kullanıcılar tarafından denenmelidir.

1. llama.cpp'yi indirin. Bu yazının yazıldığı sırada bu [çekme isteği](https://github.com/ggerganov/llama.cpp/pull/5882) çok modlu yetenekleri kaldırdığından, [bunu destekleyen son sürümü](https://github.com/ggerganov/llama.cpp/releases/tag/b2356) kullanmanız gerekir.
CUDA destekli bir Nvidia grafik kartı kullanıyorsanız şu önceden derlenmiş dosyaları indirin:
[llama-b2356-bin-win-cublas-cu12.2.0-x64.zip](https://github.com/ggerganov/llama.cpp/releases/download/b2356/llama-b2356-bin-win-cublas-cu12.2.0-x64.zip) ve [cudart-llama-bin-win-cu12.2.0-x64.zip](https://github.com/ggerganov/llama.cpp/releases/download/b2356/cudart-llama-bin-win-cu12.2.0-x64.zip)
Farklı bir grafik kartıyla çalışma adımları bu belgenin kapsamı dışındadır, ancak llama.cpp readme dosyasında bulunabilir.
2. Bu iki dosyayı aynı klasöre çıkarın.
3. Kullanmak istediğiniz modellerin nicelenmiş (quantized) biçimlerini Huggingface'te bulun. LLaVA 1.6 Vicuna 7B için: [llava-v1.6-vicuna-7b.Q4_K_M.gguf](https://huggingface.co/cjpais/llava-v1.6-vicuna-7b-gguf/blob/main/llava-v1.6-vicuna-7b.Q4_K_M.gguf) ve [mmproj-model-f16.gguf](https://huggingface.co/cjpais/llava-v1.6-vicuna-7b-gguf/blob/main/mmproj-model-f16.gguf)
4. Bu dosyaları diğer llama.cpp dosyalarının bulunduğu klasöre koyun.
5. Bir komut isteminden, model ve çok modlu projektör için .gguf dosyalarını vererek llava.cpp sunucu dosyasını aşağıdaki gibi çalıştırın:
```
server.exe -m llava-v1.6-vicuna-7b.Q4_K_M.gguf --mmproj mmproj-model-f16.gguf
```
6. NVDA ayarları iletişim kutusunda Yapay Zeka İçerik Betimleyici kategorisine ilerleyin, ardından "modelleri yönet (alt+m)" seçeneğini seçin, sağlayıcı olarak "llama.cpp"yi seçin, Tab ile "Ana URL" alanına gidin ve konsolda gösterilen uç noktayı girin (varsayılan "http://localhost:8080").
7. Alternatif olarak bu adımlardan bazılarını atlayıp llama.cpp'yi yerel makinenizden daha güçlü bir uzak sunucuda çalıştırabilir, ardından o uç noktayı girebilirsiniz.

### LiteLLM Proxy'yi kurma

LiteLLM Proxy, tek bir uç nokta üzerinden birden çok yapay zeka modeline erişmek için birleşik bir arayüz sunar; bu da model yönetimini kolaylaştırır ve sağlayıcılar arasında kolayca geçiş yapmanızı sağlar.

1. [LiteLLM proxy belgelerini](https://docs.litellm.ai/docs/proxy/quick_start) izleyerek bir LiteLLM proxy sunucusu kurun. Proxy'yi yerel olarak çalıştırabilir veya uzak bir sunucu kullanabilirsiniz.
2. Yerel olarak çalıştırıyorsanız, başlamanın en hızlı yolu şudur:
```
pip install 'litellm[proxy]'
litellm --model gpt-4o
```
Bu komut, istekleri OpenAI'nin GPT-4o modeline ileten bir proxy sunucusunu `http://localhost:4000` adresinde başlatır.
3. Üretim ortamında kullanım için birden çok modeli ve kimlik doğrulamayı yapılandırmak üzere bir `config.yaml` dosyası oluşturun. Ayrıntılar için [LiteLLM yapılandırma kılavuzuna](https://docs.litellm.ai/docs/proxy/configs) bakın.
4. NVDA ayarları iletişim kutusunda Yapay Zeka İçerik Betimleyici kategorisine ilerleyin, ardından "modelleri yönet (alt+m)" seçeneğini seçin ve sağlayıcı olarak "LiteLLM Proxy"yi seçin.
5. Proxy sunucunuzun URL'sini "Ana URL" alanına girin (örneğin yerel kurulum için "http://localhost:4000" veya uzak sunucunuzun URL'si).
6. Proxy'niz kimlik doğrulama gerektiriyorsa API anahtarını API anahtarı alanına girin. Gerektirmiyorsa boş bırakın.
7. Proxy'nizdeki kullanılabilir modelleri getirmek için "Model Listesi" düğmesine tıklayın, ardından açılır listeden kullanmak istediğiniz modeli seçin.
8. İstem, maksimum jeton ve zaman aşımı gibi diğer ayarları gerektiği gibi düzenleyin, ardından Tamam'a tıklayın.

Not: Kullanılabilir modeller ve yetenekleri LiteLLM proxy yapılandırmanıza bağlıdır. Görsel betimleme için proxy'nizin görü yetenekli modellerle yapılandırıldığından emin olun.

### Seer'ı kurma

Seer, PaliGemma2'yi API anahtarı veya bulut bağlantısı gerektirmeden kendi makinenizde çalıştırır. Bunun yalnızca altyazı (başlık) üreten bir model olduğunu unutmayın; istemler ve ek sorular desteklenmez.

1. [Seer arka plan hizmetini](https://github.com/recursia-lab/Seer) kurun. Windows (.bat) ve Linux/macOS (.sh) için tek komutluk bir yükleyici sağlanır.
2. NVDA ayarları iletişim kutusunda Yapay Zeka İçerik Betimleyici kategorisine gidin, "modelleri yönet (alt+m)" seçeneğini seçin ve "Seer (kurulum gerektirir)" seçeneğini seçin.
3. Ana URL varsayılan olarak `http://127.0.0.1:11435` şeklindedir. Hizmetin bağlantı noktasını değiştirmediyseniz olduğu gibi bırakın.
4. Tamam'a tıklayın. Betimleme istemeden önce arka plan hizmetinin çalışıyor olması gerekir.

### Datalab Chandra 2'yi kurma

Datalab Chandra 2; karmaşık düzenler, tablolar, formlar, el yazısı, grafikler ve matematik formülleri konusunda uzmanlaşmış, son teknoloji bir belge zekası ve OCR modelidir. Datalab'ın yönetilen bulut API'si, kurum içi (on-premise) bir konteyner veya kendi sunucunuzda barındırılan bir vLLM örneği üzerinden kullanılabilir.

#### Seçenek A: Datalab'ın Bulut API'sini kullanma (Önerilen)
1. [datalab.to](https://www.datalab.to) adresinde bir hesap oluşturun. Yeni hesaplar ücretsiz deneme kredisi alır.
2. [API anahtarları sayfasını](https://www.datalab.to/app/keys) ziyaret edin ve bir API anahtarı oluşturun.
3. NVDA ayarları iletişim kutusunda Yapay Zeka İçerik Betimleyici kategorisine gidin, "modelleri yönet (alt+m)" seçeneğini seçin ve "Datalab Chandra 2"yi seçin.
4. API anahtarınızı "API anahtarı" alanına girin.
5. Ana URL varsayılan olarak `https://www.datalab.to/api/v1/convert` şeklinde yapılandırılmıştır. İşleme modunu (`fast`, `balanced` veya `accurate`) ihtiyaçlarınıza göre ayarlayabilirsiniz.
6. Tamam'a tıklayın. Model artık Yapay Zeka İçerik Betimleyici menüsünde kullanılabilir olacaktır.

#### Seçenek B: vLLM ile kendi sunucunuzda barındırma
1. Yerel vLLM sunucunuzu Chandra 2 ile başlatın (örneğin `chandra_vllm` veya `vllm serve datalab-to/chandra-ocr-2` kullanarak). Sunucu varsayılan olarak `http://localhost:8000/v1` adresinde çalışır.
2. NVDA ayarları -> Yapay Zeka İçerik Betimleyici -> Modelleri yönet -> "Datalab Chandra 2" bölümünde, yerel uç noktanızı "Ana URL" alanına girin (örneğin `http://localhost:8000/v1`).
3. Model adı varsayılandan (`datalab-to/chandra-ocr-2`) farklıysa model adını girin, API anahtarını boş bırakın (veya kimlik doğrulama etkinse bir bearer belirteci girin) ve Tamam'a tıklayın.

## Kullanma

Altı kısayol tuşu varsayılan olarak tanımlanmıştır:

* NVDA+shift+i: Geçerli odağın, gezgin nesnesinin, fiziksel kameranın veya tüm ekranın betimlenmesini ya da bilgisayarın yapay zeka ile kontrol edilmesini seçebileceğiniz bir menü açar.
* NVDA+shift+u: Mevcut gezgin nesnesinin içeriğini yapay zeka kullanarak betimler.
* NVDA+shift+y: Yapay zekayı kullanarak panodaki görüntüyü (veya görüntünün dosya yolunu) betimler.
* NVDA+shift+j: Seçili kameranın kadrajında yüzünüzün konumunu betimler. Birden çok kamera bağlıysa Yapay Zeka İçerik Betimleyici menüsüne (NVDA+shift+i) gidin ve yüz algılama alt menüsündeki "kamera seç" öğesiyle kullanmak istediğiniz kamerayı seçin.
* NVDA+alt+c: Ek sorular sormak için yapay zeka sohbet iletişim kutusunu açar.
* NVDA+control+shift+p: Etkin bir bilgisayar kontrolü oturumunu duraklatır veya sürdürür.

Tanımlanmayan yedi hareket:

* Şu anda odaklanılan öğenin içeriğini yapay zeka kullanarak betimler.
* Bir ekran görüntüsü alır ve ardından yapay zekayı kullanarak betimler.
* Seçili kamerayla bir fotoğraf çeker ve ardından yapay zekayı kullanarak betimler.
* Etkin bilgisayar kontrolü oturumunu iptal eder.
* Geçerli odak nesnesinin ekran görüntüsünü alır ve panoya kopyalar.
* Geçerli gezgin nesnesinin ekran görüntüsünü alır ve panoya kopyalar.
* Tüm ekranın görüntüsünü alır ve panoya kopyalar.

Üç kopyalama komutu NVDA+shift+i menüsündeki "Görüntüyü panoya kopyala" alt menüsünde de bulunur. Bu komutlar hiçbir yapay zeka hizmetine veri göndermez. Bir ekran görüntüsünü Be My AI'ye veya bu eklentinin desteklemediği başka bir uygulamaya yapıştırmak için kullanın. Kopyalama işlemi panodaki önceki içeriğin yerine geçer.

Bunları istediğiniz zaman girdi hareketleri iletişim kutusundan özelleştirmekten çekinmeyin.

### Bir betimlemeyle ilgili ek soru sorma

Bazen yapay zekadan aldığınız yanıt yetersiz kalır. Belki görüntü düşük kalitelidir, eksiktir veya istenmeyen ayrıntılar içerir. Belki yalnızca belirli bir bölüme odaklanmak ya da bağlamı kaybetmeden daha net bir fotoğraf çekmek istersiniz.
Bir betimleme aldıktan sonra NVDA+alt+c tuşlarına basabilir veya Yapay Zeka İçerik Betimleyici bağlam menüsünden (NVDA+shift+i) "Önceki betimlemenin devamı" seçeneğini seçebilirsiniz. Varsayılan olarak odak mesaj alanındadır.
Ek bir görüntü eklemek için sohbet penceresini açık tutun ve eklentiyi normalde yaptığınız gibi kullanın. Bir görüntü alındığında (kameradan, sistem kontrolünden, ekran görüntüsünden vb.) bunu mevcut oturuma eklemek mi yoksa yeni bir oturum başlatmak mı istediğiniz sorulur.

### Bilgisayar kontrolü

Bilgisayar kontrolü, siz bir görevi tarif ettikten sonra Yapay Zeka İçerik Betimleyici'nin etkin uygulamayı fare ve klavyeyle kontrol etmesini sağlar. Elle tamamlanması zor veya erişilemez olan görevlerde yardımcı olabilir.

Bu özellik bir yapay zeka modeline bilgisayarınızın kontrolünü verdiği için dikkatli kullanın. Eklenti başlamadan önce onayınızı ister, eylemleri gerçekleştikçe bildirir ve riskli olabilecek eylemlerden önce size sorar. Yaptıklarından siz sorumlusunuz; bu nedenle oturumu izleyin ve hassas ya da geri alınması zor işlerde kullanmaktan kaçının.

Bilgisayar kontrolünü istediğiniz zaman `NVDA+Control+Shift+P` ile duraklatabilir veya sürdürebilirsiniz. Duraklatıldığında eklenti, siz sürdürene kadar bir sonraki eyleme geçmez.

Eklenti, kontrol durumunu belirtmek için sesli uyarılar kullanır. Yüksek bir bip sesi, modelin kontrolü aldığını veya yeniden devraldığını belirtir. Alçak bir bip sesi, kontrolün siz duraklattığınız için ya da modelin sizden girdi beklediği için duraklatıldığını belirtir. Kısa ve alçak bir hata bip sesi, oturumun bir API hatası nedeniyle durduğunu belirtir.

Bir kontrol oturumu etkinken model, girdi göndermeden önce ne yapacağını duyurur. Bu konuşma bitene kadar hiçbir şey olmaz; duyuruyu kesip eylemin daha erken devam etmesi için `Control` tuşuna basabilirsiniz.

Model bir eylemi nasıl tamamlayacağından emin değilse, daha fazla bilgiye ihtiyaç duyuyorsa veya sırayı başka bir nedenle size geri verirse oturum duraklatılır ve Bilgisayar Kontrolü iletişim kutusu ön plana gelir. Sohbeti sürdürmek için oraya bir ek mesaj yazın veya oturumu durdurmak için iletişim kutusunu kapatın.

Bu özellik yalnızca bilgisayar kontrolü aracı sunan modellerle çalışır: GPT-5.4, GPT-5.4 mini, GPT-5.5, GPT-5.5 pro, GPT-6 Astra, GPT-6.1 Sol, GPT-6.1 Terra, GPT-6 Luna, Claude 4.5 Sonnet, Claude 4.5 Opus, Claude 4.6 Sonnet, Claude 4.6 Opus, Claude 4.7 Opus, Claude 4.8 Opus, Claude 5 Sonnet, Claude 5 Opus, Claude 5 Fable, Claude 5.1 Fable, Claude 5.2 Fable, Claude 5.5 Haiku, Claude 5.5 Sonnet ve Claude 5.5 Opus. Diğer modeller görselleri betimleyebilir, ancak bilgisayar kontrolü için gereken yapılandırılmış fare ve klavye eylemlerini sağlamaz.

Bilgisayar kontrolünü kullanmak için:

1. Desteklenen modellerden birini yapılandırın ve seçin.
2. Modelin üzerinde çalışmasını istediğiniz uygulamayı veya pencereyi açın.
3. `NVDA+shift+i` tuşlarına basın, ardından "Bilgisayarı kontrol et..." seçeneğini seçin.
4. Yapılmasını istediğiniz görevi yazın ve Gönder'e basın.
5. Onay istemini inceleyin. Oturuma izin verirseniz eylemleri izleyin ve riskli eylem istemlerini onaylayın veya iptal edin.

Not: Bu özellik beta aşamasında kabul edilmelidir; uygulamayı daha sağlam hale getirmek için aktif olarak çalışıyoruz.

## Bağımlılıklar

Bu eklentinin ihtiyaç duyduğu bazı kütüphaneler eklenti paketine dahil edilemeyecek kadar büyüktür. Bunun yerine, eklenti kurulu olarak NVDA ilk kez başladığında bunları indirmek isteyip istemediğiniz sorulur. Evet'i seçin, indirmenin bitmesini bekleyin; ardından NVDA yeniden başlar.

İndirilen dosya, NVDA sürümünüze bağlı olarak yaklaşık 35 ile 70 MB arasında bir zip dosyasıdır. Bu deponun [libs-release](https://github.com/cartertemm/AI-content-describer/releases/tag/libs-release) sayfasından gelir. GitHub'a erişilemezse eklenti, Çin NVDA topluluğunun sağladığı bir yansı sunucuyu denemeyi önerir.

Zip dosyası şunları içerir:

* [NumPy](https://numpy.org/): diziler üzerinde matematik işlemleri; OpenCV için gereklidir.
* [OpenCV](https://opencv.org/) (`cv2`): yüz algılama özelliği için web kamerası görüntülerinde yüzünüzü bulur.
* [Pillow](https://python-pillow.org/) (`PIL`): ekran görüntüleri alır ve bunları yapay zeka modellerinin okuyabileceği görüntülere dönüştürür.
* [Markdown](https://python-markdown.github.io/): betimlemeleri başlıklar, listeler ve tablolar gibi biçimlendirmelerle gösterir.
* [pygrabber](https://github.com/andreaschiavinato/python_grabber): bilgisayarınızdaki web kameralarını listeler.
* Python standart kütüphanesinin NVDA'ya dahil olmayan birkaç modülü (`html`, `xml`, `pathlib`, `secrets` ve `_markupbase`). Yukarıdaki kütüphaneler bunlara ihtiyaç duyar.

Dosyalar, `aic-py-` ve ardından NVDA'nın Python sürümünden oluşan bir klasöre (örneğin `aic-py-3.13`) yerleştirilir. Bu klasör NVDA kullanıcı yapılandırma klasörünüzde, genellikle `%APPDATA%\nvda` içinde bulunur. Her Python sürümünün kendi klasörü vardır; yani yeni bir NVDA sürümü Python sürümünü değiştirdiğinde eklenti kütüphaneleri yeniden indirir. Eklentiyi kaldırmak, NVDA'nın geçerli Python sürümüne ait klasörü siler.

İndirme çalışmazsa kütüphaneleri kendiniz kurabilirsiniz. libs-release sayfasından `aic-py-3.13.zip` dosyasını (veya NVDA'nızın Python sürümüne uygun dosyayı) indirin, NVDA kullanıcı yapılandırma klasörünüze çıkarın ve NVDA'yı yeniden başlatın.

## Eklentiyi oluşturma

Eklenti paketini kaynaktan oluşturmak için ihtiyacınız olacaklar:

* Python dağıtımı (3.7 veya üzeri önerilir). Windows Yükleyicileri için [Python Web Sitesini](https://www.python.org) kontrol edin. Şu anda NVDA kaynak kodunun ve içerdiği üçüncü taraf modüllerin hazırlanmasının Python 3.7'nin 32 bit sürümünü gerektirdiğini lütfen unutmayın.
* Scons - [Web sitesi](https://www.scons.org/) - sürüm 4.3.0 veya üzeri. PIP aracılığıyla kurabilirsiniz. `pip install scons`
* Markdown 3.3.0 veya üzeri. `pip install markdown`

Ardından tercih ettiğiniz terminali açın:

```
git clone https://github.com/cartertemm/AI-content-describer.git
cd AI-content-describer
scons
```

`scons` komutunun yürütülmesi tamamlandıktan sonra, bu deponun kök dizinine test ve yayına hazır bir *.nvda-addon dosyası yerleştirilir.

Çevrilmesi gereken yeni dizeler eklerseniz .pot dosyasını şu şekilde yeniden oluşturmanız önemlidir:

```
scons pot
```

## Nasıl çeviri yapılır?

Bir Windows bilgisayarda:

* [poedit](https://poedit.net/) programını indirin. Her mesajı İngilizceden çevirmek için bu yazılımı kullanacaksınız.
* Tüm dizeleri içeren .pot dosyasını [buradan](https://raw.githubusercontent.com/cartertemm/AI-content-describer/main/AIContentDescriber.pot) indirin
* İndirdiğiniz dosyayı poedit programında açın. Açılan pencerede "Yeni çeviri oluştur"a tıklayın, ardından hedef dili seçin.
* Kaynak metnin içeriğini sırayla hedef dile çevirin ve çeviri alanına yapıştırın. Ek yardım için liste öğesine sağ tıklayıp -> kod konumları'nı seçebilir, ardından bir satır yukarı çıkarak "# Translators: " ile başlayan yorumu okuyabilirsiniz. Bu yorumlar ayrıca .pot dosyasında tek bir yerde toplanmıştır.
* Bitirdiğinizde dosya -> kaydet'e tıklayın veya ctrl+s tuşlarına basın, ardından yeni .mo ve .po dosyalarının kaydedileceği konumu seçin. Bana e-postayla gönderilmesi veya bir çekme isteğine eklenmesi gereken dosyalar bunlardır.
* readme.md dosyasının (bu dosyanın) içeriğini çevirin. Onu da ekleyin!

## Katkılar

Tüm katkılar çok takdir edilir ve katkıda bulunanlar belirtilir.
Aşağıdaki kişiler eklenti üzerinde çalışmıştır.

* [Cary Rowen](https://github.com/cary-rowen): bağımlılık yansılama ile eklentinin Çinli kullanıcılar için çalışmasını sağladı, Vivo Blue sağlayıcısı desteğini ekledi
* [Mazen](https://github.com/mzanm): Markdown uygulaması, diğer kod katkıları
* [Kostenkov-2021](https://github.com/Kostenkov-2021): Rusça çeviri
* [Nidza07](https://github.com/nidza07): Sırpça çeviri
* [Heorhii Halas](nvda.translation.uk@gmail.com) ve [George-br](https://github.com/George-br): Ukraynaca çeviri
* [Umut Korkmaz](umutkork@gmail.com): Türkçe çeviri
* [Platinum_Hikari](urbain_onces.0r@icloud.com): Fransızca çeviri
* [Lukas](https://4sensegaming.cz): Çekçe çeviri
* [Michaela](https://technologiebezzraku.sk): Slovakça çeviri
* [loginerror](https://github.com/theloginerror): Lehçe çeviri

Bir sorun mu buldunuz? Sorunu [sorun izleyiciye](https://github.com/cartertemm/AI-content-describer/issues) gönderin

Yeni bir özellik öneriniz mi var? Bunun için de bir bilet oluşturun, uygulamaya geçirme konusunu konuşabiliriz. İlgili sorunları olmayan çekme istekleri incelenecek, ancak özellikle yeni düzeltmenin veya işlevselliğin önerilenden farklı çalışması gerektiğine karar verirsem muhtemelen herkes için daha fazla zaman alacaktır.

Çeviriler açık kollarla karşılanır. Bu güçlü teknolojiye ne kadar çok insan erişebilirse o kadar iyi!

Github'ınız yoksa veya kullanmamayı tercih ediyorsanız, [bana bir e-posta gönderebilirsiniz](mailto:carter@ctemm.me) - carter (at) ctemm (dot) me.

Destek için teşekkürler!
