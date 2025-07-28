import requests
from bs4 import BeautifulSoup

def scrape_site_metadata(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    try:
        # Request and load time
        response = requests.get(url, headers=headers, timeout=10)
        load_time = response.elapsed.total_seconds()
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # Basic metadata
        title = soup.title.string if soup.title else "No title found"
        description = soup.find("meta", attrs={"name": "description"})
        meta_desc = description["content"] if description and "content" in description.attrs else "No meta description"

        # Headings
        h1_tags = [h.get_text(strip=True) for h in soup.find_all("h1")]
        h2_tags = [h.get_text(strip=True) for h in soup.find_all("h2")]

        # Word count
        all_text = soup.get_text(separator=' ') if soup else ""
        word_count = len(all_text.split())

        # Images and alt tag check
        images = soup.find_all("img")
        image_count = len(images)
        missing_alt = sum(1 for img in images if not img.get("alt"))

        # Canonical tag
        canonical = soup.find("link", rel="canonical")
        has_canonical = bool(canonical and canonical.get("href"))

        return {
            "title": title,
            "meta_description": meta_desc,
            "h1_tags": h1_tags,
            "h2_tags": h2_tags,
            "word_count": word_count,
            "load_time": load_time,
            "image_count": image_count,
            "missing_alt_count": missing_alt,
            "has_canonical": has_canonical
        }

    except Exception as e:
        return {"error": str(e)}


# OPTIONAL: Add logic to handle multiple URLs if needed
# def scrape_multiple_sites(urls):
#     results = []
#     total_time = 0
#     for url in urls:
#         result = scrape_site_metadata(url)
#         if 'load_time' in result:
#             total_time += result['load_time']
#         results.append(result)
#     average_load_time = total_time / len(urls) if urls else 0
#     return results, average_load_time
