"""El script parte en 68 """
from importlib.resources import path
import argparse

def partir(path_entrda):
    arch_entrada = open(path_entrda, 'rb')
    datos = arch_entrada.read()
    #Separo por archivos diferentes la cabezera y el cuerpo del XML
    longitud = datos[:68]
    cuerpo = datos[68:]
    arch_salid = open('encabezado.txt', 'wb')
    arch2_salid = open('cuerpo.txt', 'wb')
    arch2_salid.write(cuerpo)
    arch_salid.write(longitud)
    arch_entrada.close()
    arch2_salid.close()
    arch_salid.close()
 
def calcualar_xor(binario1, binario2):
    'Calcular xor de dos cadenas'
    bytes1 = list(binario1)
    bytes2 = list(binario2)

    longitud = len(bytes1)
    if len(bytes2) < longitud:
        longitud = len(bytes2)
    longitud_menor = len(bytes1)
    lista_mas_larga = bytes2
    if len(bytes2) < longitud_menor:
        longitud_menor = len(bytes2)
        lista_mas_larga = bytes1

    res_bytes = []

    for i in range(longitud):
        for i in range(longitud_menor):
           res_bytes.append(bytes1[i] ^ bytes2[i])

        return bytes(res_bytes)
    return bytes(res_bytes) + bytes(lista_mas_larga[longitud_menor:])
       
def obtenerkeystream(path_entrada1, path_entrada2, path_entrada3 ):
    #Recibe el archvio en plano
    plano = open(path_entrada1, 'rb').read()
    #Recibe el archivo Cifrado
    cifrado = open(path_entrada2, 'rb').read()
    #Obtienen el keystream de la cabezera
    key_stream = calcualar_xor(plano, cifrado)
    
    archivoatacante = open(path_entrada3,'rb').read()
    #Archivo para concatenar la cabezera modificada y el cuerpo original 
    archivofinal = open('ArchivoFinal.xml', 'wb')
    archcuerpo = open('cuerpo.txt', 'rb').read()
    #Calcula el XOR de el archivo que contienen modificacion junto con el keystream del normal
    fake = calcualar_xor(archivoatacante,key_stream)
    archivofinal.write(fake)
    archivofinal.write(archcuerpo)
    archivofinal.close()
    

    
    
    
    

if __name__ == '__main__':
    all_args =  argparse.ArgumentParser()
    all_args.add_argument("-p", "--Operacion", help="Aplicar operación, KeyStream/Partir")
    all_args.add_argument("-i1", "--input", help="Archivo de entrada", required=True)
    all_args.add_argument("-i2", "--input2", help="Solo para KeyStream - Recibe archivo cifrado ")
    all_args.add_argument("-i3", "--input3", help="Solo para KeyStream - Recibe archivo del aatcante con cabezera modificada ")

    args = vars(all_args.parse_args())
    operacion = args['Operacion']
    
    if operacion == 'partir':
        partir(args['input'])
    else:
        obtenerkeystream(args['input'],args['input2'], args['input3'])
