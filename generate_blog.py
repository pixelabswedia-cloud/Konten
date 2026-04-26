import google.generativeai as genai
import os
from datetime import datetime

# 1. Konfigurasi API
genai.configure(api_key="PASTE_API_KEY_ANDA_DI_SINI")
model = genai.GenerativeModel('gemini-pro')

# 2. Detail Artikel
topic = "How to Build a High-Performance Blog with Tailwind CSS and GitHub Pages"
keyword = "Tailwind CSS Blog SEO"

# 3. Prompt Canggih (Sesuai yang kita bahas sebelumnya)
prompt = f"""
Act as a Senior Tech Journalist. Write a high-quality, SEO-optimized blog post about: {topic}.
Primary Keyword: {keyword}

Requirements:
1. Format: Markdown.
2. Tone: Professional, engaging, and authoritative.
3. Structure: Use H2, H3, short paragraphs, and a "Pro-Tip" box.
4. Anti-AI Strategy: Use varied sentence lengths (burstiness) and real-world analogies.
5. Include a Frontmatter at the top (title, date, tags).

Write as if you are teaching a friend, using personal-sounding insights.
"""

def generate_post():
    try:
        # Panggil AI
        response = model.generate_content(prompt)
        content = response.text

        # 4. Penamaan File Otomatis (SEO Friendly)
        filename = topic.lower().replace(" ", "-").replace("?", "") + ".md"
        
        # Buat folder '_posts' jika belum ada (standar Jekyll/GitHub Pages)
        if not os.path.exists('_posts'):
            os.makedirs('_posts')

        filepath = os.path.join('_posts', filename)

        # 5. Simpan ke file .md
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
            
        print(f"✅ Success! Article saved as: {filepath}")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    generate_post()
