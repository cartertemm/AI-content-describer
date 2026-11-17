# Descripteur de contenu IA pour NVDA

Cet add-on permet d'obtenir des descriptions détaillées pour les images, les contrôles de l'interface utilisateur et autres contenus visuellement inaccessibles.

En tirant parti des capacités multimodales des modèles IA avancés et des algorithmes de vision par ordinateur, nous visons à fournir des descriptions de contenu de première classe et à augmenter l'indépendance globale. Pour plus d'informations sur les modèles sous-jacents, référez-vous à la section correspondante de ce document.

## Fonctionnalités

* Décrire l'objet de focus, l'objet navigateur, l'écran entier, ou prendre une photo avec la caméra embarquée
* Décrire toute image qui a été copiée dans le presse-papiers, que ce soit une image d'un courriel ou un chemin dans l'explorateur Windows
* Copier une image de l'objet de focus, de l'objet navigateur ou de l'écran entier dans le presse-papiers, pour la coller dans d'autres applications
* Indiquer si le visage de l'utilisateur est positionné au centre du cadre en utilisant des algorithmes de vision par ordinateur (ne nécessite pas l'accès à une API payante)
* Utiliser les modèles pris en charge pour contrôler l'application active avec des actions de souris et de clavier, pour des tâches qui pourraient être inaccessibles
* Gratuit par défaut, avec la possibilité d'ajouter votre propre clé API pour accéder à plus de modèles
* Prend en charge plusieurs fournisseurs (GPT d'OpenAI et l'offre gratuite de Pollinations, Gemini de Google, Mistral Large 4, Claude d'Anthropic, Grok de xAI, Kimi de Moonshot AI, vivo BlueLM Vision via NVDA-CN, Datalab Chandra 2, Ollama, llama.cpp, LiteLLM Proxy et Seer)
* Prend en charge une grande variété de formats incluant PNG (.png), JPEG (.jpeg et .jpg), WEBP (.webp), et GIF non animés (.gif)
* Cache optionnellement les réponses pour préserver le quota d'API
* Pour une utilisation avancée, personnaliser l'invite et le nombre de tokens pour adapter l'information à vos besoins
* Poser des questions de suivi et joindre des images supplémentaires
* Rendu Markdown pour accéder facilement aux informations structurées (il suffit d'activer le paramètre "ouvrir les résultats dans une boîte de dialogue navigable" et d'intégrer par exemple "répondre en Markdown" à la fin de vos invites)

## Cas d'utilisation

Il y avait quelques motivations principales derrière ce projet.

NVDA est capable de réaliser la reconnaissance optique de caractères (OCR) directement, ce qui représente une avancée significative. Si vous essayez d'extraire du texte d'une image ou d'un document PDF, c'est ce que vous recherchez.

Cependant, l'OCR ne peut analyser que les données qui *pourraient* être du texte. Il est moins performant pour considérer le contexte, les objets et les relations véhiculés dans ces images. Et Internet en est plein. Logos, portraits, mèmes, icônes, graphiques, diagrammes, graphiques à barres/lignes... Ils sont partout et généralement pas dans un format que les utilisateurs de lecteurs d'écran peuvent interpréter.
Jusqu'à récemment, il y avait une dépendance constante envers les auteurs de contenu fournissant des descriptions de texte alternatives. Bien que cela soit toujours indispensable, il est difficile de changer le fait qu'un haut standard de qualité est l'exception, et non la règle.

Maintenant, les possibilités sont presque infinies. Vous pourriez :

* Visualiser le bureau ou une fenêtre spécifique pour comprendre le placement des icônes lors de la formation d'autres personnes
* Obtenir des informations détaillées sur l'état des jeux, des machines virtuelles, etc. lorsque le son est insuffisant ou indisponible
* Comprendre ce qui est affiché dans un graphique
* Démystifier les captures d'écran ou les partages d'écran dans Zoom ou Microsoft Teams
* Demander à un modèle pris en charge de vous aider à utiliser une application inaccessible ou à accomplir une tâche dans la fenêtre au premier plan
* Assurer que votre visage regarde clairement la caméra et que votre arrière-plan est professionnel avant d'enregistrer des vidéos ou de participer à des réunions en ligne

## Modèles

* [Pollinations](https://pollinations.ai/) : l'équipe derrière Pollinations.AI parraine généreusement un accès gratuit à GPT4 pour ce projet, de sorte que les utilisateurs n'ont pas besoin de fournir leur propre clé API. Notez que le service s'est révélé instable, et nous recommandons vivement d'utiliser vos propres clés pour profiter pleinement de ce projet.
* [Modèles GPT d'OpenAI](https://platform.openai.com/docs/models) : nécessite une clé API OpenAI. Comprend la famille GPT-5.4 (5.4 et 5.4 mini), la famille GPT-5.5 (5.5 et 5.5 pro), la famille GPT-6 (6 Astra et 6 Luna) et la famille GPT-6.1 (6.1 Sol et 6.1 Terra). Le contrôle de l'ordinateur est pris en charge par les familles GPT-5.4, GPT-5.5, GPT-6 et GPT-6.1.
* [Google Gemini](https://deepmind.google/models/gemini/), y compris les modèles 2.5 Flash, 2.5 Flash-Lite, 2.5 Pro, 3.1 Flash-Lite, 3.1 Pro Preview, 3.5 Flash, 3.5 Flash-Lite, 3.6 Flash, 3.7 Flash, 3.8 Flash, 4 Hydrogen, 4 Argon et 4 Carbon.
* [Anthropic Claude](https://docs.anthropic.com/claude/docs/vision), y compris Claude 4.5 (Sonnet, Opus), 4.6 (Sonnet, Opus), 4.7 Opus, 4.8 Opus, 5 (Sonnet, Opus, Fable), 5.1 Fable, 5.2 Fable et 5.5 (Haiku, Sonnet, Opus). Tous prennent en charge le contrôle de l'ordinateur.
* [Mistral Large 4](https://docs.mistral.ai/models/mistral-large-4-0)
* [xAI Grok](https://docs.x.ai/developers/models), y compris Grok 4.20 (sans raisonnement), 4.3, 4.5, 4.6 et 4.7.
* [Kimi](https://platform.kimi.ai/docs/guide/use-kimi-vision-model), les modèles multimodaux de Moonshot AI, y compris Kimi K3 et Kimi K2.6.
* vivo BlueLM Vision : un modèle multimodal de vivo, accessible via un compte NVDA-CN gratuit. Voir la section de configuration ci-dessous.
* [Datalab Chandra 2](https://github.com/datalab-to/chandra) : modèle de vision et d'OCR de pointe de Datalab, spécialisé dans les mises en page complexes de documents, les tableaux, les formulaires, l'écriture manuscrite, les graphiques et les mathématiques. Prend en charge l'API cloud gérée de Datalab (sur [datalab.to](https://www.datalab.to)) ou les déploiements auto-hébergés via vLLM (avec `chandra_vllm` ou des points de terminaison `/v1` compatibles OpenAI).
* [Ollama (instable)](https://ollama.com/)
* [llama.cpp (extrêmement instable et lent selon votre matériel, testé pour fonctionner avec les modèles llava-v1.5/1.6, BakLLaVA, Obsidian, et MobileVLM 1.7B/3B)](https://github.com/ggerganov/llama.cpp)
* [LiteLLM Proxy](https://docs.litellm.ai/docs/proxy/quick_start) : accédez à plusieurs modèles IA via un serveur proxy unifié. Nécessite l'URL d'un serveur proxy LiteLLM, et éventuellement une clé API selon la configuration de votre proxy. Apparaît sous le nom "LiteLLM Proxy" dans la boîte de dialogue de configuration des modèles. Prend en charge la sélection dynamique du modèle et les questions de suivi. Compatible avec tous les formats (PNG, JPEG, WEBP, GIF).
* [Seer](https://github.com/recursia-lab/Seer) : exécute PaliGemma2 localement via le démon Seer. Aucune clé API ni connexion Internet n'est nécessaire. Remarque : il s'agit d'un modèle de légendage uniquement. Les invites et les questions de suivi ne sont pas prises en charge.

Suivez les instructions fournies ci-dessous pour faire fonctionner chacun de ces modèles.

## Pour commencer

Téléchargez la dernière version de l'add-on depuis [ce lien](https://github.com/cartertemm/AI-content-describer/releases/latest/). Cliquez sur le fichier sur un ordinateur avec NVDA installé, puis poursuivez l'installation comme indiqué.

Au premier démarrage de NVDA avec l'add-on, celui-ci propose de télécharger quelques bibliothèques supplémentaires. Consultez la section `Dépendances` de ce document pour plus de détails.

Depuis la version 2025.06.05, l'utilisation de GPT4 est gratuite grâce à la générosité de la communauté derrière PollinationsAI.

Si vous avez les ressources et l'envie d'explorer d'autres modèles, vous pouvez toujours utiliser votre propre clé API et réduire les requêtes vers leurs serveurs. Sinon, n'hésitez pas à passer directement à la section `Utilisation` de ce document.

Suivez les instructions ci-dessous pour obtenir une clé API d'un fournisseur pris en charge.

### Quel modèle utiliser ?

Nous fournissions auparavant des recommandations sur les options les moins chères et de la meilleure qualité, mais le paysage évolue si rapidement qu'il n'est plus possible de les tenir à jour.

En bref, la plupart des modèles de pointe sont désormais suffisamment précis pour la majorité des usages quotidiens, alors choisissez le fournisseur que vous connaissez.

La plupart des gens cherchent un équilibre entre précision et coût. Le [classement LLM arena](https://lmarena.ai/leaderboard) (en particulier la catégorie vision) mesure l'exactitude, tandis que le [calculateur de prix LLM](https://www.llm-prices.com/) présente les tarifs.

Si vous souhaitez utiliser le contrôle de l'ordinateur, choisissez l'un des modèles OpenAI ou Anthropic pris en charge listés ci-dessus. L'accès gratuit à Pollinations est utile pour les descriptions d'images, mais il ne prend pas en charge le contrôle de l'ordinateur.

### Obtenir une clé API d'OpenAI :

1. Allez sur la [page des clés API d'OpenAI](https://platform.openai.com/account/api-keys)
2. Si vous n'avez pas encore de compte, créez-en un. Si vous en avez un, connectez-vous.
3. Sur la page des clés API, cliquez pour créer une nouvelle clé secrète. Copiez-la dans votre presse-papiers.
4. Approvisionnez le compte avec au moins 1 $
5. Dans le dialogue de configuration de NVDA, faites défiler jusqu'à la catégorie Descripteur de Contenu IA, puis choisissez "gérer les modèles (alt+m)", sélectionnez l'un des modèles OpenAI (par exemple "GPT-6.1 Sol") comme fournisseur, tabez dans le champ de la clé API, et collez la clé que vous venez de générer ici.

À l'heure où nous écrivons ces lignes, OpenAI accorde aux nouveaux comptes développeur des crédits utilisables pendant trois mois, après quoi ils sont perdus. Passé ce délai, vous devrez acheter des crédits. Une utilisation typique ne devrait jamais dépasser 5,00 $ par mois. À titre de référence, la version originale de cet add-on a été développée pour un peu moins d'un dollar. Vous pouvez toujours vous connecter à votre compte OpenAI et cliquer sur "usage" pour consulter votre quota.

### Obtenir une clé API de Google

1. Vous aurez d'abord besoin de créer un projet Google workspace en allant sur la [console Google Cloud](https://console.cloud.google.com/projectcreate). Assurez-vous d'être connecté à votre compte Google.
2. Créez un nom entre quatre et trente caractères, comme "Gemini" ou "add-on NVDA"
3. Naviguez vers la [page des clés API de Google AI Studio](https://makersuite.google.com/app/apikey)
4. Cliquez sur "créer une clé API"
5. Dans le dialogue de configuration de NVDA, faites défiler jusqu'à la catégorie Descripteur de Contenu IA, puis choisissez "gérer les modèles (alt+m)", sélectionnez "Google Gemini" comme votre fournisseur, tabez dans le champ de la clé API, et collez la clé que vous venez de générer ici.

### Obtenir une clé API d'Anthropic

1. Connectez-vous à la [console Anthropic](https://console.anthropic.com/login).
2. Cliquez sur votre profil -> Clés API.
3. Cliquez sur Créer une clé.
4. Entrez un nom pour la clé, comme "AIContentDescriber", puis cliquez sur "Créer une clé" et copiez la valeur qui apparaît. C'est ce que vous collerez dans le champ de la clé API sous la catégorie Descripteur de Contenu IA du dialogue de configuration de NVDA -> gérer les modèles -> n'importe quel modèle Claude (par exemple "Claude 5 Sonnet").
5. Si vous ne l'avez pas déjà fait, achetez au moins 5 $ en crédits sur la [page des plans d'Anthropic](https://console.anthropic.com/settings/plans).

### Obtenir une clé API de Mistral

1. Connectez-vous ou créez un compte MistralAI en allant sur la [page de connexion MistralAI](https://auth.mistral.ai/ui/login).
2. Si vous créez un compte ou vous connectez pour la première fois, ajoutez un espace de travail comme demandé, en indiquant un nom et en acceptant les conditions générales.
3. Une fois connecté, sélectionnez "API keys" dans le menu.
4. Cliquez sur "create a new key" et copiez la clé dans votre presse-papiers. C'est cette valeur que vous collerez dans le champ de la clé API sous la catégorie Descripteur de Contenu IA du dialogue de configuration de NVDA -> gérer les modèles -> Mistral Large 4.
5. Approvisionnez le compte, le cas échéant.

### Obtenir une clé API de Kimi (Moonshot AI)

1. Connectez-vous ou créez un compte sur la [plateforme développeur Kimi](https://platform.kimi.ai/).
2. Une fois connecté, ouvrez la section des clés API de la console et créez une nouvelle clé.
3. Copiez la clé dans votre presse-papiers. C'est cette valeur que vous collerez dans le champ de la clé API sous la catégorie Descripteur de Contenu IA du dialogue de configuration de NVDA -> gérer les modèles -> Kimi K3 (ou un autre modèle Kimi).
4. Approvisionnez le compte, le cas échéant.


### Activer le modèle VIVO BlueLM Vision via NVDA-CN

Ce service est proposé gratuitement grâce à un partenariat entre VIVO (vivo.com.cn) et la communauté chinoise de NVDA (NVDACN). Il offre une reconnaissance multimodale de haute qualité et constitue le modèle recommandé pour tous les utilisateurs, en particulier ceux qui débutent.

Pour utiliser ce modèle, il vous suffit d'un compte NVDA-CN gratuit.

1.  Créer un compte : allez sur la page d'inscription de NVDA-CN : [https://nvdacn.com/admin/register.php](https://nvdacn.com/admin/register.php).
    * **Remarque** : la page est actuellement en chinois. Nous vous recommandons d'utiliser la fonction de traduction intégrée de votre navigateur pour remplir le formulaire.
    * Il vous sera demandé un nom d'utilisateur, un mot de passe et une adresse e-mail valide. Conservez votre mot de passe en lieu sûr, car la récupération automatique du mot de passe n'est pas encore disponible.
2.  Vérifier votre adresse e-mail : consultez votre boîte de réception pour trouver l'e-mail de vérification et cliquez sur le lien qu'il contient pour activer votre compte.
3.  Configurer l'add-on :
    * Ouvrez le dialogue de configuration de NVDA et allez dans la catégorie "Descripteur de Contenu IA".
    * Sélectionnez le bouton "Gérer les modèles".
    * Dans la liste des fournisseurs, choisissez "vivo BlueLM Vision (NVDA-CN)".
    * Saisissez votre nom d'utilisateur et votre mot de passe NVDA-CN dans les champs correspondants.
    * Cliquez sur OK pour enregistrer vos identifiants.

Vous pouvez maintenant utiliser le modèle VIVO. Pour tout problème lié à votre compte, vous pouvez contacter l'équipe NVDA-CN à l'adresse `support@nvdacn.com`.


### Configurer Ollama

C'est actuellement l'option privilégiée pour une installation locale.

Bien que l'intégration d'Ollama ait été testée plus en profondeur que llama.cpp, elle reste moins stable qu'un appel à une API et peut se comporter de façon étrange dans certaines configurations, jusqu'à provoquer des plantages sur les machines qui n'ont pas la configuration requise.
Au strict minimum, lors d'un premier essai, enregistrez tous vos documents et tout ce qui est important avant de continuer, au cas où cela vous arriverait.

Commencez par vérifier que vous pouvez interagir avec le modèle de vision de votre choix depuis l'interface en ligne de commande. Voici les étapes à suivre :

1. Téléchargez le programme d'installation d'Ollama pour Windows depuis la page [téléchargements d'Ollama](https://ollama.com/download).
2. Exécutez ce programme d'installation. Il se charge de récupérer toutes les dépendances dont votre machine aura besoin.
3. Trouvez le modèle que vous souhaitez utiliser. Une liste est disponible sur ollama.com -> models -> vision, ou [directement ici](https://ollama.com/search?c=vision).
4. Téléchargez et lancez ce modèle en ouvrant une invite de commande et en tapant `ollama run [model_name]`, en remplaçant bien sûr "[model_name]" par celui choisi à l'étape 3. Par exemple, `ollama run llama3.2-vision`.
5. Si tout s'est bien passé, vous arriverez dans un shell interactif où vous pouvez taper des requêtes et obtenir des réponses du modèle, un peu comme un ChatGPT local (et limité). Testez-le en posant une question (n'importe laquelle) pour vérifier qu'il fonctionne, puis tapez "/bye" pour quitter cette interface.
6. De retour dans votre fenêtre de console, tapez `ollama list`. La première colonne indique un nom comme "llama3.2-vision:latest".
7. Allez dans les paramètres du Descripteur de Contenu IA -> gérer les modèles -> Ollama. Dans le champ du nom du modèle, saisissez cette valeur et cliquez sur OK -> OK. C'est prêt ! Passez à Ollama dans le sous-menu des modèles, et cela devrait fonctionner après un certain temps.

### Configurer llama.cpp

Ce fournisseur est actuellement quelque peu bogué, et votre expérience peut varier. Il devrait vraiment seulement être tenté par des utilisateurs avancés intéressés par l'exécution de modèles auto-hébergés locaux, et ayant le matériel nécessaire pour cela.

1. Téléchargez llama.cpp. À l'heure actuelle, cette [demande de tirage](https://github.com/ggerganov/llama.cpp/pull/5882) supprime les capacités multimodales donc vous voudrez utiliser la [dernière version avec support pour cela](https://github.com/ggerganov/llama.cpp/releases/tag/b2356).
Si vous utilisez un adaptateur graphique Nvidia avec support CUDA, téléchargez ces binaires préconstruits :
[llama-b2356-bin-win-cublas-cu12.2.0-x64.zip](https://github.com/ggerganov/llama.cpp/releases/download/b2356/llama-b2356-bin-win-cublas-cu12.2.0-x64.zip) et [cudart-llama-bin-win-cu12.2.0-x64.zip](https://github.com/ggerganov/llama.cpp/releases/download/b2356/cudart-llama-bin-win-cu12.2.0-x64.zip)
Les étapes pour travailler avec un autre adaptateur graphique sont hors de portée, mais peuvent être trouvées dans le readme de llama.cpp.
2. Extrayez ces deux fichiers dans le même dossier.
3. Localisez les formats quantifiés des modèles que vous souhaitez utiliser de Huggingface. Pour LLaVA 1.6 Vicuna 7B : [llava-v1.6-vicuna-7b.Q4_K_M.gguf](https://huggingface.co/cjpais/llava-v1.6-vicuna-7b-gguf/blob/main/llava-v1.6-vicuna-7b.Q4_K_M.gguf) et [mmproj-model-f16.gguf](https://huggingface.co/cjpais/llava-v1.6-vicuna-7b-gguf/blob/main/mmproj-model-f16.gguf)
4. Mettez ces fichiers dans le dossier avec le reste des binaires de llama.cpp.
5. Depuis une invite de commande, exécutez le binaire du serveur llava.cpp, en passant les fichiers .gguf pour le modèle et le projecteur multimodal (comme suit) :
```
server.exe -m llava-v1.6-vicuna-7b.Q4_K_M.gguf --mmproj mmproj-model-f16.gguf
```
6. Dans le dialogue de configuration de NVDA, faites défiler jusqu'à la catégorie Descripteur de Contenu IA, puis choisissez "gérer les modèles (alt+m)", sélectionnez "llama.cpp" comme votre fournisseur, tabez dans le champ de l'URL de base, et entrez le point de terminaison montré dans la console (par défaut "http://localhost:8080").
7. Alternativement, vous pouvez omettre certaines de ces étapes et exécuter llama.cpp sur un serveur distant avec des spécifications supérieures à celles de votre machine locale, puis entrer ce point de terminaison à la place.

### Configurer LiteLLM Proxy

LiteLLM Proxy fournit une interface unifiée pour accéder à plusieurs modèles IA via un seul point de terminaison, ce qui simplifie la gestion des modèles et permet de passer facilement d'un fournisseur à l'autre.

1. Mettez en place un serveur proxy LiteLLM en suivant la [documentation du proxy LiteLLM](https://docs.litellm.ai/docs/proxy/quick_start). Vous pouvez exécuter le proxy localement ou utiliser un serveur distant.
2. En local, le moyen le plus rapide de commencer est :
```
pip install 'litellm[proxy]'
litellm --model gpt-4o
```
Cela démarre un serveur proxy à l'adresse `http://localhost:4000` qui transmet les requêtes à GPT-4o d'OpenAI.
3. Pour un usage en production, créez un fichier `config.yaml` pour configurer plusieurs modèles et l'authentification. Consultez le [guide de configuration de LiteLLM](https://docs.litellm.ai/docs/proxy/configs) pour plus de détails.
4. Dans le dialogue de configuration de NVDA, faites défiler jusqu'à la catégorie Descripteur de Contenu IA, puis choisissez "gérer les modèles (alt+m)" et sélectionnez "LiteLLM Proxy" comme fournisseur.
5. Saisissez l'URL de votre serveur proxy dans le champ de l'URL de base (par exemple "http://localhost:4000" en local, ou l'URL de votre serveur distant).
6. Si votre proxy exige une authentification, saisissez la clé API dans le champ de la clé API. Sinon, laissez-le vide.
7. Cliquez sur le bouton "Lister les modèles" pour récupérer les modèles disponibles sur votre proxy, puis sélectionnez le modèle à utiliser dans la liste déroulante.
8. Ajustez les autres paramètres, comme l'invite, le nombre maximal de tokens et le délai d'attente, selon vos besoins, puis cliquez sur OK.

Remarque : les modèles disponibles et leurs capacités dépendent de la configuration de votre proxy LiteLLM. Assurez-vous que votre proxy est configuré avec des modèles capables de traiter des images pour la description d'images.

### Configurer Seer

Seer exécute PaliGemma2 sur votre propre machine, sans clé API ni connexion au cloud. Notez qu'il s'agit d'un modèle de légendage uniquement ; les invites et les questions de suivi ne sont pas prises en charge.

1. Installez le [démon Seer](https://github.com/recursia-lab/Seer). Un programme d'installation en une seule commande est fourni pour Windows (.bat) et Linux/macOS (.sh).
2. Dans le dialogue de configuration de NVDA, allez dans la catégorie Descripteur de Contenu IA, choisissez "gérer les modèles (alt+m)" et sélectionnez "Seer (requires installation)".
3. L'URL de base est par défaut `http://127.0.0.1:11435`. Laissez-la telle quelle, sauf si vous avez modifié le port du démon.
4. Cliquez sur OK. Le démon doit être en cours d'exécution avant que vous ne demandiez une description.

### Configurer Datalab Chandra 2

Datalab Chandra 2 est un modèle de pointe d'analyse de documents et d'OCR, spécialisé dans les mises en page complexes, les tableaux, les formulaires, l'écriture manuscrite, les graphiques et les formules mathématiques. Il peut être utilisé via l'API cloud gérée de Datalab, un conteneur sur site ou une instance vLLM auto-hébergée.

#### Option A : utiliser l'API cloud de Datalab (recommandé)
1. Créez un compte sur [datalab.to](https://www.datalab.to). Les nouveaux comptes reçoivent des crédits d'essai gratuits.
2. Rendez-vous sur la [page des clés API](https://www.datalab.to/app/keys) et générez une clé API.
3. Dans le dialogue de configuration de NVDA, allez dans la catégorie Descripteur de Contenu IA, choisissez "gérer les modèles (alt+m)" et sélectionnez "Datalab Chandra 2".
4. Saisissez votre clé API dans le champ "Clé API".
5. L'URL de base est configurée par défaut sur `https://www.datalab.to/api/v1/convert`. Vous pouvez ajuster le mode de traitement (`fast`, `balanced` ou `accurate`) selon vos besoins.
6. Cliquez sur OK. Le modèle est maintenant disponible dans le menu du Descripteur de Contenu IA.

#### Option B : auto-hébergement avec vLLM
1. Démarrez votre serveur vLLM local avec Chandra 2 (par exemple avec `chandra_vllm` ou `vllm serve datalab-to/chandra-ocr-2`). Par défaut, le serveur s'exécute sur `http://localhost:8000/v1`.
2. Dans les paramètres de NVDA -> Descripteur de Contenu IA -> Gérer les modèles -> "Datalab Chandra 2", saisissez votre point de terminaison local dans le champ "URL de base" (par exemple `http://localhost:8000/v1`).
3. Indiquez le nom du modèle s'il diffère de celui par défaut (`datalab-to/chandra-ocr-2`), laissez la clé API vide (ou fournissez un jeton bearer si l'authentification est activée), puis cliquez sur OK.

## Utilisation

Six raccourcis clavier sont liés par défaut :

* NVDA+shift+i : Ouvre un menu demandant de décrire l'objet de focus actuel, l'objet navigateur, la caméra physique ou l'écran entier, ou de contrôler l'ordinateur avec l'IA.
* NVDA+shift+u : Décrit le contenu de l'objet navigateur actuel en utilisant l'IA.
* NVDA+shift+y : Décrit l'image (ou le chemin de fichier vers une image) dans le presse-papiers en utilisant l'IA.
* NVDA+shift+j : Décrit la position de votre visage dans le cadre de la caméra sélectionnée. Si vous avez plusieurs caméras connectées, naviguez jusqu'au menu Descripteur de Contenu IA (NVDA+shift+i) et choisissez celle que vous souhaitez utiliser avec l'option "sélectionner la caméra" dans le sous-menu de détection de visage.
* NVDA+alt+c : Ouvre la boîte de dialogue de conversation IA pour poser des questions de suivi.
* NVDA+control+shift+p : Met en pause ou reprend une session de contrôle de l'ordinateur en cours.

Sept gestes sont non liés :

* Décrire le contenu de l'élément actuellement focalisé en utilisant l'IA.
* Prendre une capture d'écran, puis la décrire en utilisant l'IA.
* Prendre une photo en utilisant la caméra sélectionnée, puis la décrire en utilisant l'IA.
* Annuler la session de contrôle de l'ordinateur en cours.
* Prendre une capture d'écran de l'objet de focus actuel et la copier dans le presse-papiers.
* Prendre une capture d'écran de l'objet navigateur actuel et la copier dans le presse-papiers.
* Prendre une capture de l'écran entier et la copier dans le presse-papiers.

Les trois commandes de copie se trouvent aussi dans le sous-menu "Copier l'image dans le presse-papiers" du menu NVDA+shift+i. Elles n'envoient rien à un service d'IA. Utilisez-les pour coller une capture dans Be My AI ou dans une autre application que cet add-on ne prend pas en charge. La copie remplace le contenu précédent du presse-papiers.

N'hésitez pas à personnaliser ces éléments à tout moment depuis le dialogue des gestes d'entrée.

### Poser une question de suivi sur une description

Parfois, la réponse de l'IA est insuffisante. L'image est peut-être de mauvaise qualité, incomplète ou contient des détails indésirables. Vous voulez peut-être vous concentrer sur une partie précise ou prendre une photo plus nette sans perdre le contexte.
Après avoir reçu une description, vous pouvez appuyer sur NVDA+alt+c, ou sélectionner "Poser une question de suivi sur la description précédente" dans le menu contextuel du Descripteur de Contenu IA (NVDA+shift+i). Par défaut, le focus est placé sur le champ du message.
Pour ajouter une image supplémentaire, gardez simplement la fenêtre de conversation ouverte et utilisez l'add-on comme d'habitude. Lorsqu'une image est prise (depuis la caméra, un contrôle du système, une capture d'écran, etc.), il vous sera demandé si vous souhaitez la joindre à la session en cours ou en démarrer une nouvelle.

### Contrôle de l'ordinateur

Le contrôle de l'ordinateur permet au Descripteur de Contenu IA de piloter l'application active avec la souris et le clavier une fois que vous avez décrit une tâche. Cela peut aider pour des tâches difficiles ou inaccessibles à réaliser manuellement.

Comme cette fonction donne à un modèle d'IA le contrôle de votre ordinateur, utilisez-la avec prudence. L'add-on demande votre consentement avant de commencer, annonce les actions au fur et à mesure et vous demande confirmation avant les actions potentiellement risquées. Vous êtes responsable de ce qu'il fait : surveillez donc la session et évitez de l'utiliser pour des travaux sensibles ou difficiles à annuler.

Vous pouvez mettre en pause ou reprendre le contrôle de l'ordinateur à tout moment avec `NVDA+Control+Shift+P`. Pendant la pause, l'add-on ne passe pas à l'action suivante tant que vous n'avez pas repris.

L'add-on utilise des bips pour indiquer l'état du contrôle. Un bip aigu signifie que le modèle prend ou reprend le contrôle. Un bip grave signifie que le contrôle est en pause, soit parce que vous l'avez mis en pause, soit parce que le modèle a besoin d'une information de votre part. Un court bip d'erreur grave signifie que la session s'est arrêtée à cause d'une erreur d'API.

Pendant une session de contrôle, le modèle annonce ce qu'il s'apprête à faire avant d'envoyer une saisie. Rien ne se passe avant la fin de cette annonce, sauf si vous appuyez sur `Control` pour l'interrompre et laisser l'action se faire plus tôt.

Si le modèle ne sait pas comment effectuer une action, a besoin de plus d'informations ou vous rend la main pour une autre raison, la session se met en pause et la boîte de dialogue Contrôle de l'ordinateur passe au premier plan. Tapez-y un message de suivi pour poursuivre la conversation, ou fermez la boîte de dialogue pour arrêter la session.

Cette fonction ne marche qu'avec les modèles qui fournissent un outil de contrôle de l'ordinateur : GPT-5.4, GPT-5.4 mini, GPT-5.5, GPT-5.5 pro, GPT-6 Astra, GPT-6.1 Sol, GPT-6.1 Terra, GPT-6 Luna, Claude 4.5 Sonnet, Claude 4.5 Opus, Claude 4.6 Sonnet, Claude 4.6 Opus, Claude 4.7 Opus, Claude 4.8 Opus, Claude 5 Sonnet, Claude 5 Opus, Claude 5 Fable, Claude 5.1 Fable, Claude 5.2 Fable, Claude 5.5 Haiku, Claude 5.5 Sonnet et Claude 5.5 Opus. Les autres modèles peuvent décrire des images, mais ils ne fournissent pas les actions structurées de souris et de clavier nécessaires au contrôle de l'ordinateur.

Pour utiliser le contrôle de l'ordinateur :

1. Configurez et sélectionnez l'un des modèles pris en charge.
2. Ouvrez l'application ou la fenêtre dans laquelle le modèle doit travailler.
3. Appuyez sur `NVDA+shift+i`, puis choisissez "Contrôler l'ordinateur...".
4. Tapez la tâche à effectuer et appuyez sur Envoyer.
5. Lisez la demande de consentement. Si vous autorisez la session, surveillez les actions et approuvez ou annulez les demandes de confirmation des actions risquées.

Remarque : cette fonction doit être considérée comme une version bêta, et nous travaillons activement à renforcer son implémentation.

## Dépendances

Certaines bibliothèques dont cet add-on a besoin sont trop volumineuses pour être incluses dans le paquet de l'add-on. À la place, au premier démarrage de NVDA avec l'add-on installé, il vous est demandé si vous voulez les télécharger. Choisissez oui, attendez la fin du téléchargement, et NVDA redémarre.

Le téléchargement est un fichier zip d'environ 35 à 70 Mo, selon votre version de NVDA. Il provient de la page [libs-release](https://github.com/cartertemm/AI-content-describer/releases/tag/libs-release) de ce dépôt. Si GitHub est inaccessible, l'add-on propose d'essayer un miroir fourni par la communauté chinoise de NVDA.

Le zip contient :

* [NumPy](https://numpy.org/) : calculs sur des tableaux, requis par OpenCV.
* [OpenCV](https://opencv.org/) (`cv2`) : repère votre visage dans les images de la webcam pour la fonction de détection de visage.
* [Pillow](https://python-pillow.org/) (`PIL`) : réalise les captures d'écran et les convertit en images lisibles par les modèles d'IA.
* [Markdown](https://python-markdown.github.io/) : affiche les descriptions avec leur mise en forme, comme les titres, les listes et les tableaux.
* [pygrabber](https://github.com/andreaschiavinato/python_grabber) : liste les webcams de votre ordinateur.
* Quelques modules de la bibliothèque standard de Python que NVDA n'inclut pas (`html`, `xml`, `pathlib`, `secrets` et `_markupbase`). Les bibliothèques ci-dessus en ont besoin.

Les fichiers sont placés dans un dossier nommé `aic-py-` suivi de la version de Python de NVDA, par exemple `aic-py-3.13`. Ce dossier se trouve dans votre dossier de configuration utilisateur de NVDA, généralement `%APPDATA%\nvda`. Chaque version de Python a son propre dossier : l'add-on télécharge donc à nouveau les bibliothèques lorsqu'une nouvelle version de NVDA change de version de Python. La désinstallation de l'add-on supprime le dossier correspondant à la version de Python actuelle de NVDA.

Si le téléchargement ne fonctionne pas, vous pouvez installer les bibliothèques vous-même. Téléchargez `aic-py-3.13.zip` (ou le fichier correspondant à la version de Python de votre NVDA) depuis la page libs-release, extrayez-le dans votre dossier de configuration utilisateur de NVDA, puis redémarrez NVDA.

## Construction de l'add-on

Pour créer le paquet de l'add-on à partir de la source, vous aurez besoin :

* d'une distribution Python (3.7 ou plus récent est recommandé). Consultez le [site Web de Python](https://www.python.org) pour les installateurs Windows. Veuillez noter qu'à l'heure actuelle, la préparation du code source de NVDA et des modules tiers inclus nécessite la version 32 bits de Python 3.7.
* Scons - [site Web](https://www.scons.org/) - version 4.3.0 ou ultérieure. Vous pouvez l'installer via PIP. `pip install scons`
* Markdown 3.3.0 ou ultérieur. `pip install markdown`

Ensuite, ouvrez votre terminal de choix :

```
git clone https://github.com/cartertemm/AI-content-describer.git
cd AI-content-describer
scons
```

Après l'exécution de la commande `scons`, un fichier *.nvda-addon sera placé à la racine de ce dépôt, prêt pour les tests et la publication.

Si vous ajoutez des chaînes supplémentaires qui nécessitent d'être traduites, il est important de reconstruire le fichier .pot comme suit :

```
scons pot
```

## Comment traduire ?

Sur une machine Windows :

* téléchargez [poedit](https://poedit.net/). C'est le logiciel que vous utiliserez pour traduire chaque message de l'anglais.
* téléchargez le fichier .pot avec toutes les chaînes [ici](https://raw.githubusercontent.com/cartertemm/AI-content-describer/main/AIContentDescriber.pot)
* Ouvrez le fichier que vous venez de télécharger dans le programme poedit. Cliquez sur "Créer une nouvelle traduction" dans la fenêtre qui apparaît, puis sélectionnez la langue cible.
* Parcourez et convertissez le contenu du texte source dans la langue cible, puis collez-le dans le champ de traduction. Pour une aide supplémentaire, n'hésitez pas à cliquer droit sur l'élément de liste -> occurrences de code, puis remontez d'une ligne pour lire le commentaire commençant par "# Translators: ". Ces commentaires sont également disponibles en un seul endroit dans le fichier .pot.
* Lorsque vous avez terminé, cliquez sur fichier -> enregistrer ou appuyez sur ctrl+s puis choisissez un emplacement pour le nouveau fichier .mo et .po à stocker. Ce sont les fichiers qui devraient m'être envoyés par courriel ou attachés dans une demande de tirage.
* Traduisez le contenu de readme.md (ce fichier). Attachez-le aussi !

## Contributions

Toutes sont grandement appréciées et seront créditées.
Les personnes suivantes ont travaillé sur l'addon.

* [Cary Rowen](https://github.com/cary-rowen) : a rendu l'add-on fonctionnel pour les utilisateurs chinois grâce à des miroirs pour les dépendances, et a ajouté la prise en charge du fournisseur Vivo Blue
* [Mazen](https://github.com/mzanm) : implémentation de Markdown, autres contributions au code
* [Kostenkov-2021](https://github.com/Kostenkov-2021) : traduction russe
* [Nidza07](https://github.com/nidza07) : traduction serbe
* [Heorhii Halas](nvda.translation.uk@gmail.com) et [George-br](https://github.com/George-br) : traduction ukrainienne
* [Umut Korkmaz](umutkork@gmail.com) : traduction turque
* [Platinum_Hikari](urbain_onces.0r@icloud.com) : traduction française
* [Lukas](https://4sensegaming.cz) : traduction tchèque
* [Michaela](https://technologiebezzraku.sk) : traduction slovaque

Vous rencontrez un problème ? Soumettez-le au [suivi des problèmes](https://github.com/cartertemm/AI-content-describer/issues)

Vous avez une suggestion pour une nouvelle fonctionnalité ? Créez également un ticket pour cela, et nous pourrons discuter de sa mise en œuvre. Les demandes de tirage sans problèmes associés seront examinées, mais sont susceptibles de prendre plus de temps pour tout le monde, surtout si je décide que la nouvelle correction ou fonctionnalité doit fonctionner différemment de ce qui a été proposé.

Les traductions sont accueillies à bras ouverts. Plus il y a de personnes qui peuvent accéder à cette technologie puissante, mieux c'est !

Si vous n'avez pas Github, ou préférez ne pas l'utiliser, vous pouvez [m'envoyer un courriel](mailto:carter@ctemm.me) - carter (at) ctemm (dot) me.

Merci pour votre soutien !
