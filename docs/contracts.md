# 静态采集步骤

execute_static 顺序执行 SAMPLE 中固定四步，每次从头开始，不提供恢复或动态展开。
步骤 arguments 可有常量，或 from/path 绑定；path 是 dict key 与列表下标组成的点分路径，不执行任意代码。
Collectors 封装真实 HTTP 来源：institutions -> directories -> details -> attachment_meta；summary 是本地整理步骤。
相同 detail 可能包含多个附件，也可能为空；inst-b 的目录清单为空是有效来源结果，而不是网络失败。
flow.fingerprint 将配置内容冻结为摘要，当前静态运行逐事件记录该值，流程业务名不提供版本隔离。
run_view 只显示每个静态 step 的最后状态；多个动态实例不能沿用同一个 step 作为唯一身份。
来源请求成功与项目依赖完整是不同概念，failed、没有输入和主动跳过须由扩展运行器明确表达。
运行结果应能保留 source 对象身份，供资料员从后续缺口回查是哪家机构哪份目录尚未取得。
