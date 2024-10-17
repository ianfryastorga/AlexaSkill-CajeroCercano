# Cajero Cercano - Skill de Alexa

## Descripción

**Cajero Cercano** es una Skill de Alexa que ayuda a los usuarios a encontrar los cajeros automáticos y cajas vecinas más cercanos a su ubicación actual utilizando la API de Google Maps.

## Características

- Obtiene la dirección del dispositivo del usuario.
- Geocodifica la dirección para obtener coordenadas geográficas.
- Utiliza la API de Places de Google Maps para encontrar cajeros cercanos.
- Proporciona al usuario una lista de los cajeros más cercanos con distancia y dirección.

## Requisitos Previos

- **Cuenta de Desarrollador de Amazon Alexa**: Puedes registrarte en [developer.amazon.com](https://developer.amazon.com/).
- **Cuenta de Google Cloud Platform** con acceso a las APIs de Google Maps (Geocoding y Places).
- **Python 3.7 o superior**.
- **Clave de API de Google Maps**: Necesitarás una clave de API con los permisos adecuados.

## Configuración

### Opción 1: Usar la Función **Code** de la Consola de Desarrollador de Amazon

#### Paso 1: Crear la Skill en la Alexa Developer Console

1. Inicia sesión en la [Alexa Developer Console](https://developer.amazon.com/alexa/console/ask).
2. Haz clic en **"Create Skill"**.
3. Ingresa el nombre de la Skill, por ejemplo, **"Cajero Cercano"**.
4. Selecciona el idioma **Español (ES)**.
5. En **"Choose a model to add to your skill"**, selecciona **"Custom"**.
6. En **"Choose a method to host your skill's backend resources"**, selecciona **"Alexa-Hosted (Python)"**.
7. Haz clic en **"Create Skill"**.

#### Paso 2: Configurar el Modelo de Interacción

1. En la pestaña **"Build"**, ve a **"Interaction Model"** > **"JSON Editor"**.
2. Define tus intents y utterances según tus necesidades. Por ejemplo, agrega un intent llamado **"BuscarCajeroIntent"**.
3. Haz clic en **"Save Model"** y luego en **"Build Model"**.

#### Paso 3: Agregar Permisos a la Skill

1. En el menú lateral, selecciona **"Permissions"**.
2. Activa el permiso para **"Dirección completa"** (`alexa::devices:all:address:full:read`).
3. Haz clic en **"Save Permissions"**.

#### Paso 4: Agregar la Clave de API de Google Maps

1. En la pestaña **"Code"**, expande la carpeta **"Environment Variables"**.
2. Haz clic en **"Add"** para agregar una nueva variable de entorno.
3. Ingresa `GOOGLE_API_KEY` como clave y tu clave de API de Google Maps como valor.
4. Haz clic en **"Save"**.

#### Paso 5: Reemplazar el Código de la Skill

1. En la pestaña **"Code"**, abre el archivo `lambda_function.py`.
2. Reemplaza el contenido de `lambda_function.py` con el código de tu Skill.
3. Si tienes un archivo `requirements.txt`, reemplázalo también con tus dependencias (por ejemplo, `requests`).
4. Haz clic en **"Save"** y luego en **"Deploy"** para desplegar el código.

#### Paso 6: Probar la Skill

1. Ve a la pestaña **"Test"** y activa el modo de prueba (cambia el interruptor a **"Development"**).
2. Prueba la Skill utilizando el simulador o tu propio dispositivo Alexa.
3. Di: **"Alexa, abre Cajero Cercano"** y luego **"¿Dónde está el cajero más cercano?"**.

#### Paso 7: Otorgar Permisos en la Aplicación Alexa

1. Abre la aplicación Alexa en tu dispositivo móvil.
2. Ve a **"Más"** > **"Skills y juegos"** > **"Tus Skills"** > **"Desarrollo"**.
3. Selecciona tu Skill **"Cajero Cercano"**.
4. Toca en **"Configuración"** > **"Permisos"**.
5. Activa el permiso para **"Dirección del dispositivo"**.
6. Guarda los cambios.

#### Paso 8: Configurar la Dirección del Dispositivo

1. En la aplicación Alexa, ve a **"Dispositivos"** > **"Echo y Alexa"**.
2. Selecciona **"Este dispositivo"**, **"Aplicación Alexa"** o el dispositivo que estés usando.
3. Toca en **"Ubicación del dispositivo"**.
4. Ingresa tu dirección completa y guarda los cambios.

### Opción 2: Usar AWS Lambda

#### Paso 1: Crear la Skill en la Alexa Developer Console

1. Inicia sesión en la [Alexa Developer Console](https://developer.amazon.com/alexa/console/ask).
2. Haz clic en **"Create Skill"**.
3. Ingresa el nombre de la Skill, por ejemplo, **"Cajero Cercano"**.
4. Selecciona el idioma **Español (ES)**.
5. En **"Choose a model to add to your skill"**, selecciona **"Custom"**.
6. En **"Choose a method to host your skill's backend resources"**, selecciona **"Provision your own"**.
7. Haz clic en **"Create Skill"**.

#### Paso 2: Configurar el Modelo de Interacción

1. En la pestaña **"Build"**, ve a **"Interaction Model"** > **"JSON Editor"**.
2. Define tus intents y utterances según tus necesidades.
3. Haz clic en **"Save Model"** y luego en **"Build Model"**.

#### Paso 3: Crear una Función Lambda en AWS

1. Inicia sesión en la consola de AWS y ve a **"Lambda"**.
2. Haz clic en **"Create function"**.
3. Selecciona **"Author from scratch"**.
4. Ingresa un nombre para la función, por ejemplo, **"CajeroCercanoFunction"**.
5. Selecciona **"Python 3.8"** como runtime.
6. En **"Permissions"**, crea o selecciona un rol con permisos para CloudWatch Logs.
7. Haz clic en **"Create function"**.

#### Paso 4: Agregar el Código a la Función Lambda

1. En la consola de Lambda, desplázate hacia abajo hasta el editor de código.
2. Copia y pega tu código en el archivo `lambda_function.py`.
3. Si tienes dependencias adicionales (por ejemplo, `requests`), necesitarás empaquetar el código y las dependencias en un archivo ZIP e importarlo:
   - Crea una carpeta en tu computadora.
   - Copia `lambda_function.py` a esa carpeta.
   - Instala las dependencias localmente dentro de esa carpeta:
     ```bash
     pip install requests -t .
     ```
   - Comprime el contenido de la carpeta en un archivo ZIP.
   - En la consola de Lambda, haz clic en **"Upload from"** > **".zip file"** y selecciona el archivo ZIP.
4. Configura las variables de entorno:
   - En la sección **"Configuration"**, ve a **"Environment variables"**.
   - Haz clic en **"Edit"** y luego en **"Add environment variable"**.
   - Agrega `GOOGLE_API_KEY` como clave y tu clave de API de Google Maps como valor.
   - Guarda los cambios.

#### Paso 5: Configurar el Handler

- Asegúrate de que el handler esté configurado como `lambda_function.lambda_handler`.

#### Paso 6: Configurar el Trigger de Alexa Skill Kit

1. En la consola de Lambda, ve a la sección **"Function overview"**.
2. Haz clic en **"Add trigger"**.
3. Selecciona **"Alexa Skills Kit"**.
4. Haz clic en **"Add"**.

#### Paso 7: Vincular la Skill con la Función Lambda

1. En la Alexa Developer Console, ve a **"Endpoint"** en el menú lateral.
2. Selecciona **"AWS Lambda ARN"** como tipo de endpoint.
3. En **"Default Region"**, pega el ARN de tu función Lambda.
4. Haz clic en **"Save Endpoints"**.

#### Paso 8: Agregar Permisos a la Skill

1. En el menú lateral, selecciona **"Permissions"**.
2. Activa el permiso para **"Dirección completa"** (`alexa::devices:all:address:full:read`).
3. Haz clic en **"Save Permissions"**.

#### Paso 9: Probar la Skill

1. En la pestaña **"Test"**, activa el modo de prueba.
2. Prueba la Skill utilizando el simulador o tu propio dispositivo Alexa.
3. Otorga los permisos y configura la dirección del dispositivo como se describe en los pasos anteriores.

## Notas Importantes

- **Gestión de Dependencias**: Cuando usas AWS Lambda, debes empaquetar tus dependencias con tu código. Esto implica instalar las dependencias en una carpeta local y luego subirlas como un paquete ZIP.
- **Variables de Entorno**: Asegúrate de configurar correctamente las variables de entorno, especialmente `GOOGLE_API_KEY`.
- **Permisos**: Los permisos deben configurarse tanto en la Alexa Developer Console como en la aplicación Alexa en tu dispositivo móvil.
- **Pruebas**: Siempre prueba tu Skill en un dispositivo físico si es posible, ya que algunas funcionalidades pueden no estar disponibles en el simulador.

## Licencia

Este proyecto se distribuye bajo la licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.
