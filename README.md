# GamePlataform
Proyect for No-SQL Databases

#### 24-May-19
A veces, al generar los datos, ocurre que se genera una fecha final muy grande. Volver a ejecutar.

**mysql** no puede acceder a través de '~/ruta/al/archivo' a directorios donde sea.

No olvidar mover los archivos a la carpeta "secure-file-priv"



## Para mongo db

> sudo systemctl start mongodb

> sudo systemctl status mongodb


SI da error

> sudo rm -rf /tmp/mongodb-27017.sock

> sudo systemctl enable mongodb


> mongoimport --db GamePlataform --collection partidas --file 
