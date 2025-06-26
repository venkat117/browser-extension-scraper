# 🧩 Browser Extension Scraper

An asynchronous Python script that extracts metadata for Browser extensions using their extension IDs.

Fetches:
- Extension Name
- Ratings
- User Count

---

## 🚀 Features

✅ Async & fast using `httpx`  
✅ Parses metadata with `BeautifulSoup`  
✅ Reads from CSV and writes output as CSV  
✅ Logs progress and errors  

---

## 🛠️ Installation

1. **Clone the repo**
2. **Install dependencies**

## 📥 Usage

Download the sample input.csv file and replace the extensiosn ids
Run: python scraper.py
After execution, you'll get a file named output.csv

## 🧪 Sample Output Table
Extension ID	Name	Ratings	Users	Status
cjpalhdlnbpafiamejdnhcphjbkeiagm	uBlock Origin	4.7	10M+	Scraped
aapocclcgogkmnckokdopfmhonfmgoek	Unknown	Unknown	Unknown	ScrapeFailed


