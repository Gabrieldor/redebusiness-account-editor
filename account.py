import requests
import pandas as pd

url = "https://www.redebusiness.com.br/requests.php"

querystring = {"f":"register"}

print("INICIANDO CADASTROS")
df = pd.read_csv("cadastro_off.csv", encoding='iso8859-1').values.tolist()

for p in df:
    p = ['' if x == 'nan' else x for x in p]
    payload = f"first_name={p[0]}&last_name={p[1]}&email={p[2]}&password={p[3]}&confirm_password={p[4]}&fid_14={p[5]}&fid_22={p[6]}&fid_23={p[7]}&gender=2347&accept_terms=on"
    headers = {
        "cookie": "YOUR_COOKIE",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Requested-With": "XMLHttpRequest"
    }
    response = requests.request("POST", url, data=payload, headers=headers, params=querystring)
    print(response.text)
    print(f"UM CADASTRO ACABOU DE SER REALIZADO")

print("CADASTROS CONCLUIDOS")