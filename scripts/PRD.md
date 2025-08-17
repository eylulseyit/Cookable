# Product Requirements Document (PRD)  
**Proje:** AI-First Development Capstone Project – Recipe Recommendation App  
**Versiyon:** 1.0  
**Hazırlayan:** Eylül  
**Tarih:** 17 Ağustos 2025  

---

## 1. Proje Özeti

Bu proje, kullanıcının elindeki malzemeleri girerek yapabileceği tarifleri öneren bir yapay zekâ destekli uygulamadır.  
Amaç, kullanıcıya hızlı, doğru ve kişiselleştirilmiş tarif önerileri sunarak yemek hazırlama sürecini kolaylaştırmaktır.  

Proje, capstone sürecinde ilk prototip olarak geliştirilecek ve ilerleyen dönemlerde kullanıcı hesabı yönetimi, sesli giriş, alışveriş listesi çıkarma gibi özellikler eklenebilecektir.  

---

## 2. Hedef Kullanıcı Kitlesi

- Evde yemek yapan kullanıcılar  
- Yemek planlamasını kolaylaştırmak isteyen kişiler  
- Malzeme bazlı tarif önerisi arayan kullanıcılar  

---

## 3. Kullanıcı Akışı

### 3.1 Ana Sayfa
- Kullanıcı uygulamaya giriş yapar ve malzeme listesi girmesi gerektiğini belirten sade bir ekran görür.  

### 3.2 Malzeme Girişi
- Kullanıcı elindeki malzemeleri metin olarak yazar ve “Gönder” butonuna tıklar.  
- Gelecekte sesli giriş opsiyonu eklenebilir.  

### 3.3 Opsiyonel Filtre Seçimi
- Kullanıcı, tarif önerileri için isteğe bağlı filtreler seçebilir (ör. vejetaryen, düşük kalorili).  

### 3.4 AI Destekli Tarif Önerisi
- Backend, kullanıcıdan gelen malzeme listesini alır.  
- Açık kaynak büyük dil modeli ile uygun tarifler üretilir ve frontend’e iletilir.  

### 3.5 Tarif Gösterimi
- Kullanıcıya önerilen tarif aşağıdaki bilgilerle gösterilir:  
  - Tarif adı  
  - Malzeme listesi  
  - Pişirme adımları  
  - Yaklaşık süre  

### 3.6 Yeni Sorgu veya Çıkış
- Kullanıcı yeni bir malzeme listesi girmek isterse süreç tekrarlanır veya uygulamadan çıkabilir.  

#### Akış Şeması (Metin)
[ Ana Sayfa ]
↓
[ Malzeme Girişi ]
↓
[ Opsiyonel: Filtre Seçimi ]
↓
[ AI Destekli Tarif Önerisi ]
↓
[ Tarif Gösterimi ]
↓
[ Yeni Sorgu veya Çıkış ]


---

## 4. Temel Özellikler

- Malzeme bazlı tarif önerisi  
- AI destekli öneri sistemi (açık kaynak LLM kullanımı)  
- Opsiyonel filtreleme (diyet tercihlerine göre)  
- Tarif detaylarını gösterme (isim, malzemeler, adımlar, süre)  
- Basit ve kullanıcı dostu arayüz  

**İlerleyen Dönemde Eklenebilecek Özellikler:**  
- Kullanıcı hesabı / oturum yönetimi  
- Tarif kaydetme ve paylaşma  
- Haftalık yemek planı önerisi  
- Sesli malzeme girişi  
- Alışveriş listesi oluşturma  

---

## 5. Teknik Gereksinimler

### 5.1 Backend
- Python 3.12 + FastAPI  
- AI modeli entegrasyonu ve veri işleme  

### 5.2 Frontend
- Next.js (React tabanlı)  
- Malzeme girişi, filtre seçimi ve tarif gösterimi  

### 5.3 Yapay Zekâ ve AI
- Açık kaynak büyük dil modeli  
- Metin analizi ve tarif önerisi  
- Tarif özetleme ve filtreleme  

### 5.4 Veritabanı
- SQLite (hafif ve kolay yönetilebilir)  
- Kullanıcı sorguları ve tarif verilerinin depolanması  

### 5.5 Versiyon Kontrol ve Proje Yönetimi
- Git ve GitHub  

### 5.6 Dağıtım
- Frontend: Vercel  
- Backend: Railway  

### 5.7 İleriki Dönem Planları
- Vektör tabanlı veri tabanı ile metin arama ve tavsiye sistemi  
- Çok adımlı AI işlemleri ve agent mimarisi  
- Sesli malzeme girişinin eklenmesi  

---

## 6. Başarı Kriterleri

- Kullanıcı malzeme listesi girdiğinde, doğru ve anlamlı tarif önerisi alması  
- Kullanıcı arayüzünün sade, hızlı ve kullanıcı dostu olması  
- AI modeli ile öneri sürecinin güvenilir ve hatasız çalışması  
- Prototip süresince temel akışın eksiksiz uygulanması  

---

## 7. Sınırlamalar

- İlk prototip yalnızca metin tabanlı malzeme girişini destekler  
- Kullanıcı hesabı ve kişiselleştirme özellikleri ilk sürümde yok  
- AI önerileri, eğitim verisi ve model kapasitesi ile sınırlı  

---

## 8. Notlar

- Projenin ilerleyen sürümlerinde kullanıcı deneyimini artıracak yeni özellikler eklenebilir.  
- AI modelinin performansı ve doğruluğu düzenli olarak test edilmelidir.  
- Cursor’da markdown formatında hazırlanmış bu PRD, hem geliştirme sürecinde rehber hem de paydaşlarla paylaşım için uygundur.
