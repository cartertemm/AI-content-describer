# AI Content Describer para NVDA

Este complemento permite obtener descripciones detalladas de imágenes, controles de interfaz de usuario y otro contenido visualmente inaccesible.

Aprovechando las capacidades multimodales de modelos de IA avanzados y algoritmos de visión por computadora, nuestro objetivo es ofrecer descripciones de contenido de primera calidad y aumentar la independencia en general. Para más información sobre los modelos subyacentes, consulte la sección correspondiente de este documento.

## Características

* Describe el objeto enfocado, el objeto del navegador, la pantalla completa, o toma una foto con la cámara integrada
* Describe cualquier imagen que se haya copiado al portapapeles, ya sea una imagen de un correo electrónico o una ruta en el explorador de Windows
* Indica si la cara del usuario está posicionada en el centro del encuadre usando algoritmos de visión por computadora (no requiere acceso de API de pago)
* Gratis por defecto, opcionalmente añada su propia clave de API para más modelos
* Compatible con múltiples proveedores (GPT de OpenAI y el nivel gratuito de Pollinations, Gemini de Google, Pixtral Large de Mistral, Claude de Anthropic, Grok de xAI, vivo BlueLM Vision a través de NVDA-CN, Ollama, llama.cpp, LiteLLM Proxy y Seer)
* Compatible con una amplia variedad de formatos incluyendo PNG (.png), JPEG (.jpeg y .jpg), WEBP (.webp) y GIF no animado (.gif)
* Opcionalmente almacena en caché las respuestas para preservar la cuota de API
* Para uso avanzado, personalice el prompt y el recuento de tokens para adaptar la información a sus necesidades
* Haga preguntas de seguimiento y adjunte imágenes adicionales
* Renderizado de Markdown para acceder fácilmente a información estructurada (simplemente active la opción "abrir resultados en un diálogo navegable" e incluya, por ejemplo, "responde en Markdown" al final de sus prompts)

## Caso de uso

Hubo algunas motivaciones principales detrás de este proyecto.

NVDA es capaz de realizar reconocimiento óptico de caracteres (OCR) de forma nativa, lo cual es revolucionario. Si está intentando extraer texto de una imagen o documento PDF, esto es lo que busca.

Sin embargo, el OCR solo puede analizar datos que *podrían* ser texto. Se queda corto a la hora de considerar el contexto, los objetos y las relaciones transmitidas en esas imágenes. E internet está lleno de ellas. Logotipos, retratos, memes, iconos, gráficos, diagramas, gráficas de barras/líneas... Los que quiera. Están en todas partes, y generalmente no están en un formato que los usuarios de lectores de pantalla puedan interpretar.
Hasta hace poco, había una dependencia inquebrantable en que los autores de contenido proporcionaran descripciones de texto alternativo. Si bien esto sigue siendo imprescindible, es difícil cambiar el hecho de que un alto estándar de calidad resulta ser la excepción, no la regla.

Ahora, las posibilidades son casi infinitas. Podría:

* Visualizar el escritorio o una ventana específica para entender la ubicación de los iconos al capacitar a otros
* Obtener información detallada sobre el estado de juegos, máquinas virtuales, etc. cuando el sonido es insuficiente o no está disponible
* Descifrar lo que se muestra en un gráfico
* Descifrar capturas de pantalla o pantallas compartidas en Zoom o Microsoft Teams
* Asegurarse de que su cara esté claramente visible en la cámara y que su fondo sea profesional antes de grabar videos o participar en reuniones en línea

## Modelos

* [Pollinations](https://pollinations.ai/): El equipo detrás de Pollinations.AI patrocina generosamente el acceso gratuito a GPT4 para este proyecto, por lo que los usuarios no necesitan proporcionar su propia clave de API. Tenga en cuenta que se ha observado que el servicio tiene errores, y recomendamos encarecidamente usar sus propias claves para aprovechar al máximo los beneficios de este proyecto.
* [OpenAI GPT y modelos de razonamiento](https://platform.openai.com/docs/models): Requiere una clave de API de OpenAI. Incluye GPT-4 turbo, GPT-4o, la familia GPT-4.1 (4.1, 4.1 mini, 4.1 nano), la familia GPT-5 (5, 5 mini, 5 nano y 5 chat), la familia GPT-5.4 (5.4, 5.4 mini, 5.4 nano), la familia GPT-5.5 (5.5 y 5.5 pro), y los modelos de razonamiento O3, O3 pro, O3 mini y O4 mini.
* [Google Gemini](https://deepmind.google/models/gemini/), incluyendo los modelos 2.5 Flash, 2.5 Flash-Lite, 2.5 Pro, 3 Flash Preview, 3.1 Flash-Lite Preview y 3.1 Pro Preview.
* [Anthropic Claude](https://docs.anthropic.com/claude/docs/vision), incluyendo Claude 4 (Sonnet, Opus), 4.1 Opus, 4.5 (Haiku, Sonnet, Opus) y 4.6 (Sonnet, Opus).
* [Pixtral Large](https://mistral.ai/en/news/pixtral-large)
* [Grok 2](https://x.ai/news/grok-2), [Grok 4](https://x.ai/news/grok-4) y [Grok 4 Fast (razonamiento y sin razonamiento)](https://x.ai/news/grok-4-fast)
* vivo BlueLM Vision: un modelo multimodal de vivo, accesible a través de una cuenta gratuita de NVDA-CN. Consulte la sección de configuración a continuación.
* [Ollama (inestable)](https://ollama.com/)
* [llama.cpp (extremadamente inestable y lento dependiendo de su hardware, probado para funcionar con los modelos llava-v1.5/1.6, BakLLaVA, Obsidian y MobileVLM 1.7B/3B)](https://github.com/ggerganov/llama.cpp)
* [LiteLLM Proxy](https://docs.litellm.ai/docs/proxy/quick_start): Acceda a múltiples modelos de IA a través de un servidor proxy unificado. Requiere una URL de servidor proxy LiteLLM, opcionalmente una clave de API dependiendo de la configuración de su proxy. Aparece como "LiteLLM Proxy" en el diálogo de configuración de modelos. Compatible con selección dinámica de modelos y preguntas de seguimiento. Compatible con todos los formatos (PNG, JPEG, WEBP, GIF).
* [Seer](https://github.com/recursia-lab/Seer): Ejecuta PaliGemma2 localmente a través del demonio Seer. No requiere clave de API ni conexión a internet. Nota: este es un modelo solo de subtitulado. Los prompts y las preguntas de seguimiento no son compatibles.

Siga las instrucciones proporcionadas a continuación para que cada uno de estos funcione.

## Primeros pasos

Descargue la última versión del complemento desde [este enlace](https://github.com/cartertemm/AI-content-describer/releases/latest/). Haga clic en el archivo en un computador con NVDA instalado y proceda con la instalación según se indique.

A partir de la versión 2025.06.05, el uso de GPT4 es gratuito gracias a la generosidad de la comunidad detrás de PollinationsAI.

Si tiene los recursos y el interés de explorar modelos adicionales, siempre puede usar su propia clave de API y reducir las solicitudes a sus servidores. Si no es así, puede pasar directamente a la sección `uso` de este documento.

Siga las instrucciones a continuación para obtener una clave de API de un proveedor compatible.

### ¿Qué modelo debería usar?

Solíamos proporcionar recomendaciones sobre las opciones más económicas y de mayor calidad, pero el panorama está cambiando tan rápidamente que no es posible mantener esto actualizado.

La respuesta corta es que la mayoría de los modelos de última generación han llegado a un punto en que son precisos para la mayoría de los casos de uso cotidianos, así que elija el proveedor con el que esté familiarizado.

La mayoría de las personas quiere lograr un equilibrio entre precisión y costo. El [LLM arena leaderboard](https://lmarena.ai/leaderboard) (específicamente la categoría de visión) mide la precisión, mientras que la [calculadora de precios LLM](https://www.llm-prices.com/) describe los precios.

### Obtener una clave de API de Open-AI:

1. Vaya a la [página de claves de API de Open-AI](https://platform.openai.com/account/api-keys)
2. Si aún no tiene una cuenta, cree una. Si ya la tiene, inicie sesión.
3. En la página de claves de API, haga clic para crear una nueva clave secreta. Cópiela al portapapeles.
4. Financie la cuenta con al menos $1
5. En el diálogo de configuración de NVDA, desplácese hacia abajo hasta la categoría AI Content Describer, luego elija "administrar modelos (alt+m)", seleccione cualquiera de los modelos de OpenAI (por ejemplo, "GPT-4 omni") como proveedor, tabule al campo de clave de API y pegue la clave que acaba de generar.

En el momento de escribir esto, Open-AI emite créditos a las nuevas cuentas de desarrollador que se pueden usar durante tres meses, después de los cuales se pierden. Tras este período, tendrá que comprar créditos. El uso típico nunca debería superar los $5.00 por mes. Como referencia, la versión original de este complemento se desarrolló por un poco menos de un dólar. Siempre es posible iniciar sesión en su cuenta de OpenAI y hacer clic en "uso" para ver su cuota.

### Obtener una clave de API de Google

1. Primero necesitará crear un proyecto de Google workspace yendo a la [consola de Google Cloud](https://console.cloud.google.com/projectcreate). Asegúrese de haber iniciado sesión en su cuenta de Google.
2. Cree un nombre de entre cuatro y treinta caracteres, como "Gemini" o "complemento de NVDA"
3. Navegue a la [página de claves de API de Google AI Studio](https://makersuite.google.com/app/apikey)
4. Haga clic en "crear clave de API"
5. En el diálogo de configuración de NVDA, desplácese hacia abajo hasta la categoría AI Content Describer, luego elija "administrar modelos (alt+m)", seleccione "Google Gemini" como su proveedor, tabule al campo de clave de API y pegue la clave que acaba de generar.

### Obtener una clave de API de Anthropic

1. Inicie sesión en la [consola de Anthropic](https://console.anthropic.com/login).
2. Haga clic en su perfil -> Claves de API.
3. Haga clic en Crear clave.
4. Ingrese un nombre para la clave, como "AIContentDescriber", luego haga clic en "Crear clave" y copie el valor que aparece. Esto es lo que pegará en el campo de clave de API bajo la categoría Ai Content Describer del diálogo de configuración de NVDA -> administrar modelos -> cualquier modelo Claude 4.x (por ejemplo, "Claude 4.6 Sonnet").
5. Si aún no lo ha hecho, compre al menos $5 en créditos en la [página de planes de Anthropic](https://console.anthropic.com/settings/plans).

### Obtener una clave de API de Mistral

1. Inicie sesión o cree una cuenta de MistralAI yendo a la [página de inicio de sesión de MistralAI](https://auth.mistral.ai/ui/login).
2. Si está creando o iniciando sesión en una cuenta por primera vez, agregue un espacio de trabajo según se le indique, proporcionando un nombre y aceptando los términos y condiciones.
3. Una vez que haya iniciado sesión, seleccione "Claves de API" del menú.
4. Haga clic en "crear una nueva clave" y cópiela al portapapeles. Este valor es lo que pegará en el campo de clave de API bajo la categoría Ai Content Describer del diálogo de configuración de NVDA -> administrar modelos -> Pixtral Large.
5. Financie la cuenta, si corresponde.


### Activar el modelo VIVO BlueLM Vision a través de NVDA-CN

Este servicio se ofrece de forma gratuita a través de una asociación entre VIVO (vivo.com.cn) y la Comunidad China de NVDA (NVDACN). Proporciona reconocimiento multimodal de alta calidad y es el modelo recomendado para todos los usuarios, especialmente para quienes están comenzando.

Para usar este modelo, solo necesita una cuenta gratuita de NVDA-CN.

1.  Crear una cuenta: Vaya a la página de registro de NVDA-CN: [https://nvdacn.com/admin/register.php](https://nvdacn.com/admin/register.php).
    * **Nota**: La página está actualmente en chino. Recomendamos usar la función de traducción integrada de su navegador para completar el formulario.
    * Se le pedirá un nombre de usuario, contraseña y una dirección de correo electrónico válida. Asegúrese de guardar su contraseña de forma segura, ya que la recuperación automática de contraseñas aún no está implementada.
2.  Verificar su correo electrónico: Revise su bandeja de entrada para encontrar un correo de verificación y haga clic en el enlace para activar su cuenta.
3.  Configurar el complemento:
    * Abra el diálogo de configuración de NVDA y navegue a la categoría "AI Content Describer".
    * Seleccione el botón "Administrar modelos".
    * De la lista de proveedores, elija "vivo BlueLM Vision (NVDA-CN)".
    * Ingrese su nombre de usuario y contraseña de NVDA-CN en los campos correspondientes.
    * Haga clic en Aceptar para guardar sus credenciales.

Ahora está configurado para usar el modelo VIVO. Para cualquier problema relacionado con la cuenta, puede contactar al equipo de NVDA-CN en `support@nvdacn.com`.


### Configurar Ollama

Esta es actualmente la opción preferida para una configuración local.

Aunque la integración de Ollama ha sido probada más extensivamente que llama.cpp, sigue siendo menos estable que llamar a una API y se sabe que se comporta de manera extraña en algunas configuraciones, incluyendo posibles cierres inesperados en máquinas que no cumplen con las especificaciones requeridas.
Como mínimo, cuando pruebe esto por primera vez, guarde todos los documentos y cualquier cosa importante antes de continuar en caso de que esto le suceda.

Comience asegurándose de poder interactuar con su modelo preferido con capacidad de visión usando la interfaz de línea de comandos. Los pasos para hacerlo son los siguientes:

1. Descargue el archivo de configuración de Ollama para Windows desde la [página de descargas de Ollama](https://ollama.com/download).
2. Ejecute este archivo de configuración. Se encargará de obtener todas las dependencias que necesita su máquina.
3. Localice el modelo que desea usar. Se puede encontrar una lista en ollama.com -> modelos -> visión, o [directamente aquí](https://ollama.com/search?c=vision).
4. Descargue e inicie este modelo abriendo un símbolo del sistema y escribiendo `ollama run [nombre_del_modelo]`, reemplazando "[nombre_del_modelo]" con el que eligió en el paso 3. Por ejemplo, `ollama run llama3.2-vision`.
5. Suponiendo que el proceso se completó correctamente, se le colocará en una interfaz interactiva donde es posible escribir consultas y obtener respuestas del modelo, algo así como un ChatGPT localizado (y limitado). Pruébelo preguntando algo (cualquier cosa) para ver si funciona, luego escriba "/bye" para salir de esta interfaz.
6. En su ventana de consola, escriba `ollama list`. La primera columna proporcionará un nombre como "llama3.2-vision:latest".
7. Navegue a la configuración de AI Content Describer -> administrar modelos -> Ollama. En el campo de nombre del modelo, ingrese este valor y haga clic en Aceptar -> Aceptar. ¡Ya está listo! Cambie a Ollama en el submenú de modelos y debería funcionar después de un momento.

### Configurar llama.cpp

Este proveedor actualmente tiene algunos errores, y los resultados pueden variar. Realmente solo debería ser intentado por usuarios avanzados con interés en ejecutar modelos locales autoalojados, y el hardware para hacerlo.

1. Descargue llama.cpp. En el momento de escribir esto, este [pull request](https://github.com/ggerganov/llama.cpp/pull/5882) elimina las capacidades multimodales, por lo que querrá usar la [última versión con soporte para esto](https://github.com/ggerganov/llama.cpp/releases/tag/b2356).
Si está ejecutando en un adaptador de gráficos Nvidia con soporte CUDA, descargue estos binarios precompilados:
[llama-b2356-bin-win-cublas-cu12.2.0-x64.zip](https://github.com/ggerganov/llama.cpp/releases/download/b2356/llama-b2356-bin-win-cublas-cu12.2.0-x64.zip) y [cudart-llama-bin-win-cu12.2.0-x64.zip](https://github.com/ggerganov/llama.cpp/releases/download/b2356/cudart-llama-bin-win-cu12.2.0-x64.zip)
Los pasos para trabajar con un adaptador de gráficos diferente están fuera del alcance, pero se pueden encontrar en el readme de llama.cpp.
2. Extraiga ambos archivos en la misma carpeta.
3. Localice los formatos cuantizados de los modelos que desea usar desde Huggingface. Para LLaVA 1.6 Vicuna 7B: [llava-v1.6-vicuna-7b.Q4_K_M.gguf](https://huggingface.co/cjpais/llava-v1.6-vicuna-7b-gguf/blob/main/llava-v1.6-vicuna-7b.Q4_K_M.gguf) y [mmproj-model-f16.gguf](https://huggingface.co/cjpais/llava-v1.6-vicuna-7b-gguf/blob/main/mmproj-model-f16.gguf)
4. Coloque estos archivos en la carpeta con el resto de los binarios de llama.cpp.
5. Desde un símbolo del sistema, ejecute el binario del servidor llava.cpp, pasando los archivos .gguf para el modelo y el proyector multimodal (como se indica a continuación):
```
server.exe -m llava-v1.6-vicuna-7b.Q4_K_M.gguf --mmproj mmproj-model-f16.gguf
```
6. En el diálogo de configuración de NVDA, desplácese hacia abajo hasta la categoría AI Content Describer, luego elija "administrar modelos (alt+m)", seleccione "llama.cpp" como su proveedor, tabule al campo de URL base e ingrese el punto de conexión que se muestra en la consola (predeterminado a "http://localhost:8080").
7. Alternativamente, puede omitir algunos de estos pasos y ejecutar llama.cpp en un servidor remoto con mejores especificaciones que su máquina local, luego ingresar ese punto de conexión en su lugar.

### Configurar LiteLLM Proxy

LiteLLM Proxy proporciona una interfaz unificada para acceder a múltiples modelos de IA a través de un único punto de conexión, simplificando la gestión de modelos y permitiendo un cambio fácil entre proveedores.

1. Configure un servidor proxy LiteLLM siguiendo la [documentación del proxy de LiteLLM](https://docs.litellm.ai/docs/proxy/quick_start). Puede ejecutar el proxy localmente o usar un servidor remoto.
2. Si ejecuta localmente, la forma más rápida de comenzar es:
```
pip install 'litellm[proxy]'
litellm --model gpt-4o
```
Esto iniciará un servidor proxy en `http://localhost:4000` que reenvía solicitudes al GPT-4o de OpenAI.
3. Para uso en producción, cree un archivo `config.yaml` para configurar múltiples modelos y autenticación. Consulte la [guía de configuración de LiteLLM](https://docs.litellm.ai/docs/proxy/configs) para más detalles.
4. En el diálogo de configuración de NVDA, desplácese hacia abajo hasta la categoría AI Content Describer, luego elija "administrar modelos (alt+m)", seleccione "LiteLLM Proxy" como su proveedor.
5. Ingrese la URL de su servidor proxy en el campo de URL base (por ejemplo, "http://localhost:4000" para local o la URL de su servidor remoto).
6. Si su proxy requiere autenticación, ingrese la clave de API en el campo de clave de API. Si no, déjelo en blanco.
7. Haga clic en el botón "Listar modelos" para obtener los modelos disponibles de su proxy, luego seleccione el modelo que desea usar del menú desplegable.
8. Ajuste otras configuraciones como prompt, tokens máximos y tiempo de espera según sea necesario, luego haga clic en Aceptar.

Nota: Los modelos disponibles y sus capacidades dependen de la configuración de su proxy LiteLLM. Asegúrese de que su proxy esté configurado con modelos con capacidad de visión para la descripción de imágenes.

### Configurar Seer

Seer ejecuta PaliGemma2 en su propia máquina sin necesidad de clave de API ni conexión en la nube. Tenga en cuenta que este es un modelo solo de subtitulado; los prompts y las preguntas de seguimiento no son compatibles.

1. Instale el [demonio Seer](https://github.com/recursia-lab/Seer). Se proporciona un instalador de un solo comando para Windows (.bat) y Linux/macOS (.sh).
2. En el diálogo de configuración de NVDA, navegue a la categoría AI Content Describer, elija "administrar modelos (alt+m)" y seleccione "Seer (requiere instalación)".
3. La URL base predeterminada es `http://127.0.0.1:11435`. Déjela como está a menos que haya cambiado el puerto del demonio.
4. Haga clic en Aceptar. El demonio debe estar en ejecución antes de intentar una descripción.

## Uso

Cinco teclas de acceso rápido están vinculadas por defecto:

* NVDA+shift+i: Muestra un menú preguntando si describir el foco actual, el objeto del navegador, la cámara física o la pantalla completa con IA.
* NVDA+shift+u: Describe el contenido del objeto del navegador actual usando IA.
* NVDA+shift+y: Describe la imagen (o la ruta de archivo a una imagen) en el portapapeles usando IA.
* NVDA+shift+j: Describe la posición de su cara en el encuadre de la cámara seleccionada. Si tiene varias cámaras conectadas, navegue al menú de AI Content Describer (NVDA+shift+i) y elija la que desee usar con el elemento "seleccionar cámara" en el submenú de detección facial.
* NVDA+alt+c: Abrir el diálogo de conversación con IA para hacer preguntas de seguimiento.

Tres gestos no están vinculados:

* Describe el contenido del elemento enfocado actualmente usando IA.
* Toma una captura de pantalla y luego la describe usando IA.
* Toma una foto con la cámara seleccionada y luego la describe usando IA.

No dude en personalizar estos en cualquier momento desde el diálogo de gestos de entrada.

### Seguimiento de una descripción

A veces, la respuesta que obtiene de una IA es insuficiente. Quizás la imagen es de baja calidad, incompleta o incluye detalles no deseados. Tal vez quiera centrarse en solo una sección determinada o tomar una foto más clara sin perder el contexto.
Después de recibir una descripción, puede presionar NVDA+alt+c, o seleccionar "Seguimiento de la descripción anterior" del menú contextual de AI Content Describer (NVDA+shift+i). Por defecto, el foco se establece en el campo de mensaje.
Para agregar una imagen adicional, simplemente mantenga abierta la ventana de conversación y use el complemento como lo haría normalmente. Cuando se tome una foto (ya sea de la cámara, control del sistema, captura de pantalla, etc.) se le preguntará si desea adjuntarla a la sesión actual o iniciar una nueva.

## Compilar el complemento

Para crear el paquete del complemento desde el código fuente, necesitará:

* Una distribución de Python (se recomienda 3.7 o posterior). Consulte el [sitio web de Python](https://www.python.org) para los instaladores de Windows. Tenga en cuenta que actualmente, preparar el código fuente de NVDA y los módulos de terceros incluidos requiere la versión de 32 bits de Python 3.7.
* Scons - [Sitio web](https://www.scons.org/) - versión 4.3.0 o posterior. Puede instalarlo a través de PIP. `pip install scons`
* Markdown 3.3.0 o posterior. `pip install markdown`

Luego abra su terminal preferida:

```
git clone https://github.com/cartertemm/AI-content-describer.git
cd AI-content-describer
scons
```

Después de que el comando `scons` termine de ejecutarse, se colocará un archivo *.nvda-addon en la raíz de este repositorio listo para pruebas y lanzamiento.

Si agrega cadenas adicionales que necesiten ser traducidas, es importante reconstruir el archivo .pot de la siguiente manera:

```
scons pot
```

## ¿Cómo traducir?

En una máquina Windows:

* Descargue [poedit](https://poedit.net/). Este es el software que usará para traducir cada mensaje del inglés.
* Descargue el archivo .pot con todas las cadenas [aquí](https://raw.githubusercontent.com/cartertemm/AI-content-describer/main/AIContentDescriber.pot)
* Abra el archivo que acaba de descargar en el programa poedit. Haga clic en "Crear nueva traducción" en la ventana que aparece, luego seleccione el idioma de destino.
* Revise y convierta el contenido del texto fuente al idioma de destino, luego péguelo en el campo de traducción. Para obtener ayuda adicional, no dude en hacer clic derecho en el elemento de la lista -> ocurrencias de código, luego suba una línea para leer el comentario que comienza con "# Translators: ". Estos comentarios también están disponibles en un solo lugar en el archivo .pot.
* Cuando termine, haga clic en archivo -> guardar o presione ctrl+s, luego elija una ubicación para que se almacenen los nuevos archivos .mo y .po. Estos son los archivos que deben enviarse por correo electrónico o adjuntarse en un pull request.
* Traduzca el contenido de readme.md (este archivo). ¡Adjúntelo también!

## Contribuciones

Todas son muy apreciadas y serán reconocidas.
Las siguientes personas han trabajado en el complemento.

* [Cary Rowen](https://github.com/cary-rowen): hizo que el complemento funcione para usuarios chinos a través de mirroring de dependencias, añadió soporte para el proveedor Vivo Blue
* [Mazen](https://github.com/mzanm): implementación de Markdown, otras contribuciones de código
* [Kostenkov-2021](https://github.com/Kostenkov-2021): traducción al ruso
* [Nidza07](https://github.com/nidza07): traducción al serbio
* [Heorhii Halas](nvda.translation.uk@gmail.com) y [George-br](https://github.com/George-br): traducción al ucraniano
* [Umut Korkmaz](umutkork@gmail.com): traducción al turco
* [Platinum_Hikari](urbain_onces.0r@icloud.com): traducción al francés
* [Lukas](https://4sensegaming.cz): traducción al checo
* [Michaela](https://technologiebezzraku.sk): traducción al eslovaco

¿Tiene un problema? Envíelo al [rastreador de problemas](https://github.com/cartertemm/AI-content-describer/issues)

¿Tiene una sugerencia para una nueva función? Cree un ticket para eso también, y podemos hablar sobre su implementación. Los pull requests sin problemas asociados serán revisados, pero es probable que requieran más tiempo para todos, especialmente si decido que la nueva corrección o funcionalidad necesita funcionar de manera diferente a lo propuesto.

Las traducciones son muy bienvenidas. Cuantas más personas puedan acceder a esta poderosa tecnología, mejor.

Si no tiene Github, o prefiere no usarlo, puede [enviarme un correo electrónico](mailto:cartertemm@gmail.com) - cartertemm (arroba) gmail (punto) com.

¡Gracias por el apoyo!
