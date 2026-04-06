# BDZYS - Belediye Demirbaş ve Zimmet Yönetim Sistemi

Bu proje, belediye bünyesinde kullanılan demirbaşların (envanterlerin) takibi ve personele zimmetlenmesi süreçlerini yönetmek amacıyla geliştirilmiştir. 

Staj süreci boyunca, gerçek bir kurumda karşılaşılabilecek ihtiyaçlar göz önünde bulundurularak tasarlanmıştır.

---

## Projenin Amacı

Demirbaşların:
- kayıt altına alınması
- personele atanması (zimmetlenmesi)
- durumlarının takip edilmesi
- geçmiş işlemlerinin izlenmesi

gibi süreçleri merkezi ve kontrollü bir şekilde yönetmek.

---

## Özellikler

### Envanter Yönetimi
- Demirbaş ekleme, güncelleme ve silme
- Kategori bazlı sınıflandırma
- Durum takibi (stokta, zimmetli, arızalı, hurda)

### Personel ve Birim Yönetimi
- Personel kayıt sistemi
- Birim bazlı yapı
- Kullanıcıların belirli birime atanması

### Zimmet İşlemleri
- Demirbaşların personele zimmetlenmesi
- İade işlemleri
- Zimmet durumuna göre demirbaşın otomatik güncellenmesi

### Yetkilendirme
- Admin kullanıcılar tüm verileri görebilir
- Birim yetkilileri sadece kendi birimlerine ait verileri görebilir

### Denetim (Audit Log)
- Sistemde yapılan ekleme, güncelleme ve silme işlemleri kayıt altına alınır
- Hangi kullanıcı ne yaptı bilgisi tutulur

### Raporlama
- Toplam demirbaş sayıları
- Kategori dağılımı
- Birim dağılımı
- Son zimmet hareketleri
- CSV export özelliği

### PDF Çıktı
- Zimmet kayıtları PDF formatında dışa aktarılabilir

---

## Kullanılan Teknolojiler

- Python
- Django
- PostgreSQL
- Bootstrap
- ReportLab (PDF üretimi)

---

## Kurulum

Projeyi çalıştırmak için:

```bash
git clone https://github.com/kaansrl/belediye-zimmet-yonetim-sistemi.git
cd belediye-zimmet-yonetim-sistemi

pip install -r requirements.txt

python manage.py migrate
python manage.py runserver
