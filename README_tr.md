# Pulsar
Windows ve MacOS için [Nebula örgüsel ağ](https://github.com/slackhq/nebula) komut satırı arayüzü istemcisi için Python tabanlı bir grafik arabirim.


Wiki'deki belgeleri okuyun

Pulsar, JS Prodüksiyon Ltd. Şti. ve GNU GPL v3.0 lisansı altında sunulmaktadır.

Bu belge şu dillerde de mevcuttur: [Almanca (Deutsch)](README_de.md) ve [İngilizce (English)](README.md)

Bu belge en son 2024-06-12 tarihinde güncellenmiştir.


## Nebula Sürümü
Nebula istemcisi derlenmiş sürüm 1.8.2

## Pulsar'ın Gerekçesi
Nebula örgüsel ağ ne kadar güzel olursa olsun, uygulanması bayağı bir teknik bilgi gerektirir. Birçok kullanıcı, Nebula'yı düzgün bir şekilde çalıştırmak için gerekli komut istemi komutlarını işleyecek kadar teknik olarak bilgili değildir. Şirketimizde bu tür kullanıcımız olduğu için, kullanıcının Nebula ağına bağlanmasına mümkün kılmak için basit bir grafik arabirimi yazmamız gerekiyordu. Kurulumda bilgi işlem departmanı tarafından biraz yardım gerekir. Ancak bir kez çalıştıktan sonra kullanımı oldukça kolaydır. 


## İşletim Sistemi Uyumluluğu

| İşletim Sistemi    | Kaynak        | Derlenmiş hal |
| ------------------ | ------------- | ------------- |
| Windows 11         | Çalışıyor     | Çalışıyor     |
| Windows 10         | Denenmedi     | Çalışıyor     |
| Windows 7          | Denenmedi     | Çalışmıyor    |
| MacOS 13.6 (Intel) | Çalışıyor     | Çalışıyor     |
| MacOS 14.2 (M1)    | Kısmi çalışıyor | Kısmi çalışıyor |

Teknolojik bakış açısından, Pulsar, Python 3.11 ve Nebula istemcisini sürdürebilen herhangi bir işletim sisteminde çalışmalıdır. Python 3.11, PyQT 6.7 ve Nebula sistem gereksinimlerine bakarak tüm platformları test etme olanağımız olmasa da, bu uygulama aşağıdaki işletim sistemlerinde çalışacaktır:

* **Windows:** 11, 10
* **macOS:** Sonoma 14, Ventura 13, Monterey 12, Big Sur 11

Linux üzerinde çalışmak için bu uygulamaya ihtiyacımız olmadığından, bu işlevselliği eklemedik. Ancak, yazılımı indirip Linux için kendiniz geliştirmek isterseniz buyurun.

PyQT 6 ve Mac M1 yonga seti uyumsuzlukları, sistem dosyası seçici iletişim kutusunun açılmasına ve metin kutularına içerik yapıştırılmasının başarısız olmasına neden olur. Ancak, gerekli bilgiler elle yazılırsa uygulama çalışır. [Ayrıntılar için Wiki'ye bakın](https://github.com/JS-Produksiyon/pulsar/wiki/Usage#issues-with-pulsar-on-macos-on-m-series-chips).

> Bu aralar kendi ihtiyaçlarımızdan dolayı Windows yazılımına odaklandığımızdan dolayı Pulsar’ın _Mac OS sürümüne çok az ilgi vermekteyiz_. Haberiniz olsun.


## Kurulum
### Hazır Sürümler
Pulsar için Windows ve MacOS'ta çalışan ikili sürümleri [Releases](releases/) sayfasını ziyaret ederek bulabilirsiniz.

En son sürümü indirin, sıkışdırılımısş dosyayı seçtiğiniz bir konuma ayıklayın ve içindeki yazılımı çalıştırın. Pulsar'ın kullanılması için kurulmasına gerek yoktur.

Windows'da Başlat menüsüne veya MacOS'ta Başlatıcı'ya manuel olarak Pulsar'a bir kısayol bağlantısı ekleyebilirsiniz


### Kaynaktan Çalıştırma
Pulsar'ın çalışması için Python 3.11 gerekir.

`git clone https://github.com/JS-Produksiyon/pulsar.git` komutunu kullanarak bir CLI (Windows'ta PowerShell veya MacOS'ta Terminal) açarak Pulsar'ın kaynak kodunu makinenize kopyalayabilirsiniz. 

Klonlandıktan sonra sanal bir ortam oluşturun: `python3.11 -m venv venv`

Windows'ta sanal ortamı `venv\Scripts\Activate.ps1` veya MacOS'ta `source venv/bin/activate` ile etkinleştirin .

`pip install -r requirements.txt` komutunu kullanarak gerekli paketleri kurun.

Gereksinimler yüklendikten sonra programı `python src/pulsar.py` komutuyla çalıştırın.


## Kullanım
Nebula komut istemi istemcisinin yetkili kullanıcı erişimine ihtiyacı olması nedeniyle Pulsar, Windows'ta bir UAC istemiyle veya MacOS'ta parolanızı isteyerek yetkilerini otomatik olarak yükseltmeye çalışacaktır.

İlk çalıştırmada Pulsar, gerekli Nebula `.yaml` yapılandırma dosyasını seçmenizi isteyecektir. Bunu seçtikten sonra, _Ayarları Kaydet_ düğmesine tıklayın ve büyük yeşil düğmeye tıklayarak Nebula ağına hemen bağlanabilmelisiniz.

> Bilgi işlem departmanının Nebula CA dosyasını, kullanıcı özel anahtarını ve sertifika dosyalarını '.yaml' yapılandırma dosyasıyla birlikte sağlaması gerekir.

Pulsar penceresinin kapatılması programı sonlandırmaz. Bunu, _Pulsar'ı Kapat_ düğmesine tıklayarak veya Pulsar simgesi Sistem Tepsisi'ne sağ tıklayarak (Windows) veya Menü Çubuğundaki Pulsar simgesine tıklayıp _Kapat_ öğesini seçerek yapmanız gerekir. 

Ek olarak, Pulsar, kullanıcının erişmesi gereken çeşitli kaynaklara kolay alan adı tabanlı erişim sağlamak için yerel `hosts` dosyasına girişler ekleme seçeneği sunar.

> `hosts` dosya formatındaki bu IP Adresi / Ana Bilgisayar Adı çiftlerinin bilgi işlem departmanı tarafından sağlanması gerekir.


## Uygulamanın adı neden "Pulsar"?
Nebula örgü ağ aracı, adını birçok yıldız içeren parlak gazlardan oluşan göksel cisimden almıştır. Bir örgü ağı oldukça şekilsizdir ve birçok düğüm de içerir. Bu uygulama, nebuladaki bir yıldızın var olması gibi, bir düğümün ağa bağlanmasını mümkün kılar. Ve bağlanmak için bir sinyal çıkardığı için, belirli bir frekansta titreşen manyetize bir nötron yıldızı olan pulsarın görüntüsü uygun bir görüntü gibi görünüyordu. Böylece Nebula'ya bağlanmak için Pulsar'ı kullanırsınız.



