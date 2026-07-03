import os
import sys
from datetime import datetime
from google import genai

# 1. API Anahtarı Kontrolü
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    print("Hata: GEMINI_API_KEY bulunamadı!")
    sys.exit(1)

client = genai.Client(api_key=api_key)

# 2. Günün Tarihini Al
bugunun_tarihi = datetime.now().strftime("%d.%m.%Y")

# 3. Medya_AI.txt dosyasını oku
try:
    with open("Medya_AI.txt", "r", encoding="utf-8") as f:
        protokol_metni = f.read()
except FileNotFoundError:
    print("Hata: Medya_AI.txt dosyası bulunamadı!")
    sys.exit(1)

# 4. Tarih Enjeksiyonu
guncellenmis_prompt = protokol_metni.replace("[gün, ay, yıl]", bugunun_tarihi)

print(f"{bugunun_tarihi} tarihi için Medya Anlatı Analizi başlatılıyor...")

try:
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=guncellenmis_prompt,
    )
    
    # AI çıktısını Markdown'dan HTML satır sonlarına basitçe uyarlayalım
    rapor_icerigi = response.text.replace("\n", "<br>")
    
    # 5. Web sayfası (index.html) oluşturma
    html_sablonu = f"""<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Medya Anlatı Analizi - {bugunun_tarihi}</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f7f6; color: #333; line-height: 1.6; padding: 20px; }}
        .container {{ max-width: 900px; margin: 0 auto; background: #fff; padding: 40px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); border-radius: 8px; }}
        h1 {{ color: #1a365d; border-bottom: 2px solid #e2e8f0; padding-bottom: 10px; }}
        .tarih {{ color: #718096; font-weight: bold; margin-bottom: 30px; }}
        .rapor {{ background-color: #f7fafc; padding: 20px; border-left: 4px solid #3182ce; border-radius: 4px; font-family: monospace; white-space: pre-wrap; font-size: 14px; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Medya Anlatı Analizi Raporu</h1>
        <div class="tarih">Rapor Tarihi: {bugunun_tarihi}</div>
        <div class="rapor">{rapor_icerigi}</div>
    </div>
</body>
</html>"""

    # HTML dosyasını diske kaydet
    with open("index.html", "w", encoding="utf-8") as html_file:
        html_file.write(html_sablonu)
        
    print("index.html başarıyla oluşturuldu.")
    
except Exception as e:
    print(f"AI çalıştırılırken hata oluştu: {e}")
    sys.exit(1)
