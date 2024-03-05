import csv, zipfile, os
import requests
from PyPDF2 import PdfReader

zip_file_url = 'https://disclosures-clerk.house.gov/public_disc/financial-pdfs/2024FD.zip'
pdf_file_url = 'https://disclosures-clerk.house.gov/public_disc/ptr-pdfs/2024/'
member = 'Allen'
r = requests.get(zip_file_url)
zipfile_name = '2024.zip'

with open(zipfile_name, 'wb') as f:
    f.write(r.content)

# Extract ZIP File
# https://docs.python.org/3/library/zipfile.html#zipfile-objects

with zipfile.ZipFile(zipfile_name) as z:
    z.extractall('./')

# Open File.txt
with open('2024FD.txt') as f:
    for line in csv.reader(f, delimiter='\t'):
        if line[1] == member:
            print(line)
            date = line[7]
            doc_id = line[8]

            r = requests.get(f"{pdf_file_url}{doc_id}.pdf")
            if not os.path.isdir(f'./{member}_disclosures'):
              os.mkdir(f'./{member}_disclosures')
            with open(f"./{member}_disclosures/{doc_id}.pdf", 'wb') as pdf_file:
                pdf_file.write(r.content)

# Clean up files
directory = os.listdir()
for file in directory:
    if '2024' in file:
        os.remove(file)

# Open pdf
tickers = []
directory = os.listdir(f'./{member}_disclosures')
for pdf in directory:
    if '.pdf' in pdf:
      reader = PdfReader(f'./{member}_disclosures/{pdf}')
      number_of_pages = len(reader.pages)
      page = reader.pages[0]
      text = page.extract_text()
      words = text.split(' ')
      for word in words:
        if word.startswith('(') and ')' in word:
            tickers.append(word.partition(')')[0][1:])

print(tickers)