# 📅 Shift & Task Planner – Vardiya ve Görev Atama Sistemi

Bu proje, belirli bir tarih aralığında çalışanlara vardiya (shift) ve görev (task) ataması yapar. Atamalar rastgele olarak gerçekleştirilir ve sonuçlar hem Excel dosyası olarak kaydedilir hem de grafiksel olarak görselleştirilir.

---

## 🚀 Özellikler

- 15 günlük planlama dönemi oluşturur
- 5 çalışan için rastgele vardiya atamaları yapar (%90 olasılıkla)
- Vardiyalara görev atamaları yapar (%80 olasılıkla)
- Her kayıt için `AssignType` değeri üretir (örneğin: BoldIQ, Manual vs.)
- Çıktıları Excel dosyası ve grafik görseli olarak dışa aktarır

---

## 📂 Oluşan Dosyalar

- `planlama_verisi.xlsx`: 
  - Schedule (plan bilgisi)
  - ScheduleAssignedShift (vardiyalar)
  - ScheduleAssignedTask (görevler)
- `veri_gorsel_analiz.png`: Atama türlerine göre grafiksel analiz

---

## 🔢 AssignType Açıklamaları

| Kod | Açıklama        |
|-----|-----------------|
| 0   | BoldIQ          |
| 1   | Manual          |
| 2   | Unassigned      |
| 3   | Unscheduled     |
| 4   | Shift Changed   |

---

## ⚙️ Gereksinimler

```bash
pip install pandas matplotlib seaborn xlsxwriter
