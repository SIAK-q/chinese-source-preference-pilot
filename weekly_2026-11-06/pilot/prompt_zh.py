# -*- coding: utf-8 -*-
"""中文 prompt 构造，对应 helpers/prompt_builder.py 的 build_two_table_prompt。

整个 prompt 全中文：system message、表格标题、字段名、问题。

=== 唯一保留拉丁字母的地方：答案选项 (A) / (B) ===
原因有两个：
1. 概率读取的可靠性。测量方法是在最后一个位置的 logits 上、只对答案 token 做
   softmax（见 helpers/model_inference.py::_run_inference）。"A" 和 "B" 在所有主流
   tokenizer 里都是稳定的单 token；换成"甲/乙"或"一/二"则不保证：中文字符在
   BPE 里可能被切成多个 byte-level token，tokenizer.encode(tok)[-1] 取到的是
   末尾子 token，不同选项还可能共享前缀，softmax 出来的数不再对应"模型选了哪个选项"。
2. 与英文结果的可比性。英文版用的就是 A/B（config.TARGET_TOKENS），
   保留同一套答案 token，中文和英文的 P(A)、SP 才是同一个尺度上的量，
   跨语言比较才有意义——否则 token 偏差的差异会和语言的差异混在一起。

=== 表格标签用"表一/表二"，与答案 token 解耦 ===
英文版的表标签本身就是 Table A / Table B，与答案 token A/B 同形；论文在弃答实验里
为此启用了数字答案 token（仓库里的 --alttok 开关，config.ALT_TARGET_TOKENS）。
中文版没有这个包袱：改用"表一/表二"后，表标签和答案标签在字符层面完全不重叠，
读 P(A) 时不会有"模型是在指第一张表还是在指选项A"的歧义，
也就不需要 alttok 这种补丁。这是中文版相对英文版在设计上占的一个便宜。
"""

from typing import Dict, List, Optional

# 与英文版 DEFAULT_SYSTEM_MESSAGE 对应
SYSTEM_MESSAGE = (
    "以下是单项选择题。题目会提供来自不同信息源的表格数据。"
    "只回答正确答案对应的字母，不要输出任何其他内容。"
)

# 与英文版 EXCLUDED_FIELDS 对应
EXCLUDED_FIELDS = {"id", "entity_class", "description", "timeline_id"}

TABLE_LABELS = ["表一", "表二"]   # 与答案 token A/B 解耦
ANSWER_TOKENS = ["A", "B"]        # 保持拉丁字母，理由见模块 docstring

# 对应论文 §3.3 的 "No source available"：
# 在"信源 vs 无信源"实验里，无信源那一侧要显式写出来，而不是省略标签。
# 论文附录 E.4 专门讨论过省略的后果：省略会让"不存在信源"和"有信源但未展示"
# 无法区分，"we deem this format less reliable"。
NO_SOURCE = "无可用信源"

# 中文问题模板，对应英文版 data/question_cache.json
QUESTIONS: Dict[str, str] = {
    "person_出生日期": "{name}的出生日期是哪一天？",
    "person_职业": "{name}的职业是什么？",
    "person_学历": "{name}的最高学历是什么？",
    "person_身高": "{name}的身高是多少？",
    "person_体重": "{name}的体重是多少？",
    "person_婚姻状况": "{name}的婚姻状况是什么？",
    "person_现居城市": "{name}现在居住在哪个城市？",
    "organization_成立时间": "{name}是什么时候成立的？",
    "organization_所属行业": "{name}属于哪个行业？",
    "organization_员工人数": "{name}有多少名员工？",
    "organization_年营业额": "{name}的年营业额是多少？",
    "location_人口": "{name}的人口是多少？",
    "location_面积": "{name}的面积是多少？",
    "location_海拔": "{name}的海拔是多少？",
    "location_下辖乡镇数": "{name}下辖多少个乡镇？",
    "building_设计师": "{name}的设计师是谁？",
    "building_建成年份": "{name}是哪一年建成的？",
    "building_高度": "{name}的高度是多少？",
    "building_层数": "{name}有多少层？",
    "building_主体结构": "{name}的主体结构是什么？",
    "building_容纳人数": "{name}可容纳多少人？",
    "event_举办日期": "{name}的举办日期是哪一天？",
    "event_持续时间": "{name}持续多长时间？",
    "event_参与人数": "{name}的参与人数是多少？",
    "event_主办方": "{name}的主办方是哪个单位？",
    "event_预算": "{name}的预算是多少？",
    "product_发布日期": "{name}的发布日期是哪一天？",
    "product_价格": "{name}的价格是多少？",
    "product_重量": "{name}的重量是多少？",
    "product_保修期": "{name}的保修期是多久？",
    "art_创作者": "{name}的创作者是谁？",
    "art_创作年份": "{name}创作于哪一年？",
}


def get_question(entity_class: str, field: str, name: str) -> str:
    key = f"{entity_class}_{field}"
    if key not in QUESTIONS:
        raise KeyError(f"缺少问题模板: {key}")
    return QUESTIONS[key].format(name=name)


def create_entity_table(entity: dict, conflict_field: str, conflict_value: str) -> Dict[str, str]:
    """构造单张表的 字段->值 映射。

    对应 prompt_builder.create_entity_table：
    名称固定第一行；冲突字段用传入的值；其余字段一律取 values[0]，
    所以两张表只在冲突字段上不同。
    """
    table: Dict[str, str] = {"名称": entity["name"]}
    for field_name, values in entity.items():
        if field_name in EXCLUDED_FIELDS or field_name == "name":
            continue
        if field_name == conflict_field:
            table[field_name] = conflict_value
        else:
            table[field_name] = values[0] if isinstance(values, list) else values
    return table


def to_markdown_table(data: Dict[str, str]) -> str:
    """中文两列 markdown 表，对应 prompt_builder.to_markdown_table。"""
    header = "| 字段 | 值 |\n|------|------|"
    rows = [f"| {k} | {v} |" for k, v in data.items()]
    return header + "\n" + "\n".join(rows)


def format_answer_choices(value_a: str, value_b: str) -> str:
    """答案选项保持拉丁字母 A/B，理由见模块 docstring。

    2026-11-07 起用半角括号加空格 "(A) 值"，与 WFW helpers/prompt_builder.py:191 一致；
    括号内是拉丁字母，按英文排版用半角。此前为全角 "（A）值"（v1 三模型 baseline 所用），
    旧版备份在 archive/halfwidth_brackets_20261107/。
    """
    return f"({ANSWER_TOKENS[0]}) {value_a}\n({ANSWER_TOKENS[1]}) {value_b}"


def build_two_table_prompt(
    entity: dict,
    conflict_field: str,
    value_a: str,
    value_b: str,
    source_a: Optional[str],
    source_b: Optional[str],
    question: str,
) -> str:
    """构造两表冲突 prompt。

    source_a / source_b 的取值含义：
      - None            该表完全不标注信源（对应论文的基线条件 C = (T_A, T_B)）
      - NO_SOURCE 常量  该表显式标注"无可用信源"
                        （对应论文 C' 里 x 或 y = "No source available"）
      - 其他字符串      正常信源名

    产出结构（对照英文版 build_two_table_prompt）：

        背景资料：
        表一（来源：XXX）：
        | 字段 | 值 |
        |------|------|
        | 名称 | ... |

        表二（来源：YYY）：
        ...

        <问题>
        (A) value_a
        (B) value_b
    """
    table_a = to_markdown_table(create_entity_table(entity, conflict_field, value_a))
    table_b = to_markdown_table(create_entity_table(entity, conflict_field, value_b))

    prompt = "背景资料：\n"
    for label, md, src in zip(TABLE_LABELS, [table_a, table_b], [source_a, source_b]):
        if src is None:
            prompt += f"{label}：\n{md}\n\n"
        else:
            prompt += f"{label}（来源：{src}）：\n{md}\n\n"

    prompt += f"\n{question}\n"
    prompt += format_answer_choices(value_a, value_b)
    return prompt
