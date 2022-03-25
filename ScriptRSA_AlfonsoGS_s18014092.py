from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from importlib.resources import path

import gmpy2, os, binascii, argparse  
   
def GenerateKeys(pathSalida):
        # Generar llave privada
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )

    # Extraer llave publica de llave privada
    public_key = private_key.public_key()

    # Convertir llave privada a bytes, sin cifrar los bytes
    # Obviamente a partir de los bytes se puede guardar en un archivo binario
    private_key_bytes = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )

    # Convertir la llave publica en bytes
    public_key_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )


    #Guardar archivos
    File_PrivateK = open(pathSalida + 'PrivateKey.pem', 'wb+')
    File_PublicK = open(pathSalida + 'PublicKey.pem', 'wb+')
    File_PrivateK.write(private_key_bytes)
    File_PublicK.write(public_key_bytes)
    File_PrivateK.close
    File_PublicK.close
    print('Se crearon las llaves en el directorio') 
    
def simple_rsa_encrypt(m, publickey):
    # public_numbers regresa una estructura de datos con 'e' y 'n'
    numbers = publickey.public_numbers()
    # el cifrado es (m ** e) % n
    return gmpy2.powmod(m, numbers.e, numbers.n)  
  
def simple_rsa_decrypt(c, privatekey):
    # private_numbers regresa una estructura de datos con 'd' y 'n'
    numbers = privatekey.private_numbers()
    # el descifrado es (c ** d) % n
    return gmpy2.powmod(c, numbers.d, numbers.public_numbers.n) 

def int_to_bytes(i):
    # asegurarse de que es un entero python
    i = int(i)
    return i.to_bytes((i.bit_length()+7)//8, byteorder='big')   
    
def cifrararchivos(path_Key, Path_arch):
    #Obtencion de la llave atra vez del archivo PEM
    public_key_bytes = open(path_Key, 'rb').read()
    public_key = serialization.load_pem_public_key(
    public_key_bytes,
    backend=default_backend())
    file = open(Path_arch, 'rb').read()
    int_mensaje = int.from_bytes(file, byteorder='big')
    cifrado = simple_rsa_encrypt(int_mensaje, public_key)
    cifrado = str(cifrado)
    #bytes_mensaje= int_mensaje(cifrado)
    File_encryp = open('FileEncryp.txt', 'w+')
    File_encryp.write(cifrado)
    File_encryp.close()
    print('Se encripto correctamente') 
    
def descifrararchivos(path_key, Path_arch):
    private_key_bytes = open(path_key, 'rb').read()
    private_key = serialization.load_pem_private_key(
        private_key_bytes,
        backend=default_backend(),
        password=None) 
    FileEncryp = open(Path_arch, 'rb').read()
    FileEncryp = int(FileEncryp)
    decifrar = simple_rsa_decrypt(FileEncryp, private_key)
    bytes_mensaje = int_to_bytes(decifrar)
    bytes_mensaje = str(bytes_mensaje)
    File = open('FileDesencryp.txt', 'w+')
    File.write(bytes_mensaje)
    File.close()
    print('Se desencripto correctamente')  
   

    
    

if __name__ == '__main__':
    all_args =  argparse.ArgumentParser()
    all_args.add_argument("-o", "--operacion", help="Operacion a realizar", required=True)
    all_args.add_argument("-p", "--path", help="Path de salida de sus llaves", required=True)
    all_args.add_argument("-a", "--archivo", help="Archivo para Encriptar/Desencriptar" required=True)
    args = vars(all_args.parse_args())
    operacion = args['operacion']
    #GenerateKeys(args['path'])
    #cifrararchivos(args['path'], args['archivo'])
    descifrararchivos(args['path'], args['archivo'])


