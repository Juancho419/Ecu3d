import json
import tkinter as tk
from tkinter import messagebox
import pandas as pd
import matplotlib.pyplot as plt
import os

archivo_historial = r"M:/EQ_V2.0/historial_analisis.csv"

# Función para guardar los resultados
def guardar_analisis(nombre_proyecto, costo_estimado, semanas_estimadas):
    nuevo_dato = {
        "Proyecto": nombre_proyecto,
        "Costo_Estimado": costo_estimado,
        "Semanas_Estimadas": semanas_estimadas
    }

    os.makedirs(os.path.dirname(archivo_historial), exist_ok=True)

    if os.path.exists(archivo_historial):
        df_historial = pd.read_csv(archivo_historial)
        df_historial = pd.concat([df_historial, pd.DataFrame([nuevo_dato])], ignore_index=True)
        df_historial = df_historial.tail(5)
    else:
        df_historial = pd.DataFrame([nuevo_dato])

    df_historial.to_csv(archivo_historial, index=False)

def graficar_ultimos_analisis():
    if not os.path.exists(archivo_historial):
        print("Aún no hay análisis guardados.")
        return

    df_historial = pd.read_csv(archivo_historial)

    if df_historial.empty:
        print("El archivo existe pero no contiene datos.")
        return

    proyectos = df_historial["Proyecto"]
    costos = df_historial["Costo_Estimado"]
    semanas = df_historial["Semanas_Estimadas"]

    fig, ax1 = plt.subplots(figsize=(10, 5))

    color = 'tab:blue'
    ax1.set_xlabel('Proyectos analizados')
    ax1.set_ylabel('Costo Estimado ($)', color=color)
    ax1.plot(proyectos, costos, marker='o', linestyle='-', linewidth=2, color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()  
    color = 'tab:green'
    ax2.set_ylabel('Semanas Estimadas', color=color)  
    ax2.plot(proyectos, semanas, marker='o', linestyle='--', linewidth=2, color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    plt.title("Comparativa de Costo y Tiempo en últimos 5 análisis")
    fig.tight_layout()  
    plt.grid(True)
    plt.show()

def cargar_configuracion():
    try:
        with open("M:\\EQ_V2.0\\Configuracion_Proyecto2.0.json", "r") as f:
            config = json.load(f)
        print("Configuración cargada correctamente:")
        print(config)
        return config
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo cargar el archivo de configuración: {e}")
        return None

def crear_gui(config):
    root = tk.Tk()
    root.title("Ecualizador de Producción - V2.0")

    entries = {}
    row = 0

    # Campo nombre del proyecto
    tk.Label(root, text="Nombre del Proyecto:", font=("Arial", 12, "bold")).grid(row=row, column=0, padx=5, pady=5, sticky='w')
    nombre_proyecto_entry = tk.Entry(root)
    nombre_proyecto_entry.grid(row=row, column=1, padx=5, pady=5)
    nombre_proyecto_entry.insert(0, config["proyecto"].get("nombre_proyecto", ""))
    entries["nombre_proyecto"] = nombre_proyecto_entry
    row += 1

    # Sección: Parámetros Generales
    tk.Label(root, text="Parámetros Generales", font=("Arial", 12, "bold")).grid(row=row, column=0, columnspan=2, pady=10)
    row += 1
    general_fields = [
        ("Cantidad de Episodios", "episodios"),
        ("Duración del Episodio (segundos)", "duracion_segundos"),
        ("Cantidad de Props", "cantidad_props"),
        ("Cantidad de Personajes", "cantidad_personajes"),
        ("Cantidad de Environments", "cantidad_environments"),
        ("Porcentaje de Reuso (%)", "porcentaje_reuso"),
        ("Dificultad del Proyecto (1-10)", "dificultad"),
        ("Costo diario por artista ($)", "costo_diario")
    ]
    for label_text, key in general_fields:
        tk.Label(root, text=label_text + ":").grid(row=row, column=0, sticky="w", padx=5, pady=5)
        entry = tk.Entry(root)
        entry.grid(row=row, column=1, padx=5, pady=5)
        if key == "episodios":
            entry.insert(0, "1")
        else:
            default = config["proyecto"].get(key, "")
            entry.insert(0, str(default))
        entries[key] = entry
        row += 1

    # Sección: Preproducción
    tk.Label(root, text="Preproducción", font=("Arial", 12, "bold")).grid(row=row, column=0, columnspan=2, pady=10)
    row += 1
    pre_fields = [
        ("Concept Artists (mínimo 1)", ("concept_artists", "valor")),
        ("Modeladores (mínimo 1)", ("modeladores", "valor")),
        ("Riggers (mínimo 1)", ("riggers", "valor"))
    ]
    for label_text, (section, key) in pre_fields:
        tk.Label(root, text=label_text + ":").grid(row=row, column=0, sticky="w", padx=5, pady=5)
        entry = tk.Entry(root)
        entry.grid(row=row, column=1, padx=5, pady=5)
        default = config["preproduccion"][section].get(key, "")
        entry.insert(0, str(default))
        entries[f"pre_{section}"] = entry
        row += 1

    # Sección: Producción
    tk.Label(root, text="Producción", font=("Arial", 12, "bold")).grid(row=row, column=0, columnspan=2, pady=10)
    row += 1
    prod_fields = [
        ("Storyboard (mínimo 1)", ("storyboard", "valor")),
        ("Animadores (mínimo 3)", ("animadores", "valor"))
    ]
    for label_text, (section, key) in prod_fields:
        tk.Label(root, text=label_text + ":").grid(row=row, column=0, sticky="w", padx=5, pady=5)
        entry = tk.Entry(root)
        entry.grid(row=row, column=1, padx=5, pady=5)
        default = config["produccion"][section].get(key, "")
        entry.insert(0, str(default))
        entries[f"prod_{section}"] = entry
        row += 1

    # Sección: Postproducción (solo fase 1, ya que fases 2 y 3 se integran en el cálculo inicial)
    tk.Label(root, text="Postproducción", font=("Arial", 12, "bold")).grid(row=row, column=0, columnspan=2, pady=10)
    row += 1
    # Solo se solicita la cuota de días para la fase 1
    post_fields = [
        ("Fase 1 - Cuota de días", ("fase1", "cuota_dias"))
    ]
    for label_text, (section, key) in post_fields:
        tk.Label(root, text=label_text + ":").grid(row=row, column=0, sticky="w", padx=5, pady=5)
        entry = tk.Entry(root)
        entry.grid(row=row, column=1, padx=5, pady=5)
        default = config["postproduccion"][section].get(key, "")
        entry.insert(0, str(default))
        entries[f"post_{section}_{key}"] = entry
        row += 1

    # Botón ANALIZAR
    btn = tk.Button(root, text="ANALIZAR", command=lambda: analizar_proyecto_with_entries(config, entries))
    btn.grid(row=row, column=0, columnspan=2, pady=10)

    root.mainloop()

def analizar_proyecto_with_entries(config, entries):
    try:
        # Extraer parámetros generales
        nombre_proyecto = entries["nombre_proyecto"].get()
        episodios = int(entries["episodios"].get())
        duracion_segundos = int(entries["duracion_segundos"].get())
        props = int(entries["cantidad_props"].get())
        personajes = int(entries["cantidad_personajes"].get())
        environments = int(entries["cantidad_environments"].get())
        porcentaje_reuso = float(entries["porcentaje_reuso"].get()) / 100
        dificultad = int(entries["dificultad"].get())
        costo_diario = float(entries["costo_diario"].get())
        
        # Extraer parámetros de preproducción
        pre_concept = int(entries["pre_concept_artists"].get())
        pre_modeladores = int(entries["pre_modeladores"].get())
        pre_riggers = int(entries["pre_riggers"].get())
        pre_total = pre_concept + pre_modeladores + pre_riggers
        pre_min = 1 + 1 + 1
        
        # Extraer parámetros de producción
        prod_storyboard = int(entries["prod_storyboard"].get())
        prod_animadores = int(entries["prod_animadores"].get())
        prod_total = prod_storyboard + prod_animadores
        prod_min = 1 + 3
        
        # Extraer parámetros de postproducción (solo fase 1)
        post_fase1 = int(entries["post_fase1_cuota_dias"].get())
        # En esta versión, no se pide tiempo adicional para animación ni otras fases
        
        # Parámetros globales
        dias_laborales_semana = config["parametros_globales"]["dias_laborales_semana"]
        dias_laborales_mes = config["parametros_globales"]["dias_laborales_mes"]
        
        # Fórmula base para el contenido:
        # - Cada prop suma 0.5 días.
        # - Cada personaje suma 1.5 días.
        # - Cada environment suma 4 días.
        # - La duración del episodio se divide entre 20.
        # Se multiplica por (1 - porcentaje_reuso) para reducir el tiempo a medida que se reutilizan assets.
        base_time = (props * 0.5 + personajes * 1.5 + environments * 4 + (duracion_segundos / 20)) * (1 - porcentaje_reuso)
        if dificultad > 6:
            base_time *= 1.055  # Aumenta un 5.5% si la dificultad es mayor a 6
        
        # Factor de reducción en pre y producción
        factor_pre = pre_min / pre_total if pre_total > 0 else 1
        factor_prod = prod_min / prod_total if prod_total > 0 else 1
        global_factor = (factor_pre + factor_prod) / 2
        
        # Tiempo ajustado para el contenido de un episodio
        adjusted_time = base_time * global_factor
        
        # Tiempo de postproducción (solo fase 1)
        post_time = post_fase1
        
        # Tiempo total por episodio
        time_per_episode = adjusted_time + post_time
        
        # Tiempo total del proyecto (en días)
        total_time_days = episodios * time_per_episode
        total_time_weeks = total_time_days / dias_laborales_semana
        total_time_months = total_time_days / dias_laborales_mes
        
        # Estimación de personal:
        # Se considera que en postproducción se usa un personal fijo de 5 personas.
        fixed_post_staff = 5
        total_staff = pre_total + prod_total + fixed_post_staff
        
        # Costo por episodio
        cost_per_episode = (adjusted_time * (pre_total + prod_total) + post_time * fixed_post_staff) * costo_diario
        total_cost = episodios * cost_per_episode
        
           
       ### nombre_proyecto = entries["nombre_proyecto"].get()
        
        resultado = (
            f"Tiempo Estimado del Proyecto:\n"
            f"  {total_time_days:.1f} días\n"
            f"  {total_time_weeks:.1f} semanas\n"
            f"  {total_time_months:.1f} meses\n\n"
            f"Costo Estimado: ${total_cost:.2f}\n\n"
            f"Factor Global (Pre/Prod): {global_factor:.2f}"
        )

        # Mostramos resultado en ventana emergente
        messagebox.showinfo("Análisis de Proyecto", resultado)

        # Guardamos análisis para la gráfica
        guardar_analisis(nombre_proyecto, total_cost, total_time_weeks)

        # Mostramos gráfica automáticamente después de cada análisis
        graficar_ultimos_analisis()

    except Exception as e:
        messagebox.showerror("Error en análisis", str(e))
        
if __name__ == "__main__":
    config = cargar_configuracion()
    if config:
        crear_gui(config)