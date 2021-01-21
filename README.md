<center><u><h1>Email Taxonomy</h1></u></center>

## 1. Índice

1. Índice
2. Introducción
3. Descripción
    * 3.1 Descripción de los campos
4. Estrutura de carpetas
5. Parámetros
    * 5.1 Archivo de configuración
    * 5.2 Datos de entrada
6. Resultados
7. Ejecución

## 2. Introducción
Email Taxonomy es una aplicación que analiza y clasifica correos electrónicos.
Email Taxonomy realiza una clasificación de correos electrónicos analizando los temas principales (topics) que se tratan en dichos correos. El algoritmo implementado para esta clasificación es el algoritmo de Latent Dirichlet Allocation (LDA).

## 3. Descripción

### 3.1 Descripción de los campos

## 4. Estrutura de carpetas
```python
email-taxonomy
    |
    |-------- config/
    |              |-------- config.json
    |
    |-------- code/
    |
    |-------- data/
    |             |-------- enron-dataset.csv
    |
    |-------- logs/
    |
    |-------- output/
    |            |-------- model_trained/
    |
    |-------- tmp/
```

Para que la aplicación funcione se debe respetar esta estructura de carpetas.

** Nota:** \
Dentro de la carpeta tmp/ se crearán archivos de datos temporales de todas las ejecuciones por las que pasa el conjunto de datos.

## 5. Parámetros

### 5.1 Archivo de configuración

El archivo `config.json`debe estar ubicado en la carpeta `config``

#### Variables requeridas

    "train": (boolean) variable para indicar que entrene un modelo LDA
    "predict": (boolean) variable para indicar que haga una predicción sobre ese modelo
    "n_top_words": (integer) número de n top palabras de cada tópic.

### 5.2 Datos de entrada

Se requiere un archivo de entrada, un csv que contenga la informacion de correos electrónicos. En este caso:
* **enron_05_17_2015_with_labels_v2_100K_chunk_1_of_6.csv**: dataset con los correos electrónicos de los empleados de la empresa Enron.

## 6. Resultados

Entre los resultados, se guardan tres archivos:
1) El modelo LDA.
2) El modelo de Count Vectorizer
3) Un excel con las palabras mas relevantes de cada topic.

## 7. Ejecución

Para esta aplicacion se ha utilizado la versión de Python 3.8.0. Para ejecutar este proyecto, tanto solo hay situarse en la raíz del proyecto y ejecutar la siguiente línea de código:

```python
python3.8 code/main_app.py
```