# Sistema de Tiempo Real | monitor-ritmo-cardiaco - Universidad de Cartagena

Desarrollado por **Luis Miguel Mejia** y **Saad Bittar**

## Requerimiento

Desarrollar un sistema IoT para el seguimiento y análisis del ritmo cardíaco y la variación del ritmo cardíaco haciendo uso del microframework Flask. El sistema debe permitir realizar las siguientes operaciones:

- Posibilitar el inicio y la detención de la captura del ritmo cardiaco (HR) y la variabilidad del ritmo cardíaco(RR).  Los datos serán recibidos al mismo tiempo. 
- Permitir la consulta del histórico de las sesiones. Cada sesión tiene un código estampa que la distingue y está asociada a un conjunto de capturas de HR y RR.
- Obtener para cada sesión: el promedio del HR y de RR, el valor máximo y mínimo de HR y RR,  la desviación estándar de los valores HR y RR(SDRR), el porcentaje pRR50 de la variabilidad del ritmo cardíaco. 
- Determinar el riesgo asociado a las métricas de promedio de la variabilidad del ritmo cardíaco, SDRR y pRR50 (ver diapositiva siguiente)
- Presentar en tiempo real las gráficas del ritmo cardíaco (HR) y de la variabilidad del ritmo cardíaco (RR).
- Obtener los centroides de los datos del ritmo cardíaco y de la variabilidad del ritmo cardíaco. 

## Comandos

### camando para habilitar emulacion de dos puertos seriales
```
sudo socat -d -d PTY,link=/dev/ttyS23 PTY,link=/dev/ttyS24
```

### comando para ejecutar el cinturon bluetooth
```
sudo python3 backend/cinturon.py
```

### comando para iniciar el worker
```
sudo rq worker monitor-cardiaco -u redis://localhost
```

### comando para ejecutar el servidor de flask (backend)
```
gunicorn3 backend.monitor.app:app --reload
```

### comando para ejecutar la aplicacion de vue.js (frontend)
```
cd frontend && npm run serve
```
