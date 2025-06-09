import os
import re
import requests
import mailbox
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from email.utils import make_msgid
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import uuid
import mimetypes

# === CONFIGURATION ===
#FILE_NAME = "Alliexpress.mbox"
FILE_NAME = "Soriana.mbox"
FILE_OUTPUT_PREFIX = "2016_01_01_2024_12_31_"
INPUT_MBOX = "G:/work/backup/mbox backup/original/_MBOX-" + FILE_NAME
OUTPUT_MBOX = "G:/work/backup/mbox backup/image_merged/" + FILE_OUTPUT_PREFIX + FILE_NAME
IMAGE_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.gif', '.svg', '.bmp', '.webp')
IMAGE_MIME_TYPES = ('image/jpeg', 'image/png', 'image/gif', 'image/svg+xml', 'image/bmp', 'image/webp')

'''def is_image_url(url):
    #print("URL: " + url )
    return url.lower().startswith('http') and url.lower().endswith(IMAGE_EXTENSIONS)'''

def is_tag_img(tag):
    return tag.name == 'img' and tag.has_attr('src')

def is_image_url(url):
    if not url.lower().startswith('http'):
        return False
    try:
        response = requests.head(url, allow_redirects=True, timeout=5)
        content_type = response.headers.get('Content-Type', '').lower()
        #print("Content-Type: " + content_type + " url: " + url)
        return any(content_type.startswith(img_type) for img_type in IMAGE_MIME_TYPES)
    except requests.RequestException:
        return False

def download_image(url):
    #print("Url: " + url)
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.content
    except Exception as e:
        print(f"Failed to download {url}: {e}")
        return None

def embed_images(msg):
    
    '''if not msg.is_multipart():
        return msg'''

    html_part = None
    for part in msg.walk():
        if part.get_content_type() == 'text/html':
            html_part = part
            break

    if not html_part:
        return msg  # No HTML content to modify

    html = html_part.get_payload(decode=True).decode(html_part.get_content_charset() or 'utf-8', errors='replace')
    soup = BeautifulSoup(html, 'html.parser')
    #print("HTML: " + html)
    image_map = {}

    # List of attributes that may contain image URLs
    image_attrs = ['src', 'href', 'data-src', 'data-original', 'background']

    # Search all tags
    for tag in soup.find_all(True):
        for attr in image_attrs:
            url = tag.get(attr)
            if url and (is_tag_img or is_image_url(url)):
                #print("Tag: " + tag.name + " tag element: " + url)
                # Download and check content type
                image_data = download_image(url)
                if image_data:
                    cid = str(uuid.uuid4())
                    tag[attr] = f"cid:{cid}"
                    ##print("map: " + url + " -> " + f"cid:{cid}")
                    image_map[cid] = (url, image_data)

        
        # Handle inline style attributes with background-image: url(...)
        style = tag.get('style')
        if style:
            #urls = re.findall(r'url\(["\']?(http[^)"\']+\.(?:jpg|jpeg|png|gif|svg|bmp|webp))["\']?\)', style, re.IGNORECASE)
            urls = re.findall(r'url\(["\']?(http[^)"\']+)["\']?\)', style, re.IGNORECASE)
            for url in urls:
                image_data = download_image(url)
                if image_data:
                    cid = str(uuid.uuid4())
                    new_style = style.replace(url, f"cid:{cid}")
                    tag['style'] = new_style
                    image_map[cid] = (url, image_data)

    new_html = str(soup)
    ##print("HTML: " + new_html)

    # Create the nested structure
    related_msg = MIMEMultipart('related')
    alt_part = MIMEMultipart('alternative')
    sanitized_html = new_html.encode('utf-8', 'replace').decode('utf-8', 'replace')
    alt_part.attach(MIMEText(sanitized_html, 'html'))
    related_msg.attach(alt_part)

    for cid, (url, data) in image_map.items():
        #content_type = mimetypes.guess_type(url)[0] or 'application/octet-stream'
        content_type = mimetypes.guess_type(url)[0] or 'image/jpeg'
        maintype, subtype = content_type.split('/', 1)

        img_part = MIMEImage(data, _subtype=subtype)
        img_part.add_header('Content-ID', f"<{cid}>")
        img_part.add_header('Content-Disposition', 'inline', filename=f"{cid}.{subtype}")
        related_msg.attach(img_part)

    # Copy headers
    for header, value in msg.items():
        if header.lower() not in ['content-type', 'content-transfer-encoding', 'mime-version']:
            related_msg[header] = value

    related_msg['MIME-Version'] = '1.0'

    return related_msg

# Read and convert MBOX
input_mbox = mailbox.mbox(INPUT_MBOX)
output_mbox = mailbox.mbox(OUTPUT_MBOX)
output_mbox.lock()

for index, msg in enumerate(input_mbox):
    new_msg = embed_images(msg)
    output_mbox.add(new_msg)
    print(f"---------------------Processed message {index + 1} -------------------------")
    ##if index > 2:
    ##    break

output_mbox.flush()
output_mbox.close()
input_mbox.close()