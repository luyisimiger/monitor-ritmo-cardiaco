# monitor-ritmo-cardiaco
Sistema Tiempo Real | Proyecto Corte 3

# comando para ejecutar el servidor de flask (backend)
gunicorn3 backend.monitor.app:app --reload

# comando para iniciar el worker
sudo rq worker monitor-cardiaco -u redis://localhost

# camando para habilitar emulacion de dos puertos seriales
sudo socat -d -d PTY,link=/dev/ttyS23 PTY,link=/dev/ttyS24

# comando para ejecutar el cinturon bluetooth
sudo python3 backend/cinturon.py

# comando para ejecutar la aplicacion de vue.js (frontend)
cd frontend && npm run serve
