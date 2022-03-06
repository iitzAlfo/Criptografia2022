from importlib.resources import path
import base64, argparse
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend


def cifrar(path_entrada, path_salida,key, iv):
    aesCipher = Cipher(algorithms.AES(key),
                       modes.CTR(iv),
                       backend = default_backend)
    aesEncryptor = aesCipher.encryptor()
    salida = open(path_salida, 'wb')
    for buffer in open(path_entrada, 'rb'):
        cifrado = aesEncryptor.update(buffer)
        salida.write(cifrado)
    

    aesEncryptor.finalize()
    salida.close()
    
def descifrar(path_entrada, path_salida, key, iv):
    aesCipher = Cipher(algorithms.AES(key),
                    modes.CTR(iv),
                    backend = default_backend)
    aesDecryptor = aesCipher.decryptor()
    salida = open(path_salida, 'wb')
    plano = b''
    for buffer in open(path_entrada, 'rb'):
        plano = aesDecryptor.update(buffer)
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
    if len(llave) != 16:
        print('La llave de entrada debe ser de 16 bytes')
        exit()
    
    if operacion == 'cifrar':
        cifrar(args['input'], args['output'], llave, iv)
    else:
        descifrar(args['input'], args['output'], llave, iv)