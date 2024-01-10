## App Web Credit Management (Demo)
Dentro de este sistema unicamente se pueden realizar 3 acciones: 
+ Dar de alta un cliente,
+ Crear un nuevo tipo de credito,
+ Solicitar un credito. 

Dependiendo el tipo de usuario, puede realizar una o mas acciones.

Un usuario nuevo, no registrado, solo va a poder acceder a los tipos de creditos, a la seccion Acerca de mi y podrá registarse como un nuevo usuario-Cliente. Al resgistrarse el nuevo usuario, tambien se crea un nuevo cliente con los datos que ingreso, vinculado uno con otro.

Un Usuario-cliente logueado, ademas de la navegacion de un usuario no registrado, va a tener estas acciones:
+ Editar sus datos personales,
+ Agregar un avatar,
+ Solicitar un créditos,
+ Ver, modificar o eliminar UNICAMENTE los creditos solicitados por el mismo,
+ Cerrar sesion.

Un usuario admin va a poder hacer todo lo anterior salvo solicitar un credito, y tambien va a tener acceso a:
+ Ver, editar, eliminar todos los creditos otorgados y actualizar los montos de las cuotas vencidas,
+ Crear, ver, editar y eliminar los tipos de creditos,
+ Crear, ver, editar y eliminar clientes.

Los créditos estan relacionados con los tipos de creditos y con los clientes: unicamente un cliente registrado puede solicitar un credito y las opciones de creditos son las existentes.

## Instruciones uso app
+ Primero registrarse como nuevo cliente. Se puede hacer desde el boton de navegacion 'Registrarse'.
+ Ver los tipos de creditos para evaluar la tasa,
+ Por ultimo, solicitar un crédito.

## Acceso SuperUser
Usuario: admin
Contraseña: 12345678