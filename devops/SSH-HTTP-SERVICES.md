Qué es un servicio SSH? 

Por qué es importante el servicio SSH?
para conectarse remotamente desde tu pc local a un servidor o pc que esté en otra locación diferente a la tuya.

Protocolos y puertos

# Pasos
- instalar VirtualBox
- instalar Ubuntu
- Crear la máquina virtual en VirtualBox
- Poner a correr la máquina virtual (En este caso una máquina virtual con sistema operativo Ubuntu)


Lo primero que vamos hacer cuando entremos a un servidor nuevo en Ubuntu es:
apt-get update 
sudo apt-get update  -> es para ejecutar el comando como administrador para hacer una actualización del sistema. Actualizar los repositorios para que obtengan la ultima versión de los programas.
sudo , luego el comando apt-get y luego el parametro update

sudo apt-get upgrade -> aplicar esas actualizaciones.

revisamos si el puerto está abierto
ss -tulpn -> ss muestra los puertos que están corriendo en mi servidor.

en el puerto 22 corre el servicio ssh

systemctl status sshd -> para revisar el estado del servicio ssh
loaded -> lo tengo habilitado para que se inicie cuando el servidor arranque
active -> servicio apagado o prendido

hostname -I -> para revisar la IP del servidor
whoami -> para saber el usuario del servidor

ssh user@192.168.0.10

en este punto ya puedes ejecutar comandos linux

vamos a revisar los archivos del servicio ssh
cd /etc/ssh
ls
ls -l

sudo vim sshd_config: (o es ssh_config)
cada servicio tiene un archivo de configuración, que nos permite establecer diferentes parametros en el
cambiarle el puerto a 2297
quitar el permitRootLogin
PermitRootLogin no
esc, :wq (escriba y salga)  , :q! (salga sin guardar)

systemctl restart ssh
systemctl reload ssh
systemctl status ssh


sudo reboot -> reiniciar el servidor
ss -tulpn -> debería aparecer el puerto 2297

ps -> listar los procesos en el servidor, aux -> los procesos que estén abiertos y escuchando, grep -> filtrar 
ps aux | grep 2297
systemctl start ssh

En tu maquina local
ssh user@ip -p 2297

En el servidor
systemctl enable ssh -> cuando se reinicie el servidor, va aplicar los cambios. Es decir, esto ya es un servicio que se puede ejecutar desde que arranca el pc.
systemctl disable ssh


en el servidor:
sudo apt remove ssh

sudo apt install ssh

ifconfig
sudo apt install net-tools

lo -> loopback -> que quiere decir: yo mismo, sirve mucho para hacer pruebas locales 127.0.0.1

nc -vz 127.0.0.1 22 -> para revisar los puertos abiertos en tu servidor o un servidor remoto
nc -vz 127.0.0.1 2297



mkdir ejemplo
cd ejemplo
touch hola{1..9}.txt
ls

python3 -m http.server 80

puerto 80 es el servicio http que me permite exponer a mi una aplicación web, que no tiene seguridad

http:/ip:80

para habilitar el archivo en segundo plano
python3 -m http.server 80 & -> ejecuta en segundo plano

jobs -> me muestra mis servicios en segundo plano corriendo

sudo reboot
si reinicio el servidor, se cae el servidor

entonces, cómo hago para mantener corriendo el servicio?
la mejor forma es creando un servicio en linux:

sudo vim /etc/systemd/system/myweb.service
Description= HTTP WebService in python
ExecStart=/usr/bin/python3 -m http.server 80 -d /home/david/ejemplo
Restart=always
User=root
...

which python3 -> en cuál ruta está python3

systemctl status myweb.service
systemctl start myweb.service
systemctl status myweb.service

systemctl restart myweb.service
systemctl daemon-reload

vamos a exponer el index.html

rm * -> para que borremos todos los archivos que teníamos
vim index.html
vim styles.css

curl localhost:80 -I
curl -> trae info de una página web
localhost -> yo mismo
-I -> para que me entregue cuál es el resultado
