-- PRODUCTORA
ALTER TABLE PRODUCTORA ADD PRIMARY KEY (IDPRODUCTORA);
-- SAGA
ALTER TABLE SAGA ADD PRIMARY KEY (IDSAGA);
-- JUEGO
ALTER TABLE JUEGO ADD PRIMARY KEY (IDJUEGO);
-- JUEGOSGENERO
ALTER TABLE JUEGOSGENERO ADD PRIMARY KEY (IDJUEGO, IDGENERO);
-- GENERO
ALTER TABLE GENERO ADD PRIMARY KEY (IDGENERO);
-- BIBLIOTECA
ALTER TABLE BIBLIOTECA ADD PRIMARY KEY (IDJUEGO, IDUSUARIO);
-- DESEADOS
ALTER TABLE DESEADOS ADD PRIMARY KEY (IDJUEGO,IDUSUARIO);
-- USUARIO
ALTER TABLE USUARIO ADD PRIMARY KEY (IDUSUARIO);
-- IDIOMASJUEGO
ALTER TABLE IDIOMASJUEGO ADD PRIMARY KEY (IDJUEGO,IDIDIOMA);
-- IDIOMAS
ALTER TABLE IDIOMAS ADD PRIMARY KEY (IDIDIOMA);
-- RESENA
ALTER TABLE RESENA ADD PRIMARY KEY (IDJUEGO,IDUSUARIO);
-- JUEGOPLATAFORMA
ALTER TABLE JUEGOPLATAFORMA ADD PRIMARY KEY (IDJUEGO,IDPLATAFORMA);
-- PLATAFORMA
ALTER TABLE PLATAFORMA ADD PRIMARY KEY (IDPLATAFORMA);
-- AVATAR
ALTER TABLE AVATAR ADD PRIMARY KEY (IDJUEGO,IDUSUARIO);
-- PARTIDAS
ALTER TABLE PARTIDAS ADD PRIMARY KEY (IDJUEGO, IDUSUARIO , FECHAINICIO, FECHAFIN);


-- PRODUCTORA
--

-- SAGA
ALTER TABLE SAGA ADD 
    FOREIGN KEY (IDPRODUCTORA) 
        REFERENCES PRODUCTORA(IDPRODUCTORA);

-- JUEGO
ALTER TABLE JUEGO ADD 
    FOREIGN KEY (IDSAGA) 
        REFERENCES SAGA(IDSAGA);

-- JUEGOSGENERO
ALTER TABLE JUEGOSGENERO ADD 
    FOREIGN KEY (IDJUEGO) 
        REFERENCES JUEGO(IDJUEGO);

ALTER TABLE JUEGOSGENERO ADD 
    FOREIGN KEY (IDGENERO) 
        REFERENCES GENERO(IDGENERO);

-- GENERO
--

-- BIBLIOTECA
ALTER TABLE BIBLIOTECA ADD 
    FOREIGN KEY (IDJUEGO) 
        REFERENCES JUEGO(IDJUEGO);

ALTER TABLE BIBLIOTECA ADD 
    FOREIGN KEY (IDUSUARIO) 
        REFERENCES USUARIO(IDUSUARIO);

-- DESEADOS
ALTER TABLE DESEADOS ADD 
    FOREIGN KEY (IDJUEGO) 
        REFERENCES JUEGO(IDJUEGO);

ALTER TABLE DESEADOS ADD 
    FOREIGN KEY (IDUSUARIO) 
        REFERENCES USUARIO(IDUSUARIO);

-- USUARIO
--

-- IDIOMASJUEGO
ALTER TABLE IDIOMASJUEGO ADD 
    FOREIGN KEY (IDJUEGO) 
        REFERENCES JUEGO(IDJUEGO);

ALTER TABLE IDIOMASJUEGO ADD 
    FOREIGN KEY (IDIDIOMA) 
        REFERENCES IDIOMAS(IDIDIOMA);


-- IDIOMAS
--

-- RESENA
ALTER TABLE RESENA ADD 
    FOREIGN KEY (IDJUEGO) 
        REFERENCES JUEGO(IDJUEGO);

ALTER TABLE RESENA ADD 
    FOREIGN KEY (IDUSUARIO) 
        REFERENCES USUARIO(IDUSUARIO);


-- JUEGOPLATAFORMA
ALTER TABLE JUEGOPLATAFORMA ADD 
    FOREIGN KEY (IDJUEGO) 
        REFERENCES JUEGO(IDJUEGO);

ALTER TABLE JUEGOPLATAFORMA ADD 
    FOREIGN KEY (IDPLATAFORMA) 
        REFERENCES PLATAFORMA(IDPLATAFORMA);


-- PLATAFORMA
--

-- AVATAR
ALTER TABLE AVATAR ADD 
    FOREIGN KEY (IDJUEGO) 
        REFERENCES JUEGO(IDJUEGO);

ALTER TABLE AVATAR ADD 
    FOREIGN KEY (IDUSUARIO) 
        REFERENCES USUARIO(IDUSUARIO);


-- PARTIDAS
ALTER TABLE PARTIDAS ADD 
    FOREIGN KEY (IDJUEGO) 
        REFERENCES AVATAR(IDJUEGO);

ALTER TABLE PARTIDAS ADD 
    FOREIGN KEY (IDUSUARIO) 
        REFERENCES AVATAR(IDUSUARIO);
