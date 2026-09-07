**AI 客服已在高频、规则明确的业务中进入生产，企业下一阶段应投资于可持续解决问题的能力。** 截至 2026 年 9 月 7 日，Intercom、Zendesk、Salesforce 都有正式收费产品和具名生产案例；商业化已经发生，但公开证据尚不足以证明三者可以按相近成本、在任意企业复制相同效果。最值得关注的进展，是 AI 开始读取真实订单、执行授权操作，并把例外事项交给人工；最需要谨慎的地方，是“解决”“结果”“使用量”仍由不同规则计算。

判断试点是否进入生产，应看真实客户是否持续使用、系统是否完成业务操作或有效接管，以及服务质量与总成本是否进入日常管理。功能上线、签约客户数和演示成功率，分别只能回答其中一部分问题。

竞争关系也已变化。Salesforce 于 6 月 15 日宣布拟以约 **36 亿美元收购 Fin，即原 Intercom 公司**；8 月 26 日财报仍将交易列为待完成，并预计在其 2027 财年第三季度，即 2026 年 8 月至 10 月交割。截止日前的公开信息不足以确认交割完成，因此下文比较三条现有产品路线，保留 Fin 后续整合的不确定性。[收购公告](https://www.salesforce.com/uk/news/press-releases/2026/06/15/salesforce-signs-definitive-agreement-to-acquire-fin/)、[最新财报](https://www.salesforce.com/news/press-releases/2026/08/26/fy27-q2-earnings/)

以下为截止日可见美元公开标价；席位价格按年付折算到月，企业折扣、渠道、数据和实施费用须另核。

| 产品路线 | 嵌入企业流程的方式 | 公开收费结构 | 采购时最关键的区别 |
|---|---|---|---|
| Intercom / Fin | 使用 Intercom 帮助台，或在既有帮助台前接入 Fin；以 Procedures 调用业务系统 | Fin 每个结果 **$0.99 起**；Essential / Advanced / Expert 席位分别 **$29 / $85 / $132**；单独用 Fin 无须购买其席位。[定价](https://www.intercom.com/pricing) | 部分完成流程后的转人工也可能收费；须分开统计自主解决与辅助完成 |
| Zendesk | 在既有工单、路由、知识库和坐席工作台中逐步加入 AI | Suite Team / Professional **$55 / $115**；Copilot 附加项 **$50**；AI 解决额度及超额价格按合同。[定价](https://www.zendesk.com/au/pricing/) | 新版能力开放不等于无限免费使用；报表“自动解决”与收费结果口径不同 |
| Salesforce | 通用 Agentforce 连接 CRM 与业务系统；预配置 Help Agent 简化自助服务部署 | 通用方案 **$2 / 对话**或 **$500 / 10 万 Flex Credits**；Help Agent **$2 / 解决**；基础许可等另计。[通用定价](https://www.salesforce.com/agentforce/pricing/)、[自助服务定价](https://www.salesforce.com/service/customer-self-service/pricing/) | 同时提供用量和结果计费；须明确购买的产品、包含用量及会话时间边界 |

**Intercom / Fin 的优势是较低的流程改造门槛，以及从知识问答向业务处理扩展的路径。** 企业可以保留 Zendesk、Salesforce 等既有帮助台，让 Fin 接待客户、读取知识，遇到例外再交回原来的人工队列。这降低了全量迁移工单系统的必要性，也使 Fin 能争取并非 Intercom 帮助台用户的预算。[产品说明](https://fin.ai/procedures)

其 Procedures 支持把操作流程写成自然语言，再加入分支规则、代码和外部系统连接。例如，取消订单需要先查询状态、确认资格，再调用业务接口执行。退款条件可以固定为程序规则，解释和追问交给模型；需要人工决定时则升级处理。企业真正购买的是这段服务流程的自动化，因此知识库负责人、接口权限和例外处理规则会直接决定上线效果。产品具备连接能力，并不代表客户的后台系统已经准备好。[Procedures](https://fin.ai/procedures)

收费也随之扩展。Fin 在 2026 年将计费表述从 resolutions 转向 outcomes：客户确认解决、答复后没有继续求助，或者完成指定 Procedure，包括某些交接，都可能构成付费结果；同一对话只收费一次。对需要人工最终批准的业务，这种机制可以为前面的资料收集和处理收费。但客户不再回复也可能意味着放弃。采购时必须抽样检查付费事件，并核对独立部署的最低月承诺，否则财务容易把“付费结果数”误当“完全无需人工的案件数”。[计费规则](https://www.intercom.com/pricing)

规模证据已超出试点。Intercom 在 2026 年 5 月自报，Fin 每周完整解决超过 **200 万次对话**，这是生产使用量的厂商披露，未经过公开独立质量审计。[运营披露](https://www.intercom.com/blog/ready-for-your-busiest-day-how-we-scale/)

Synthesia 的具名案例进一步说明了收益的条件：在回顾 2024 年扩容的案例中，客户报告 Fin 解决率为 **55%**，整体解决耗时下降 **96%**；但也承认，早期知识库相互矛盾导致回答不一致，需要重整内容并增加知识维护人手。该案例是供应商发布的客户前后对比，不能把 96% 的等待与处理耗时下降换算为同等人工成本节省。它更支持一个具体判断：对于增长快、重复咨询多且愿意维护内容的软件业务，继续投入有依据；仅接入机器人而不整顿知识与流程，收益容易落空。[Synthesia 案例](https://fin.ai/customers/synthesia)

**Zendesk 的路线是把已有服务组织逐步升级为人机共同处理工单。** 对拥有成熟路由、服务时限、知识库和质检流程的企业，其价值在于让 AI 接入现有工作台：前端处理常见请求，后端读取订单和客户信息，Copilot 辅助人工判断与执行。2026 年的变化包括统一原有 Essential、Advanced 两类 AI agent 能力，以及在 3 月完成 Forethought 收购后，于 6 月开放其附加产品购买，并支持其他服务平台。由此，Zendesk 同时经营既有客户升级和跨平台 AI 服务。[产品调整](https://support.zendesk.com/hc/en-us/articles/10487730059034-Announcing-expanded-access-to-AI-agent-capabilities-for-all-Zendesk-customers)、[Forethought 产品公告](https://support.zendesk.com/hc/en-us/articles/10850639885082-Announcing-Forethought-AI-agents-by-Zendesk-for-customers)

其生产案例体现的是从窄场景扩大覆盖。SeatGeek 先面向可认证的登录用户，解决“我的票在哪里”，通过实时 API 获取订单信息。按 Zendesk 发布的客户案例，到 2025 年第二季度，其自动解决率达到 **51.5%**，AI 客服满意度从 **34% 升至 70%**。这是有具体业务动作和使用人群的采用证据；同时，它属于客户自报、无对照组的历史案例，不能证明 2026 年新产品在所有业务上已经达到同样效果。[SeatGeek 案例](https://www.zendesk.co.uk/customer/seatgeek/)

2026 年的计费和统计调整尤其值得关注。新版区分人工最终接手的 Assisted escalation、未再求助但未通过验证的 Contained resolution，以及通过模型验证的 Verified resolution。前两类不消耗解决额度，第三类才计费。这里的“验证”是供应商的模型评估，不属于第三方独立审计，企业仍应核对真实业务结果。[分层规则](https://support.zendesk.com/hc/en-us/articles/9570369117338-About-automated-resolution-tiers)

与此同时，5 月 18 日起，报表“自动解决率”的分子由 Verified 扩大为 **Contained 加 Verified**，历史记录也会重新映射。报表上涨可能部分来自定义变化，不能直接解释为客户问题解决得更好。额度、超额和迁移期间单价需看具体合同，官方示例账单中的价格只是占位数，不能沿用网上流传的统一每次报价。[报表变更](https://support.zendesk.com/hc/en-us/articles/10677925692698-Announcing-changes-to-AI-agent-reporting)、[额度与迁移规则](https://support.zendesk.com/hc/en-us/articles/10479528943130-Upgrading-from-automated-resolutions-to-resolution-allowances)

对已有 Zendesk 的企业，合理投入顺序是保留成熟服务流程，优先扩大能调用可靠数据的自动化，再评估跨系统复杂处理；采购前应先对齐旧合同、新功能和新统计口径。

**Salesforce 的主要价值在于，把客服请求转化为有客户身份、权限和业务上下文的操作。** 已经使用其 CRM 的企业，可以让 Agentforce 从 Data 360 获取客户与交易数据，调用业务接口执行操作，再将结果写回服务记录。对改签、退订、账户变更这类任务，客户是否有权操作、系统是否真实完成，比回答流畅更重要。原有数据与流程越完整，新增 AI 的价值越容易兑现；数据分散、规则混乱的企业则仍需承担整合工作。

Engine 的案例说明了这条路线如何进入生产。其虚拟助手 Eva 读取预订信息、确认授权，调用预订平台 API 完成取消或变更；复杂团体行程则创建人工案件，保留对话、客户资料和推荐步骤。Salesforce 在 2026 年 6 月发布的客户案例称，Agentforce 自动解决 **50% 的聊天请求**，客服平均处理时长下降 **15%**。它提供了具体流程的采用证据，效果仍属客户自报；聊天请求的比例不能扩大为全部渠道的一半工作量，更不能换算为一半人员成本。[Engine 案例](https://www.salesforce.com/customer-stories/engine/agentic-service/)

2026 年 7 月开放的 **Help Agent** 又向降低实施门槛迈进一步：预配置知识接入、渠道和常用操作，面向帮助站点、门户及聊天等入口。这意味着 Salesforce 在通用流程编排之外，也直接销售较易部署的客服产品。预配置能减少重复搭建，但订单规则和额外业务操作仍需企业配置，不能把“几分钟部署”的官方宣传当作全部生产准备时间。[Help Agent 发布公告](https://www.salesforce.com/news/stories/agentforce-help-agent-announcement/)

商业规模已经可观，但财务指标边界更宽。其截至 7 月底的季度披露，Agentforce 年化经常性收入 ARR 超过 **15 亿美元**，同比增长超过 **240%**；同一公告注明，本季口径包含其 AI 产品、Slackbot 和 Headless 360。这个年化指标不等于当季确认收入，也不代表活跃生产客户数。不能把它全部归为自主客服，或忽略口径变化推算相同产品的增长。拟收购 Fin 表明 Salesforce 还在补充专用客服产品与客户覆盖，其整合收益仍待实现。[第二季度财报](https://www.salesforce.com/news/press-releases/2026/08/26/fy27-q2-earnings/)

计费需要分产品看。通用 Agentforce 的标准动作消耗 **20 个 Flex Credits**，折合 **$0.10 / 动作**，数据、渠道和基础许可等另核；员工 AI 附加许可为 **$125 / 人月**，对应内部人员使用。[通用收费说明](https://www.salesforce.com/agentforce/pricing/)

Help Agent 则为 **$2 / 解决**，该结果内的 Agentforce 动作和 Data 360 查询不限量，不能再机械叠加通用动作单价。其解决判定包含达到最低交互要求后，用户未反馈、也未要求升级的会话；聊天超过 **两小时**可能计为第二次解决。因此，同样称为结果计费，仍要审查“什么算解决”和“一个问题会计费几次”。[Help Agent 定价](https://www.salesforce.com/service/customer-self-service/pricing/)、[计量规则](https://help.salesforce.com/s/articleView?id=service.service_cloud_billable_usage_types.htm&language=en_US&type=5)

**投入优先级应由业务边界和可兑现收益决定。** 可以优先扩大身份可确认、规则稳定、量大且容易核验的任务，例如查票、订单查询、标准订阅问题，以及有明确条件的取消操作。选择范围时应扣除原有帮助中心、表单和规则自动化已经解决的需求，衡量 AI 真正新增的价值。对于知识复杂、例外较多的业务，先投资检索、摘要和人工辅助也有依据。

独立研究对后一类路径提供了更强的效果证据。2025 年《经济学季刊》的研究利用 **5,172 名客服人员**的分阶段采用数据，发现 AI 辅助使每小时解决问题数平均提高约 **15%**，较少经验人员受益更大。研究对象是保留最终责任的人工客服，来自一家企业；它支持辅助工作的价值，不能用来证明三家自主客服产品的效果或排名。[Generative AI at Work](https://academic.oup.com/qje/article/140/2/889/7990658?login=false)

应谨慎扩大的场景包括高额退款、身份或账户争议、需要责任认定的投诉，以及依赖多方履约的复杂售后。这里一次错误授权或客户流失，可能抵消大量常规咨询的节省。流程应明确由谁批准、怎样撤销操作、失败后由谁接手。低咨询量、知识经常冲突、后台接口不稳定的企业，也应先解决这些基础问题。

行业反例同样需要完整理解。美国 SEC 在 2025 年审阅 Klarna 上市材料时，曾因其 CEO 关于部分 AI 服务质量较低的言论，要求解释采用策略如何调整；这是可核验的监管问询，不能据此认定 AI 客服整体失败。Klarna 的 2025 年年报仍自报 AI 处理 **80% 的客服聊天**、当年节省约 **5,900 万美元**，同时保留人工支持。这些数字来自公司日志和估计，尚非独立效果验证。质量争议与持续规模使用可以并存，企业需要同时管理两者。[SEC 问询第 2 页](https://www.sec.gov/Archives/edgar/data/2003292/000000000025005760/filename1.pdf)、[Klarna 年报，PDF 第 188 页](https://s205.q4cdn.com/644747736/files/doc_financials/2025/q4/Klarna-Group-plc-20-F-2025.pdf)

经济性应统一到“每个持续解决的问题的总成本”：分子包括席位、AI 用量、数据与渠道、接口维护、知识运营、质检，以及转人工和重复联系成本；分母排除误关单与随后重开的案件。AI 压低简单咨询量后，人工队列可能留下更难的问题，平均处理时长上升未必是退步。节省的工时也只有转化为少招人、少加班、降低外包费用或吸收增长，才成为可兑现收益。三家选择应分别优先考虑 Fin 的叠加部署便利、Zendesk 的既有服务流程、Salesforce 的 CRM 和业务数据基础。

**未来三个月，即 2026 年 9 月 8 日至 12 月 7 日，建议用以下指标决定扩容，而非预设一个通用自动化率目标。** 以下是企业内部验证建议，不是行业已实现的平均水平。

1. **持久解决率与真实覆盖率。** 先固定问题类别、语言和渠道等资格条件，以期间全部符合条件的请求为分母；同时报告 AI 实际覆盖比例，以及抽查确认解决、七天内未因同一问题重新求助的比例。跨渠道合并同一问题，只比较已满观察期的样本。未接入、转人工和客户放弃均应可见，防止只挑简单问题使数字上升。
2. **质量与接管成本。** 对照人工或原有自动化，跟踪重开率、投诉率、满意度及调查回应率；抽样核对订单、退款等后台状态。转人工后是否保留上下文、客户是否需要重新解释，也应计入体验和人工耗时。
3. **全成本及兑现情况。** 按问题类别计算每个持续解决问题的成本，观察高峰期用量账单、重试与人工补救费用。要求工时收益对应到外包费、加班或新增业务承接，避免把供应商估算的“节省人数”直接计入预算。
4. **从试点到连续运行。** 记录上线后的持续使用、知识维护投入、接口失败和错误操作；新增场景应经过小流量验证再放量。对高风险操作，应设定单次严重越权即可暂停该流程的条件，保留人工服务能力。

供应商侧则有三个具体观察点：Fin 收购是否完成，以及帮助台兼容、合同和产品路线是否改变；Zendesk 新计费规则下 Verified 占比、账单变化及旧版迁移进度；Salesforce 是否提供口径稳定的客服业务使用、续约或扩容证据。Zendesk 已公告旧版 Essential 等功能将于 **12 月 10 日移除**，因此本观察窗口应以完成迁移和验证为目标，而非等到停用后补救。[旧版迁移公告](https://support.zendesk.com/hc/en-us/articles/10904648529690-Announcing-the-end-of-support-for-AI-agents-Essential-and-legacy-functionality-Important-dates-and-migration-guidance)

如果同类请求的成本持续下降、质量不劣于基线，而且维护负担可承受，应逐步增加覆盖范围；若报表变好而重开、投诉或人工补救上升，应暂停扩大。公开信息目前不足以给三家做统一效果排名，企业自己的连续生产数据应成为下一笔预算的主要依据。

参考来源按证据类型列示，正文链接对应具体论断：

- **官方产品与价格**：[Intercom 定价](https://www.intercom.com/pricing)、[Fin Procedures](https://fin.ai/procedures)、[Zendesk 定价](https://www.zendesk.com/au/pricing/)、[Zendesk 解决结果分层](https://support.zendesk.com/hc/en-us/articles/9570369117338-About-automated-resolution-tiers)（2026-08-24）、[报表口径调整](https://support.zendesk.com/hc/en-us/articles/10677925692698-Announcing-changes-to-AI-agent-reporting)（2026-05-27）、[Agentforce 定价](https://www.salesforce.com/agentforce/pricing/)、[Help Agent 定价](https://www.salesforce.com/service/customer-self-service/pricing/)。动态价格页按截止日可见版本使用。
- **官方商业与产品进展**：[Salesforce 拟收购 Fin](https://www.salesforce.com/uk/news/press-releases/2026/06/15/salesforce-signs-definitive-agreement-to-acquire-fin/)（2026-06-15）、[Salesforce 2027 财年第二季度财报](https://www.salesforce.com/news/press-releases/2026/08/26/fy27-q2-earnings/)（2026-08-26）、[Help Agent 发布](https://www.salesforce.com/news/stories/agentforce-help-agent-announcement/)（2026-06-25 公告，7 月开放）、[Fin 生产规模披露](https://www.intercom.com/blog/ready-for-your-busiest-day-how-we-scale/)（2026-05-19）、[Forethought 产品开放购买](https://support.zendesk.com/hc/en-us/articles/10850639885082-Announcing-Forethought-AI-agents-by-Zendesk-for-customers)（2026-06-04 起）。
- **供应商发布的客户案例**：[Synthesia](https://fin.ai/customers/synthesia)（回顾 2024 年扩容）、[SeatGeek](https://www.zendesk.co.uk/customer/seatgeek/)（指标截至 2025 年第二季度）、[Engine](https://www.salesforce.com/customer-stories/engine/agentic-service/)（2026-06-04）。均不视为独立效果审计。
- **独立学术与监管记录**：Brynjolfsson、Li、Raymond，[Generative AI at Work](https://academic.oup.com/qje/article/140/2/889/7990658?login=false)，*The Quarterly Journal of Economics*，2025；[SEC 致 Klarna 问询函](https://www.sec.gov/Archives/edgar/data/2003292/000000000025005760/filename1.pdf)（2025-05-30）。
- **企业自身的经营披露**：[Klarna 2025 年年报](https://s205.q4cdn.com/644747736/files/doc_financials/2025/q4/Klarna-Group-plc-20-F-2025.pdf)，PDF 第 188 页；其中客服效果和节省金额为公司内部统计与估计。
