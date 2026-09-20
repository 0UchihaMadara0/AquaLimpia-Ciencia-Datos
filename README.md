# Proyecto de Ciencia de Datos - AquaLimpia S.A.

## Descripción del proyecto

AquaLimpia S.A. es una empresa dedicada al tratamiento de aguas
residuales urbanas e industriales.

El proyecto tiene como propósito analizar el desempeño de sus plantas
de tratamiento, identificar patrones asociados a la calidad del
efluente y generar información que apoye la toma de decisiones de las
áreas de Operaciones y Gestión Ambiental.

---

## Objetivo general

Analizar el desempeño de las plantas de tratamiento de AquaLimpia S.A.,
identificando patrones asociados a la DBO del efluente, la eficiencia
de remoción y el cumplimiento normativo.

---

## Objetivos específicos

- Comparar el desempeño de las plantas de tratamiento.
- Calcular la eficiencia de remoción de DBO.
- Analizar la relación entre DBO de entrada y DBO de salida.
- Evaluar el comportamiento del cumplimiento normativo.
- Explorar la relación entre variables operacionales y desempeño.
- Generar información diferenciada para Operaciones y Gestión Ambiental.
- Construir un dashboard exploratorio para facilitar la interpretación
  de los resultados.

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

El dataset contiene 200 registros correspondientes a tres plantas de
tratamiento:

- Planta Centro
- Planta Norte
- Planta Sur

El período analizado comprende desde el 1 de julio hasta el
28 de octubre de 2025.

---

## Variables principales

Las principales variables utilizadas son:

- Fecha de registro.
- Planta de tratamiento.
- Caudal de entrada.
- DBO de entrada.
- DBO de salida.
- SST de salida.
- pH del efluente.
- Energía utilizada en aireación.
- Lodos generados.
- Cumplimiento normativo.

También se genera la variable:

`eficiencia_remocion_pct`

calculada mediante:

Eficiencia (%) =
((DBO entrada - DBO salida) / DBO entrada) × 100

---

## Flujo de trabajo

El proyecto utiliza el siguiente flujo analítico:

Dataset original

↓

Validación de estructura

↓

Preparación y transformación de datos

↓

Cálculo de indicadores

↓

Análisis descriptivo y estadístico

↓

Generación de gráficos

↓

Dashboard interactivo

↓

Generación de archivos de salida

↓

Control de versiones mediante Git y GitHub

---

## Librerías utilizadas

El proyecto utiliza las siguientes librerías de Python:

- pandas
- matplotlib
- scipy
- openpyxl
- streamlit
- plotly
- numpy
- joblib

Las dependencias también están documentadas en:

`requirements.txt`

Para instalarlas se puede utilizar:

```bash
pip install -r requirements.txt