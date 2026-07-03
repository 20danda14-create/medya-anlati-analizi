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

# 2. Günün Tarihini Al (Örn: 02.07.2026)
bugunun_tarihi = datetime.now().strftime("%d.%m.%Y")

# 3. Medya_AI.txt dosyasını oku
try:
    with open("Medya_AI.txt", "r", encoding="utf-8") as f:
        protokol_metni = f.read()
except FileNotFoundError:
    print("Hata: Medya_AI.txt dosyası bulunamadı!")
    sys.exit(1)

# 4. Dinamik Tarih Enjeksiyonu ([gün, ay, yıl] alanlarını değiştiriyoruz)
guncellenmis_prompt = protokol_metni.replace("[gün, ay, yıl]", bugunun_tarihi)

# 5. Gemini API'sine Gönder ve Çalıştır
print(f"{bugunun_tarihi} tarihi için Medya Anlatı Analizi başlatılıyor...")

try:
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=guncellenmis_prompt,
    )
    
    print("\n================== ANALİZ SONUCU ==================\n")
    print(response.text)
    print("\n===================================================\n")
    
except Exception as e:
    print(f"AI çalıştırılırken hata oluştu: {e}")
    sys.exit(1)
