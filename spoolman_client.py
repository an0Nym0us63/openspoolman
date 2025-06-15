import requests
from config import SPOOLMAN_API_URL, SPOOL_SORTING, LOCATION_MAPPING
import json

def patchExtraTags(spool_id, old_extras, new_extras):
  for key, value in new_extras.items():
    old_extras[key] = value

  resp = requests.patch(f"{SPOOLMAN_API_URL}/spool/{spool_id}", json={
    "extra": old_extras
  })
  print(resp.text)
  print(resp.status_code)
  
def patchLocation(spool_id, ams_id='', tray_id=''):
  location = ''
  ams_name='AMS_'+str(ams_id)
  if LOCATION_MAPPING != '' :
    d = dict(item.split(":", 1) for item in LOCATION_MAPPING.split(";"))
    if ams_name in d:
        if ams_id ==100:
            location = d[ams_name]
        else:
            location = d[ams_name] + ' '+ str(tray_id)

  resp = requests.patch(f"{SPOOLMAN_API_URL}/spool/{spool_id}", json={
    "location": location
  })
  print(resp.text)
  print(resp.status_code)


def getSpoolById(spool_id):
  response = requests.get(f"{SPOOLMAN_API_URL}/spool/{spool_id}")
  print(response.status_code)
  print(response.text)
  return response.json()


def fetchSpoolList(archived=False):
  archi='?allow_archived=0'
  if archived:
    archi='?allow_archived=1'
  if SPOOL_SORTING:
    response = requests.get(f"{SPOOLMAN_API_URL}/spool{archi}&sort={SPOOL_SORTING}")
  else:
    response = requests.get(f"{SPOOLMAN_API_URL}/spool{archi}")
    
  print(response.status_code)
  print(response.text)
  return response.json()

def consumeSpool(spool_id, use_weight):
  print(f'Consuming {use_weight} from spool {spool_id}')

  response = requests.put(f"{SPOOLMAN_API_URL}/spool/{spool_id}/use", json={
    "use_weight": use_weight
  })
  print(response.status_code)
  print(response.text)

def fetchSettings():
  response = requests.get(f"{SPOOLMAN_API_URL}/setting/")
  print(response.status_code)
  print(response.text)

  # JSON in ein Python-Dictionary laden
  data = response.json()

  # Extrahiere die Werte aus den relevanten Feldern
  extra_fields_spool = json.loads(data["extra_fields_spool"]["value"])
  extra_fields_filament = json.loads(data["extra_fields_filament"]["value"])
  base_url = data["base_url"]["value"]
  currency = data["currency"]["value"]

  settings = {}
  settings["extra_fields_spool"] = extra_fields_spool 
  settings["extra_fields_filament"] = extra_fields_filament
  settings["base_url"] = base_url.replace('"', '')
  settings["currency"] = currency.replace('"', '')

  return settings