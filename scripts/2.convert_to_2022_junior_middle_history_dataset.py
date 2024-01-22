import os
import json
from tqdm import tqdm

system_prompt = "你是中学历史学习助手，内在是InternLM-7B大模型。你的开发者是安泓郡。开发你的目的是为了提升中学生对历史学科的学习效果。你将对中学历史知识点做详细、耐心、充分的解答。"


if __name__ == "__main__":
    dataset = []

    path = os.path.join("datasets", "middle", "2022_junior_middle_classification_std.json")
    with open(path, "r", encoding='utf-8') as f:
        all_test = json.load(f)

    subjects = all_test["subjects"]
    topics = all_test["topics"]
    tests = all_test["test"]

    print("创建：知识点归纳类问题...")
    for test in tqdm(tests):
        content = test["content"].replace("##n##", "\n")
        dataset.append({
            "conversation": [
                {
                    "system": system_prompt,
                    "input": "请问以下问题属于中学历史学科中的哪一个专题？{}".format(content),
                    "output": "{}。".format(subjects[test["subject_id"] - 1])
                }
            ]
        })
        dataset.append({
            "conversation": [
                {
                    "system": system_prompt,
                    "input": "{}。以上问题属于哪一个专题？".format(content),
                    "output": "{}。".format(subjects[test["subject_id"] - 1])
                }
            ]
        })
        dataset.append({
            "conversation": [
                {
                    "system": system_prompt,
                    "input": "请问以下问题属于中学历史学科中的哪一个知识点？{}".format(content),
                    "output": "{}。".format(topics[test["topic_id"] - 1])
                }
            ]
        })
        dataset.append({
            "conversation": [
                {
                    "system": system_prompt,
                    "input": "{}。以上问题属于哪一个知识点？".format(content),
                    "output": "{}。".format(topics[test["topic_id"] - 1])
                }
            ]
        })

    print("创建：单选题及其派生类问题...")
    choice_func = {
        0: "A",
        1: "B",
        2: "C",
        3: "D"
    }
    for test in tqdm(tests):
        if test["type"] != 0:
            continue
        content = test["content"].replace("##n##", "\n")
        dataset.append({
            "conversation": [
                {
                    "system": system_prompt,
                    "input": "{}：A.{} B.{} C.{} D.{}".format(content, test["choices"][0], test["choices"][1], test["choices"][2], test["choices"][3]),
                    "output": "选择{}。{}。".format(choice_func[test["ans"]], test["analysis"])
                }
            ]
        })
        for i in range(4):
            if i == test["ans"]:
                dataset.append({
                    "conversation": [
                        {
                            "system": system_prompt,
                            "input": "{}：{}".format(content, test["choices"][i]),
                            "output": "正确。"
                        }
                    ]
                })
                dataset.append({
                    "conversation": [
                        {
                            "system": system_prompt,
                            "input": "{}：{}。这句话对吗？".format(content, test["choices"][i]),
                            "output": "正确。"
                        }
                    ]
                })
                dataset.append({
                    "conversation": [
                        {
                            "system": system_prompt,
                            "input": "以下说法是否正确？{}：{}。".format(content, test["choices"][i]),
                            "output": "正确。"
                        }
                    ]
                })
            else:
                dataset.append({
                    "conversation": [
                        {
                            "system": system_prompt,
                            "input": "{}：{}".format(content, test["choices"][i]),
                            "output": "错误。"
                        }
                    ]
                })
                dataset.append({
                    "conversation": [
                        {
                            "system": system_prompt,
                            "input": "{}：{}。这句话对吗？".format(content, test["choices"][i]),
                            "output": "错误。"
                        }
                    ]
                })
                dataset.append({
                    "conversation": [
                        {
                            "system": system_prompt,
                            "input": "以下说法是否正确？{}：{}。".format(content, test["choices"][i]),
                            "output": "错误。"
                        }
                    ]
                })

    print("创建：填空类问题...")
    for test in tqdm(tests):
        if test["type"] != 1:
            continue
        content = test["content"].replace("##n##", "\n")
        dataset.append({
            "conversation": [
                {
                    "system": system_prompt,
                    "input": "填空题。{}？".format(content),
                    "output": "{}。{}".format(test["ans"], test["analysis"])
                }
            ]
        })
        dataset.append({
            "conversation": [
                {
                    "system": system_prompt,
                    "input": "请在“（ ）”中填入适当内容。{}？".format(content),
                    "output": "{}。{}".format(test["ans"], test["analysis"])
                }
            ]
        })
        dataset.append({
            "conversation": [
                {
                    "system": system_prompt,
                    "input": "{}？填空".format(content),
                    "output": "{}。{}".format(test["ans"], test["analysis"])
                }
            ]
        })

    print("创建：综合类问题...")
    for test in tqdm(tests):
        if test["type"] != 2:
            continue
        content = test["content"].replace("##n##", "\n")
        dataset.append({
            "conversation": [
                {
                    "system": system_prompt,
                    "input": "{}？".format(content),
                    "output": "{}。{}".format(test["ans"], test["analysis"])
                }
            ]
        })

    print("创建：身份认知类问题...")
    dataset.append({
        "conversation": [
            {
                "system": system_prompt,
                "input": "你是谁？",
                "output": "我是中学历史学习助手，内在是InternLM-7B大模型，开发者是安泓郡。"
            }
        ]
    })
    dataset.append({
        "conversation": [
            {
                "system": system_prompt,
                "input": "请介绍以下你自己。",
                "output": "我是中学历史学习助手，内在是InternLM-7B大模型，开发者是安泓郡。"
            }
        ]
    })
    dataset.append({
        "conversation": [
            {
                "system": system_prompt,
                "input": "做一下自我介绍。",
                "output": "我是中学历史学习助手，内在是InternLM-7B大模型，开发者是安泓郡。"
            }
        ]
    })
    dataset.append({
        "conversation": [
            {
                "system": system_prompt,
                "input": "为什么要开发你？",
                "output": "为了提升中学生对历史学科的学习效果。中学历史学科作为培养学生综合素质和历史意识的重要学科，对于学生的发展具有深远的影响。"
            }
        ]
    })

    print(len(dataset))
    output = json.dumps(dataset, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ':'))
    with open(os.path.join("datasets", "2022_junior_middle_history.json"), "w", encoding='utf-8') as f:
        f.write(output)