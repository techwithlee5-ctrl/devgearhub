import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict

BASE_DIR = Path(__file__).parent
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

# Load product database
products = json.load(open(BASE_DIR / "products.json"))

PRODUCTS = ["laptop", "monitor", "keyboard", "mouse", "chair", "desk"]
AUDIENCE = ["developers", "programmers", "coders", "designers", "remote workers"]
COUNTRIES = ["usa", "uk", "canada", "australia"]


# ---------------- KEYWORD GENERATION ----------------

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


# ---------------- PRODUCT SELECTION ----------------

def select_products(category, audience):
    matches = [
        p for p in products
        if p["category"] == category and audience in p["best_for"]
    ]
    return matches[:3] or products[:3]


# ---------------- HTML BUILDERS ----------------

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
        "text": "The best {data['product']} depends on performance, comfort, and value. Our top picks are listed above."
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
Below are our top recommendations.
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

<p><a href="index.html">← Back to homepage</a></p>

<footer>
<p><em>As an Amazon Associate, we earn from qualifying purchases.</em></p>
</footer>

</body>
</html>
"""


# ---------------- INDEX PAGE GENERATOR ----------------

def build_index(pages):
    year = datetime.now().year
    grouped = defaultdict(list)

    for p in pages:
        grouped[p["product"]].append(p)

    blocks = ""
    for product, items in grouped.items():
        links = "".join(
            f'<li><a href="{i["slug"]}.html">{i["title"]}</a></li>'
            for i in items[:20]
        )
        blocks += f"""
        <section>
          <h2>Best {product.title()} Guides</h2>
          <ul>{links}</ul>
        </section>
        <hr/>
        """

    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Best Tech Gear for Developers (2025)</title>
  <meta name="description" content="Expert reviews and buying guides for laptops, monitors, keyboards, chairs and more.">

  <style>
    body {{ font-family: Arial; max-width: 1100px; margin: auto; padding: 20px }}
    h1 {{ text-align: center }}
    a {{ text-decoration: none }}
  </style>
</head>
<body>

<h1>Best Tech Gear for Developers ({year})</h1>

<p style="text-align:center;">
Unbiased buying guides and recommendations for developers, programmers, coders, designers and remote workers.
</p>

{blocks}

<footer>
<p><em>As an Amazon Associate, we earn from qualifying purchases.</em></p>
</footer>

</body>
</html>
"""


# ---------------- SITEMAP ----------------

def generate_sitemap(pages):
    base = "https://yourusername.github.io/yoursite/"
    urls = "\n".join(
        f"<url><loc>{base}{p['slug']}.html</loc></url>"
        for p in pages
    )

    sitemap = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
<url><loc>{base}</loc></url>
{urls}
</urlset>
"""
    (OUTPUT_DIR / "sitemap.xml").write_text(sitemap)


# ---------------- MAIN ----------------

def main():
    pages = generate_keywords()

    for p in pages:
        selected = select_products(p["product"], p["audience"])
        cards = build_cards(selected)
        html = build_page(p, cards)

        (OUTPUT_DIR / f"{p['slug']}.html").write_text(html, encoding="utf-8")

    index_html = build_index(pages)
    (OUTPUT_DIR / "index.html").write_text(index_html, encoding="utf-8")

    generate_sitemap(pages)

    print(f"Generated {len(pages)} pages + index.html + sitemap.xml")


if __name__ == "__main__":
    main()
