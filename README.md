# BDZYS - Belediye Demirbaş ve Zimmet Yönetim Sistemi

Bu proje, belediye bünyesinde kullanılan demirbaşların (envanterlerin) takibi ve personele zimmetlenmesi süreçlerini yönetmek amacıyla geliştirilmiştir. Sistem, gerçek kullanım senaryoları dikkate alınarak tasarlanmış olup, merkezi ve kontrollü bir yönetim sağlamayı hedefler.

---

## Projenin Amacı

Demirbaşların:

* kayıt altına alınması
* personele atanması (zimmetlenmesi)
* durumlarının takip edilmesi
* geçmiş işlemlerinin izlenmesi

gibi süreçleri tek bir sistem üzerinden yönetmek.

---

## Özellikler

### Envanter Yönetimi

* Demirbaş ekleme, güncelleme ve silme
* Kategori bazlı sınıflandırma
* Durum takibi (stokta, zimmetli, arızalı, hurda)

### Personel ve Birim Yönetimi

* Personel kayıt sistemi
* Birim bazlı yapı
* Kullanıcıların belirli birime atanması

### Zimmet İşlemleri

* Demirbaşların personele zimmetlenmesi
* İade işlemleri
* Zimmet durumuna göre demirbaşın otomatik güncellenmesi

### Yetkilendirme

* Admin kullanıcılar tüm verilere erişebilir
* Birim yetkilileri sadece kendi birimlerine ait verileri görebilir

### Denetim (Audit Log)

* Sistem üzerinde yapılan ekleme, güncelleme ve silme işlemleri kayıt altına alınır
* Hangi kullanıcının hangi işlemi yaptığı izlenebilir

### Raporlama

* Toplam demirbaş sayıları
* Kategori dağılımı
* Birim dağılımı
* Son zimmet hareketleri
* CSV export özelliği

### PDF Çıktı

* Zimmet kayıtları PDF formatında dışa aktarılabilir

---

## Teknik Detaylar

* Zimmet işlemleri sırasında demirbaş durumu, Django **signal** yapısı kullanılarak otomatik olarak güncellenmektedir.
* Rol bazlı yetkilendirme ile kullanıcılar sadece kendi birimlerine ait verilere erişebilir.
* Audit log sistemi sayesinde tüm kritik işlemler kayıt altına alınmaktadır.

---

## Proje Yapısı

```
envanter   → Demirbaş, personel ve birim yönetimi  
zimmet     → Zimmet işlemleri  
auditlog   → Sistem log kayıtları  
raporlar   → Dashboard ve analiz ekranları  
core       → Proje genel ayarları  
users      → Kullanıcı yönetimi  
```

---

## Kullanılan Teknolojiler

* Python
* Django
* PostgreSQL
* Bootstrap
* ReportLab (PDF üretimi)

---

## Kurulum

Projeyi çalıştırmak için:

```bash
git clone https://github.com/kaansrl/belediye-zimmet-yonetim-sistemi.git
cd belediye-zimmet-yonetim-sistemi

pip install -r requirements.txt

python manage.py migrate
python manage.py runserver
```

---

## Ekran Görüntüleri

### Dashboard (Raporlama Ekranı)
<img width="1865" height="863" alt="image" src="https://github.com/user-attachments/assets/6852b47a-ce26-4c47-9b56-6e1f8df5a12c" />

---

### Admin Paneli
<img width="1253" height="868" alt="image" src="https://github.com/user-attachments/assets/219dd647-9de9-4311-8a78-e891a0d3cca6" />

---
## Not

Bu proje, staj süreci kapsamında geliştirilmiş olup gerçek bir kurumda kullanılabilecek bir sistem mantığıyla tasarlanmıştır.
