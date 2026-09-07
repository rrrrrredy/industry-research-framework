**可灵、Runway 与 Google Veo：商业内容制作竞争格局**

信息截止：2026 年 9 月 7 日。本文依据公开产品文档、价目、合同及独立评测核验，未购买服务或进行生成实测。“已开放”指官方明确提供的访问路径，不代表本企业账号已经通过支付、地域或模型权限验证。

**业务判断：电商先试可灵，品牌制作优先比较 Runway 与 Veo，但采购入口会改变结论。**

以已有商品图制作中文社媒短片，可灵适合列为第一批候选；已有剪辑团队、经常需要改镜头和多人审稿，Runway 更值得测试；面向海外、重视声音与画面共同生成，或已有 Google Cloud 采购体系，Veo 值得进入候选。这是根据功能和交付环节作出的适配判断，尚无证据证明某一家能全面提高商品转化率。

三者的竞争已同时发生在模型、制作平台和企业采购层。可灵侧重把主体参考、多镜头、中文及原生音频放入生成流程；Runway 将自有模型、第三方模型、编辑和协作整合在一个制作环境；Veo 通过 Flow、开发者 API 和 Cloud 服务接触不同客户。Runway 平台也提供可灵和 Veo，因此“选哪个模型”与“向谁采购”必须分别决定。[可灵 3.0 指南](https://kling.ai/quickstart/klingai-video-3-model-user-guide)、[Runway 更新记录](https://runway.com/changelog)、[Veo 开发文档](https://ai.google.dev/gemini-api/docs/veo)

可灵已有明确的商业需求证据：快手 8 月 19 日财报披露，其二季度收入超过人民币 8.5 亿元，并披露原生 4K 和 3.0 Turbo 上线。这说明产品已有付费规模；本次未取得另外两家同口径的视频服务收入，不能据此排列市场份额。品牌奖项和厂商精选案例同样不能回答普通团队需要重试多少次。[快手二季度财报](https://ir.kuaishou.com/news-releases/news-release-details/kuaishou-technology-announces-second-quarter-and-interim-2026)

**截至截止日，普通客户实际从哪里进入**

| 服务入口 | 文档确认的访问条件 | 仍影响采购的限制 |
|---|---|---|
| 可灵国内站、国际站 | 官方[国内入口与国际站](https://ir.kuaishou.com/news-releases/news-release-details/kuaishou-launches-full-beta-testing-kling-ai-global-users-0)均存在；3.0 有操作指南，付费权益按购买时套餐确定 | 国内外合同、价格和权益不可互套；4K、Turbo 的发布和标价，不能证明每档会员均有权限 |
| 可灵 API、企业服务 | 有独立开发者入口、模型价目和资源包；[企业服务](https://kling.ai/dev/enterprise-membership)走咨询、企业验证等流程 | 最低现金门槛、具体包有效期、模型权限和并发需在开通时确认；部分企业能力标为有限内测 |
| Runway 网页 | [Gen-4.5](https://help.runwayml.com/hc/en-us/articles/46974685288467-Creating-with-Gen-4-5)明确面向 Standard 及以上；9 月 4 日新增可自助购买的 Team 方案 | 免费账户仅能访问部分模型；专业导出按具体套餐，不能用免费试用推定全部能力 |
| Runway API | 开发者可自助注册、充值；[网页与 API 积分独立](https://help.runwayml.com/hc/en-us/articles/21668552945171-Runway-API-FAQs) | 配额按组织和模型管理；本次未验证中国大陆主体的支付与网络条件 |
| Google Flow | [入门要求](https://support.google.com/flow/answer/16353333?hl=en)：18 岁并完成验证、位于支持地区；Plus/Pro/Ultra 及部分 Workspace 有对应权限 | [积分页](https://support.google.com/flow/answer/16526234?hl=en)另列每日 50 免费积分，但入门页仍列订阅要求；免费资格以账户为准，高峰免费生成可能暂停 |
| Gemini Developer API | 支持地区的合资格开发者账户、API 密钥与付费层；Veo 无免费 API 档 | [3.1 系列](https://ai.google.dev/gemini-api/docs/veo)在该入口仍标 Preview，受账户配额约束 |
| Google Cloud 的 Veo | Cloud 项目、计费及权限；[3.1 Standard/Fast 的指定 001 型号](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/veo/3-1-generate)为 GA，Lite 为 Preview | 所核型号文档列 us-central1；区域、配额及功能按型号核对，不能视为所有地区和功能均正式开放 |
| Gemini 应用 | 当前[视频帮助页](https://support.google.com/gemini/answer/16126339?hl=en)指向 Gemini Omni | 未证实普通用户能指定 Veo；不将“可生成视频”列为已确认的 Veo 入口 |

地域是前置条件。[Flow 名单](https://support.google.com/flow/answer/16353544?hl=en)和[Gemini API 名单](https://ai.google.dev/gemini-api/docs/available-regions)均未列中国大陆。仅在大陆运营、没有符合要求的海外主体与团队时，不能把这两个入口设为默认生产路线；也不能从香港支持 Flow 推导香港支持全部 Google API。Cloud 的部署区域与客户所在地是不同问题，须分别核验。

**成本：能比较的是明确交付参数下的生成账单**

月费购买的是一组权益，积分是各平台内部计量单位，API 则可能有固定兑换率。Runway Standard 月付 15 美元，年付等效每月 12 美元、含 625 积分；年付价格需要年度承诺，网页积分也不能拿到 API 使用。Flow Pro 每月额外提供 1,000 积分，非 Ultra 用户生成 Fast 每条 20 积分、Quality 每条 100 积分；一次请求可能产出多条并分别扣费，未用月度积分不结转。这些数字只能用于各自套餐预算。[Runway 订阅价目](https://runway.com/pricing)、[Flow 扣费规则](https://support.google.com/flow/answer/16526234?hl=en)

本次可确认的一组同口径例子，是通过两个渠道调用 **Veo 3.1 Fast：纯文生视频、8 秒、1920×1080、16:9、有声、不加参考素材或增强工序，每次一个输出**：

| 采购渠道 | 公开计费 | 一条 8 秒 | 十条、合计 80 秒 |
|---|---|---:|---:|
| Gemini Developer API | 1080p 有声 0.12 美元/秒 | 0.96 美元 | 9.60 美元 |
| Runway API | 有声 15 API 积分/秒，1 积分＝0.01 美元 | 1.20 美元 | 12.00 美元 |

这里比较的是同一命名模型及上述公开输出规格的渠道标价，不保证底层版本、排队速度和结果质量完全一致；不含税、重试、剪辑、配音修改或企业支持。参数和计算可由[Google 价目](https://ai.google.dev/gemini-api/docs/pricing#veo-3.1)、[Runway API 价目](https://docs.dev.runwayml.com/guides/pricing/)及其[官方接口参数](https://github.com/runwayml/sdk-node/blob/main/src/resources/text-to-video.ts)复核。

另两组原始报价应单列：可灵官方国际 API 价目中，3.0 的 1080p 无声为 0.112 美元/秒，有声且未指定音色为 0.168 美元/秒，资源包最低支出与折扣尚未闭合；Runway Gen-4.5 API 为 12 积分/秒，即 0.12 美元/秒，基础输出为 720p，专业格式另计。它们不能与上表直接组成“同质量成片”的价格排名。[可灵 API 价目](https://kling.ai/dev/pricing)、[Runway 模型规格](https://docs.dev.runwayml.com/guides/models/)

采购应记录“每条验收通过素材的总成本”：包含全部重试的订阅或用量账单，加上人工筛选、商品修正、声音和后期费用，除以最终通过数量。重试用量已经进入账单时不重复加计。已成功生成但商品错误的片段仍可能收费；失败退款也不会补回交期。单价稍高但少一次客户返工的路线，可能更便宜；目前没有统一实测支持三者的最终成本排序。

例如，上表 Google 路线十条视频的生成费为 9.60 美元；假设只有两条能验收，每条合格素材仅生成环节就变为 4.80 美元，再加人工。这只是敏感性示例，不是实测合格率。资源包还应计入到期浪费，低产量团队应比较整个结算周期的现金支出，不能默认所有赠送额度都会有效消耗。

**电商短视频：围绕真实商品图做试点**

可灵 3.0 提供主体参考、首尾帧、3—15 秒、多镜头和包括中文在内的原生音频控制。对已拍好产品图、需要持续制作开场钩子、场景变体和中文展示片的团队，这些能力值得首先验证。建议保留真实商品图作为主体依据，价格、规格和关键包装文字由后期精确叠加；参考功能不能自动证明商标、配件数量和商品结构逐帧正确。[可灵操作指南](https://kling.ai/quickstart/klingai-video-3-model-user-guide)

Runway 的电商价值更偏向重复制作流程：从商品素材到生成、替换、后期和团队复核。开发者文档已有 Product Ad、Product Swap、Product UGC 等配方，但其计费是完整流程价，不能套用 Gen-4.5 单模型每秒价。若团队每天要更换商品、复用模板并接入内部素材系统，它值得与可灵同时测试；若只有一名运营偶尔出片，流程搭建未必划算。[Runway 配方与计费](https://docs.dev.runwayml.com/guides/pricing/)

Veo 可试海外生活方式广告、氛围镜头和依赖环境声的产品短片，但中文口播不能凭样片直接承诺：Gemini API 文档称英语充分支持，其他语言尚未经评估。Flow 内也有实际功能取舍：Quality 不支持 Ingredients 参考组合；延长 Veo 3.1 的 8 秒视频须切到 Lite。转用 Gemini API 时，延长又由 Standard/Fast 提供且限 720p。模型名称相似，不能假设流程可以直接搬家。[Flow 功能表](https://support.google.com/flow/answer/16352836?hl=en)、[Veo API 限制](https://ai.google.dev/gemini-api/docs/veo)

试点顺序可从背景氛围、节日场景和已公开商品的短镜头开始，再扩展到展示动作。涉及使用功效、尺寸对比和安装步骤的内容，应由真实演示支撑；生成画面若改变商品事实，即便更吸引人也应淘汰。进入付费投放后，还需在相同商品、优惠和受众条件下比较素材效果，制作成本下降与转化改善应分别验证。

**品牌营销：修改能力、保密与权利决定采购层级**

Runway 适合先试概念提案、已有实拍素材的视觉变化和多轮审稿。Team 支持共享项目、评论与积分；Aleph 提供视频编辑，Ruby 已提供 SDR 转 HDR，专业导出也进入产品和接口。其价值要看客户提出“保留主体、只改背景或灯光”后，还需重做多少内容。具有这些工具，不等于修改能一次成功。[Runway 更新记录](https://runway.com/changelog)、[模型与输出格式](https://docs.dev.runwayml.com/guides/models/)

Veo 适合测试声音与画面一起设计的品牌镜头；已有 Cloud 采购、权限和数据管理体系的企业，可优先评估对应 GA 接口。可灵则可竞争中文叙事、多镜头提案和高频品牌社媒素材。对于精确代言人形象、连续人物表演、逐字对白和必须保持一致的英雄商品镜头，三家都应先过实际修改验收，再承诺替代实拍。

交付前还应明确素材用途：提案用的情绪镜头、社媒竖版和最终品牌母版，验收标准不同。客户要求专业编码、调色空间或可继续编辑的文件时，先核对套餐和附加成本；“可导出 4K”也应区分原生生成与放大。只考察在线播放效果，会低估交给后期团队时的转换和修复工作。

商业使用许可、保密承诺和侵权责任是三个不同问题：

- **可灵国际站**：付费协议 3.1.2 明确允许会员商业使用输出，且冲突时付费协议优先；但一般协议将上传内容视为非保密，并保留用于训练等用途的授权，另有申请撤回机制。不能因付费可商用就上传未发布新品。企业“不训练”需落入实际合同；国内站、API 专项约定及免费期输出后续商用范围仍需确认。[付费协议](https://kling.ai/docs/payment-policy)、[一般协议](https://kling.ai/docs/user-policy)
- **Runway**：普通条款允许合规商用，也允许使用输入输出训练；企业条款则明确不以客户内容训练，并将客户内容纳入保密。Team 的协作权益不能自行等同企业合同。其服务侵权赔偿也不能泛化为整支生成广告的输出担保。[普通条款](https://runway.com/terms-of-use)、[企业条款](https://runway.com/enterprise-terms)
- **Google**：Flow 提供关闭产品改进的开关，但数据说明仍提醒不要输入保密信息；Gemini 付费 API 不用输入输出改善产品，不能将这一承诺套给个人 Flow。Cloud 的 Veo 被列入特定赔偿服务，输出赔偿针对未修改输出且有商标、无权使用输入等例外，不能承诺最终广告全面获赔。[Flow 数据说明](https://support.google.com/flow/answer/17025472?hl=en)、[API 条款](https://ai.google.dev/gemini-api/terms)、[赔偿名单](https://cloud.google.com/terms/generative-ai-indemnified-services)、[Cloud 条款](https://cloud.google.com/terms/service-terms)

因此，保密新品会把选择从普通会员推向具备对应承诺的企业服务，甚至暂缓上传；代言人、声音和商标授权仍需业务方持有。Flow 输出含 SynthID，可见水印可设置，但印度、韩国、越南自动加注。客户若规定无可见水印，应在实际使用地区先验收导出结果。[Flow 水印规则](https://support.google.com/flow/answer/16353333?hl=en)

**可靠性证据：能够支持试用，尚不足以支持无人值守交付**

独立盲评并未给出稳定的统一胜者。截止日 Artificial Analysis 有声文生视频池中，可灵 3.0 Pro 为 1108±5、Veo 3.1 为 1091±6；有声图生视频池中，Veo 为 1087±7、可灵为 1072±6。输入方式改变，排序也改变；Gen-4.5 不在这两个有声池内，不能据此排三家总榜。盲评测的是观看偏好，不是商品准确率、客户修改通过率或广告转化。[文生榜](https://artificialanalysis.ai/video/leaderboard/text-to-video)、[图生榜](https://artificialanalysis.ai/video/leaderboard/image-to-video)、[方法](https://artificialanalysis.ai/video/methodology)

交付层面也有实际限制。Runway 8 月 19 日记录 Gen-4.5 图生视频性能下降，事件创建至解决约一小时；这不是完整故障时长，更不能据此计算月度可用率或断言它比另外两家不稳。其 API 文档说明最大并发不构成高负载下的吞吐保证。[事故记录](https://status.runwayml.com/incidents/n5lh5cg1cv3n)、[配额说明](https://docs.dev.runwayml.com/usage/tiers/)

Google 文档列出 Veo 高峰生成可能到六分钟，音频处理失败可能不出视频，接口视频需在两天内下载；这些是公开边界而非 SLA。可灵资源包说明购买更多额度不会自动增加并发。三家目前都缺少在同一批真实商品、同样人工投入下，可公开复核的端到端商业验收率。[Veo 限制](https://ai.google.dev/gemini-api/docs/veo)、[可灵资源包规则](https://kling.ai/dev/pricing)

建议先用已公开素材开展小规模试点：电商选十个不同包装、材质的商品，品牌选两份真实简报；先核实账户资格，再给候选路线相同的镜头要求、重试上限和修改任务。记录全部废片、人工分钟、总账单及交付耗时，分别衡量商品准确性和品牌修改通过率。

测试应覆盖团队真实工作时段，并单列最慢任务、审核阻断和需要人工重提的次数。品牌测试必须包含一次客户式修改，电商测试必须包含换商品后的复用；否则容易把某个幸运样片的表现误认为稳定产能。扩大试点前先满足商品事实准确、授权明确和截止前可交付，再评估节省比例。

可灵若商品细节返工多，电商首选应改变；Runway 若协作节省不足以覆盖费用与搭建成本，应退回更直接的生成路线；Veo 若地域、中文或功能切换不符合流程，即使镜头更受偏好也应退出该项目。保密和授权不满足时先解决合同，固定交期项目则保留已验收库存和备用制作方式。扩大采购的依据应是合格素材更便宜、客户修改更可控且能按时交付。
