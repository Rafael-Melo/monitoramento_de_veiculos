import re

def standardize_plate(placa):
    placa = re.sub(r'[^A-Z0-9]', '', placa.upper())

    equivalencia_letras = {'0': 'O', '1': 'I', '4': 'A', '5': 'S', '8': 'B', '2': 'Z'}
    equivalencia_numeros = {'O': '0', 'I': '1', 'A': '4', 'S': '5', 'B': '8', 'Z': '2'}

    placa_corrigida = list(placa)

    for i in range(3):
        if placa_corrigida[i] in equivalencia_letras:
            placa_corrigida[i] = equivalencia_letras[placa_corrigida[i]]
    
    for i in range (3, len(placa_corrigida)):
        # Pula o 5º caractere se a placa for padrão Mercosul
        if i == 4 and len(placa_corrigida) == 7 and placa_corrigida[i].isalpha():
            continue

        if placa_corrigida[i] in equivalencia_numeros:
            placa_corrigida[i] = equivalencia_numeros[placa_corrigida[i]]
    
    return ''.join(placa_corrigida)

value = standardize_plate('4BC1S3A')
print(value)