from fastapi import FastAPI
import pandas as pd

df_movies = pd.read_csv("./DatosProcesados/movies.csv")
df_crew = pd.read_csv("./DatosProcesados/crew.csv") 
df_cast = pd.read_csv("./DatosProcesados/cast.csv")
df_recomendation=pd.read_csv("./DatosProcesados/recomendation.csv")
app = FastAPI()

@app.get('/peliculas_idioma/{Idioma}')
def peliculas_idioma(Idioma: str):
    '''Ingresas el idioma, retornando la cantidad de peliculas producidas en el mismo'''

    # Filtrar las filas que contengan el idioma deseado en la columna 'spoken_languages'
    peliculas_en_idioma = df_movies[df_movies['spoken_languages'].str.contains(Idioma, case=False, na=False)]
    
    # Contar la cantidad de filas que cumplen con el filtro
    cantidad_peliculas = len(peliculas_en_idioma)
    
    # Generar el mensaje de retorno
    mensaje_retorno = f"{cantidad_peliculas} cantidad de películas fueron estrenadas en {Idioma}"
    
    return mensaje_retorno

@app.get('/peliculas_duracion/{pelicula}')
def peliculas_duracion(pelicula: str):
    '''Ingresas la película, retornando la duración y el año'''
    
    # Filtrar la fila que coincide con el nombre de la película
    pelicula_filtrada = df_movies[df_movies['title'] == pelicula]
    
    if pelicula_filtrada.empty:
        return {'mensaje': 'Película no encontrada'}
    
    # Obtener la duración y el año de lanzamiento de la película filtrada
    duracion = pelicula_filtrada['runtime'].values[0]  # Suponiendo que 'runtime' es la duración
    anio = pelicula_filtrada['release_year'].values[0]  # Suponiendo que 'release_year' es el año de lanzamiento
    
    # Generar el diccionario de retorno
    respuesta = {'pelicula': pelicula, 'duracion': int(duracion), 'anio': int(anio)}
    
    return respuesta

@app.get('/franquicia/{franquicia}')
def franquicia(franquicia: str):
    # Filtrar las filas que pertenecen a la franquicia deseada en la columna 'belongs_to_collection'
    franquicia_filtrada = df_movies[df_movies['belongs_to_collection'] == franquicia]
    
    if not franquicia_filtrada.empty:
        # Contar la cantidad de películas en la franquicia
        cantidad_peliculas = len(franquicia_filtrada)
        
        # Calcular la ganancia total y el promedio de ganancia
        ganancia_total = franquicia_filtrada['revenue'].sum()  # Suponiendo que 'revenue' es la ganancia
        ganancia_promedio = franquicia_filtrada['revenue'].mean()
        
        # Generar el diccionario de retorno
        respuesta = {
            'franquicia': franquicia,
            'cantidad': cantidad_peliculas,
            'ganancia_total': ganancia_total,
            'ganancia_promedio': ganancia_promedio
        }
        return respuesta
    else:
        return None

@app.get('/peliculas_pais/{pais}')
def peliculas_pais(pais: str):
    '''Ingresas el pais, retornando la cantidad de peliculas producidas en el mismo'''

    # Filtrar las filas que contienen el país deseado en la columna 'production_countries'
    peliculas_en_pais = df_movies[df_movies['production_countries'].str.contains(pais, case=False, na=False)]
    
    # Contar la cantidad de películas que cumplen con el filtro
    cantidad_peliculas = len(peliculas_en_pais)
    
    # Generar el diccionario de retorno
    respuesta = {'pais': pais, 'cantidad': cantidad_peliculas}
    
    return respuesta

@app.get('/productoras_exitosas/{productora}')
def productoras_exitosas(productora: str):
    '''Ingresas la productora, entregandote el revunue total y la cantidad de peliculas que realizo '''

    # Filtrar las filas que contienen la productora deseada en la columna 'production_companies'
    peliculas_de_productora = df_movies[df_movies['production_companies'].str.contains(productora, case=False, na=False)]
    
    if not peliculas_de_productora.empty:
        # Calcular el revenue total y la cantidad de películas de la productora
        revenue_total = peliculas_de_productora['revenue'].sum()
        cantidad_peliculas = len(peliculas_de_productora)
        
        # Generar el diccionario de retorno
        respuesta = {
            'productora': productora,
            'revenue_total': revenue_total,
            'cantidad de pelis': cantidad_peliculas
        }
        return respuesta
    else:
        return 'Invalido'

@app.get('/get_director/{nombre_director}')
def get_director(nombre_director: str):

    ''' Se ingresa el nombre de un director que se encuentre dentro de un dataset debiendo devolver el éxito del mismo medido a través del retorno. 
    Además, deberá devolver el nombre de cada película con la fecha de lanzamiento, retorno individual, costo y ganancia de la misma. En formato lista'''
    
    # Filtrar las filas del DataFrame 'df_crew' que corresponden al director dado
    director_filas = df_crew[   (df_crew['department'] == 'Directing') & 
                                (df_crew['job'] == 'Director') & 
                                (df_crew['name'] == nombre_director)
                            ]
    
    if not director_filas.empty:
        
        # Filtrar las filas del DataFrame 'df_movies' que corresponden al director
        peliculas_director = df_movies[df_movies['id'].isin(director_filas['id'])]
        
        # Calcular el éxito del director
        retorno_total_director = 0
        if peliculas_director['budget'].sum() != 0:
            retorno_total_director = peliculas_director['revenue'].sum() / peliculas_director['budget'].sum()
        
        # Crear una lista de películas con detalles
        peliculas = []
        for index, row in peliculas_director.iterrows():
            if row['budget'] != 0:
                retorno_pelicula = row['revenue'] / row['budget']
            else:
                retorno_pelicula = 0
            peliculas.append({
                'pelicula': row['title'],
                'anio': row['release_year'],
                'retorno_pelicula': retorno_pelicula,
                'budget_pelicula': row['budget'],
                'revenue_pelicula': row['revenue']
            })


# ML
@app.get('/recomendacion/{titulo}')
def obtener_recomendaciones_por_titulo(titulo:str):
    '''Ingresas un nombre de pelicula y te recomienda las similares en una lista''' 
    filtro = df_recomendation['Movie'] == titulo
    if filtro.any():  # Verificar si hay al menos una coincidencia en el título
        recomendaciones = df_recomendation.loc[filtro, 'Recomendacion'].values
        return recomendaciones[0]
    else:
        return None  # No se encontró el título en la lista