// ~/.config/Neo4j Desktop/Application/relate-data/dbmss/dbms-a09a2452-8f48-4ddc-ba67-5a48898151be/import


MATCH (s:Productora) DETACH DELETE s;
MATCH (s:Saga) DETACH DELETE s;
MATCH (s:Juego) DETACH DELETE s;
MATCH (s:Avatar) DETACH DELETE s;
MATCH (s:Partida) DETACH DELETE s;
MATCH (s:Venta) DETACH DELETE s;

LOAD CSV WITH HEADERS FROM 'file:///Productora.csv' AS row
CREATE (:Productora {id: row.IDPRODUCTORA, nombre: row.NOMBRE});


LOAD CSV WITH HEADERS FROM 'file:///Saga.csv' AS row
MATCH (p:Productora {id: row.IDPRODUCTORA})
CREATE (p)-[:TIENE_SAGA]->(:Saga {id: row.IDSAGA, nombre: row.NOMBRE, fecha: row.FECHA});


LOAD CSV WITH HEADERS FROM 'file:///Juego.csv' AS row
MATCH (s:Saga {id: row.IDSAGA})
CREATE (s)-[:TIENE_JUEGO]->(:Juego {id: row.IDJUEGO, titulo: row.TITULO, precio: row.PRECIO, fechaLanzamiento: row.FECHALANZAMIENTO, descripcion: row.DESCRIPCION, urlImagen: row.URLIMAGEN, clasificacion: row.CLASIFICACION, puntuacion: row.PUNTUACION});


LOAD CSV WITH HEADERS FROM 'file:///Avatar.csv' AS row
MATCH (j:Juego {id: row.IDJUEGO})
CREATE (j)-[:TIENE_AVATAR]->(:Avatar {id: row.IDUSUARIO, nombre: row.NOMBRE});



LOAD CSV WITH HEADERS FROM 'file:///Partida.csv' AS row
MATCH (a:Avatar {id: row.IDUSUARIO})
CREATE (a)-[:TIENE_PARTIDA]->(:Partida {idJuego: row.IDJUEGO, fechaInicio: row.FECHAINICIO, fechaFin: row.FECHAFIN, online: row.ONLINE_});

LOAD CSV WITH HEADERS FROM 'file:///Biblioteca.csv' AS row
MATCH (j:Juego {id: row.IDJUEGO})
CREATE (j)-[:TIENE_VENTA]->(:Venta {idJuego: row.IDJUEGO, idUsuario: row.IDUSUARIO, modoAdquisicion: row.MODOADQUISICION, fechaAdquisicion: row.FECHAADQUISICION, descuento: row.DESCUENTO, precioCompra: row.PRECIOCOMPRA})