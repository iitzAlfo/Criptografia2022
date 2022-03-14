echo "Hola, bienvenido al ejecutor del Ataque de 
de maleabilidad de CTR "
sleep 3
clear
echo "1.Como primer paso se debe de cifrar el archivo del atacante en este caso “atacante.xml” 
se cifrara con el código de la anterior practica aplicando CTR"
python3 AES_CTR.py -p cifrar -i atacante.xml -o atacantecifrado.xml -l +5DCqGseeFLQrqRrKV734Q== -iv GsreYioNASUCdD/W2bPXMQ==
sleep 4
clear
echo "Se debe de usar el AtaqueMaleableCTR.py pero en 
modo partir para poder extraer la cabecera  del archivo cifrado"
python3 AtaqueMaleableCTR.py -p partir -i1 atacantecifrado.xml
sleep 4
clear
echo "Como tercer paso se debe de desencriptar la cabezara que
se extrajo para poder modificarla y obtener el keystream"
python3 AES_CTR.py -p cifrar -i encabezado.txt -o cabeceraplana.txt -l +5DCqGseeFLQrqRrKV734Q== -iv GsreYioNASUCdD/W2bPXMQ==
sleep 4
clear
echo "Por ultimo se debe de ejecutar la función obtenerkeystream, 
donde recibe los parámetros de la cabecera original en plano y la encriptada, 
posteriormente recibirá la modificada y aplicara XOR 
con el Keystream de los anteriores y se unirá junto con el cuerpo "
python3 AtaqueMaleableCTR.py -p keystream -i1 cabeceraplana.txt -i2 encabezado.txt -i3 cabeceraModificada.txt
sleep 6
clear
echo "Comprobación de excito desencriptar 
el archivo para verificar "
sleep 2
python3 AES_CTR.py -p cifrar -i ArchivoFinal.xml -o FinalDesencriptado.txt -l +5DCqGseeFLQrqRrKV734Q== -iv GsreYioNASUCdD/W2bPXMQ==
clear
echo "Operacion completada con extio, Bye"
echo "By: Alfonso Garcia Salas"
sleep 4
