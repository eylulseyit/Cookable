# Capstone Project Tasks

## Faz 1: Fikir ve Planlama (Tamamlandı)
- [x] Problem tanımı ve fikir üretimi (PRD.md ile yapıldı).
- [x] Kullanıcı akışı ve teknoloji seçimi (PRD.md içinde tanımlandı).

## Faz 2: Kodlama ve AI Entegrasyonu (Tamamlandı)
- [x] GitHub reposu kuruldu ve proje yapılandırıldı.
- [x] Temel özellik geliştirildi (Malzeme girişi -> AI Tarif çıktısı).
- [x] Google Gemini LLM entegrasyonu sağlandı.

## Faz 3: Otomasyon ve Ajans Mantığı (Tamamlandı)
- [x] Tarifi analiz edip alışveriş listesi çıkaran bir otomasyon kur.
- [x] Alışveriş listesi özelliği backend'e eklendi (RecipeService üzerinde).
- [ ] LangChain kullanarak daha yetenekli bir "Gurme Asistan Ajanı" oluştur.
  - [x] Ajan için gerekli `langchain_experimental` paketini kur.
  - [x] Ajanın kullanacağı "araçları" (tool) oluştur:
    - [x] Tarif Varyasyonu Aracı
    - [x] İçecek Eşleştirme Aracı
    - [x] Sunum Önerisi Aracı
  - [x] Ajanı ve frontend'in kullanacağı yeni API endpoint'ini oluştur.
  - [x] Frontend'e ajan özelliklerini kontrol edecek butonları ekle.
  - [x] Ajan sonuçlarını gösterecek modern bir UI bileşeni (modal/card) tasarla.

## Faz 4: RAG veya Fine-tuning Uygulaması (Tamamlandı)
- [x] Mevcut tarifleri saklamak için bir VectorDB entegrasyonu yap (Chroma, FAISS vb.).
- [x] Kullanıcının malzemelerine en uygun tarifi VectorDB'den bulan bir RAG (Retrieval-Augmented Generation) sistemi kur.

## Faz 5: Yayınlama ve Demo
- [ ] Frontend uygulamasını Vercel'e dağıt.
- [ ] Backend uygulamasını Railway'e dağıt.
- [ ] Proje için bir tanıtım sayfası (Landing Page) oluştur.
- [ ] Projenin demo videosunu veya GIF'ini hazırla.
