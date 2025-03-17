import base64
import uuid
import os
from config import WEB_UPLOADDIR
from jwt import decode, InvalidTokenError
from core.models import ServerMode

def run_cmd(cmd):
  return os.popen(cmd).read()

def initialize():
  return run_cmd('python3 setup.py')

def generate_uuid():
  return str(uuid.uuid4())[0:6]

def decode_base64(text):
  return base64.b64decode(text).decode('utf-8')

def get_identity(token):
  try:
    return decode(token, options={"verify_signature": True, "verify_exp": True}).get('identity')
  except InvalidTokenError:
    return None

def save_file(filename, text):
  try:
    safe_filename = os.path.basename(filename)
    f = open(os.path.join(WEB_UPLOADDIR, safe_filename), 'w')
    f.write(text)
    f.close()
  except Exception as e:
    text = str(e)
  return text

def is_level_easy():
  mode = ServerMode.query.one()
  return mode.hardened == False

def is_level_hard():
  mode = ServerMode.query.one()
  return mode.hardened == True

def set_mode(mode):
  mode = ServerMode.set_mode(mode)
