import csv
import asyncio
import httpx
from bs4 import BeautifulSoup
import logging
import os

# Setup logging
logging.basicConfig(level=logging.INFO)

async def scrape_extension(extension_id: str, client: httpx.AsyncClient):
    base_url = f"https://chrome.google.com/webstore/detail/{extension_id}"

    details = {
        "ExtensionId": extension_id,
        "Name": "Unknown",
        "Ratings": "Unknown",
        "UserCount": "Unknown",
        "Status": "ScrapeFailed"
    }

    try:
        logging.info(f"🔍 Requesting: {base_url}")
        response = await client.get(base_url, timeout=20.0)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # Name from <title>
        title_tag = soup.find("title")
        if title_tag:
            details["Name"] = title_tag.text.replace(" - Chrome Web Store", "").strip()

        # Ratings
        rating_tag = soup.find("p", class_="xJEoWe")
        if rating_tag:
            details["Ratings"] = rating_tag.text.strip()

        # User count
        user_div = soup.find("div", class_="F9iKBc")
        if user_div and "users" in user_div.text.lower():
            details["UserCount"] = user_div.text.split("users")[0].strip().replace(",", "")

        details["Status"] = "Scraped"
        logging.info(f"✅ Scraped: {extension_id} | Name: {details['Name']}")

    except Exception as e:
        logging.error(f"❌ Error scraping {extension_id}: {e}")
        details["Status"] = f"Error: {str(e)}"

    return details


async def scrape_from_csv(input_csv: str, output_csv: str):
    if not os.path.exists(input_csv):
        logging.error(f"🚫 Input file not found: {input_csv}")
        return

    extension_ids = []
    # DEBUG: Print the raw lines
    with open(input_csv, "r", encoding="utf-8") as f:
        lines = f.readlines()
        print("📝 Raw input.csv lines:")
        for line in lines:
            print(line.strip())

    # Use csv.DictReader safely
    with open(input_csv, mode="r", encoding="utf-8") as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            ext_id = row.get("ExtensionId") or row.get("extensionid") or ""
            ext_id = ext_id.strip()
            if ext_id and len(ext_id) == 32:
                extension_ids.append(ext_id)

    logging.info(f"📦 Found {len(extension_ids)} valid extension IDs: {extension_ids}")
    if not extension_ids:
        logging.warning("🚫 No valid extension IDs found. Exiting.")
        return

    # Scrape all extensions
    async with httpx.AsyncClient(follow_redirects=True) as client:
        tasks = [scrape_extension(ext_id, client) for ext_id in extension_ids]
        results = await asyncio.gather(*tasks)

    # Write to output
    with open(output_csv, mode="w", newline="", encoding="utf-8") as outfile:
        fieldnames = ["ExtensionId", "Name", "Ratings", "UserCount", "Status"]
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    logging.info(f"✅ Finished. Output saved to: {output_csv}")


if __name__ == "__main__":
    asyncio.run(scrape_from_csv("input.csv", "output.csv"))
