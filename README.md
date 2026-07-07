# Análisis de Texto Bíblico - Proyecto de Laboratorio de PLN

Un proyecto integral de **Procesamiento de Lenguaje Natural (PLN)** para analizar textos bíblicos (Antiguo y Nuevo Testamento) utilizando Python. Este proyecto abarca las etapas de análisis estadístico, modelado clásico, arquitectura web (API REST) y visualización interactiva, cumpliendo con los requerimientos de los Laboratorios 2 y 3.

---

# 📋 Tabla de Contenidos

- [Descripción General](#-descripción-general)
- [Características](#-características)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Instalación](#-instalación)
- [Uso](#-uso)
- [Módulos](#-módulos)
- [Requisitos](#-requisitos)
- [Salida](#-salida)
- [Detalles Técnicos](#-detalles-técnicos)

---

# 🎯 Descripción General

Este proyecto analiza el corpus completo de la Biblia (English Standard Version / BBE) utilizando técnicas modernas de Procesamiento de Lenguaje Natural.

La aplicación evolucionó desde una colección de scripts independientes hacia una **arquitectura cliente-servidor**, donde el procesamiento pesado se realiza mediante una API REST desarrollada con FastAPI y la interacción con el usuario se lleva a cabo mediante un dashboard desarrollado en Streamlit.

Entre sus funcionalidades se incluyen:

- Análisis de sentimientos utilizando VADER.
- Vectorización mediante TF-IDF.
- Embeddings con Word2Vec.
- Clasificación de texto utilizando Naive Bayes.
- Búsqueda semántica mediante similitud del coseno.
- Generación estadística de texto utilizando modelos N-Gram.
- Visualizaciones interactivas en 2D y 3D mediante PCA.

---

# ✨ Características

- Arquitectura Cliente-Servidor con FastAPI + Streamlit.
- Generación de texto mediante modelos Unigram, Bigram, Trigram y Quadgram.
- Representación vectorial utilizando TF-IDF y Word2Vec.
- Visualización interactiva 2D y 3D con Plotly.
- Búsqueda semántica de versículos mediante similitud del coseno.
- Análisis de sentimientos con VADER.
- Clasificación automática de versículos mediante Naive Bayes Multinomial.
- Dashboard con estadísticas dinámicas y filtros en tiempo real.

---

# 📁 Estructura del Proyecto

```text
.
├── README.md
├── UMLLAB2.drawio
├── archive/
│   ├── key_english.csv
│   └── t_bbe.csv
├── api.py
├── app.py
├── buscador.py
├── clasificador.py
├── visualizacion.py
└── src/
    ├── book.py
    ├── chapter.py
    ├── genre.py
    ├── loader.py
    ├── testament.py
    ├── verse.py
    └── nlp/
        ├── classifier.py
        ├── cleaner.py
        ├── generator.py
        ├── metrics.py
        ├── pipeline.py
        ├── sentiment.py
        ├── stopwords.py
        ├── tfidf.py
        └── w2v.py
```

---

# 🚀 Instalación

## Prerrequisitos

- Python 3.8 o superior
- pip

## 1. Clonar el repositorio

```bash
git clone <repositorio>
cd Laboratorio2
```

## 2. Crear un entorno virtual

Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

Windows

```bash
venv\Scripts\activate
```

## 3. Instalar dependencias

```bash
pip install pandas numpy scikit-learn matplotlib seaborn wordcloud nltk fastapi uvicorn streamlit requests gensim plotly
```

## 4. Preparar los datos

Crear una carpeta llamada **archive/** con los siguientes archivos:

```
archive/
├── key_english.csv
└── t_bbe.csv
```

- **key_english.csv:** metadatos de los libros.
- **t_bbe.csv:** corpus de versículos bíblicos.

---

# 📖 Uso

El proyecto puede utilizarse mediante una interfaz web o desde la línea de comandos.

---

## Opción A: Interfaz Web (Recomendada)

### Iniciar la API

```bash
uvicorn api:app
```

Esperar hasta visualizar:

```
Application startup complete
```

Durante el inicio se generan automáticamente:

- TF-IDF
- Word2Vec
- PCA
- Modelos N-Gram

Este proceso puede tardar algunos minutos.

---

### Iniciar Streamlit

En otra terminal:

```bash
streamlit run app.py
```

La aplicación abrirá automáticamente el navegador.

La interfaz contiene cuatro módulos:

- Dashboard
- Search
- PCA & Word2Vec
- Generator

---

## Opción B: Línea de comandos

### Clasificación y generación

```bash
python clasificador.py
```

### Buscador semántico

```bash
python buscador.py
```

### Visualizaciones

```bash
python visualizacion.py
```

---

# 📚 Módulos

## Clases principales

### Verse

Representa un versículo individual junto con sus frecuencias de palabras.

### Chapter

Contenedor de versículos pertenecientes a un capítulo.

### Book

Contenedor de capítulos con metadatos del libro.

### Testament

Contenedor del Antiguo o Nuevo Testamento.

---

## Procesamiento de PLN

### pipeline.py

Implementa el flujo principal de procesamiento.

### cleaner.py

Realiza:

- Conversión a minúsculas.
- Eliminación de puntuación.
- Eliminación de stopwords.

### tfidf.py

Implementa:

- TF-IDF
- Normalización L2
- Similitud del coseno

### w2v.py

Entrena un modelo Word2Vec y genera embeddings promedio por versículo.

### generator.py

Construye modelos probabilísticos N-Gram para generación de texto.

### sentiment.py

Realiza análisis de sentimientos utilizando VADER.

### classifier.py

Entrena y evalúa el clasificador Naive Bayes.

### metrics.py

Calcula métricas de similitud y distancia.

### stopwords.py

Contiene la lista de stopwords utilizadas durante el procesamiento.

---

# 📦 Requisitos

| Biblioteca | Uso |
|------------|-----|
| fastapi | API REST |
| uvicorn | Servidor ASGI |
| streamlit | Dashboard |
| requests | Comunicación API |
| gensim | Word2Vec |
| plotly | Visualizaciones interactivas |
| scikit-learn | PCA, Naive Bayes y TF-IDF |
| pandas | Manipulación de datos |
| numpy | Operaciones numéricas |
| matplotlib | Gráficos estáticos |
| seaborn | Visualizaciones |
| wordcloud | Nube de palabras |
| nltk | Procesamiento de lenguaje y VADER |

---

# 📊 Salida

## Streamlit

- Dashboard interactivo.
- Resultados de búsqueda.
- Gráficos Plotly.
- Embeddings 2D y 3D.
- Generación de texto.

---

## CLI

Se generan imágenes como:

- `evolucionsentimientolibros.png`
- `matrizconfusion_nb2.png`
- `nube_palabras_*.png`

Además de reportes tabulares en consola.

---

# 🔬 Detalles Técnicos

## Arquitectura

El procesamiento pesado se realiza completamente en FastAPI.

Durante el inicio de la aplicación se cargan en memoria:

- Corpus
- TF-IDF
- Word2Vec
- PCA
- Modelos N-Gram

La interfaz Streamlit únicamente consume los endpoints REST y renderiza los resultados.

Endpoints principales:

- `/dashboard`
- `/search`
- `/embeddings`
- `/generate`

---

## Generación de Texto

La generación utiliza modelos estadísticos N-Gram.

Se implementan:

- Unigram
- Bigram
- Trigram
- Quadgram

La generación se basa en cadenas de Markov y probabilidades obtenidas a partir de frecuencias del corpus.

No se utilizan modelos neuronales preentrenados.

---

## Embeddings

Se implementan dos representaciones vectoriales:

### TF-IDF

Representación dispersa basada en frecuencia de términos.

### Word2Vec

Embeddings densos generados mediante Gensim.

Cada versículo se representa mediante el promedio de los vectores de sus palabras.

---

## Reducción de dimensionalidad

Las representaciones vectoriales son proyectadas mediante PCA a:

- 2 Componentes Principales
- 3 Componentes Principales

Estas proyecciones son utilizadas por Plotly para generar visualizaciones interactivas que permiten observar la distribución semántica de los versículos entre el Antiguo y Nuevo Testamento.


