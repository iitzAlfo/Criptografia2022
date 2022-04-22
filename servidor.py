import socket
import sys
from turtle import clear
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, hmac
from cryptography.hazmat.backends import default_backend
import llaves
"""
Separar la llaves cifradas y descifrar con llave del receptor

"""

def crear_socket_servidor(puerto):
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind(('', int(puerto)))  # hace el bind en cualquier interfaz disponible
    return servidor

def obtener_mensaje(socket):

    try:
        mensaje = socket.recv(1024)
        separacion(mensaje)
    except:
        print('Conexion cerrada')
        exit()

def separacion(mensaje): 
    #Separar cada uno de los datos
    llaves_cifradas=mensaje[:256]
    signature = mensaje[256:512]
    texto = mensaje[512:541]
    mac = mensaje [541:]
    #Descifro llaves
    llaves_descifradas = descifrar_llaves(llaves_cifradas) 
    aes,iv,fmac = separacion_aes_iv_mac(llaves_descifradas) 
    #verificacion de datos correctos
    verificar_firma_llaves(signature,aes,iv,fmac) 
    binario = llaves_cifradas + signature + texto 
    vmac = calcular_hmac(binario,fmac) 
    if vmac != mac:
        print('Al parecer tu MAC presenta problemas')
        exit()
    else:
        print('Mac Correcta')
        plano = descifrar_mensaje(texto,aes,iv)
        print(plano)

def descifrar_mensaje(texto,aes,iv):
    aesCipher = Cipher(algorithms.AES(aes),
                       modes.CTR(iv),
                       backend = default_backend)
    aesDecryptor = aesCipher.decryptor()
    plano = b''
    plano = aesDecryptor.update(texto)
    aesDecryptor.finalize()
    return plano



def calcular_hmac(binario, fmac):
    codigo = hmac.HMAC(fmac, hashes.SHA256(), backend = default_backend())
    codigo.update(binario)
    return codigo.finalize()

def descifrar_llaves(llaves_cifradas):
    llaves_descifradas = llave_privada_receptor.decrypt(
        llaves_cifradas,
        padding.OAEP(
        mgf = padding.MGF1(algorithm = hashes.SHA256()),
        algorithm = hashes.SHA256(),
        label = None))
    return llaves_descifradas

def separacion_aes_iv_mac(llaves_descifradas):
    aes=llaves_descifradas[:16]
    iv= llaves_descifradas[16:32]
    mac=llaves_descifradas[-128:]
    return aes,iv,mac

def atencion(cliente, clientes):
    while True:
        mensaje = obtener_mensaje(cliente)
        cliente.close()

def verificar_firma_llaves(signature,aes, iv, mac):
    mensaje = aes + iv + mac
    try:
      llave_publica_propia.verify(
          signature,
          mensaje,
          padding.PSS(
              mgf=padding.MGF1(hashes.SHA256()),
              salt_length=padding.PSS.MAX_LENGTH),
          hashes.SHA256())
      print('Verificacion Correcta')
    except:
      print('Verificacion de Firma incorrecta')

def escuchar(servidor):
    servidor.listen(5) 
    clientes = []
    while True:
        cliente, _ = servidor.accept() 
        clientes.append(cliente)
        atencion(cliente, clientes) 



if __name__ == '__main__':
    servidor = crear_socket_servidor(sys.argv[1])
    llaveprivada_receptor_path= sys.argv[2]
    llave_privada_receptor = llaves.recuperar_privada_from_path(llaveprivada_receptor_path)
    
    llave_publica_propia_path= sys.argv[3]
    llave_publica_propia = llaves.recuperar_publica_from_path(llave_publica_propia_path)
    print('Escuchando...')
    escuchar(servidor)
    
    #Ejecucuon -> python3 servidor.py 9025 ./privada_receptor.pem ./publica.pem