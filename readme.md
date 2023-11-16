# AI Content Describer for NVDA

This add-on makes it possible to obtain detailed descriptions for images and other visually inaccessible content.

Leveraging the multimodal capabilities of the GPT-4 large language model, we aim to deliver best-in-class content descriptions. For more information about the underlying model, refer to [GPT-4V](https://openai.com/research/gpt-4v-system-card).

## Features

* Describe the focus object, navigator object, or entire screen
* Describe any image that has been copied to the clipboard, be it a picture from an email or a path in windows explorer
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

Download the latest release of the add-on from [this link](https://github.com/cartertemm/AIImageDescriber/releases/latest/). Click on the file on a computer with NVDA installed, then follow the instructions below to obtain an API key from OpenAI:

1. Go to https://platform.openai.com/account/api-keys
2. If you don't yet have an account, create one. If you do, log in.
3. On the API keys page, click to create a new secret key. Copy it to your clipboard.
4. In the NVDA settings dialog, scroll down to the AI Content Describer category, then tab into the API key field and paste the item you just generated here.

At the time of this writing, OpenAI issues credits to new developer accounts that can be used for three months, after which they are lost.

Following this period, you will have to purchase credits. Typical usage shouldn't ever exceed $5.00 per month. For a referencepoint, the original version of this add-on was developed for slightly under a dollar. It is always possible to login to your OpenAI account and click on "usage" to get your quota.

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
scons
```

After the `scons` command is finished executing, you should see a *.nvda-addon file ready for release.

## Contributions

All are highly appreciated.

Find an issue? Submit it to the [issue tracker](https://github.com/cartertemm/AI-content-describer/issues)

Have a suggestion for a new feature? Create a ticket for that as well, and we can talk about implementing it. Pull requests without associated issues will be reviewed, but are likely to take up more time for everyone, especially if I decide the new fix or functionality needs to work differently.

Translations are welcomed with open arms.

If you don't have Github, or prefer not to use it, you can [shoot me an email](mailto:cartertemm@gmail.com) - cartertemm (at) gmail (dot) com.

Thanks for the support!
