

MATCH (p:Productora)-[:TIENE_SAGA]->(s:Saga)-[:TIENE_JUEGO]->(j:Juego)-[:TIENE_AVATAR]->(a:Avatar)-[:TIENE_PARTIDA]->(pt:Partida)
RETURN p, s, j, a, pt;
