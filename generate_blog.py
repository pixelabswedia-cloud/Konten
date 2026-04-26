import os
import google.generativeai as genai
from datetime import datetime

# Konfigurasi API
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("Error: API Key tidak ditemukan!")
    exit(1)

genai.configure(api_key=api_key)

# MENGGUNAKAN MODEL TERBARU 2026
# Kita ganti ke 'gemini-1.5-flash-latest' agar lebih stabil
model = genai.GenerativeModel('gemini-1.5-flash-latest')

def get_next_title():
    if not os.path.exists('titles.txt'):
        print("Error: titles.txt tidak ditemukan!")
        return None
    with open('titles.txt', 'r', encoding='utf-8') as f:
        titles = f.readlines()
    if not titles:
        print("Info: titles.txt kosong!")
        return None
    current_title = titles[0].strip()
    with open('titles.txt', 'w', encoding='utf-8') as f:
        f.writelines(titles[1:])
    return current_title

def run():
    topic = get_next_title()
    if not topic:
        return

    print(f"Sedang memproses judul: {topic}")

    prompt = f"Write a professional SEO blog post in English about: {topic}. Use Markdown with H2 and H3 headings. Start directly with the article content."

    try:
        # Menambahkan pengecekan keamanan
        response = model.generate_content(prompt)
        
        if not response.text:
            print("❌ AI tidak memberikan respon teks.")
            return

        content = response.text

        if not os.path.exists('_posts'):
            os.makedirs('_posts')

        date_str = datetime.now().strftime("%Y-%m-%d")
        safe_title = topic.lower().replace(" ", "-").replace("?", "").replace("!", "")
        filename = f"_posts/{date_str}-{safe_title}.md"

        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        
        print(f"✅ Berhasil! File tersimpan di: {filename}")

    except Exception as e:
        print(f"❌ Terjadi kesalahan: {e}")

if __name__ == "__main__":
    run()
