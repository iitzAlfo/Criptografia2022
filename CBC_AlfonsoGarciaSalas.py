from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import argparse
import os
import base64

def cifrar(path_entrada, path_salida, key, iv):
    padder = padding.PKCS7(128).padder()
    """
    Cifrado.

    Keyword Arguments:
    returns: bin
    """
    aesCipher = Cipher(algorithms.AES(key),
                       modes.CBC(iv),
                       backend = default_backend)
    aesEncryptor = aesCipher.encryptor()
    salida = open(path_salida, 'wb')
    for buffer in open(path_entrada, 'rb'):
        c = padder.update(buffer)
        cifrado = aesEncryptor.update(c)
        cifrado += padder.finalize()

    cifrado = aesEncryptor.update(cifrado)
    salida.write(cifrado)
    
    aesEncryptor.finalize()
    salida.close()
    
    
def descifrar(path_entrada, path_salida, key, iv):
    unpadder = padding.PKCS7(128).unpadder()
    aesCipher = Cipher(algorithms.AES(key),
                       modes.CBC(iv),
                       backend = default_backend)
    aesDecryptor = aesCipher.decryptor()
    salida = open(path_salida, 'wb')
    plano = b''
    for buffer in open(path_entrada, 'rb'):
        plano = aesDecryptor.update(buffer)
        c = unpadder.update(plano)
        

    plano += unpadder.finalize()
    salida.write(plano)
    
    aesDecryptor.finalize()
    salida.close()

if __name__ == '__main__':
    all_args =  argparse.ArgumentParser()
    all_args.add_argument("-p", "--Operacion", help="Aplicar operación, cifrar/descifrar")
    all_args.add_argument("-i", "--input", help="Archivo de entrada", required=True)
    all_args.add_argument("-o", "--output", help="Archivo de salida", required=True)
    all_args.add_argument("-l", "--llave", help="Llave", required=True)
    all_args.add_argument("-iv", "--iv", help="Vector", required=True)
    args = vars(all_args.parse_args())
    operacion = args['Operacion']

    # Preparar llave recibida en base64
    llave = base64.b64decode(args['llave'])
    iv = base64.b64decode(args['iv'])
    print (llave)
    if len(llave) != 16:
        print('La llave de entrada debe ser de 16 bytes')
        exit()
    
    if operacion == 'cifrar':
        cifrar(args['input'], args['output'], llave, iv)
    else:
        descifrar(args['input'], args['output'], llave, iv)
        
"""
llave: +5DCqGseeFLQrqRrKV734Q==
IV: GsreYioNASUCdD/W2bPXMQ==
Ejecucion:
python3 CBC.py -p cifrar -i prueba.txt -o cifrado.txt -l +5DCqGseeFLQrqRrKV734Q== -iv GsreYioNASUCdD/W2bPXMQ==
"""    
