import pandas as pd  
import random 
from datetime import datetime, timedelta  
from pathlib import Path 
import webbrowser  
import matplotlib.pyplot as plt  
import seaborn as sns  

# 1. Schedule tablosu oluşturuluyor (planlama dönemi bilgisi)
schedule_id = 500  
date_start = datetime(2025, 5, 1)  
date_end = datetime(2025, 5, 15)  

# Tek satırlık planlama verisi tabloya yazılıyor
df_schedule = pd.DataFrame([{
    "ScheduleId": schedule_id,
    "StartDate": date_start.date(),
    "EndDate": date_end.date()
}])

print("\n📅 Schedule tablosu:")
print(df_schedule)  

# 2. Shift tablosu oluşturuluyor (çalışanlara vardiya ataması)
employee_ids = [18001, 18002, 18003, 18004, 18005]  
shift_base_id = 10000  
shift_records = []  
shift_counter = 0  

# Her çalışana her gün için vardiya ataması yapılır
for emp_id in employee_ids:
    for i in range(15):  # 15 günlük süre
        if random.random() < 0.9:  # %90 olasılıkla vardiya ver
            shift_start = date_start + timedelta(days=i, hours=random.choice([7, 9, 13]))  # Vardiya başlama zamanı
            shift_end = shift_start + timedelta(hours=8)  # Vardiya 8 saat sürer
            shift_records.append({
                "Id": shift_base_id + shift_counter,
                "ScheduleId": schedule_id,
                "EmployeeId": emp_id,
                "ShiftId": 3000 + shift_counter,
                "ShiftStart": shift_start,
                "ShiftEnd": shift_end,
                "AssignType": random.randint(0, 4)  # Atama türü rastgele belirlenir
            })
            shift_counter += 1

# Shift kayıtları tabloya aktarılır
df_shifts = pd.DataFrame(shift_records)

print("\n👷‍♂️ Shift tablosu:")
print(df_shifts.head())  

# 3. Task tablosu oluşturuluyor (vardiyalara görev ataması)
task_base_id = 2000  
task_records = []
task_counter = 0

# Shift'lere görev ataması yapılır (%80 olasılıkla)
for _, row in df_shifts.iterrows():
    if random.random() < 0.8:
        task_start = row["ShiftStart"] + timedelta(minutes=random.choice([0, 30, 60]))
        task_end = task_start + timedelta(hours=1)
        task_records.append({
            "Id": task_counter + 1,
            "ShiftId": row["ShiftId"],
            "TaskId": task_base_id + task_counter,
            "TaskStart": task_start,
            "TaskEnd": task_end,
            "AssignType": random.randint(0, 4)
        })
        task_counter += 1

# Task kayıtları tabloya aktarılır
df_tasks = pd.DataFrame(task_records)

print("\n📝 Task tablosu:")
print(df_tasks.head()) 

# 4. AssignType açıklamaları
assign_type_map = {
    0: "BoldIQ",
    1: "Manual",
    2: "Unassigned",
    3: "Unscheduled",
    4: "Shift Changed"
}

# Sayısal değerler açıklayıcı metne çevriliyor
df_shifts["AssignLabel"] = df_shifts["AssignType"].map(assign_type_map)
df_tasks["AssignLabel"] = df_tasks["AssignType"].map(assign_type_map)

# 5. Veriler Excel dosyasına yazılıyor
excel_dosya_adi = "planlama_verisi.xlsx"

with pd.ExcelWriter(excel_dosya_adi, engine="xlsxwriter") as writer:
    df_schedule.to_excel(writer, sheet_name="Schedule", index=False)
    df_shifts.to_excel(writer, sheet_name="ScheduleAssignedShift", index=False)
    df_tasks.to_excel(writer, sheet_name="ScheduleAssignedTask", index=False)

    # Otomatik sütun genişliği ayarı
    for sheet, df in zip(["Schedule", "ScheduleAssignedShift", "ScheduleAssignedTask"],
                         [df_schedule, df_shifts, df_tasks]):
        worksheet = writer.sheets[sheet]
        for i, col in enumerate(df.columns):
            width = max(df[col].astype(str).map(len).max(), len(col)) + 2
            worksheet.set_column(i, i, width)

# Excel dosyasının kaydedildiği yol yazdırılır
dosya_yolu = Path(excel_dosya_adi).absolute()
print(f"\n✅ Excel dosyası başarıyla oluşturuldu:\n{dosya_yolu}")

# Kullanıcıya dosyayı açmak isteyip istemediği sorulur
while True:
    cevap = input("\nExcel dosyasını açmak ister misiniz? [E/H]: ").strip().upper()
    if cevap in ['E', 'H']:
        break
    print("Lütfen geçerli bir seçenek girin (E veya H)")

if cevap == 'E':
    try:
        webbrowser.open(f"file://{dosya_yolu}")  
        print("Excel dosyası açılıyor...")
    except Exception as e:
        print(f"Dosya açılırken hata oluştu: {e}")
else:
    print("Excel dosyası açılmadı. İstediğiniz zaman bu konumdan ulaşabilirsiniz:")
    print(dosya_yolu)

# 6. Grafik ile analiz fonksiyonu tanımlanır
def visualize_data():
    plt.style.use("ggplot")

    labels = ["BoldIQ (0)", "Manual (1)", "Unassigned (2)", "Unscheduled (3)", "Shift Changed (4)"]
    colors = ["#4CAF50", "#F44336", "#9E9E9E", "#FFEB3B", "#673AB7"]

    shift_counts = df_shifts["AssignType"].value_counts().sort_index()
    task_counts = df_tasks["AssignType"].value_counts().sort_index()

    df_schedule["Duration"] = (pd.to_datetime(df_schedule["EndDate"]) - pd.to_datetime(df_schedule["StartDate"]))\
                                .dt.days  # Plan süresi hesaplanır

    fig, axes = plt.subplots(3, 1, figsize=(12, 18))  # 3 grafik çizimi için hazırla

    # Shift grafiği
    axes[0].bar(labels, shift_counts, color=colors, edgecolor="black")
    for bar, count in zip(axes[0].patches, shift_counts):
        axes[0].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                     str(count), ha='center', fontsize=11, fontweight='bold')
    axes[0].set_title("Shift AssignType Dağılımı", fontsize=14)
    axes[0].set_ylabel("Vardiya Sayısı")

    # Task grafiği
    axes[1].bar(labels, task_counts, color=colors, edgecolor="black")
    for bar, count in zip(axes[1].patches, task_counts):
        axes[1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                     str(count), ha='center', fontsize=11, fontweight='bold')
    axes[1].set_title("Task AssignType Dağılımı", fontsize=14)
    axes[1].set_ylabel("Görev Sayısı")

    # Schedule süresi grafiği
    axes[2].bar(df_schedule["ScheduleId"].astype(str), df_schedule["Duration"],
                color="#3F51B5", edgecolor="black")
    axes[2].set_title("Schedule Süresi (gün olarak)", fontsize=14)
    axes[2].set_ylabel("Gün")
    axes[2].set_xlabel("Schedule ID")

    plt.tight_layout()
    plt.savefig("veri_gorsel_analiz.png", dpi=300)  
    print("\n📊 Grafik görseli kaydedildi: veri_gorsel_analiz.png")
    plt.show()  

# Fonksiyon çağrılarak grafikler oluşturulur
visualize_data()