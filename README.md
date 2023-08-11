# MoviesRecomendation

# Sistema de Recomendación para Plataforma de Streaming - README

¡Bienvenido/a al repositorio del proyecto de desarrollo de un sistema de recomendación para una plataforma de streaming! En este README, encontrarás información esencial sobre el proyecto, su objetivo, el rol del Data Scientist y los pasos que se han seguido para lograr el desarrollo del sistema de recomendación.

## Descripción del Proyecto

En este proyecto, hemos abordado el desafío de crear un sistema de recomendación desde cero para una start-up que ofrece servicios de agregación de plataformas de streaming. El objetivo principal es diseñar un modelo de Machine Learning que proporcione recomendaciones a los usuarios en función de los datasets iniciales.

## Rol del Data Scientist

Como Data Scientist, mi tarea fue crear el modelo de recomendación desde cero. Sin embargo, antes de llegar a este punto, se hizo evidente que los datos disponibles eran poco maduros, a continuación se deja un enlace por si se quieren revisar:

[DataSets](https://drive.google.com/drive/u/0/folders/1OXVDvmAxOYmEG15Ns0d8UA9Z6Tbdx34l)


Tenían algunos problemas para su estudio como anidamiento de datos, falta de transformaciones,etc. Para superar estos desafíos, asumí un papel de Data Engineer al principio del proyecto para preparar los datos y establecer las bases para el desarrollo del modelo. Obteniendo los siguientes resultados:

[https://github.com/Benjaminmxxx/MoviesRecomendation/tree/main/DatosProcesados](DataSets Limpios)


## Pasos Realizados

El proyecto se ha dividido en las siguientes etapas:

### 1. Ingeniería de Datos

Como los datos iniciales no eran adecuados para el desarrollo del modelo, se realizó un proceso de ingeniería de datos. Esto implicó limpiar los datos, realizar transformaciones necesarias.

## Preparación de los DataSets.csv para la API

En esta fase de preparación de datos, se aplicaron una serie de transformaciones clave para asegurar la viabilidad y eficacia del MVP. Entre las transformaciones realizadas se incluyen:

- **Desanidamiento de Campos:** Dada la naturaleza anidada de algunos campos como, se llevó a cabo un proceso de desanidamiento para convertir estos campos en estructuras planas que se puedan consultar de manera eficiente en la API. Los valores de estos campos anidados se unieron nuevamente al conjunto de datos, lo que facilita las futuras consultas de la API. 

- **Manejo de Valores Nulos:** Para garantizar la coherencia, los valores nulos en estos campos se rellenaron con el número 0, lo que permitirá cálculos y análisis sin problemas.

- **Limpieza de Fechas:** El campo release date, que contiene las fechas de estreno, fue sometido a una limpieza exhaustiva. Se eliminaron los valores nulos y se formatearon las fechas para que cumplan con el estándar AAAA-mm-dd, lo que facilitará su uso en consultas y análisis posteriores.

- **Creación de Nuevas Columnas:** Con el objetivo de enriquecer el conjunto de datos, se crearon nuevas columnas.

- **Eliminación de Columnas no Utilizadas:** Para simplificar y optimizar el conjunto de datos, se eliminaron las columnas que no serán utilizadas en el proceso de recomendación.

Estas transformaciones fueron esenciales para garantizar que los DataSets.csv fueran aptos para su uso en la API del sistema de recomendación. Las acciones tomadas durante esta fase sentaron las bases para el desarrollo exitoso del sistema y la generación de recomendaciones precisas y efectivas para los usuarios.

### 2. Análisis de Datos

Se realizó un análisis de los datos disponibles, identificando su calidad, estructura y potenciales problemas. Esto ayudó a comprender la magnitud de la tarea y a definir los pasos siguientes.

### 3. Desarrollo de la API

En la fase de desarrollo de la API, se propuso la implementación del framework FastAPI para exponer los datos de la empresa. Las funciones implementadas en esta API brindan a los usuarios la capacidad de acceder a datos relevantes y realizar consultas específicas sobre el contenido y las características de las películas y series disponibles en la plataforma de streaming.

- `peliculas_idioma(Idioma: str)`: Permite ingresar un idioma y devuelve la cantidad de películas producidas en ese idioma. Ejemplo de retorno: "X cantidad de películas fueron estrenadas en idioma Y."

- `peliculas_duracion(Pelicula: str)`: Permite ingresar una película y devuelve la duración y el año de lanzamiento. Ejemplo de retorno: "Duración: X. Año: XX."

- `franquicia(Franquicia: str)`: Al ingresar una franquicia, retorna la cantidad de películas, ganancia total y ganancia promedio de la franquicia. Ejemplo de retorno: "La franquicia X posee Y películas, una ganancia total de Z y una ganancia promedio de W."

- `peliculas_pais(Pais: str)`: Permite ingresar un país y retorna la cantidad de películas producidas en ese país. Ejemplo de retorno: "Se produjeron X películas en el país Y."

- `productoras_exitosas(Productora: str)`: Al ingresar una productora, devuelve el revenue total y la cantidad de películas que realizó. Ejemplo de retorno: "La productora X ha tenido un revenue de Y."

- `get_director(nombre_director)`: Permite ingresar el nombre de un director que se encuentre en el dataset y devuelve su nivel de éxito, junto con el nombre de cada película que dirigió, su fecha de lanzamiento, retorno individual, costo y ganancia. La información se presenta en un formato de lista.

### 3.1 Diseño del Modelo

Una vez que los datos estuvieron preparados, se procedió a diseñar el modelo de recomendación. Se implemento un modelo de recomendación utilizando técnicas de procesamiento de lenguaje natural (NLP), usando TfidfVectorizer para crear representaciones numéricas de texto basadas en TF-IDF (Term Frequency-Inverse Document Frequency) se asigno puntuaciones a las palabras de acuerdo a la combinación de columnas "title", "genres" y "overview" para saber su importancia relativa y se uso cosine_similarity para calcular la similitud de coseno entre vectores que calcula la similitud de coseno entre todos los pares de películas utilizando la matriz TF-IDF. Esto mide cuán similares son los documentos en función de sus características numéricas.

 En un DataFrame llamado "item_similarity" se guardaron los resultados de similitud de coseno , donde las filas y columnas representan títulos de películas, y los valores en la intersección indican la similitud entre las películas correspondientes. 

Para optimizar espacio en el deploy de la API se obto por realizar una iteración sobre "item_similarity" que generara un diccionario "my_dict" donde se ingresa en las claves títulos de películas y en los valores listas de títulos de películas recomendadas de acuerdo al valor de similitud, después se convierte en un DataFrame llamado "df" con dos columnas: "Movie" (Película) y "Recomendacion" (Recomendación). Finalmente, este DataFrame se exporta a un archivo CSV llamado "recomendation.csv".

El resultado final es un archivo CSV que contiene las recomendaciones para cada película, y se proporciona una función para obtener las recomendaciones de una película específica.


### 4. Despliegue del MVP

Se implementó un MVP (Minimum Viable Product) del sistema de recomendación en el entorno de la plataforma de Render. Se integró el modelo en la infraestructura existente y se realizaron pruebas exhaustivas para asegurar su funcionalidad y rendimiento en un entorno real.
