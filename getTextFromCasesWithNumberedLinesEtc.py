
import pdfminer
import urllib.request
import io
import requests
import pdfplumber

def open_pdf_url_write_temp_pdf(url):
  headers = {
      "User-Agent":
      "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
  }
  r = requests.get(url, headers=headers)
  on_fly_mem_obj = io.BytesIO(r.content)
  return on_fly_mem_obj

def process_text_from_pdf(mem_obj):
  with pdfplumber.open(mem_obj) as pdf:
    doc_text = []
    bold_text = []
    for page in pdf.pages:
      page1 = page  
      vert_lines = [line for line in page1.lines if line['height'] > 780]
      xleft = 0
      for vline in vert_lines:
        if vline['x0'] <= 150:
          xleft = max(xleft, vline['x0'])
      #print(xleft)
      lines = page1.rects  #lines
      footnote_break = [line for line in lines if line['width'] == 144.02]
      ybottom = 40
      if len(footnote_break) == 1:
        
        ybottom = footnote_break[0]['y0']
      bounding_box = (
          int(xleft), 30, int(page1.width), int(page1.height - ybottom)
      )  
      crop_area = page1.crop(bounding_box)
      crop_text = crop_area.extract_text(y_tolerance=0.5).split("\n")  
      #new_crop_text = []
#       for line in crop_text:
#         if any(c.isalpha() for c in line):
#           new_crop_text.append(
#               line
#           )  # added the newline back to try and get easier heading breaks
#       bold_text.append(
#           page1.filter(lambda obj: obj["object_type"] == "char" and "Bold" in
#                        obj["fontname"]).extract_text())
      doc_text.extend(crop_text)#new_crop_text)  #add each page to the doc_text overall
    doc_text = " ".join(doc_text)
    return doc_text#, bold_text
    
URL = 'https://www.govinfo.gov/content/pkg/USCOURTS-cofc-1_13-vv-00710/pdf/USCOURTS-cofc-1_13-vv-00710-3.pdf'
URL = 'https://www.govinfo.gov/content/pkg/USCOURTS-cofc-1_09-vv-00453/pdf/USCOURTS-cofc-1_09-vv-00453-0.pdf'
#case with line numbers
#URL = 'https://www.govinfo.gov/content/pkg/USCOURTS-cand-1_21-cv-02290/pdf/USCOURTS-cand-1_21-cv-02290-1.pdf'
#bullet points page 1 and footnotes page 3
#URL = 'https://www.govinfo.gov/content/pkg/USCOURTS-cand-3_18-md-02843/pdf/USCOURTS-cand-3_18-md-02843-56.pdf'

pdf = open_pdf_url_write_temp_pdf(URL)
text = process_text_from_pdf(pdf)
print(text[:2000])

from citeurl import Citator
citator = Citator()


citations = citator.list_cites(text)


print(citations[0].text)
# 42 USC § 1988(b)
print(citations[0].tokens)
# {'Title': '42', 'Section': '1988', 'subsection': '(b)'}
print(citations[0].URL)

import pysbd
# text = "My name is Jonas E. Smith. Please turn to p. 55."
seg = pysbd.Segmenter(language="en", clean=False)
print(seg.segment(text))