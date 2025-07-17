# AI 内容描述器

本插件旨在解决视觉内容的获取难题，能够为图像、用户界面控件等提供详尽的描述。

我们利用了先进的 AI 模型和计算机视觉算法的多模态能力，旨在提供一流的内容描述，从而全面提升用户的独立性。关于所使用底层模型的更多信息，请参阅本文档的相应部分。

## 功能特性

*   描述**焦点对象**、**导航对象**、全屏幕，或使用内置摄像头拍摄照片。
*   描述已复制到剪贴板的图像，无论是电子邮件中的图片，还是 Windows 资源管理器中的图片文件路径。
*   利用计算机视觉算法判断用户的脸部是否位于取景框中（此功能无需付费 API）。
*   默认模型免费使用，您也可以选择添加自己的 API 密钥以解锁更多模型。
*   支持多家服务提供商（OpenAI 的 GPT、Google 的 Gemini、Mistral 的 Pixtral Large、Anthropic 的 Claude 3、XAI 的 Grok、Ollama 和 llama.cpp）。
*   支持多种图像格式，包括 PNG (.png)、JPEG (.jpeg 和 .jpg)、WEBP (.webp) 和非动画 GIF (.gif)。
*   可选择缓存识别结果，以节省 API 调用额度。
*   对于高级用户，可以自定义提示词和 token 数量，以满足个性化需求。
*   支持在获得描述后，继续追问或上传其他的图片。
*   支持 Markdown 渲染，方便您访问结构化信息（只需在设置中启用“在浏览模式中显示结果”，并在提示词末尾加入“以 Markdown 格式回答”等指令即可）。

## 应用场景

这个项目源于几个核心需求。

NVDA 本身就具备强大的光学字符识别（OCR）功能，这是一项颠覆性的技术。如果您需要从图片或 PDF 文档中提取文字，那么 NVDA 的自带功能是您的首选。

然而，OCR 只能分析那些*可能*包含文字的图像数据，却无法理解图像所传达的上下文、物体及其相互关系。互联网上充斥着大量此类图像：商标、肖像、表情包、图标、图表、示意图、柱状/折线图……应有尽有。这些图像无处不在，但屏幕阅读器通常无法直接描述这些图像。
过去，我们高度依赖内容创作者提供替代文本。尽管这依然是网页无障碍的最佳实践，但一个不争的事实是：高质量的替代文本并不多见。

现在，有了 AI 的加持，解锁了无限可能。您可以：

*   在提供培训时，将桌面或特定窗口“可视化”，从而清晰地了解图标的布局。
*   当游戏、虚拟机等应用无声时，获取其状态的详细信息。
*   轻松弄清楚图表或插图所展示的内容。
*   在 Zoom 或 Microsoft Teams 会议中，快速理解他人分享的屏幕截图或投屏画面。
*   在录制视频或参加在线会议前，确保自己的面部正对摄像头且背景环境适宜。

## 支持的模型

*   [GPT4 vision](https://platform.openai.com/docs/guides/vision)，包括 4O、O1、O3 及其衍生模型。
*   [Google Gemini pro vision](https://blog.google/technology/ai/google-gemini-ai/)，包括最新的 1.5 Flash、1.5 Flash 8B、Flash 2.0、Flash 2.0 Lite Preview、2.5 Flash 和 2.5 Pro 模型。
*   [Claude 3 和 4 (Haiku, Sonett, and Opus)](https://docs.anthropic.com/claude/docs/vision)
*   [Pixtral Large](https://mistral.ai/en/news/pixtral-large)
*   [Grok-2](https://x.ai/news/grok-2)
*   [Ollama (不稳定)](https://ollama.com/)
*   [llama.cpp (极不稳定，速度取决于硬件，经测试可与 llava-v1.5/1.6、BakLLaVA、Obsidian 和 MobileVLM 1.7B/3B 模型配合使用)](https://github.com/ggerganov/llama.cpp)

请按照以下说明设置，以确保这些模型能正常工作。

## 快速入门

请从[此链接](https://github.com/cartertemm/AI-content-describer/releases/latest/)下载插件的最新版本。在安装了 NVDA 的电脑上双击该文件，并按照提示完成安装。

自 2025.06.05 版本起，得益于 PollinationsAI 社区的大力支持，GPT4 模型可以免费使用。

如果您有能力且希望探索其他模型，可以随时使用自己的 API 密钥，这样可以节省公共资源。如果不需要，请直接跳至本文档的`用法`部分。

请按照以下说明，从支持的提供商处获取 API 密钥。
如果您不确定该如何选择，本插件开发者和测试人员的共识是：Gemini 的定价目前更具优势，而 OpenAI 在准确性上似乎略胜一筹。Claude 3 Haiku 是最便宜且速度最快的选择，但识别质量时好时坏。
当然，以上结论在很大程度上取决于具体的使用场景，我们鼓励您多尝试不同的模型和提示词，以找到最适合自己的方案。

### 获取 OpenAI 的 API 密钥：

1.  前往 [OpenAI 的 API 密钥 页面](https://platform.openai.com/account/api-keys)。
2.  如果您还没有账户，请先注册一个；如果已有账户，请直接登录。
3.  在 API 密钥 页面，点击“创建新密钥”，然后将其复制到剪贴板。
4.  为您的账户充值至少 1 美元。
5.  打开 NVDA **设置**对话框，找到“AI 内容描述器”**类别**，选择“管理模型(M)”。在提供商列表中选择“GPT4 Vision”，接着按 Tab 键到 API 密钥编辑框，粘贴您刚刚生成的密钥。

在撰写本文时，OpenAI 会向新注册的开发者账户赠送为期三个月的免费额度，该额度到期后将作废。之后，您需要自行购买额度。正常使用情况下，每月的费用一般不会超过 5 美元。作为参考，本插件的早期开发版本，其 API 总花费还不到 1 美元。您可以随时登录 OpenAI 账户，点击“用量”查询您的额度使用情况。

### 获取 Google 的 API 密钥

1.  首先，您需要前往 [Google Cloud Console](https://console.cloud.google.com/projectcreate) 创建一个 Google Workspace 项目。请确保您已登录您的 Google 账户。
2.  创建一个长度在 4 到 30 个字符之间的名称，例如“Gemini”或“NVDA 插件”。
3.  前往 [Google AI Studio API 密钥页面](https://makersuite.google.com/app/apikey)。
4.  点击“创建 API 密钥”。
5.  打开 NVDA **设置**对话框，找到“AI 内容描述器”**类别**，选择“管理模型(M)”。在提供商列表中选择“Google Gemini”，接着按 Tab 键到 API 密钥编辑框，粘贴您刚刚生成的密钥。

### 获取 Anthropic 的 API 密钥

1.  登录 [Anthropic 控制台](https://console.anthropic.com/login)。
2.  点击您的个人资料 -> API 密钥。
3.  点击“创建密钥”。
4.  为密钥输入一个名称（如“AIContentDescriber”），然后点击“创建密钥”并复制显示的值。请将此值粘贴到 NVDA **设置**对话框中“AI 内容描述器”**类别**下的“管理模型” -> “Claude 3”的 API 密钥编辑框中。
5.  如果您尚未充值，请在 [Anthropic 套餐页面](https://console.anthropic.com/settings/plans)至少购买 5 美元的额度。

### 获取 Mistral 的 API 密钥

1.  前往 [MistralAI 登录页面](https://auth.mistral.ai/ui/login)，登录或创建一个 MistralAI 账户。
2.  如果您是首次创建或登录账户，请按提示添加一个工作区，提供名称并接受条款和条件。
3.  登录后，从菜单中选择“API 密钥”。
4.  点击“创建新密钥”，并将其复制到剪贴板。请将此值粘贴到 NVDA **设置**对话框中“AI 内容描述器”**类别**下的“管理模型” -> “Pixtral”的 API 密钥编辑框中。
5.  如果需要，请为账户充值。


### 注册 NVDA-CN 账户，使用 VIVO 蓝心大模型

该服务由 VIVO (vivo.com.cn) 与 NVDA 中文社区 (NVDACN) 合作免费提供。它具备高质量的多模态识别能力。

要使用此模型，您只需要一个免费的 NVDA-CN 账号。

1.  **注册账号**：访问 NVDA-CN 注册页面：[https://nvdacn.com/admin/register.php](https://nvdacn.com/admin/register.php)。
    *   您需要提供用户名、密码和一个有效的电子邮箱地址。由于该网站尚未实现自助密码找回功能，请务必妥善保管您的密码。
2.  **验证您的邮箱**：检查您的收件箱，找到验证邮件并点击其中的链接以激活您的账号。
3.  **配置插件**：
    *   打开 NVDA 设置对话框，并找到“AI 内容描述器”分类。
    *   选择“管理模型”按钮。
    *   在类别列表中，选择“vivo BlueLM Vision (NVDA-CN)”。
    *   在相应的输入框中，填入您刚刚创建的 NVDA-CN 用户名和密码。
    * 可以使用中文撰写提示词，或者明确告知模型以中文回答。
    *   点击“确定”以保存您的凭据。

现在，您已经设置完毕，可以开始使用 VIVO 模型了。如遇任何与账号相关的问题，您可以通过 `support@nvdacn.com` 联系 NVDA-CN 团队。


### 设置 Ollama

这是目前本地部署的首选方案。

尽管 Ollama 的集成测试比 llama.cpp 更为广泛，但它仍不如调用 API 稳定，并且在某些配置下可能会出现异常行为，甚至在不满足硬件要求的计算机上会导致崩溃。
以防万一，在首次尝试此功能前，请务必保存所有文档和重要内容。

首先，请确保您能够使用命令行界面与您喜欢的视觉模型进行交互。步骤如下：

1.  从 [Ollama 下载页面](https://ollama.com/download)下载 Ollama for Windows 的安装文件。
2.  运行此安装文件。它会自动获取您计算机所需的所有依赖项。
3.  找到您想使用的模型。您可以在 ollama.com -> models -> vision，或直接[在此处](https://ollama.com/search?c=vision)找到支持的模型列表。
4.  打开命令提示符，输入 `ollama run [model_name]` 来下载并启动该模型，请务必将“[model_name]”替换为您在第 3 步中选择的模型名称。例如：`ollama run llama3.2-vision`。
5.  假设上述过程成功完成，您将会进入一个交互式命令行界面，您可以在其中输入提示词并获取回答，可以把它想象成一个本地化（且功能有限）的 ChatGPT。通过提问（任何问题）来测试它是否正常工作，然后输入“/bye”退出此界面。
6.  回到您的控制台窗口，输入 `ollama list`。第一列将提供一个名称，例如“llama3.2-vision:latest”。
7.  前往“AI 内容描述器”设置 -> “管理模型” -> “Ollama”。在模型名称编辑框中，输入此值，然后点击“确认” -> “确认”。这样就设置好了！在模型子菜单中切换到 Ollama，稍等片刻即可正常使用。

### 设置 llama.cpp

该提供商目前尚存在一些问题，效果因人而异。建议仅由有兴趣运行本地自托管模型且拥有相应硬件的高级用户尝试。

1.  下载 llama.cpp。在撰写本文时，此[pull request](https://github.com/ggerganov/llama.cpp/pull/5882)移除了多模态功能，因此您需要使用[支持此功能的最后一个版本](https://github.com/ggerganov/llama.cpp/releases/tag/b2356)。
    如果您在支持 CUDA 的 Nvidia 显卡上运行，请下载这些预编译的二进制文件：
    [llama-b2356-bin-win-cublas-cu12.2.0-x64.zip](https://github.com/ggerganov/llama.cpp/releases/download/b2356/llama-b2356-bin-win-cublas-cu12.2.0-x64.zip) 和 [cudart-llama-bin-win-cu12.2.0-x64.zip](https://github.com/ggerganov/llama.cpp/releases/download/b2356/cudart-llama-bin-win-cu12.2.0-x64.zip)
    其他显卡的设置步骤不在本文档讨论范围内，但可以在 llama.cpp 的自述文件中找到。
2.  将这两个文件解压到同一个文件夹中。
3.  从 Huggingface 找到您想使用的模型的量化格式。对于 LLaVA 1.6 Vicuna 7B 模型：[llava-v1.6-vicuna-7b.Q4_K_M.gguf](https://huggingface.co/cjpais/llava-v1.6-vicuna-7b-gguf/blob/main/llava-v1.6-vicuna-7b.Q4_K_M.gguf) 和 [mmproj-model-f16.gguf](https://huggingface.co/cjpais/llava-v1.6-vicuna-7b-gguf/blob/main/mmproj-model-f16.gguf)
4.  将这些文件与其余的 llama.cpp 二进制文件放在同一个文件夹中。
5.  在命令提示符中，运行 llava.cpp 服务器二进制文件，并传入模型和多模态投影器的 .gguf 文件（如下所示）：
    ```
    server.exe -m llava-v1.6-vicuna-7b.Q4_K_M.gguf --mmproj mmproj-model-f16.gguf
    ```
6.  打开 NVDA **设置**对话框，找到“AI 内容描述器”**类别**，选择“管理模型(M)”。在提供商列表中选择“llama.cpp”，接着按 Tab 键到“基础 URL”编辑框，然后输入控制台中显示的端点（默认为“http://localhost:8080”）。
7.  或者，您可以省略其中一些步骤，在配置比您本地机器更高的远程服务器上运行 llama.cpp，然后输入该服务器的端点地址。

## 用法

默认分配了五个快捷键：

*   NVDA+Shift+I：弹出一个菜单，询问是描述当前焦点、导航对象、物理摄像头还是全屏幕。
*   NVDA+Shift+U：使用 AI 描述当前导航对象的内容。
*   NVDA+Shift+Y：使用 AI 描述剪贴板中的图像（或图像文件路径）。
*   NVDA+Shift+J：描述您的面部在所选摄像头画面中的位置。如果您连接了多个摄像头，请前往“AI 内容描述器”菜单（NVDA+Shift+I），并在“面部检测”子菜单的“选择摄像头”选项中选择您想使用的摄像头。
*   NVDA+Alt+I：打开 AI 对话框，以进行追问。

有三项功能未分配默认快捷键：

*   使用 AI 描述当前焦点。
*   截取屏幕截图，然后使用 AI 进行描述。
*   使用所选摄像头拍摄照片，然后使用 AI 进行描述。

您可以随时在“按键与手势”对话框中自定义这些快捷键。

### 对描述进行追问

有时候，AI 返回的描述可能不够充分。也许是图像质量差、不完整，或包含不感兴趣的细节。或者您想聚焦于某个特定部分，亦或在不丢失上下文的情况下拍一张更清晰的照片。
在收到描述后，您可以按下 NVDA+Shift+C，或从“AI 内容描述器”上下文菜单（NVDA+Shift+I）中选择“对先前的描述进行追问”。默认情况下，焦点会设置在消息编辑框。
要添加其他图片，只需保持对话窗口打开，并照常使用本插件。当拍摄一张图片（无论是来自摄像头、系统控件、截图等）时，系统会询问您是将其附加到当前会话，还是开始一个新会话。

## 创建插件包

要从源代码创建插件包，您需要准备以下环境：

*   一个 Python 发行版（推荐 3.7 或更高版本）。请访问 [Python 网站](https://www.python.org)获取 Windows 安装程序。请注意，目前准备 NVDA 源代码和其包含的第三方模块需要 32 位的 Python 3.7。
*   Scons - [网站](https://www.scons.org/) - 版本 4.3.0 或更高。您可以通过 PIP 安装：`pip install scons`
*   Markdown 3.3.0 或更高版本：`pip install markdown`

然后打开您选择的终端：

```
git clone https://github.com/cartertemm/AI-content-describer.git
cd AI-content-describer
scons
```

`scons` 命令执行完毕后，一个 *.nvda-addon 文件将被放置在本仓库的根目录中，可供测试或发布。

如果您添加了需要翻译的新字符串，请务必使用如下命令重新生成 .pot 文件：

```
scons pot
```

## 如何翻译？

在 Windows 平台上：

*   下载 [poedit](https://poedit.net/)。您需要使用这个软件来翻译每个英文条目。
*   在此[下载](https://raw.githubusercontent.com/cartertemm/AI-content-describer/main/AIContentDescriber.pot)包含所有字符串的 .pot 文件。
*   在 poedit 程序中打开您刚刚下载的文件。在出现的窗口中点击“创建新翻译”，然后选择目标语言。
*   将源文本的内容逐条翻译成目标语言，然后将其粘贴到翻译编辑框中。如需额外帮助，可以随时右键点击列表项 -> 代码位置，然后向上移动一行阅读以“# Translators: ”开头的注释。这些注释也包含在 .pot 文件中。
*   完成后，点击“文件” -> “保存”或按 Ctrl+S，然后为新的 .mo 和 .po 文件选择一个保存位置。这些文件应通过电子邮件发送给我或通过 pull request 提交。
*   翻译 readme.md（即本文件）的内容，并一并附上！

## 贡献

我们非常感谢所有的贡献，并将予以致谢。
以下人员参与了本插件的开发工作。

*   [Mazen](https://github.com/mzanm)：Markdown 实现及其他代码贡献
*   [Kostenkov-2021](https://github.com/Kostenkov-2021)：俄语翻译
*   [Nidza07](https://github.com/nidza07)：塞尔维亚语翻译
*   [Heorhii Halas](nvda.translation.uk@gmail.com) 和 [George-br](https://github.com/George-br)：乌克兰语翻译
*   [Umut Korkmaz](umutkork@gmail.com)：土耳其语翻译
*   [Platinum_Hikari](urbain_onces.0r@icloud.com)：法语翻译
*   [Lukas](https://4sensegaming.cz)：捷克语翻译
*   [Michaela](https://technologiebezzraku.sk)：斯洛伐克语翻译
*   [Cary-rowen](https://github.com/cary-rowen)：简体中文翻译

遇到问题？请在 [GitHub Issue](https://github.com/cartertemm/AI-content-describer/issues) 中提交。

若有新功能提案？也请创建一个 Issue，我们可以讨论如何实现它。没有关联 Issue 的 pull request 也会被评审，但可能会花费大家更多时间，尤其是当我发现，你的解决方案和我设想的不一样，需要重做时。

我们热烈欢迎各种语言的翻译。能让更多人用上这项强大的技术，是再好不过的事了！

如果您没有 GitHub 账户，或不想使用这种方式，可以[给我发邮件](mailto:cartertemm@gmail.com) - cartertemm (at) gmail (dot) com。

感谢您的支持！