# Descripteur de contenu IA pour NVDA

Cet add-on permet d'obtenir des descriptions détaillées pour les images, les contrôles de l'interface utilisateur et autres contenus visuellement inaccessibles.

En tirant parti des capacités multimodales des modèles IA avancés et des algorithmes de vision par ordinateur, nous visons à fournir des descriptions de contenu de première classe et à augmenter l'indépendance globale. Pour plus d'informations sur les modèles sous-jacents, référez-vous à la section correspondante de ce document.

## Fonctionnalités

* Décrire l'objet de focus, l'objet navigateur, l'écran entier, ou prendre une photo avec la caméra embarquée
* Décrire toute image qui a été copiée dans le presse-papiers, que ce soit une image d'un courriel ou un chemin dans l'explorateur Windows
* Indiquer si le visage de l'utilisateur est positionné au centre du cadre en utilisant des algorithmes de vision par ordinateur (ne nécessite pas l'accès à une API payante)
* Supporte plusieurs fournisseurs (GPT4 d'OpenAI, Gemini de Google, Claude 3 d'Anthropic, et llama.cpp)
* Prend en charge une grande variété de formats incluant PNG (.png), JPEG (.jpeg et .jpg), WEBP (.webp), et GIF non animés (.gif)
* Cache optionnellement les réponses pour préserver le quota d'API
* Pour une utilisation avancée, personnaliser l'invite et le nombre de tokens pour adapter l'information à vos besoins
* Rendu Markdown pour accéder facilement aux informations structurées (intégrer par exemple "répondre en Markdown" à la fin de vos invites)

## Cas d'utilisation

Il y avait quelques motivations principales derrière ce projet.

NVDA est capable de réaliser la reconnaissance optique de caractères (OCR) directement, ce qui représente une avancée significative. Si vous essayez d'extraire du texte d'une image ou d'un document PDF, c'est ce que vous recherchez.

Cependant, l'OCR ne peut analyser que les données qui *pourraient* être du texte. Il est moins performant pour considérer le contexte, les objets et les relations véhiculés dans ces images. Et Internet en est plein. Logos, portraits, mèmes, icônes, graphiques, diagrammes, graphiques à barres/lignes... Ils sont partout et généralement pas dans un format que les utilisateurs de lecteurs d'écran peuvent interpréter.
Jusqu'à récemment, il y avait une dépendance constante envers les auteurs de contenu fournissant des descriptions de texte alternatives. Bien que cela soit toujours indispensable, il est difficile de changer le fait que un haut standard de qualité est l'exception, et non la règle.

Maintenant, les possibilités sont presque infinies. Vous pourriez :

* Visualiser le bureau ou une fenêtre spécifique pour comprendre le placement des icônes lors de la formation d'autres personnes
* Obtenir des informations détaillées sur l'état des jeux, des machines virtuelles, etc. lorsque le son est insuffisant ou indisponible
* Comprendre ce qui est affiché dans un graphique
* Démystifier les captures d'écran ou les partages d'écran dans Zoom ou Microsoft Teams
* Assurer que votre visage regarde clairement la caméra et que votre arrière-plan est professionnel avant d'enregistrer des vidéos ou de participer à des réunions en ligne

## Modèles

* [Vision GPT4](https://platform.openai.com/docs/guides/vision)
* [Vision pro Gemini de Google](https://blog.google/technology/ai/google-gemini-ai/)
* [Claude 3 (Haiku, Sonett, et Opus)](https://docs.anthropic.com/claude/docs/vision)
* [llama.cpp (extrêmement instable et lent selon votre matériel, testé pour fonctionner avec les modèles llava-v1.5/1.6, BakLLaVA, Obsidian, et MobileVLM 1.7B/3B)](https://github.com/ggerganov/llama.cpp)

Suivez les instructions fournies ci-dessous pour faire fonctionner chacun de ces modèles.

## Pour commencer

Téléchargez la dernière version de l'add-on depuis [ce lien](https://github.com/cartertemm/AI-content-describer/releases/latest/). Cliquez sur le fichier sur un ordinateur avec NVDA installé, puis suivez les instructions ci-dessous pour obtenir une clé API d'un fournisseur pris en charge.
Si vous n'êtes pas sûr du fournisseur à utiliser, le consensus des développeurs et testeurs de cet add-on est que Gemini offre actuellement des prix plus raisonnables, tandis qu'OpenAI semble fournir un degré de précision plus élevé. Claude 3 haiku est l'option la moins chère et la plus rapide mais la qualité est variable.
Bien sûr, ces résultats dépendent fortement de la tâche à accomplir, donc nous recommandons d'expérimenter avec différents modèles et invites pour trouver ce qui fonctionne le mieux.

### Obtenir une clé API d'OpenAI:

1. Allez sur https://platform.openai.com/account/api-keys
2. Si vous n'avez pas encore de compte, créez-en un. Si vous en avez un, connectez-vous.
3. Sur la page des clés API, cliquez pour créer une nouvelle clé secrète. Copiez-la dans votre presse-papiers.
4. Approvisionnez le compte avec au moins 1 $.
5. Dans le dialogue de configuration de NVDA, faites défiler jusqu'à la catégorie Descripteur de Contenu IA, puis choisissez "gérer les modèles (alt+m)", sélectionnez "Vision GPT4" comme fournisseur, tabez dans le champ de la clé API, et collez la clé que vous venez de générer ici.

### Obtenir une clé API de Google

1. Vous aurez d'abord besoin de créer un projet Google workspace en suivant ce lien. Assurez-vous d'être connecté à votre compte. https://console.cloud.google.com/projectcreate
2. Créez un nom entre quatre et trente caractères, comme "gemini" ou "add-on NVDA"
3. Naviguez vers cet URL : https://makersuite.google.com/app/apikey
4. Cliquez sur "créer une clé API"
5. Dans le dialogue de configuration de NVDA, faites défiler jusqu'à la catégorie Descripteur de Contenu IA, puis choisissez "gérer les modèles (alt+m)", sélectionnez "Gemini de Google" comme votre fournisseur, tabez dans le champ de la clé API, et collez la clé que vous venez de générer ici.

### Obtenir une clé API d'Anthropic

1. Connectez-vous à la [console Anthropic](https://console.anthropic.com/login).
2. Cliquez sur votre profil -> Clés API.
3. Cliquez sur Créer une clé.
4. Entrez un nom pour la clé, comme "DescripteurContenuIA", puis cliquez sur "Créer une clé" et copiez la valeur qui apparaît. C'est ce que vous collerez dans le champ de la clé API sous la catégorie Descripteur de Contenu IA du dialogue de configuration de NVDA -> gérer les modèles -> Claude 3.
5. Si vous ne l'avez pas déjà fait, achetez au moins 5 $ en crédits sur la page des plans à https://console.anthropic.com/settings/plans.

### Configurer llama.cpp

Ce fournisseur est actuellement quelque peu bogué, et votre expérience peut varier. Il devrait vraiment seulement être tenté par des utilisateurs avancés intéressés par l'exécution de modèles auto-hébergés locaux, et ayant le matériel nécessaire pour cela.

1. Téléchargez llama.cpp. À l'heure actuelle, cette [demande de tirage](https://github.com/ggerganov/llama.cpp/pull/5882) supprime les capacités multimodales donc vous voudrez utiliser la [dernière version avec support pour cela](https://github.com/ggerganov/llama.cpp/releases/tag/b2356).
Si vous utilisez un adaptateur graphique Nvidia avec support CUDA, téléchargez ces binaires préconstruits :
[llama-b2356-bin-win-cublas-cu12.2.0-x64.zip](https://github.com/ggerganov/llama.cpp/releases/download/b2356/llama-b2356-bin-win-cublas-cu12.2.0-x64.zip) et [cudart-llama-bin-win-cu12.2.0-x64.zip](https://github.com/ggerganov/llama.cpp/releases/download/b2356/cudart-llama-bin-win-cu12.2.0-x64.zip)
Les étapes pour travailler avec un autre adaptateur graphique sont hors de portée, mais peuvent être trouvées dans le readme de llama.cpp.
2. Extrayez ces deux fichiers dans le même dossier.
3. Localisez les formats quantifiés des modèles que vous souhaitez utiliser de Huggingface. Pour LLaVA 1.6 Vicuna 7B : [llava-v1.6-vicuna-7b.Q4_K_M.gguf](https://huggingface.co/cjpais/llava-v1.6-vicuna-7b-gguf/blob/main/llava-v1.6-vicuna-7b.Q4_K_M.gguf) et [mmproj-model-f16.gguf](https://huggingface.co/cjpais/llava-v1.6-vicuna-7b-gguf/blob/main/mmproj-model-f16.gguf)
4. Mettez ces fichiers dans le dossier avec le reste des binaires de llama.cpp.
5. Depuis un invite de commande, exécutez le binaire du serveur llama.cpp, en passant les fichiers .gguf pour le modèle et le projecteur multimodal (comme suit) :
`server.exe -m llava-v1.6-vicuna-7b.Q4_K_M.gguf --mmproj mmproj-model-f16.gguf`
6. Dans le dialogue de configuration de NVDA, faites défiler jusqu'à la catégorie Descripteur de Contenu IA, puis choisissez "gérer les modèles (alt+m)", sélectionnez "llama.cpp" comme votre fournisseur, tabez dans le champ de l'URL de base, et entrez le point de terminaison montré dans la console (par défaut à "http://localhost:8080").
7. Alternativement, vous pourriez omettre certaines de ces étapes et exécuter llama.cpp sur un serveur distant avec des spécifications supérieures à celles de votre machine locale, puis entrez ce point de terminaison à la place.

## Utilisation

Quatre raccourcis clavier sont liés par défaut :

* NVDA+shift+i : Ouvre un menu demandant de décrire l'objet de focus actuel, l'objet navigateur, la caméra physique, ou l'écran entier avec IA.
* NVDA+shift+u : Décrit le contenu de l'objet navigateur actuel en utilisant l'IA.
* NVDA+shift+y : Décrit l'image (ou le chemin de fichier vers une image) dans le presse-papiers en utilisant l'IA.
* NVDA+shift+j : Décrit la position de votre visage dans le cadre de la caméra sélectionnée. Si vous avez plusieurs caméras connectées, naviguez jusqu'au menu Descripteur de Contenu IA (NVDA+shift+i) et choisissez celle que vous souhaitez utiliser avec l'option "sélectionner la caméra" dans le sous-menu de détection de visage.

Trois gestes sont non liés :

* Décrire le contenu de l'élément actuellement focalisé en utilisant l'IA.
* Prendre une capture d'écran, puis la décrire en utilisant l'IA.
* Prendre une photo en utilisant la caméra sélectionnée, puis la décrire en utilisant l'IA.

N'hésitez pas à personnaliser ces éléments à tout moment depuis le dialogue des gestes d'entrée.

## Construction de l'add-on

Pour créer le paquet de l'add-on à partir de la source, vous aurez besoin :

* d'une distribution Python (3.7 ou plus récent est recommandé). Consultez le [site Web de Python](https://www.python.org) pour les installateurs Windows. Veuillez noter qu'à l'heure actuelle, la préparation du code source de NVDA et des modules tiers inclus nécessite la version 32 bits de Python 3.7.
* Scons - [site Web](https://www.scons.org/) - version 4.3.0 ou ultérieure. Vous pouvez l'installer via PIP. `pip install scons`
* Markdown 3.3.0 ou ultérieur. `pip install markdown`

Ensuite, ouvrez votre terminal de choix :

git clone https://github.com/cartertemm/AI-content-describer.git
cd AI-content-describer
scons
vbnet

Après l'exécution de la commande `scons`, un fichier *.nvda-addon sera placé à la racine de ce répertoire prêt pour les tests et la publication.

Si vous ajoutez des chaînes supplémentaires qui nécessitent d'être traduites, il est important de reconstruire le fichier .pot comme suit :

scons pot
less

## Comment traduire ?

Sur une machine Windows :

* téléchargez [poedit](https://poedit.net/). C'est le logiciel que vous utiliserez pour traduire chaque message de l'anglais.
* téléchargez le fichier .pot avec toutes les chaînes [ici](https://raw.githubusercontent.com/cartertemm/AI-content-describer/main/AIContentDescriber.pot)
* Ouvrez le fichier que vous venez de télécharger dans le programme poedit. Cliquez sur "Créer une nouvelle traduction" dans la fenêtre qui apparaît, puis sélectionnez la langue cible.
* Parcourez et convertissez le contenu du texte source dans la langue cible, puis collez-le dans le champ de traduction. Pour une aide supplémentaire, n'hésitez pas à cliquer droit sur l'élément de liste -> occurrences de code, puis remontez d'une ligne pour lire le commentaire commençant par "# Traducteurs : ". Ces commentaires sont également disponibles en un seul endroit dans le fichier .pot.
* Lorsque vous avez terminé, cliquez sur fichier -> enregistrer ou appuyez sur ctrl+s puis choisissez un emplacement pour le nouveau fichier .mo et .po à stocker. Ce sont les fichiers qui devraient m'être envoyés par courriel ou attachés dans une demande de tirage.
* Traduisez le contenu de readme.md (ce fichier). Attachez-le aussi !

## Contributions

Toutes sont grandement appréciées et seront créditées.
Les personnes suivantes ont travaillé sur l'addon.

* [Mazen](https://github.com/mzanm)
* [Kostenkov-2021](https://github.com/Kostenkov-2021)
* [nidza07](https://github.com/nidza07)
* [Heorhii Halas](nvda.translation.uk@gmail.com)

Vous rencontrez un problème ? Soumettez-le au [suivi des problèmes](https://github.com/cartertemm/AI-content-describer/issues)

Vous avez une suggestion pour une nouvelle fonctionnalité ? Créez également un ticket pour cela, et nous pourrons discuter de sa mise en œuvre. Les demandes de tirage sans problèmes associés seront examinées, mais sont susceptibles de prendre plus de temps pour tout le monde, surtout si je décide que la nouvelle correction ou fonctionnalité doit fonctionner différemment de ce qui a été proposé.

Les traductions sont accueillies à bras ouverts. Plus il y a de personnes qui peuvent accéder à cette technologie puissante, mieux c'est !

Si vous n'avez pas Github, ou préférez ne pas l'utiliser, vous pouvez [m'envoyer un courriel](mailto:cartertemm@gmail.com) - cartertemm (at) gmail (dot) com.

Merci pour votre soutien!