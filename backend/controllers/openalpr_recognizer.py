import os
import subprocess
import json
from pprint import pprint
from backend.controllers.base_plate_recognizer import BasePlateRecognizer

class OpenALPRDetector(BasePlateRecognizer):

    def find_plate(self, caminho_imagem):
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
            print("⚠️ Docker retornou saída vazia.")
            print(f'Erro na execução do Docker: {resultado.stderr}')
            print("stderr:", resultado.stderr)
            return []
        
        print("📦 Saída do Docker:")
        print(resultado.stdout)
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

            placa_corrigida = self._standardize_plate(placa_original)
            placa_valida = self._validate_plate(placa_corrigida)

            placas_detectadas.append({
                "caminho_imagem": caminho_imagem,
                "placa_original": placa_original,
                "placa_corrigida": placa_corrigida,
                "placa_valida": placa_valida,
                "xmin": xmin,
                "xmax": xmax,
                "ymin": ymin,
                "ymax": ymax,
            })
        
        return placas_detectadas

    def find_plate_in_video(self, caminho_video, frame_interval=30):
        import cv2

        resultados_video = []
        video = cv2.VideoCapture(caminho_video)
        frame_count = 0

        if not video.isOpened():
            print(f'Erro ao abrir o vídeo: {caminho_video}')
            return []
        
        while True:
            ret, frame = video.read()

            if not ret:
                break

            if frame_count % frame_interval == 0:
                caminho_frame = f'frame_temp_{frame_count}.jpg'
                cv2.imwrite(caminho_frame, frame)
                if not os.path.exists(caminho_frame):
                    print(f"❌ Frame não salvo: {caminho_frame}")
                else:
                    print(f"✅ Frame salvo: {caminho_frame}")

                docker_path = f'/data/{caminho_frame}'

                deteccoes = self.find_plate(docker_path)

                for d in deteccoes:
                    resultados_video.append(d)

                os.remove(caminho_frame)
            
            frame_count += 1
        
        video.release()
        return resultados_video
