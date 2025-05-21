import os
import subprocess
import json
from pprint import pprint

def find_plate(caminho_imagem):
    comando = [
        "docker",                       # comando principal do Docker
        "run",                          # executa o conteúdo
        "--rm",                         # remove o contêiner após a execução
        "-v",                           # monta o volume
        f"{os.getcwd()}:/data:ro",      # mapeia o diretório atual como /data no contêiner
        "openalpr",                     # nome da imagem Docker a ser usada
        "-c",                           # definir o país para o reconhecimento
        "br",                           # código do país: Brasil
        "-j",                           # saída em formato JSON
        caminho_imagem
    ]

    resultado = subprocess.run(comando, capture_output=True, text=True)

    print("Diretório atual:", os.getcwd())

    if resultado.returncode !=0:
        print(f'Erro na execução do Docker: {resultado.stderr}')
        return []
    
    # print(f"caminho: {os.getcwd()}")
    # print(resultado)

    dados = json.loads(resultado.stdout)
    # pprint(dados)
    placas_detectadas = []

    for resultado in dados.get("results", []):
        placa_original = resultado.get("plate", "")
        box = resultado.get("coordinates", [{}])

        xmin = min(p.get('x') for p in box)
        xmax = max(p.get('x') for p in box)
        ymin = min(p.get('y') for p in box)
        ymax = max(p.get('y') for p in box)

        placas_detectadas.append({
            "caminho_imagem": caminho_imagem,
            "placa_original": placa_original,
            "xmin": xmin,
            "xmax": xmax,
            "ymin": ymin,
            "ymax": ymax,
        })
    
    return placas_detectadas


placas = find_plate('/data/backend/assets/image1.jpg')
print(placas)

#  C:\Users\rmelo\Documents\TESTES PYTHON\FLET\monitoramento_de_veiculos\backend\assets\h786poj.jpg