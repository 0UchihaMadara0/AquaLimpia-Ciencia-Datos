# Proyecto de Ciencia de Datos - AquaLimpia S.A.

## Descripción del proyecto

AquaLimpia S.A. es una empresa dedicada al tratamiento de aguas residuales urbanas e industriales.

El propósito de este proyecto es analizar el desempeño de sus plantas de tratamiento, identificar patrones asociados a la calidad del efluente y generar información que apoye la toma de decisiones de las áreas de Operaciones y Gestión Ambiental.

El proyecto integra análisis exploratorio de datos, análisis estadístico, evaluación de calidad, visualizaciones, dashboard interactivo, programación modular, notebook reproducible y control de versiones mediante Git y GitHub.

---

## Objetivo general

Analizar el desempeño de las plantas de tratamiento de AquaLimpia S.A., identificando patrones asociados a la DBO del efluente, la eficiencia de remoción y el cumplimiento normativo.

---

## Objetivos específicos

- Comparar el desempeño de las plantas de tratamiento.
- Calcular la eficiencia de remoción de DBO.
- Analizar la relación entre DBO de entrada y DBO de salida.
- Evaluar el comportamiento del cumplimiento normativo.
- Explorar la relación entre variables operacionales y desempeño.
- Evaluar la calidad de los datos utilizados.
- Identificar valores potencialmente atípicos.
- Generar información diferenciada para Operaciones y Gestión Ambiental.
- Construir un dashboard exploratorio interactivo.
- Implementar funciones modulares mediante NumPy, SciPy y Joblib.
- Documentar el análisis mediante un notebook reproducible.

---

## Preguntas de investigación

1. ¿Existen diferencias de desempeño entre las plantas?
2. ¿Qué relación existe entre la DBO de entrada y la DBO de salida?
3. ¿El caudal de entrada presenta asociación con la eficiencia del tratamiento?
4. ¿Cómo se comporta el cumplimiento normativo entre plantas y a través del tiempo?
5. ¿Qué variables operacionales presentan mayor asociación con los registros de incumplimiento?

---

## Dataset

El análisis utiliza el archivo:

`dataset_set_A_aguas_residuales.xlsx`

El dataset contiene **200 registros** correspondientes a tres plantas de tratamiento:

- Planta Centro.
- Planta Norte.
- Planta Sur.

El período analizado comprende desde el **1 de julio de 2025 hasta el 28 de octubre de 2025**.

Entre las principales variables disponibles se encuentran:

- Fecha de registro.
- Planta.
- Caudal de entrada.
- DBO de entrada.
- SST de entrada.
- pH de entrada.
- Energía de aireación.
- Lodos generados.
- DBO de salida.
- Cumplimiento normativo.

---

## Estructura del proyecto

```text
AquaLimpia-Ciencia-Datos/
│
├── dataset_set_A_aguas_residuales.xlsx
├── analisis_aqualimpia.py
├── analisis_aqualimpia.ipynb
├── dashboard_aqualimpia.py
├── evaluacion_calidad.py
├── README.md
├── requirements.txt
├── .gitignore
│
├── src/
│   ├── __init__.py
│   ├── funciones_analisis.py
│   └── persistencia.py
│
├── graficos/
│   ├── cumplimiento_por_planta.png
│   ├── dbo_entrada_vs_salida.png
│   └── evolucion_dbo_salida.png
│
└── outputs/
    ├── resumen_por_planta.xlsx
    ├── salida_operaciones.xlsx
    ├── salida_gestion_ambiental.xlsx
    ├── resultados_analisis.joblib
    └── informe_calidad_datos.xlsx
```

---

## Flujo de trabajo

El proyecto sigue un proceso reproducible compuesto por las siguientes etapas:

1. Carga del dataset original.
2. Validación de la estructura de los datos.
3. Preparación y transformación de los datos.
4. Cálculo de indicadores derivados.
5. Análisis descriptivo.
6. Análisis estadístico.
7. Evaluación de la calidad de los datos.
8. Detección de valores potencialmente atípicos.
9. Generación de visualizaciones.
10. Construcción del dashboard exploratorio interactivo.
11. Generación de archivos específicos para las áreas de Operaciones y Gestión Ambiental.
12. Persistencia y recuperación de resultados mediante Joblib.
13. Documentación del análisis mediante Jupyter Notebook y README.
14. Control de versiones y trazabilidad mediante Git y GitHub.

---

## Librerías utilizadas

El proyecto utiliza principalmente las siguientes librerías:

- Pandas.
- NumPy.
- SciPy.
- Matplotlib.
- Plotly.
- Streamlit.
- OpenPyXL.
- Joblib.

Las dependencias utilizadas se encuentran registradas en:

`requirements.txt`

Para instalarlas se puede ejecutar:

```bash
pip install -r requirements.txt
```

---

## Análisis principal

El archivo:

`analisis_aqualimpia.py`

realiza el procesamiento principal del dataset.

Entre sus principales funciones se encuentran:

- carga y validación de los datos;
- preparación y transformación de variables;
- cálculo de eficiencia de remoción de DBO;
- generación de indicadores generales;
- elaboración de resúmenes por planta;
- cálculo de correlación de Pearson;
- identificación de valores potencialmente atípicos;
- generación de gráficos;
- exportación de archivos de resultados;
- almacenamiento y recuperación de resultados mediante Joblib.

Para ejecutarlo:

```bash
python analisis_aqualimpia.py
```

---

## Notebook reproducible

El archivo:

`analisis_aqualimpia.ipynb`

presenta de forma secuencial las principales etapas del análisis realizado.

El notebook incluye:

- carga del dataset;
- preparación de los datos;
- cálculo de eficiencia de remoción;
- indicadores generales;
- resumen y comparación por planta;
- correlación de Pearson;
- identificación de valores potencialmente atípicos;
- evaluación de calidad;
- visualizaciones;
- conclusiones principales.

El notebook puede visualizarse directamente desde GitHub, permitiendo revisar tanto el código como los resultados generados.

---

## Programación modular

Las funciones reutilizables del proyecto se encuentran almacenadas en la carpeta:

`src/`

### `funciones_analisis.py`

Incluye funciones relacionadas con:

- cálculo vectorizado de eficiencia de remoción mediante NumPy;
- correlación de Pearson mediante SciPy;
- detección de valores potencialmente atípicos mediante Z-score.

### `persistencia.py`

Contiene funciones para:

- guardar resultados mediante Joblib;
- recuperar resultados previamente almacenados.

Esta estructura permite separar las operaciones específicas del script principal y mejora la organización, reutilización y mantenibilidad del código.

---

## Evaluación de calidad de los datos

El archivo:

`evaluacion_calidad.py`

realiza una evaluación automática de distintos aspectos de calidad del dataset.

Las validaciones realizadas consideran:

- valores nulos;
- registros duplicados;
- fechas inválidas;
- valores de cumplimiento fuera del dominio esperado;
- valores negativos en variables que no deberían presentarlos;
- casos donde la DBO de salida sea superior a la DBO de entrada;
- valores potencialmente atípicos en la DBO de salida.

Los resultados obtenidos fueron:

| Indicador de calidad | Resultado |
|---|---:|
| Registros analizados | 200 |
| Valores nulos | 0 |
| Registros duplicados | 0 |
| Fechas inválidas | 0 |
| Valores de cumplimiento inválidos | 0 |
| Valores negativos | 0 |
| DBO salida > DBO entrada | 0 |
| Valores potencialmente atípicos en DBO de salida | 2 |

Los dos registros potencialmente atípicos fueron identificados utilizando un criterio de Z-score absoluto superior a 3.

Estos registros no fueron eliminados automáticamente, debido a que podrían representar condiciones reales o excepcionales del proceso y requieren revisión antes de ser considerados errores.

El informe generado se almacena en:

`outputs/informe_calidad_datos.xlsx`

---

## Principales resultados

A partir de los 200 registros analizados se obtuvieron los siguientes resultados generales:

- DBO de salida promedio: **36,18 mg/L**.
- Eficiencia promedio de remoción: **87,09 %**.
- Cumplimiento normativo general: **22,50 %**.
- Correlación entre DBO de entrada y DBO de salida: **r = 0,759**.
- Significancia estadística: **p < 0,001**.
- Valores potencialmente atípicos en DBO de salida: **2**.

### Resultados por planta

| Planta | Registros | DBO salida promedio | Eficiencia promedio | Cumplimiento |
|---|---:|---:|---:|---:|
| Planta Centro | 75 | 35,90 mg/L | 87,51 % | 22,67 % |
| Planta Norte | 71 | 36,56 mg/L | 86,65 % | 16,90 % |
| Planta Sur | 54 | 36,06 mg/L | 87,10 % | 29,63 % |

Durante el período analizado, la Planta Sur presentó el mayor porcentaje de cumplimiento, mientras que la Planta Norte presentó el menor.

La correlación positiva entre DBO de entrada y DBO de salida indica que mayores concentraciones de DBO de entrada tienden a asociarse con mayores concentraciones de DBO en el efluente.

Este resultado representa una asociación estadística y no demuestra por sí solo una relación causal.

---

## Dashboard exploratorio

El archivo:

`dashboard_aqualimpia.py`

implementa un dashboard interactivo utilizando Streamlit y Plotly.

El dashboard permite:

- filtrar información por planta;
- seleccionar rangos de fechas;
- visualizar la cantidad de registros;
- consultar la DBO promedio de salida;
- consultar la eficiencia promedio de remoción;
- visualizar el porcentaje de cumplimiento normativo;
- comparar el comportamiento entre plantas;
- analizar la relación entre DBO de entrada y DBO de salida;
- observar la evolución temporal de la DBO;
- explorar relaciones entre variables operacionales y desempeño.

Para ejecutarlo:

```bash
streamlit run dashboard_aqualimpia.py
```

---

## Visualizaciones generadas

El proyecto genera los siguientes gráficos:

`graficos/cumplimiento_por_planta.png`

`graficos/dbo_entrada_vs_salida.png`

`graficos/evolucion_dbo_salida.png`

Estas visualizaciones permiten comparar el comportamiento de las plantas y analizar las principales relaciones identificadas durante el estudio.

---

## Archivos de salida

Como parte del procesamiento se generan archivos destinados a distintas áreas de AquaLimpia S.A.

### Área de Operaciones

Archivo:

`outputs/salida_operaciones.xlsx`

Contiene información relacionada con:

- fecha;
- planta;
- caudal de entrada;
- DBO de entrada;
- DBO de salida;
- energía de aireación;
- lodos generados;
- eficiencia de remoción;
- estado de cumplimiento.

### Área de Gestión Ambiental

Archivo:

`outputs/salida_gestion_ambiental.xlsx`

Contiene información relacionada con:

- fecha;
- planta;
- DBO del efluente;
- eficiencia de remoción;
- cumplimiento normativo.

### Resumen por planta

También se genera:

`outputs/resumen_por_planta.xlsx`

Este archivo contiene indicadores resumidos para cada planta de tratamiento.

---

## Persistencia de resultados

Mediante Joblib se genera el archivo:

`outputs/resultados_analisis.joblib`

Este archivo permite almacenar y recuperar los principales resultados obtenidos durante el análisis sin necesidad de repetir todos los cálculos.

---

## Control de versiones

El proyecto utiliza Git y GitHub para mantener trazabilidad sobre los cambios realizados.

Durante el desarrollo se registraron commits independientes asociados a las principales etapas del proyecto:

1. Configuración inicial del proyecto.
2. Incorporación del análisis exploratorio y resultados.
3. Incorporación del dashboard exploratorio interactivo.
4. Incorporación de la documentación técnica.
5. Modularización del análisis mediante NumPy, SciPy y Joblib.
6. Incorporación de la evaluación de calidad de datos.
7. Incorporación del notebook reproducible.
8. Actualización de la documentación final del proyecto.

---

## Repositorio GitHub

El proyecto completo se encuentra disponible en:

https://github.com/0UchihaMadara0/AquaLimpia-Ciencia-Datos

---

## Conclusión

El proyecto desarrollado permite analizar el desempeño de las plantas de tratamiento de AquaLimpia S.A. mediante un proceso reproducible que integra preparación de datos, análisis descriptivo, análisis estadístico, evaluación de calidad, programación modular, visualización interactiva, generación de archivos especializados y control de versiones.

Los resultados permiten comparar el desempeño de las plantas, evaluar la relación entre variables relevantes y disponer de información diferenciada para las áreas de Operaciones y Gestión Ambiental.

La incorporación del notebook facilita la revisión secuencial del análisis, mientras que la estructura modular mejora la reutilización del código. Finalmente, Git y GitHub proporcionan trazabilidad sobre la evolución del proyecto y permiten centralizar los datos, scripts, resultados y documentación técnica en un único repositorio.