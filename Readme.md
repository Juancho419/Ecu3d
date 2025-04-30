# Ecu3D - Ecualizador de Producción Animada

**Versión 2.0**  
Este proyecto permite estimar de manera simple y visual:
- El **tiempo total de producción** de un proyecto de animación.
- El **costo estimado** considerando personal y recursos.
- Incluye interfaz gráfica (Tkinter), generación de gráficas (Matplotlib) y lectura de configuración desde JSON.

## Funcionalidades

- Carga parámetros desde un archivo JSON.
- Interfaz gráfica para ingresar datos clave del proyecto.
- Estimación automática de tiempo y costo.
- Generación de gráficos de desempeño recientes.

## Requisitos

- Python 3.10 o superior
- Librerías:
  - tkinter (GUI)
  - pandas
  - matplotlib

## Cómo ejecutar

1. Asegúrate de tener `Configuracion_Proyecto2.0.json` en la misma carpeta.
2. Ejecuta desde consola:

```bash
python ecu3D_v2.py
