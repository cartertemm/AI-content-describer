# AI Content Describer for NVDA

This add-on makes it possible to obtain detailed descriptions for images and other visually inaccessible content.

Leveraging the multimodal capabilities of advanced AI models, we aim to deliver best-in-class content descriptions.
For more information about the underlying models, refer to the models section of this document.

## Features

* Describe the focus object, navigator object, or entire screen
* Describe any image that has been copied to the clipboard, be it a picture from an email or a path in windows explorer
* Supports multiple providers (OpenAI's GPT4, Google's Gemini, Anthropic's Claude 3, and llama.cpp)
* Supports a wide variety of formats including PNG (.png), JPEG (.jpeg and .jpg), WEBP (.webp), and non-animated GIF (.gif)
* Optionally caches responses to preserve API quota
* For advanced use, customize the prompt and token count to tailor information to your needs
* Markdown rendering to easily access structured information

## Use case

There were a few primary motivations behind this project.

NVDA is capable of performing optical character recognition (OCR) out of the box, which is a game changer. If you are trying to get text out of an image or PDF document, this is what you're looking for.

However, OCR is only able to analyze data that *might* be text. It falls short at considering the context, objects and relationships conveyed in those images. And the internet is full of them. Logos, portraits, memes, icons, charts, diagrams, bar/line graphs... You name it. They're everywhere, and usually not in a format that screen reader users can interpret.
Until recently, there has been an unwavering reliance on content authors providing alternative text descriptions. While this is still a must, it's difficult to change the fact that a high standard of quality happens to be the exception, not the rule.

Now, the possibilities are almost endless. You might:

* Visualize the desktop or a specific window to understand the placement of icons when training others
* Get detailed info about the status of games, virtual machines, etc when sound is insufficient or unavailable
* Figure out what is displayed in a graph
* Demystify screenshots or screen shares in Zoom or Microsoft Teams
* Ensure your face is looking clearly at the camera and that your background is professional before recording videos or participating in online meetings

## Models

* [GPT4 vision](https://platform.openai.com/docs/guides/vision)
* [Google Gemini pro vision](https://blog.google/technology/ai/google-gemini-ai/)
* [Claude 3 (Haiku, Sonett, and Opus)](https://docs.anthropic.com/claude/docs/vision)
* [llama.cpp (extremely unstable and slow depending on your hardware, tested to work with llava-v1.5/1.6, BakLLaVA, Obsidian, and MobileVLM 1.7B/3B models)](https://github.com/ggerganov/llama.cpp)

Follow the instructions provided below to get each of these working.

## Getting started

Download the latest release of the add-on from [this link](https://github.com/cartertemm/AI-content-describer/releases/latest/). Click on the file on a computer with NVDA installed, then follow the instructions below to obtain an API key from a supported provider.
If you are unsure about which one to use, the consensus of this addon's developer and testers is that Gemini currently offers more reasonable pricing, while OpenAI seems to provide a higher degree of accuracy. Claude 3 haiku is the cheapest and fastest option but the quality is hit or miss.
Of course, these results are highly dependent on the task at hand, so we recommend experimenting with different models and prompts to find what works best.

### Obtaining an API key from OpenAI:

1. Go to https://platform.openai.com/account/api-keys
2. If you don't yet have an account, create one. If you do, log in.
3. On the API keys page, click to create a new secret key. Copy it to your clipboard.
4. Fund the account with at least $1
5. In the NVDA settings dialog, scroll down to the AI Content Describer category, then choose "manage models (alt+m)", select "GPT4 Vision" as the provider, tab into the API key field, and paste the key you just generated here.

At the time of this writing, OpenAI issues credits to new developer accounts that can be used for three months, after which they are lost. Following this period, you will have to purchase credits. Typical usage shouldn't ever exceed $5.00 per month. For a point of reference, the original version of this add-on was developed for slightly under a dollar. It is always possible to login to your OpenAI account and click on "usage" to get your quota.

### Obtaining an API key from Google

1. You will first need to create a Google workspace project by following this link. Make sure you are logged in to your account. https://console.cloud.google.com/projectcreate
2. Create a name between four and thirty characters, like "gemini" or "NVDA add-on"
3. Navigate to this URL: https://makersuite.google.com/app/apikey
4. Click "create API key"
5. In the NVDA settings dialog, scroll down to the AI Content Describer category, then choose "manage models (alt+m)", select "Google Gemini" as your provider, tab into the API key field, and paste the key you just generated here.

### Obtaining an API key from Anthropic

1. Login to the [Anthropic console](https://console.anthropic.com/login).
2. Click on your profile -> API keys.
3. Click Create Key.
4. Enter a name for the key, like "AIContentDescriber", then click on "Create Key" and copy the value that shows up. This is what you will paste into the API key field under the Ai Content Describer category of the NVDA settings dialog -> manage models -> Claude 3.
5. If you haven't already, purchase at least $5 in credits under the plans page at https://console.anthropic.com/settings/plans.

### Setting up llama.cpp

This provider is currently somewhat buggy, and your milage may very. It should really only be attempted by advanced users with an interest in running local self-hosted models, and the hardware to do so.

1. Download llama.cpp. At the time of this writing, this [pull request](https://github.com/ggerganov/llama.cpp/pull/5882) removes multimodal capabilities so you will want to use the [last version with support for this](https://github.com/ggerganov/llama.cpp/releases/tag/b2356).
If you are running on an Nvidia graphics adapter with CUDA support, download these prebuilt binaries:

[llama-b2356-bin-win-cublas-cu12.2.0-x64.zip](https://github.com/ggerganov/llama.cpp/releases/download/b2356/llama-b2356-bin-win-cublas-cu12.2.0-x64.zip) and [cudart-llama-bin-win-cu12.2.0-x64.zip](https://github.com/ggerganov/llama.cpp/releases/download/b2356/cudart-llama-bin-win-cu12.2.0-x64.zip)

The steps for working with a different graphics adapter are out of scope, but can be found in the llama.cpp readme.

2. Extract both of these files into the same folder.
3. Locate the quantized formats of the models you'd like to use from Huggingface. For LLaVA 1.6 Vicuna 7B: [llava-v1.6-vicuna-7b.Q4_K_M.gguf](https://huggingface.co/cjpais/llava-v1.6-vicuna-7b-gguf/blob/main/llava-v1.6-vicuna-7b.Q4_K_M.gguf) and [mmproj-model-f16.gguf](https://huggingface.co/cjpais/llava-v1.6-vicuna-7b-gguf/blob/main/mmproj-model-f16.gguf)
4. Put these files in the folder with the rest of the llama.cpp binaries.
5. From a command prompt, run the llava.cpp server binary, passing the .gguf files for the model and multimodal projector (as follows):

`server.exe -m llava-v1.6-vicuna-7b.Q4_K_M.gguf --mmproj mmproj-model-f16.gguf`

6. In the NVDA settings dialog, scroll down to the AI Content Describer category, then choose "manage models (alt+m)", select "llama.cpp" as your provider, tab into the base URL field, and enter the endpoint shown in the console (defaults to "http://localhost:8080").
7. Alternatively, you may omit some of these steps and run llama.cpp on a remote server with higher specs than your local machine, then enter that endpoint instead.

## Usage

Three hotkeys are bound by default:

* NVDA+shift+i: Pops up a menu asking whether to describe the current focus, navigator object, or entire screen with AI.
* NVDA+shift+u: Describe the contents of the current navigator object using AI.
* NVDA+shift+y: Describe the image (or file path to an image) on the clipboard using AI.

Two gestures are unbound:

* Describe the contents of the currently focused item using AI.
* Take a screenshot, then describe it using AI.

Don't hesitate to customize these at any time from the input gestures dialog.

## Building the add-on

To create the add-on package from source, you will need:

* a Python distribution (3.7 or later is recommended). Check the [Python Website](https://www.python.org) for Windows Installers. Please note that at present, preparing the NVDA source code and included third party modules requires the 32-bit version of Python 3.7.
* Scons - [Website](https://www.scons.org/) - version 4.3.0 or later. You can install it via PIP. `pip install scons`
* Markdown 3.3.0 or later. `pip install markdown`

Then open your terminal of choice:

```
git clone https://github.com/cartertemm/AI-content-describer.git
cd AI-content-describer
scons
```

After the `scons` command is finished executing, a *.nvda-addon file will be placed in the root of this repository ready for testing and release.

If you add additional strings that need to be translated, it is important to rebuild the .pot file like so:

```
scons pot
```

## How to translate?

On a windows machine:

* download [poedit](https://poedit.net/). This is the software you will use to translate each message from English.
* download the .pot file with all the strings [here](https://raw.githubusercontent.com/cartertemm/AI-content-describer/main/AIContentDescriber.pot)
* Open the file you just downloaded in the poedit program. Click "Create new translation" in the window that appears, then select the target language.
* Go through and convert the contents of the source text into the target language, then paste it into the translation field. For extra help, feel free to right click the list item -> code occurrences, then go up a line to read the comment starting with "# Translators: ". These comments are additionally made available in one place in the .pot file.
* When done, click file -> save or press ctrl+s then choose a location for the new .mo and .po file to be stored. These are the files that should be emailed to me or attached in a pull request.
* Translate the contents of readme.md (this file). Attach it too!

## Contributions

All are highly appreciated and will be credited.

Facing a problem? Submit it to the [issue tracker](https://github.com/cartertemm/AI-content-describer/issues)

Have a suggestion for a new feature? Create a ticket for that as well, and we can talk about implementing it. Pull requests without associated issues will be reviewed, but are likely to take up more time for everyone, especially if I decide the new fix or functionality needs to work differently than what was proposed.

Translations are welcomed with open arms.

If you don't have Github, or prefer not to use it, you can [shoot me an email](mailto:cartertemm@gmail.com) - cartertemm (at) gmail (dot) com.

Thanks for the support!
