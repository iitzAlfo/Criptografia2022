from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from importlib.resources import path

import gmpy2, os, binascii, argparse  
   
def GenerateKeys(pathSalida):
    """Funcion que genera las llaves"""
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
    

  
    
def cifrararchivos(path_Key, Path_arch):
    """Funcion que cifra contenido de un archivo con padding"""
    #Obtencion de la llave atra vez del archivo PEM
    public_key_bytes = open(path_Key, 'rb').read()
    public_key = serialization.load_pem_public_key(
    public_key_bytes,
    backend=default_backend())
    file = open(Path_arch, 'rb').read()
    #int_mensaje = int.from_bytes(file, byteorder='big')
    cifrado = public_key.encrypt(
        file,
        padding.OAEP(
            mgf = padding.MGF1(algorithm = hashes.SHA256()),
            algorithm = hashes.SHA256(),
        label= None))
    #cifrado = str(cifrado)
    #bytes_mensaje= int_mensaje(cifrado)
    File_encryp = open('FileEncryp.txt', 'wb+')
    File_encryp.write(cifrado)
    File_encryp.close()
    print('Se encripto correctamente') 
    
def descifrararchivos(path_key, Path_arch):
    """Funcion que descifra archivos"""
    private_key_bytes = open(path_key, 'rb').read()
    private_key = serialization.load_pem_private_key(
        private_key_bytes,
        backend=default_backend(),
        password=None) 
    FileEncryp = open(Path_arch, 'rb').read()
    decifrar = private_key.decrypt(
        FileEncryp,
        padding.OAEP(
            mgf= padding.MGF1(algorithm = hashes.SHA256()),
            algorithm = hashes.SHA256(),
        label = None))
    decifrar = str(decifrar)
    File = open('FileDesencryp.txt', 'w+')
    File.write(decifrar)
    File.close()
    print('Se desencripto correctamente')  
   

    
    

if __name__ == '__main__':
    all_args =  argparse.ArgumentParser()
    all_args.add_argument("-o", "--operacion", help="Operacion a realizar, cllaves, cifrar,descifrar", required=True)
    all_args.add_argument("-p", "--path", help="Path de salida de sus llaves o entrada si va a descifrar", required=True)
    all_args.add_argument("-a", "--archivo", help="Archivo para Encriptar/Desencriptar")
    args = vars(all_args.parse_args())
    operacion = args['operacion']
    if operacion == 'cllaves':
        GenerateKeys(args['path'])
    if operacion == 'cifrar':
        cifrararchivos(args['path'], args['archivo'])
    if operacion == 'descifrar':
        descifrararchivos(args['path'], args['archivo'])
        
        





