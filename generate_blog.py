import google.generativeai as genai
import os
from datetime import datetime

# 1. SETUP API
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("Error: GEMINI_API_KEY tidak ditemukan di Secrets GitHub!")
    exit(1)

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

# 2. FUNGSI AMBIL JUDUL
def get_next_title():
    if not os.path.exists('titles.txt'):
        print("Error: file titles.txt tidak ditemukan!")
        return None
    
    with open('titles.txt', 'r', encoding='utf-8') as f:
        titles = f.readlines()
    
    if not titles:
        print("Info: titles.txt kosong!")
        return None
    
    current_title = titles[0].strip()
    
    # Simpan sisa judul kembali ke file
    with open('titles.txt', 'w', encoding='utf-8') as f:
        f.writelines(titles[1:])
        
    return current_title

# 3. JALANKAN PROSES
def run():
    topic = get_next_title()
    if not topic:
        return

    print(f"Sedang memproses judul: {topic}")

    prompt = f"Write a professional SEO blog post in English about: {topic}. Use Markdown with H2 and H3 headings. Do not include introductory small talk, start directly with the title."

    try:
        response = model.generate_content(prompt)
        content = response.text

        # Pastikan folder _posts ada
        if not os.path.exists('_posts'):
            os.makedirs('_posts')
            print("Folder _posts berhasil dibuat secara otomatis.")

        # Buat nama file: YYYY-MM-DD-judul-seo.md
        date_str = datetime.now().strftime("%Y-%m-%d")
        safe_title = topic.lower().replace(" ", "-").replace("?", "").replace("!", "")
        filename = f"_posts/{date_str}-{safe_title}.md"

        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        
        print(f"✅ Berhasil! File tersimpan di: {filename}")

    except Exception as e:
        print(f"❌ Terjadi kesalahan saat memanggil AI: {e}")

if __name__ == "__main__":
    run()
