# AI Content Describer for NVDA

This add-on makes it possible to obtain detailed descriptions for images and other visually inaccessible content.

Leveraging the multimodal capabilities of advanced AI models, we aim to deliver best-in-class content descriptions. For more information about the underlying model, refer to [GPT-4V](https://openai.com/research/gpt-4v-system-card).

## Features

* Describe the focus object, navigator object, or entire screen
* Describe any image that has been copied to the clipboard, be it a picture from an email or a path in windows explorer
* Supports multiple providers (currently OpenAI's GPT4 and Google's Gemini)
* Supports a wide variety of formats including PNG (.png), JPEG (.jpeg and .jpg), WEBP (.webp), and non-animated GIF (.gif)
* Optionally caches responses to preserve API quota
* For advanced use, customize the prompt and token count to tailor information to your needs

## Use case

There were a few primary motivations behind this project.

NVDA is capable of performing optical character recognition (OCR) out of the box, which is a game changer. If you are trying to get text out of an image or PDF document, this is what you're looking for.

However, OCR is only able to analyze data that *might* be text. It falls short at considering the context, objects and relationships conveyed in those images. And the internet is full of them. Logos, portraits, memes, icons, charts, diagrams, bar/line graphs... You name it. They're everywhere, and usually not in a format that screen reader users can interpret.
Until recently, there has been an unwavering reliance on content authors providing alternative text descriptions. While this is still a must, it's difficult to change the fact that a high standard of quality happens to be the exception, not the rule.

Now, the possibilities are almost endless. You might:

* Visualize the desktop or a specific window to understand the placement of icons when training others
* Get detailed info about the status of games, virtual machines, etc when sound is insufficient or unavailable
* Figure out what is displayed in a graph
* Demystify screenshots
* Ensure your face is looking clearly at the camera before recording videos or participating in online meetings

## Getting started

Download the latest release of the add-on from [this link](https://github.com/cartertemm/AI-content-describer/releases/latest/). Click on the file on a computer with NVDA installed, then follow the instructions below to obtain an API key from a supported provider.
If you are unsure about which one to use, the consensus of this addon's developer and testers is that Gemini currently offers more reasonable pricing, while OpenAI seems to provide a higher degree of accuracy. Of course, these results are highly dependent on the task at hand, so we recommend experimentation with different models and prompts to find what works best.

### Obtaining an API key from OpenAI:

1. Go to https://platform.openai.com/account/api-keys
2. If you don't yet have an account, create one. If you do, log in.
3. On the API keys page, click to create a new secret key. Copy it to your clipboard.
4. Fund the account with at least $1
5. In the NVDA settings dialog, scroll down to the AI Content Describer category, then choose "GPT4 Vision" as the provider, tab into the API key field, and paste the key you just generated here.

At the time of this writing, OpenAI issues credits to new developer accounts that can be used for three months, after which they are lost. Following this period, you will have to purchase credits. Typical usage shouldn't ever exceed $5.00 per month. For a point of reference, the original version of this add-on was developed for slightly under a dollar. It is always possible to login to your OpenAI account and click on "usage" to get your quota.

### Obtaining an API key from Google

1. You will first need to create a Google workspace project by following this link. Make sure you are logged in to your account. https://console.cloud.google.com/projectcreate
2. Create a name between four and thirty characters, like "gemini" or "NVDA add-on"
3. Navigate to this URL: https://makersuite.google.com/app/apikey
4. Click "create API key"
5. In the NVDA settings dialog, scroll down to the AI Content Describer category, then choose "Google Gemini" as your provider, tab into the API key field, and paste the key you just generated here.

## Using

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
