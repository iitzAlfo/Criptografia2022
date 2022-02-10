"""
Cesar con archivos de TEXTO
Alumno: Alfonso Garcia Salas

"""

def cifrar(contenido, shift):
    encrypted_text = " "
    for a in contenido:
        if a == " ":
            encrypted_text = encrypted_text + a
            
        else:
            #Inicializo con la primera pos del alfabeto
            pos = ord(a) - ord ("a")
            #Enceunto la nueva pos conteniendo en 26 por el numero de caracteres
            new_pos = (pos + shift) % 26
            #Sumo la pos con la primera letra del alfabeto
            new_word= new_pos + ord ("a")
            #convierto el caracter
            new_character = chr(new_word)
            encrypted_text = encrypted_text + new_character
    return encrypted_text

def decifrar(encriptado, shift):
    decrypted_text = " "
    for a in encriptado:
        if a == " ":
            decrypted_text = decrypted_text + a
        else:
            pos = ord(a) - ord("a")
            new_pos = (pos - shift) % 26
            new_word =  new_pos+ ord ("a")
            new_string = chr(new_word)
            decrypted_text = decrypted_text + new_string
    return decrypted_text
            
            
def ArchivoEncripta(fileName, shift):
    file = open(fileName, "r")
    filew = open("text_encrypted.txt", "w")
    for line in file:
      lineNew = cifrar(line, shift)  
      filew.write(lineNew)
      
    file.close
    filew.close
    
def ArchivoDesencripta(fileName, shift):
    file = open(fileName, "r")
    filew = open("text_Decrypted.txt", "w")
    for line in file:
      lineNew = decifrar(line, shift)  
      filew.write(lineNew)
      
    file.close
    filew.close






       
if __name__ == '__main__':
    encripta = ArchivoEncripta("hola.txt",3)
    #desencripta = ArchivoDesencripta("text_encrypted.txt",3)

            
            
    
