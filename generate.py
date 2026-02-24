import json
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).parent
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

# Load product database
products = json.load(open(BASE_DIR / "products.json"))

# Keyword generator
PRODUCTS = ["laptop", "monitor", "keyboard", "mouse", "chair", "desk"]
AUDIENCE = ["developers", "programmers", "coders", "designers", "remote workers"]
COUNTRIES = ["usa", "uk", "canada", "australia"]


def generate_keywords():
    pages = []
    for p in PRODUCTS:
        for a in AUDIENCE:
            for c in COUNTRIES:
                slug = f"best-{p}-for-{a}-in-{c}".replace(" ", "-")
                title = f"Best {p.title()} for {a.title()} in {c.upper()}"
                pages.append({
                    "slug": slug,
                    "title": title,
                    "product": p,
                    "audience": a,
                    "country": c.upper()
                })
    return pages


# Product selector
def select_products(category, audience):
    selected = []
    for p in products:
        if p["category"] == category and audience in p["best_for"]:
            selected.append(p)
    return selected[:3] or products[:3]


# Build product HTML cards
def build_cards(items):
    html = ""
    for p in items:
        features = "".join(f"<li>{f}</li>" for f in p["features"])
        html += f"""
        <div class="product">
          <h3>{p['name']}</h3>
          <p><strong>Price:</strong> {p['price']}</p>
          <ul>{features}</ul>
          <a href="{p['link']}" target="_blank" rel="nofollow sponsored">
            Check Price on Amazon
          </a>
        </div>
        <hr/>
        """
    return html


# Build HTML page
def build_page(data, cards):
    year = datetime.now().year
    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>{data['title']} ({year})</title>
  <meta name="description" content="{data['title']} – Expert recommendations and buying guide.">

  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [{{
      "@type": "Question",
      "name": "Which is the best {data['product']} for {data['audience']}?",
      "acceptedAnswer": {{
        "@type": "Answer",
        "text": "The best {data['product']} depends on performance, comfort, and value for money. Our top picks are listed above."
      }}
    }}]
  }}
  </script>

  <style>
    body {{ font-family: Arial; max-width: 900px; margin: auto; padding: 20px }}
    .product {{ border: 1px solid #ddd; padding: 15px; border-radius: 6px }}
    a {{ background: #ff9900; padding: 10px 15px; color: #000; text-decoration: none; border-radius: 5px }}
  </style>

</head>
<body>

<h1>{data['title']} ({year})</h1>

<p>
Finding the best {data['product']} for {data['audience']} in {data['country']} can significantly improve productivity.
Below are our top recommendations based on performance, durability, and value.
</p>

<h2>Top Picks</h2>
{cards}

<h2>Buying Guide</h2>
<ul>
  <li>Performance & reliability</li>
  <li>Build quality</li>
  <li>Warranty & support</li>
  <li>Customer reviews</li>
</ul>

<footer>
<p><em>As an Amazon Associate, we earn from qualifying purchases.</em></p>
</footer>

</body>
</html>
"""


# Sitemap generator
def generate_sitemap(pages):
    base = "https://yourusername.github.io/yoursite/"
    urls = "\n".join([f"<url><loc>{base}{p['slug']}.html</loc></url>" for p in pages])
    sitemap = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{urls}
</urlset>
"""
    (OUTPUT_DIR / "sitemap.xml").write_text(sitemap)


# Main runner
def main():
    pages = generate_keywords()

    for p in pages:
        matched_products = select_products(p["product"], p["audience"])
        cards = build_cards(matched_products)
        html = build_page(p, cards)

        out_file = OUTPUT_DIR / f"{p['slug']}.html"
        out_file.write_text(html, encoding="utf-8")

    generate_sitemap(pages)
    print(f"Generated {len(pages)} SEO pages successfully")


if __name__ == "__main__":
    main()
