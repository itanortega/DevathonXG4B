# 🎃 Tic Tac Toe de Halloween (Multijugador con WebSockets)


## 🕹️ Objetivo principal

Construir una experiencia de **juego multijugador en tiempo real** usando WebSockets, en la que dos jugadores puedan:

- Enfrentarse por turnos en un tablero de **Tres en Raya (Tic Tac Toe)**.  
- Seleccionar un **avatar spooky** (fantasma, calabaza, vampiro, etc.).  
- Ver los movimientos reflejados **en vivo** en ambas interfaces.

## 🐳 Puesta en marcha con Docker (servidor WebSocket)

Requisitos previos  
- Docker Engine 20.10+  
- Docker Compose v2+  

1. Clona / descarga el repo y entra en la carpeta raíz (donde estén `Dockerfile` y `docker-compose.yml`).

2. Crea el archivo de entorno con la clave secreta:  
   ```bash
   echo "FLASK_SECRET_KEY=halloween-secret-key-$(date +%s)" > .env
   ```

3. Construye y levanta el contenedor en segundo plano:
    ```
    docker compose up -d --build
    ```

4. Comprueba que el servidor esté corriendo y ve los logs en tiempo real:
    ```
    docker compose logs -f backend
    ```
    Verás algo así:
[2025-10-21 14:22:10] Cliente conectado: qJv4Xx9...

5. Para detener y eliminar contenedores:
```
docker compose down
```

¡Tu servidor de Tic Tac Toe Halloween ya está escuchando en ws://localhost:5000 (protocolo Socket.IO)!

## 🔐 CORS en producción


1. Añade la variable al `.env` (uno o varios separados por comas, sin espacios):  
   ```bash
   # .env
   FLASK_SECRET_KEY=halloween-secret-key
   FLASK_ENV=development
   FRONTEND_URL=http://localhost:5173
