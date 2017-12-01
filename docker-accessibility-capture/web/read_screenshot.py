import couchdb
import base64
from PIL import Image
import sys
from io import StringIO, BytesIO
import os

# Intialize Database
couchdbserver = os.getenv("COUCHDBSERVER")
couchdbserver = couchdbserver if couchdbserver is not None else "http://127.0.0.1:5984"
couch = couchdb.Server(couchdbserver)
print("Server: " + couchdbserver)

couchdbname = os.getenv("COUCHDBNAME")
couchdbname = couchdbname if couchdbname is not None else "accessibility"
print("Database: " + couchdbname)

db = None
try: 
  db = couch[couchdbname] 
except Exception: 
  print("Database not initialized. Run setup.sh first.")
  sys.exit(1)

all_screenshots = db.view('screenshots/all')
for screenshot in all_screenshots:
  document = screenshot['value']
  file_name = document['screenshot']
  image_data = document['image_data']

  image_decoded = base64.b64decode(image_data)
  image_bytes = BytesIO(image_decoded)
  image_pil = Image.open(image_bytes)
  image_pil.show()

