# Pasos para crear la arquitectura


¿Qué es AWS IAM?
AWS Identity and Access Management (IAM) is an AWS service that helps you manage access to your AWS account and resources. It also provides a centralized view of who and what are allowed inside your AWS account (authentication), and who and what have permissions to use and work with your AWS resources (authorization).

¿Qué es un IAM user?
An IAM user represents a person or service that interacts with AWS. You define the user in your AWS account. Any activity done by that user is billed to your account. When you create a user, that user can sign in to gain access to the AWS resources inside your account.

IAM Groups
An IAM group is a collection of users. All users in the group inherit the permissions assigned to the group. This makes it possible to give permissions to multiple users at once. It’s a more convenient and scalable way of managing permissions for users in your AWS account. This is why using IAM groups is a best practice.

IAM Policies
To manage access and provide permissions to AWS services and resources, you create IAM policies and attach them to an IAM identity. Whenever an IAM identity makes a request, AWS evaluates the policies associated with them.


1) crear el role para que las instancias EC2 puedan comunicarse con S3 y DynamoDB
- En la consola escribir IAM
- Darle click en roles, luego en create role
- seleccionar aws service, seleccionar ec2 instances, next
- poner los permission policies, escribir s3FullAccess, y DynamoDBFullAccess, next
- ponerle un nombre
- create role
- revisar que el role se creó correctamente

2) crear usuario
- En la consola estar en IAM service
- click en users, luego add users, username
- enable consolo access (quiero que este usuario pueda hacer login en la consola de aws)
- next
- create a group
- le damos un nombre, le agregamos permission policies, ec2FullAccess, create user group
- agregamos el usuario al nuevo user group
- next
- create user
- revisar que lo creaste bien
- le damos en security credentials
- tenemos la parte de Access Keys, estas permiten a tus usuarios hacer llamadas a AWS usando cosas como AWS command line, AWS SDK, tal vez necesiten que su código esté disponible para acceder a recursos o servicios de AWS
- create an access key
- check command line
- chek I understand ...
- next
- create access key
- con esos access key ya puedes configurar tu command line localmente
- si ya no la necesitas, le das en la parte de access key, actions, deactivate, luego actions delete

¿Qué es EC2?
Amazon EC2 is a web service that provides secure, resizable compute capacity in the cloud. With this service, you can provision virtual servers called EC2 instances. 

¿Qué es AMI?
When launching an EC2 instance, the first setting you configure is which operating system you want by selecting an Amazon Machine Image (AMI).

EC2 instance locations

Unless otherwise specified, when you launch EC2 instances, they are placed in a default virtual private cloud (VPC). The default VPC is suitable for getting started quickly and launching public EC2 instances without having to create and configure your own VPC.

Any resource that you put inside the default VPC will be public and accessible by the internet, so you shouldn’t place any customer data or private information in it.

When you get more comfortable with networking on AWS, you should change this default setting to choose your own custom VPCs and restrict access with additional routing and connectivity mechanisms.

When architecting any application for high availability, consider using at least two EC2 instances in two separate Availability Zones.

2) crear ec2 instance
- buscamos ec2 services en la consola
- instances, launch an instance
- name, Amazon linux, t2.micro (free tier), key pair (login) para conectarse con ssh, en este caso no la necesitamos
- network settings, edit, y de ahi podemos seleccionar la vpc y la subnet
- default vpc, and no subnet preference
- creamos un security group, que es un firewall que permite http and https trafico
- add security group
- type http, https , anywhere
- advanced details, agregarle IAM instance role que ya hemos creado
- agregar un script que se correra cuando se prenda la EC2
- launch instance

3) crear una lambda function para editar el tamaño de una foto una vez subida
- ir a lambda section
- create a function
- author from scratch
- name, runtime (python 3.9)
- permisions, use an existing role, LambdaS3FullAccess (read and write in S3)
- create function
- add trigger
- seleccionamos s3
- seleccionar el bucket creado
- event type (ONLY PUT)
- input/ -> cuando se suban fotos a esta carpeta en s3, dispare el trigger
NOTA: tener cuidado en el prefix y suffix, porque si por ejemplo nosotros después de ejecutar la lambda, guardamos la imagen en el mismo directorio, va haber un bucle infinito de la lambda
- click add
- en la parte de code
- upload from, .zip file, poner el codigo
- ya podemos ensayar
- ir a s3 bucket
- entrar a la carpeta input/
- subir una foto y ver cómo se dispara el trigger
