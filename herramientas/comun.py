# HistoKHB — utilidades comunes para voces y láminas animadas (Google Cloud, crédito de la prueba).
# Credenciales: variable GOOGLE_APPLICATION_CREDENTIALS = ruta al .json de la cuenta de servicio (NUNCA dentro del repo).
import os,json,threading
from google.oauth2 import service_account
from google.auth.transport.requests import AuthorizedSession
REPO=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJ="project-ed6acb55-3daa-4829-8a3"
TMP=os.path.join(REPO,'herramientas','_tmp'); os.makedirs(TMP,exist_ok=True)
_cr=None; _loc=threading.local()
def sess():
    global _cr
    if _cr is None: _cr=service_account.Credentials.from_service_account_file(os.environ['GOOGLE_APPLICATION_CREDENTIALS'],scopes=['https://www.googleapis.com/auth/cloud-platform'])
    if not hasattr(_loc,'s'): _loc.s=AuthorizedSession(_cr)
    return _loc.s
def J(p): return json.load(open(os.path.join(REPO,p),encoding='utf-8'))
def fichas_de(cap): idx=J('datos/indice.json'); return [k for c in idx['capitulos'] if c['id']==cap for k in c['f']]
def seccion_de(k): return J('datos/indice.json')['fichas'][k]['sec']
