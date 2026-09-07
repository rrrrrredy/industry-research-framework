**可灵、Runway 与 Google Veo：商业内容制作竞争研究**

信息截止：2026 年 9 月 7 日。

对电商短视频和品牌营销团队，三者值得试用的理由不同：可灵适合列入商品图转视频、中文短叙事的试用名单；Runway 更值得有实拍底片、需要反复修改的团队评估为制作工作台；Veo 可优先试做带对白和环境声的创意草样，批量生产则须选择合适的程序化调用接口（API）、合同与配额。这是基于公开功能及条款的业务判断，尚无同一组商单实测支持“某家整体最好”。

三者的服务也发生重叠。Runway 同时销售自研模型、可灵和 Veo 等第三方模型；Google 的创作界面和模型 API 又是不同服务。企业实际购买的是“模型＋入口＋工作流＋合同”：同一个模型换入口，费用、功能和数据安排都可能改变。因此，模型画质偏好只能帮助缩小候选范围，不能直接决定采购。[Runway 套餐与模型](https://runway.com/pricing)、[API 模型计价](https://docs.dev.runwayml.com/guides/pricing/)。

普通客户截至截止日的公开访问条件如下。本研究核验了公开说明，未登录购买或发起生成；“有自助入口”不等于已经验证目标账户的权限、付款和网络。

| 服务入口 | 可核验的使用条件 | 仍不能据此认定的事项 |
|---|---|---|
| 可灵国际应用 | 有自助会员入口；7 月 28 日官方说明列出 Standard 的 1080p、商用及去品牌水印权益，较高套餐享新功能优先权 | 未核实每档账户的 3.0、Omni、4K 菜单；Ultra 仍有按情况邀请的测试权益。[会员说明](https://kling.ai/blog/kling-video-3-0-credit-cost-guide?tab=all) |
| 可灵境内及第三方 API | 境内可查到快手主体的 API 服务合同；fal 已公开 Kling 3.0 Pro 图生视频端点及密钥调用方法 | 境内具体模型开通、采购金额、并发配额未完整确认；fal 权限和报价不能代替可灵直销条件。[境内合同](https://market.aliyun.com/product/protocol.htm?code=cmgjllm00073513)、[fal 接口](https://fal.ai/models/fal-ai/kling-video/v3/pro/image-to-video/api) |
| Runway 网页及 API | Gen-4.5 网页要求 Standard 或以上；API 自助注册开发者账户、组织、密钥并单独充值，起充 10 美元 | 网页会员不等于 API 余额；企业数据和赔偿安排不能外推普通会员。[使用指南](https://help.runwayml.com/hc/en-us/articles/46974685288467-Creating-with-Gen-4-5)、[API 开通](https://docs.dev.runwayml.com/guides/setup/) |
| Google Flow | 要求年龄验证且满 18 岁、位于支持地区；使用 Google AI Plus／Pro／Ultra 或符合条件的 Workspace 权益 | Google AI 订阅销售地区不等于 Flow 可用地区；免费访问与积分页面说明不完全一致，免费额度不能作为计划产能。[访问条件](https://support.google.com/flow/answer/16353333?hl=en)、[积分说明](https://support.google.com/flow/answer/16526234?hl=en) |
| Google 开发者服务 | Gemini API 的 Veo 使用付费层，3.1 系列标为 Preview（预览）；Google Cloud 的 `veo-3.1-generate-001` 已 GA（正式发布），仍受项目、区域和配额约束 | 同名 Veo 不代表相同开放阶段；正式发布也不是无限容量承诺。[Gemini API](https://ai.google.dev/gemini-api/docs/pricing)、[Cloud 模型说明](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/veo/3-1-generate) |

两个容易改变购买决定的细节是：Flow 和 Gemini API 的支持地区均未列中国大陆，不能因为有中文界面就假设境内团队能用；Runway、fal 的境内账户与支付体验也未实测。另一个是 Gemini 应用当前帮助页已改为 Gemini Omni，购买“Gemini 视频功能”不能保证得到指定 Veo。可灵 2 月发布时的 Ultra 抢先体验同样只能证明首发状态，不能替代 9 月的套餐核验。[Flow 地区](https://support.google.com/flow/answer/16353544?hl=en)、[API 地区](https://ai.google.dev/gemini-api/docs/available-regions)、[Gemini 应用](https://support.google.com/gemini/answer/16126339?hl=en-gb)、[可灵首发公告](https://ir.kuaishou.com/zh-hans/news-releases/news-release-details/keling30xiliemoxingquanmianshangxian)。

成本须分三层看。订阅费购买入口和额度，例如 Runway Standard 月付 15 美元，年付折算每月 12 美元，均含每月 625 点；年付折算价对应全年承诺，不是按月购买价。可灵官方说明同时存在首购优惠和续费价，动态结算价未完整核验；Google One 本次读取未取得完整现金价，均不据旧报价补齐。应用积分则是各自的计量单位：Flow Pro 每月 1,000 点，非 Ultra 的 Veo Fast 每结果 20 点、Quality 100 点，而且一次请求可能产生多个结果。它们不能与 Runway 或可灵积分等额相除。[Runway 定价](https://runway.com/pricing)、[Flow 积分规则](https://support.google.com/flow/answer/16526234?hl=en)。

按量费用只有在公开参数相符时才比较。下面限定同一 fal 渠道、单张 16:9 起始图、1080p、8 秒、开启原生音频、无声音定制及续接，计算单个生成结果的美元标价，不含税、其他制作环节或折扣。

| 端点 | 每生成秒 | 8 秒标价 |
|---|---:|---:|
| Kling 3.0 Pro 图生视频 | $0.168 | $1.344 |
| Veo 3.1 图生视频 | $0.40 | $3.20 |

依据为 fal 的[可灵报价](https://fal.ai/models/fal-ai/kling-video/v3/pro/image-to-video)、[Pro 分辨率说明](https://fal.ai/learn/tools/seedance-2-0-vs-kling-3-0)、[Veo 报价](https://fal.ai/models/fal-ai/veo3.1/image-to-video)与[参数表](https://fal.ai/models/fal-ai/veo3.1/image-to-video/api)。这是公开收费维度一致的局部比较；帧率、码率和采用率未统一，不能当作同质量成片比较。Gen-4.5 API 基础生成价为每秒 12 点、每点 $0.01，即 $0.12／秒，但公开基础规格为 720p，未核实匹配此音画规格的完整费用，因此未纳入此表。Google 直连 Gemini API 另有 1080p Fast 每秒 $0.12、Lite $0.08，不能用上表 Standard 档概括 Veo 的成本范围。[Runway API 价格](https://docs.dev.runwayml.com/guides/pricing/)、[Google API 价格](https://ai.google.dev/gemini-api/docs/pricing)。

真正应管理的是采用秒成本：把同批任务的订阅分摊、API 按量、加购积分及人工审片后期费用相加，再除以最终采用秒数；订阅内已经包含的积分不要重复计费。在按量计费下，若采用秒数仅占付费生成秒数的 25%，纯生成成本就是每生成秒标价的四倍。这是测算假设，并非三家的实测通过率。服务器成功返回、商业验收通过和准时交付，是三个不同结果。

对电商业务，优先试的是“把已有商品素材变成更多可投放版本”，而不是一次生成完整广告。一个适合起步的任务，是用已经审核的商品主图制作数秒场景镜头，再由剪辑人员加入卖点、价格、字幕和行动提示。这样可以把测试问题收窄：同一商品在不同背景、光线和运动下，是否仍然准确，多少次生成能得到一个可用版本。转化率是否提升仍需真实投放实验，不能从视频更漂亮推导出来。

可灵值得列入试用名单的依据，是其 3.0 系列的图像参考、首尾帧、多镜头和最长 15 秒能力，以及包含中文在内的原生音画功能。先试主体运动较小的展示、场景氛围和短剧情草样，能直接检验这些控制是否降低制作时间。涉及旋转展示、手拿商品、开盖倒液等动作时，则应逐帧对照瓶形、数量、标识、材质和颜色；参考图能提供约束，但官方展示没有证明所有细节会保持不变。[可灵 3.0 使用指南](https://kling.ai/quickstart/klingai-video-3-model-user-guide)。

商品保真会推翻单纯按模型价格得出的选择。例如一瓶护肤品的标签、容量或泵头改变，即使镜头具有高级感，也不应计入采用秒数。产品实物、包装文字和价格层宜使用经过审核的原始素材，把生成能力放在背景、过场和非关键环境上；必要时采用合成制作。一次生成整条广告虽然减少拼接，却把商品、动作、文案、声音同时交给随机结果，任何一项失败都可能造成整段重做。数百个商品批量铺开之前，先测少量高频品类更能发现真实审片负担。

已有实拍底片的电商团队应同时测试 Runway。Aleph 2 的公开产品说明支持对最长 30 秒、1080p 既有视频进行修改，工作方式包括先编辑单帧、再把修改传播到视频。它的价值假设是减少换景、补拍和版本修改，而不是重新生成商品本身。Runway 8 月的更新还把图像与视频合成节点开放给全部客户，为原始商品素材和生成背景组合提供工具路径。试点应同时检查“要求修改的地方是否正确”和“其他地方是否被意外改变”；公开功能说明没有保证后者永不发生。[Aleph 2 编辑器](https://runway.com/product/ai-video-editor)、[Runway 更新记录](https://runway.com/changelog)。

Veo 更适合先试生活方式片段、对白节奏和带环境声的短场景，再决定是否扩展到商品主镜头。Fast、Lite 提供较低的公开生成费，但节省多少后期，取决于声音是否能直接采用。品牌名、促销规则和规格口播应按文字稿逐句验收，需要精确控制时可保留独立配音及字幕流程。跨语言制作尤其要核对所选端点：可灵官方发布列出多种语言，而 fal 的 Kling 3.0 Pro 音频参数目前只列中文和英文，并说明其他语言会转为英文。因此“模型支持某语言”不能代替“此采购入口支持此语言”。[可灵发布说明](https://ir.kuaishou.com/zh-hans/news-releases/news-release-details/keling30xiliemoxingquanmianshangxian)、[fal 音频参数](https://fal.ai/models/fal-ai/kling-video/v3/pro/image-to-video/api)。

据此，境内电商可先核验可灵境内付费合同及接口，再用商品图做小批试制；有稳定实拍资产和较多换景需求的团队，可把 Runway 编辑与合成加入对照；已有合适海外账户、需要音画一体的团队，可加测 Veo。若商品细节错误需要大量人工修复、必需语言在入口缺失，或截止日前无法拿到配额，这个顺序就应改变。需要精确演示机械结构、真实功效或连续复杂操作的素材，现有证据不足以支持直接交由任一家端到端生成。

品牌营销的购买逻辑有所不同。概念片、分镜预演、情绪板和社交传播素材，允许创作团队先选视觉方向，再处理商标、字幕和声音；一个镜头的单价未必是最大成本。此时应比较从创意评审到修改定稿的总工时：客户要求换季节、调服装、保留人物和机位时，能否修改现有镜头，还是必须重新生成并挑选。Runway 将模型、编辑、素材组织和交付格式放在同一平台，其工作台价值正来自这类反复修改。

具体采购时仍要区分套餐。Runway 8 月新增的素材批注标为企业功能；Gen-4.5／Aleph 2 的 ProRes、PNG 序列输出便于接入专业剪辑，但当前帮助页限定 Max、旧 Unlimited 和 Enterprise，其中 Gen-4.5 另加每秒 5 点。8 月发布记录曾写 Pro 及以上，采购应按当前具体帮助页核对，不能直接沿用较宽的发布口径。格式还须在生成时选择，事后更换需要重新生成。对频繁交接制作公司、存在统一品牌资产和多轮审批的项目，减少寻找素材及转码的时间，可能比生成单价差异更有价值，仍须在实际流程中验证。[Runway 更新记录](https://runway.com/changelog)、[当前格式与套餐规则](https://help.runwayml.com/hc/en-us/articles/54396547993491-Exporting-Videos-in-ProRes-and-PNG-Sequence-Formats)、[Gen-4.5 计费](https://help.runwayml.com/hc/en-us/articles/46974685288467-Creating-with-Gen-4-5)。

Flow 的品牌创作价值则在于把参考素材与镜头组织放入可视化流程，但 Veo 各档并非逐级完整升级：当前 3.1 Fast、Lite 支持参考素材（Ingredients／References），Quality 不支持；要续接已有 3.1 视频，需转用 Lite。也就是说，提高质量档位可能失去依赖的参考控制。Flow 的视频编辑还包含 Gemini Omni 的能力，不能统算成 Veo 的优势。必须持续使用品牌角色、指定服装或同一场景时，应先验证所需控制和所选档位能够共存，再比较画面。[Flow 功能矩阵](https://support.google.com/flow/answer/16352836?hl=en)。

高分辨率品牌主视觉需要单独验收。可灵官方已在 5 月公布其 3.0 系列原生 4K 的应用，Cloud Veo 3.1 文档也列出 4K，而 Gen-4.5 公开基础规格为 720p；这足以支持把不同输出路径纳入测试，不能证明任何一条路径已经达到电视广告或大屏交付要求。仍需检查实际账户、输出格式、颜色、压缩以及商品细节。可灵公布的制作团队案例可证明专业团队尝试使用，未披露重做次数和完整成本，不能作为普遍节约预算的证据。[可灵 4K 与制作案例](https://kling.ai/blog/kling-ai-introduces-native-4k-video-model)、[Cloud 输出规格](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/veo/3-1-generate)。

商用许可和素材保密是可能直接否决采购的条件。可灵国际通用条款第 4.6 条有商业使用许可要求，但付费补充协议优先适用，其第 3.1.2 条明确允许会员将输出商用，并限制用于竞争产品；不能只读通用条款便说“可灵付费内容也不能商用”。另一方面，国际通用条款的内容授权包含训练用途，而阿里云市场所载快手 API 合同第 5.1 条约定输入输出不用于训练，第 6.4 条不限制生成物商用。这些是不同合同，不能互相替代，也不能据其中一份为全部第三方转售服务背书。[国际通用条款](https://kling.ai/docs/user-policy)、[付费补充协议](https://kling.ai/docs/payment-policy)、[境内 API 合同](https://market.aliyun.com/product/protocol.htm?code=cmgjllm00073513)。

Runway 明确允许生成内容商用；企业第三方模型 FAQ 还说明，企业合同、数据处理和相应赔偿安排可覆盖平台内第三方模型，提供方不以客户内容训练。[Runway 商用](https://help.runwayml.com/hc/en-us/articles/21668707517587-Can-I-use-the-content-I-made-in-Runway-for-commercial-purposes)、[企业第三方政策](https://help.runwayml.com/hc/en-us/articles/51248305153683-Enterprise-FAQ-Third-party-Models-in-Runway)。

Google Flow 表示不主张原创输出所有权，但其内容改进和人工审核安排应单独核对。Google Cloud 则约定未经许可或指示不使用客户数据训练，且截至 7 月 20 日的赔偿服务清单包含通过 Cloud API 使用的正式版 Veo。赔偿仍受输入权利、未修改输出及商标等例外限制，不是所有营销素材的权利保险，也不能外推至消费版 Flow 或全部预览接口。[Flow 商用说明](https://support.google.com/flow/answer/16353333?hl=en)、[Flow 数据安排](https://support.google.com/flow/answer/17025472?hl=en)、[Cloud 条款](https://cloud.google.com/terms/service-terms)与[赔偿清单](https://cloud.google.com/terms/generative-ai-indemnified-services)。

因此，未发布新品、代言人或保密客户素材，可能使推荐从便捷会员入口转向条款合适的企业或 API 合同。商用授权不自动提供独占性，也不替用户清除商标、人物肖像、声音和输入素材的权利。品牌还应检查平台标识是否符合交付约定：Flow 输出含不可见 SynthID，印度、韩国、越南用户会自动附加可见水印；若交付要求与所选入口冲突，应换合适入口或调整制作方式。[Flow 水印与使用规则](https://support.google.com/flow/answer/16353333?hl=en)。

可靠性证据目前只支持有边界的结论。Artificial Analysis 通过同提示词下的匿名成对投票衡量偏好，并区分有声、无声榜单；它不能回答商品标识是否准确、客户是否批准、峰值时段能否准时返回。厂商演示和精选案例也缺少全部尝试的分母。Runway 自己披露 Gen-4.5 仍有因果错误和物体意外消失的问题；Flow 说明低质量音频可能导致生成失败并退还积分。前者意味着画面验收风险，后者说明退款不等于时间损失消失。[独立评测方法与榜单](https://artificialanalysis.ai/video/leaderboard/text-to-video)、[Runway 已知局限](https://runwayml.com/research/introducing-runway-gen-4.5)、[Flow 失败说明](https://support.google.com/flow/answer/16353333?hl=en)。

批量交付还受并发和排队影响。Runway API 的使用档位决定并发，超额任务可能进入等待；其旧 Unlimited 的保留期虽已公告延至 11 月 30 日，却不是新用户可购买的无限产能，宽松模式速度会变化且不覆盖 Veo。Flow 同样有限速，Cloud 配额也要按实际项目确认。本轮未获得三方同口径的可用率、峰值延迟和商业验收率，不能给出“哪家交付最稳”的排名。[Runway API 档位](https://docs.dev.runwayml.com/usage/tiers/)、[8 月 27 日 Unlimited 说明](https://help.runwayml.com/hc/en-us/articles/18053095835795-Unlimited-plan-details)。

建议以两组小型试点作采购依据：电商组使用已审核的真实商品素材，品牌组使用可公开参考素材和明确修改任务；让候选服务处理同一任务，限定尝试次数与人工时间。分别记录商品及人物保真、修改后不相关内容变化、采用秒数、实际账单、审片后期工时和最长等待，不能只保存最好看的结果。小样本的最长等待仅帮助排期，不冒充服务承诺；投放效果则另用受控实验衡量。

可以先启动的，是可替换的商品氛围镜头、已有底片的版本修改、品牌分镜和音画草样。扩大采购应以实测采用成本低于现有流程、目标账户与合同满足要求、高峰期排队仍能满足交期为条件。商品或角色一致性不达标，就保留实拍与合成；地区或商用条件不合适，就调整服务入口；无法保证活动截止日前完成，就保留已审核备用镜头。这些限制任何一项成立，都足以改变初步的模型偏好。

来源说明：除文中注明发布日期的材料外，动态产品、定价、地区和帮助页面均按 2026 年 9 月 7 日读取。官方资料用于确认公开功能和合同，fal 用于其自身渠道的费用与参数，独立榜单仅用于说明偏好评测的证据边界。
