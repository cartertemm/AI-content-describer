# AI 内容描述器

本插件旨在解决视觉内容的获取难题，能够为图像、用户界面控件及其他视觉上无法访问的内容提供详尽的描述。

我们利用了先进的 AI 模型和计算机视觉算法的多模态能力，旨在提供一流的内容描述，从而全面提升用户的独立性。关于所使用底层模型的更多信息，请参阅本文档的相应部分。

## 功能特性

*   描述焦点对象、导航对象、全屏幕，或使用内置摄像头拍摄照片。
*   描述已复制到剪贴板的图像，无论是电子邮件中的图片，还是 Windows 资源管理器中的图片文件路径。
*   将焦点对象、导航对象或全屏幕的图像复制到剪贴板，以便粘贴到其他应用中。
*   利用计算机视觉算法判断用户的脸部是否位于取景框中央（此功能无需付费 API）。
*   使用支持的模型，通过鼠标和键盘操作控制当前应用，以完成可能无法无障碍访问的任务。
*   默认免费使用，您也可以选择添加自己的 API 密钥以解锁更多模型。
*   支持多家服务提供商（OpenAI 的 GPT 和免费的 Pollinations 服务、Google 的 Gemini、Mistral Large 4、Anthropic 的 Claude、xAI 的 Grok、Moonshot AI 的 Kimi、通过 NVDA-CN 提供的 vivo BlueLM Vision、Datalab Chandra 2、Ollama、llama.cpp、LiteLLM Proxy 和 Seer）。
*   支持多种图像格式，包括 PNG (.png)、JPEG (.jpeg 和 .jpg)、WEBP (.webp) 和非动画 GIF (.gif)。
*   可选择缓存识别结果，以节省 API 调用额度。
*   对于高级用户，可以自定义提示词和 token 数量，以满足个性化需求。
*   支持在获得描述后，继续追问或附加其他图片。
*   支持 Markdown 渲染，方便您访问结构化信息（只需在设置中启用“在浏览模式中显示结果”，并在提示词末尾加入“以 Markdown 格式回答”等指令即可）。

## 应用场景

这个项目源于几个核心需求。

NVDA 本身就具备强大的光学字符识别（OCR）功能，这是一项颠覆性的技术。如果您需要从图片或 PDF 文档中提取文字，那么 NVDA 的自带功能是您的首选。

然而，OCR 只能分析那些*可能*包含文字的图像数据，却无法理解图像所传达的上下文、物体及其相互关系。互联网上充斥着大量此类图像：商标、肖像、表情包、图标、图表、示意图、柱状/折线图……应有尽有。这些图像无处不在，但屏幕阅读器用户通常无法理解它们。
过去，我们高度依赖内容创作者提供替代文本。尽管这依然必不可少，但一个不争的事实是：高质量的替代文本并不多见。

现在，有了 AI 的加持，几乎有无限可能。您可以：

*   在提供培训时，将桌面或特定窗口“可视化”，从而清晰地了解图标的布局。
*   当声音信息不足或没有声音时，获取游戏、虚拟机等的状态详情。
*   轻松弄清楚图表所展示的内容。
*   在 Zoom 或 Microsoft Teams 会议中，快速理解他人分享的屏幕截图或投屏画面。
*   让支持的模型帮您操作无法无障碍访问的应用，或在前台窗口中完成任务。
*   在录制视频或参加在线会议前，确保自己的面部正对摄像头且背景环境适宜。

## 支持的模型

*   [Pollinations](https://pollinations.ai/)：Pollinations.AI 团队慷慨地为本项目免费提供 GPT4 访问权限，因此用户无需提供自己的 API 密钥。请注意，该服务不时会出现问题，我们强烈建议您使用自己的密钥，以充分发挥本插件的全部功能。
*   [OpenAI GPT 模型](https://platform.openai.com/docs/models)：需要 OpenAI API 密钥。包括 GPT-5.4 系列（5.4 和 5.4 mini）、GPT-5.5 系列（5.5 和 5.5 pro）、GPT-6 系列（6 Astra 和 6 Luna）以及 GPT-6.1 系列（6.1 Sol 和 6.1 Terra）。GPT-5.4、GPT-5.5、GPT-6 和 GPT-6.1 系列均支持计算机控制。
*   [Google Gemini](https://deepmind.google/models/gemini/)，包括 2.5 Flash、2.5 Flash-Lite、2.5 Pro、3.1 Flash-Lite、3.1 Pro Preview、3.5 Flash、3.5 Flash-Lite、3.6 Flash、3.7 Flash、3.8 Flash、4 Hydrogen、4 Argon 和 4 Carbon 模型。
*   [Anthropic Claude](https://docs.anthropic.com/claude/docs/vision)，包括 Claude 4.5（Sonnet、Opus）、4.6（Sonnet、Opus）、4.7 Opus、4.8 Opus、5（Sonnet、Opus、Fable）、5.1 Fable、5.2 Fable 和 5.5（Haiku、Sonnet、Opus）。以上模型均支持计算机控制。
*   [Mistral Large 4](https://docs.mistral.ai/models/mistral-large-4-0)
*   [xAI Grok](https://docs.x.ai/developers/models)，包括 Grok 4.20（非推理版）、4.3、4.5、4.6 和 4.7。
*   [Kimi](https://platform.kimi.ai/docs/guide/use-kimi-vision-model)，Moonshot AI 的多模态模型，包括 Kimi K3 和 Kimi K2.6。
*   vivo BlueLM Vision：vivo 推出的多模态模型，通过免费的 NVDA-CN 账号使用。请参阅下文的设置部分。
*   [Datalab Chandra 2](https://github.com/datalab-to/chandra)：Datalab 推出的先进视觉与 OCR 模型，擅长处理复杂的文档版式、表格、表单、手写内容、图表和数学公式。支持 Datalab 的托管云 API（位于 [datalab.to](https://www.datalab.to)），也支持通过 vLLM 自行部署（使用 `chandra_vllm` 或兼容 OpenAI 的 `/v1` 端点）。
*   [Ollama (不稳定)](https://ollama.com/)
*   [llama.cpp (极不稳定，速度取决于硬件，经测试可与 llava-v1.5/1.6、BakLLaVA、Obsidian 和 MobileVLM 1.7B/3B 模型配合使用)](https://github.com/ggerganov/llama.cpp)
*   [LiteLLM Proxy](https://docs.litellm.ai/docs/proxy/quick_start)：通过统一的代理服务器访问多个 AI 模型。需要 LiteLLM 代理服务器的 URL，根据代理配置，可能还需要 API 密钥。在模型配置对话框中显示为“LiteLLM Proxy”。支持动态选择模型和追问。兼容所有格式（PNG、JPEG、WEBP、GIF）。
*   [Seer](https://github.com/recursia-lab/Seer)：通过 Seer 守护进程在本地运行 PaliGemma2。无需 API 密钥，也无需联网。注意：这是一个仅生成图片说明的模型，不支持提示词和追问。

请按照以下说明设置，以确保这些模型能正常工作。

## 快速入门

请从[此链接](https://github.com/cartertemm/AI-content-describer/releases/latest/)下载插件的最新版本。在安装了 NVDA 的电脑上双击该文件，并按照提示完成安装。

NVDA 首次加载本插件启动时，会询问是否下载一些额外的库。详情请参阅本文档的`依赖项`部分。

自 2025.06.05 版本起，得益于 PollinationsAI 社区的大力支持，GPT4 模型可以免费使用。

如果您有能力且希望探索其他模型，可以随时使用自己的 API 密钥，这样可以减少对其服务器的请求。如果不需要，请直接跳至本文档的`用法`部分。

请按照以下说明，从支持的提供商处获取 API 密钥。

### 我应该使用哪个模型？

我们过去会推荐最便宜和质量最高的选择，但这一领域变化太快，我们已无法及时更新这些推荐。

简而言之，目前大多数先进模型的准确性都已足以应对大部分日常使用场景，因此选择您熟悉的提供商即可。

大多数人希望在准确性和成本之间取得平衡。[LLM arena 排行榜](https://lmarena.ai/leaderboard)（特别是其中的视觉类别）衡量模型的准确性，而 [LLM 价格计算器](https://www.llm-prices.com/)列出了各模型的价格。

如果您想使用计算机控制功能，请选择上文列出的受支持的 OpenAI 或 Anthropic 模型。免费的 Pollinations 服务适合用于图像描述，但不支持计算机控制。

### 获取 OpenAI 的 API 密钥：

1.  前往 [OpenAI 的 API 密钥 页面](https://platform.openai.com/account/api-keys)。
2.  如果您还没有账户，请先注册一个；如果已有账户，请直接登录。
3.  在 API 密钥 页面，点击“创建新密钥”，然后将其复制到剪贴板。
4.  为您的账户充值至少 1 美元。
5.  打开 NVDA 设置对话框，找到“AI 内容描述器”类别，选择“管理模型(M)”。选择任意一个 OpenAI 模型（例如“GPT-6.1 Sol”）作为提供商，接着按 Tab 键到 API 密钥编辑框，粘贴您刚刚生成的密钥。

在撰写本文时，OpenAI 会向新注册的开发者账户赠送为期三个月的免费额度，该额度到期后将作废。之后，您需要自行购买额度。正常使用情况下，每月的费用一般不会超过 5 美元。作为参考，本插件最初版本的开发花费还不到 1 美元。您可以随时登录 OpenAI 账户，点击“用量”查询您的额度使用情况。

### 获取 Google 的 API 密钥

1.  首先，您需要前往 [Google Cloud Console](https://console.cloud.google.com/projectcreate) 创建一个 Google Workspace 项目。请确保您已登录您的 Google 账户。
2.  创建一个长度在 4 到 30 个字符之间的名称，例如“Gemini”或“NVDA 插件”。
3.  前往 [Google AI Studio API 密钥页面](https://makersuite.google.com/app/apikey)。
4.  点击“创建 API 密钥”。
5.  打开 NVDA 设置对话框，找到“AI 内容描述器”类别，选择“管理模型(M)”。在提供商列表中选择“Google Gemini”，接着按 Tab 键到 API 密钥编辑框，粘贴您刚刚生成的密钥。

### 获取 Anthropic 的 API 密钥

1.  登录 [Anthropic 控制台](https://console.anthropic.com/login)。
2.  点击您的个人资料 -> API 密钥。
3.  点击“创建密钥”。
4.  为密钥输入一个名称（如“AIContentDescriber”），然后点击“创建密钥”并复制显示的值。请将此值粘贴到 NVDA 设置对话框中“AI 内容描述器”类别下的“管理模型” -> 任意 Claude 模型（例如“Claude 5 Sonnet”）的 API 密钥编辑框中。
5.  如果您尚未充值，请在 [Anthropic 套餐页面](https://console.anthropic.com/settings/plans)至少购买 5 美元的额度。

### 获取 Mistral 的 API 密钥

1.  前往 [MistralAI 登录页面](https://auth.mistral.ai/ui/login)，登录或创建一个 MistralAI 账户。
2.  如果您是首次创建或登录账户，请按提示添加一个工作区，提供名称并接受条款和条件。
3.  登录后，从菜单中选择“API 密钥”。
4.  点击“创建新密钥”，并将其复制到剪贴板。请将此值粘贴到 NVDA 设置对话框中“AI 内容描述器”类别下的“管理模型” -> “Mistral Large 4”的 API 密钥编辑框中。
5.  如果需要，请为账户充值。

### 获取 Kimi（Moonshot AI）的 API 密钥

1.  在 [Kimi 开发者平台](https://platform.kimi.ai/)登录或创建一个账户。
2.  登录后，打开控制台中的 API 密钥部分，创建一个新密钥。
3.  将密钥复制到剪贴板。请将此值粘贴到 NVDA 设置对话框中“AI 内容描述器”类别下的“管理模型” -> “Kimi K3”（或其他 Kimi 模型）的 API 密钥编辑框中。
4.  如果需要，请为账户充值。


### 注册 NVDA-CN 账户，使用 VIVO 蓝心大模型

该服务由 VIVO (vivo.com.cn) 与 NVDA 中文社区 (NVDACN) 合作免费提供。它具备高质量的多模态识别能力，推荐所有用户使用，尤其是刚开始使用本插件的用户。

要使用此模型，您只需要一个免费的 NVDA-CN 账号。

1.  **注册账号**：访问 NVDA-CN 注册页面：[https://nvdacn.com/admin/register.php](https://nvdacn.com/admin/register.php)。
    *   **注意**：该页面目前为中文。非中文用户可以使用浏览器自带的翻译功能来填写表单。
    *   您需要提供用户名、密码和一个有效的电子邮箱地址。由于该网站尚未实现自助密码找回功能，请务必妥善保管您的密码。
2.  **验证您的邮箱**：检查您的收件箱，找到验证邮件并点击其中的链接以激活您的账号。
3.  **配置插件**：
    *   打开 NVDA 设置对话框，并找到“AI 内容描述器”分类。
    *   选择“管理模型”按钮。
    *   在提供商列表中，选择“vivo BlueLM Vision (NVDA-CN)”。
    *   在相应的输入框中，填入您的 NVDA-CN 用户名和密码。
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
7.  前往“AI 内容描述器”设置 -> “管理模型” -> “Ollama”。在模型名称编辑框中，输入此值，然后点击“确定” -> “确定”。这样就设置好了！在模型子菜单中切换到 Ollama，稍等片刻即可正常使用。

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
6.  打开 NVDA 设置对话框，找到“AI 内容描述器”类别，选择“管理模型(M)”。在提供商列表中选择“llama.cpp”，接着按 Tab 键到“基础 URL”编辑框，然后输入控制台中显示的端点（默认为“http://localhost:8080”）。
7.  或者，您可以省略其中一些步骤，在配置比您本地机器更高的远程服务器上运行 llama.cpp，然后输入该服务器的端点地址。

### 设置 LiteLLM Proxy

LiteLLM Proxy 提供统一的接口，让您通过单个端点访问多个 AI 模型，从而简化模型管理，并可轻松在不同提供商之间切换。

1.  按照 [LiteLLM 代理文档](https://docs.litellm.ai/docs/proxy/quick_start)搭建 LiteLLM 代理服务器。您可以在本地运行代理，也可以使用远程服务器。
2.  如果在本地运行，最快的入门方式是：
```
pip install 'litellm[proxy]'
litellm --model gpt-4o
```
这会在 `http://localhost:4000` 启动一个代理服务器，并将请求转发给 OpenAI 的 GPT-4o。
3.  在生产环境中，请创建一个 `config.yaml` 文件来配置多个模型和身份验证。详情请参阅 [LiteLLM 配置指南](https://docs.litellm.ai/docs/proxy/configs)。
4.  打开 NVDA 设置对话框，找到“AI 内容描述器”类别，选择“管理模型(M)”，然后在提供商列表中选择“LiteLLM Proxy”。
5.  在“基础 URL”编辑框中输入您的代理服务器 URL（例如，本地代理为“http://localhost:4000”，否则填写您的远程服务器 URL）。
6.  如果您的代理需要身份验证，请在 API 密钥编辑框中输入 API 密钥；否则请留空。
7.  点击“列出模型”按钮，从代理获取可用模型，然后从下拉列表中选择您要使用的模型。
8.  根据需要调整提示词、最大 token 数和超时等其他设置，然后点击“确定”。

注意：可用的模型及其功能取决于您的 LiteLLM 代理配置。请确保代理中配置了具备视觉能力的模型，以便进行图像描述。

### 设置 Seer

Seer 在您自己的计算机上运行 PaliGemma2，无需 API 密钥或云端连接。请注意，这是一个仅生成图片说明的模型，不支持提示词和追问。

1.  安装 [Seer 守护进程](https://github.com/recursia-lab/Seer)。它为 Windows (.bat) 和 Linux/macOS (.sh) 提供了一键安装脚本。
2.  打开 NVDA 设置对话框，找到“AI 内容描述器”类别，选择“管理模型(M)”，然后选择“Seer (requires installation)”。
3.  基础 URL 默认为 `http://127.0.0.1:11435`。除非您更改了守护进程的端口，否则请保持不变。
4.  点击“确定”。在请求描述之前，守护进程必须处于运行状态。

### 设置 Datalab Chandra 2

Datalab Chandra 2 是一款先进的文档智能与 OCR 模型，擅长处理复杂版式、表格、表单、手写内容、图表和数学公式。您可以通过 Datalab 的托管云 API、本地部署的容器或自行托管的 vLLM 实例来使用它。

#### 方案 A：使用 Datalab 云 API（推荐）
1.  在 [datalab.to](https://www.datalab.to) 注册账户。新账户可获得免费试用额度。
2.  访问 [API 密钥页面](https://www.datalab.to/app/keys)并生成一个 API 密钥。
3.  打开 NVDA 设置对话框，找到“AI 内容描述器”类别，选择“管理模型(M)”，然后选择“Datalab Chandra 2”。
4.  在“API 密钥”编辑框中输入您的 API 密钥。
5.  基础 URL 默认为 `https://www.datalab.to/api/v1/convert`。您可以根据需要调整处理模式（`fast`、`balanced` 或 `accurate`）。
6.  点击“确定”。该模型随后将出现在“AI 内容描述器”菜单中。

#### 方案 B：使用 vLLM 自行托管
1.  使用 Chandra 2 启动本地 vLLM 服务器（例如使用 `chandra_vllm` 或 `vllm serve datalab-to/chandra-ocr-2`）。服务器默认运行在 `http://localhost:8000/v1`。
2.  在 NVDA 设置 -> “AI 内容描述器” -> “管理模型” -> “Datalab Chandra 2”中，将本地端点输入“基础 URL”编辑框（例如 `http://localhost:8000/v1`）。
3.  如果模型名称与默认值（`datalab-to/chandra-ocr-2`）不同，请设置模型名称。API 密钥留空（如果启用了身份验证，请提供 bearer 令牌），然后点击“确定”。

## 用法

默认分配了六个快捷键：

*   NVDA+shift+i：弹出一个菜单，询问是描述当前焦点、导航对象、物理摄像头、全屏幕，还是使用 AI 控制计算机。
*   NVDA+shift+u：使用 AI 描述当前导航对象的内容。
*   NVDA+shift+y：使用 AI 描述剪贴板中的图像（或图像文件路径）。
*   NVDA+shift+j：描述您的面部在所选摄像头画面中的位置。如果您连接了多个摄像头，请前往“AI 内容描述器”菜单（NVDA+shift+i），并在“面部检测”子菜单的“选择摄像头”选项中选择您想使用的摄像头。
*   NVDA+alt+c：打开 AI 对话框，以进行追问。
*   NVDA+control+shift+p：暂停或恢复正在进行的计算机控制会话。

有七项功能未分配默认快捷键：

*   使用 AI 描述当前焦点的内容。
*   截取屏幕截图，然后使用 AI 进行描述。
*   使用所选摄像头拍摄照片，然后使用 AI 进行描述。
*   取消正在进行的计算机控制会话。
*   截取当前焦点对象的图像并复制到剪贴板。
*   截取当前导航对象的图像并复制到剪贴板。
*   截取全屏幕的图像并复制到剪贴板。

这三条复制命令也位于 NVDA+shift+i 菜单的“复制图像到剪贴板”子菜单中。它们不会向任何 AI 服务发送内容。您可以用它们将截图粘贴到 Be My AI 或本插件不支持的其他应用中。复制操作会覆盖剪贴板中原有的内容。

您可以随时在“按键与手势”对话框中自定义这些快捷键。

### 对描述进行追问

有时候，AI 返回的描述可能不够充分。也许是图像质量差、不完整，或包含不感兴趣的细节。或者您想聚焦于某个特定部分，亦或在不丢失上下文的情况下拍一张更清晰的照片。
在收到描述后，您可以按下 NVDA+alt+c，或从“AI 内容描述器”上下文菜单（NVDA+shift+i）中选择“对先前的描述进行追问”。默认情况下，焦点会设置在消息编辑框。
要添加其他图片，只需保持对话窗口打开，并照常使用本插件。当拍摄一张图片（无论是来自摄像头、系统控件、截图等）时，系统会询问您是将其附加到当前会话，还是开始一个新会话。

### 计算机控制

计算机控制功能可以让“AI 内容描述器”在您描述任务后，使用鼠标和键盘控制当前应用。这有助于完成那些难以手动操作或无法无障碍访问的任务。

由于此功能会让 AI 模型控制您的计算机，请谨慎使用。插件会在开始前征求您的同意，实时报告正在执行的操作，并在执行可能有风险的操作前询问您。您需要对它的行为负责，因此请密切关注会话过程，避免将其用于敏感或难以撤销的工作。

您可以随时按 `NVDA+Control+Shift+P` 暂停或恢复计算机控制。暂停期间，插件不会继续执行下一步操作，直到您恢复为止。

插件会用提示音表示控制状态。高音表示模型正在接管或恢复控制。低音表示控制已暂停，可能是您手动暂停，也可能是模型需要您输入信息。短促的低音错误提示音表示会话因 API 错误而停止。

控制会话进行期间，模型会在发送输入前播报它将要执行的操作。在播报结束之前不会执行任何操作，除非您按 `Control` 键打断播报，让操作提前执行。

如果模型不确定如何完成某个操作、需要更多信息，或以其他方式将控制权交还给您，会话将暂停，“计算机控制”对话框会切换到前台。您可以在其中输入后续消息以继续对话，或关闭对话框以结束会话。

此功能仅适用于提供计算机控制工具的模型：GPT-5.4、GPT-5.4 mini、GPT-5.5、GPT-5.5 pro、GPT-6 Astra、GPT-6.1 Sol、GPT-6.1 Terra、GPT-6 Luna、Claude 4.5 Sonnet、Claude 4.5 Opus、Claude 4.6 Sonnet、Claude 4.6 Opus、Claude 4.7 Opus、Claude 4.8 Opus、Claude 5 Sonnet、Claude 5 Opus、Claude 5 Fable、Claude 5.1 Fable、Claude 5.2 Fable、Claude 5.5 Haiku、Claude 5.5 Sonnet 和 Claude 5.5 Opus。其他模型可以描述图像，但无法提供计算机控制所需的结构化鼠标和键盘操作。

使用计算机控制的步骤：

1.  配置并选择一个受支持的模型。
2.  打开您希望模型操作的应用或窗口。
3.  按 `NVDA+shift+i`，然后选择“控制计算机...”。
4.  输入您要执行的任务，然后点击“发送”。
5.  查看同意提示。如果您允许启动会话，请密切关注其操作，并对任何有风险操作的提示进行批准或取消。

注意：此功能目前应视为测试版功能，我们正在积极改进，使其更加可靠和安全。

## 依赖项

本插件所需的部分库体积过大，无法包含在插件包中。因此，在安装本插件后首次启动 NVDA 时，系统会询问您是否下载这些库。选择“是”，等待下载完成，NVDA 将自动重启。

下载内容是一个约 35 到 70 MB 的 zip 文件，具体大小取决于您的 NVDA 版本。它来自本仓库的 [libs-release](https://github.com/cartertemm/AI-content-describer/releases/tag/libs-release) 页面。如果无法访问 GitHub，插件会提供尝试从 NVDA 中文社区提供的镜像下载的选项。

该 zip 文件包含：

*   [NumPy](https://numpy.org/)：数组运算库，OpenCV 依赖它。
*   [OpenCV](https://opencv.org/) (`cv2`)：在摄像头图像中识别您的面部，用于面部检测功能。
*   [Pillow](https://python-pillow.org/) (`PIL`)：截取屏幕截图，并将其转换为 AI 模型可以读取的图像。
*   [Markdown](https://python-markdown.github.io/)：以带格式的方式显示描述，例如标题、列表和表格。
*   [pygrabber](https://github.com/andreaschiavinato/python_grabber)：列出您计算机上的摄像头。
*   NVDA 未包含的几个 Python 标准库模块（`html`、`xml`、`pathlib`、`secrets` 和 `_markupbase`）。上述库需要用到它们。

这些文件存放在名为 `aic-py-` 加上 NVDA 的 Python 版本号的文件夹中，例如 `aic-py-3.13`。该文件夹位于您的 NVDA 用户配置文件夹中，通常为 `%APPDATA%\nvda`。每个 Python 版本都有单独的文件夹，因此当新的 NVDA 版本更换了 Python 版本时，插件会重新下载这些库。卸载插件时，会删除 NVDA 当前 Python 版本对应的文件夹。

如果下载失败，您可以手动安装这些库。从 libs-release 页面下载 `aic-py-3.13.zip`（或与您的 NVDA Python 版本对应的文件），将其解压到您的 NVDA 用户配置文件夹中，然后重启 NVDA。

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

*   [Cary Rowen](https://github.com/cary-rowen)：通过依赖项镜像让中国用户能够使用本插件，并添加了对 vivo 蓝心大模型的支持
*   [Mazen](https://github.com/mzanm)：Markdown 实现及其他代码贡献
*   [Kostenkov-2021](https://github.com/Kostenkov-2021)：俄语翻译
*   [Nidza07](https://github.com/nidza07)：塞尔维亚语翻译
*   [Heorhii Halas](nvda.translation.uk@gmail.com) 和 [George-br](https://github.com/George-br)：乌克兰语翻译
*   [Umut Korkmaz](umutkork@gmail.com)：土耳其语翻译
*   [Platinum_Hikari](urbain_onces.0r@icloud.com)：法语翻译
*   [Lukas](https://4sensegaming.cz)：捷克语翻译
*   [Michaela](https://technologiebezzraku.sk)：斯洛伐克语翻译
*   [loginerror](https://github.com/theloginerror)：波兰语翻译

遇到问题？请在 [GitHub Issue](https://github.com/cartertemm/AI-content-describer/issues) 中提交。

若有新功能提案？也请创建一个 Issue，我们可以讨论如何实现它。没有关联 Issue 的 pull request 也会被评审，但可能会花费大家更多时间，尤其是当我发现，你的解决方案和我设想的不一样，需要重做时。

我们热烈欢迎各种语言的翻译。能让更多人用上这项强大的技术，是再好不过的事了！

如果您没有 GitHub 账户，或不想使用这种方式，可以[给我发邮件](mailto:carter@ctemm.me) - carter (at) ctemm (dot) me。

感谢您的支持！
