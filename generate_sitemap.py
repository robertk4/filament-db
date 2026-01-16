import os

# --- CONFIGURATION ---
BASE_URL = "https://robertk4.github.io/filament-db/"
OUTPUT_DIR = "docs"

def generate_sitemap():
    print(f"Generating sitemap for {BASE_URL}...")

    urls = []
    # Scan the docs folder
    for root, dirs, files in os.walk(OUTPUT_DIR):
        for file in files:
            if file.endswith(".html"):
                rel_path = os.path.relpath(os.path.join(root, file), OUTPUT_DIR)
                rel_path = rel_path.replace("\\", "/") # Windows fix

                if rel_path == "index.html":
                    full_url = BASE_URL
                else:
                    full_url = f"{BASE_URL}{rel_path}"

                urls.append(full_url)

    # Build XML
    xml_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml_content += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for url in urls:
        xml_content += f"  <url>\n    <loc>{url}</loc>\n  </url>\n"
    xml_content += '</urlset>'

    with open(f"{OUTPUT_DIR}/sitemap.xml", "w", encoding="utf-8") as f:
        f.write(xml_content)

    print(f"Success! Created sitemap.xml with {len(urls)} pages.")

if __name__ == "__main__":
    generate_sitemap()
