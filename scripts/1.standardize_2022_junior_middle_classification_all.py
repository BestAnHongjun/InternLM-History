import os
import json


if __name__ == "__main__":
    path = os.path.join("datasets", "middle", "2022_junior_middle_classification_washed.json")
    with open(path, "r", encoding='utf-8') as f:
        test_all = json.load(f)

    subjects = test_all["subjects"]
    topics = test_all["topic"]
    tests = test_all["test"]

    output = ""

    new_test = dict()
    new_test["subjects"] = subjects
    new_test["topics"] = topics
    new_test["test"] = []

    choice_func = {
        "A": 0,
        "B": 1,
        "C": 2,
        "D": 3
    }

    for i, test in enumerate(tests):
        test_content = test["content"]
        area = test_content.split("）")[0].split("（")[-1]
        content = test_content.split("（{}）".format(area))[-1]
        ans = content.split("【答案】")[-1]
        analysis = content.split("【解析】")[-1]
        content = content.split("【答案】")[0]
        ans = ans.split("【解析】")[0]
        ans = ans.replace("##n##", "")
        analysis = analysis.replace("##n##", "").replace(" ", "")

        # 单选题
        if ans == "A" or ans == "B" or ans == "C" or ans == "D":
            content = content.replace("．", ".")
            choice_a = content.split("A.")[-1]
            choice_b = choice_a.split("B.")[-1]
            choice_c = choice_b.split("C.")[-1]
            choice_d = choice_c.split("D.")[-1]

            content = content.split("A.")[0]
            choice_a = choice_a.split("B.")[0]
            choice_b = choice_b.split("C.")[0]
            choice_c = choice_c.split("D.")[0]

            content = content.replace("##n##", "").replace("##t##", "").strip()
            choice_a = choice_a.replace("##n##", "").replace("##t##", "").strip()
            choice_b = choice_b.replace("##n##", "").replace("##t##", "").strip()
            choice_c = choice_c.replace("##n##", "").replace("##t##", "").strip()
            choice_d = choice_d.replace("##n##", "").replace("##t##", "").strip()

            test_i = {
                "tid": i + 1,
                "subject_id": test["subject_id"],
                "topic_id": test["topic_id"],
                "type": 0,
                "origin": area,
                "content": content,
                "choices": [choice_a, choice_b, choice_c, choice_d],
                "ans": choice_func[ans],
                "analysis": analysis
            }
            new_test["test"].append(test_i)
        elif "_" in content:
            while "__" in content:
                content = content.replace("__", "_")
            content = content.replace("_", "（ ）")
            test_i = {
                "tid": i + 1,
                "subject_id": test["subject_id"],
                "topic_id": test["topic_id"],
                "type": 1,
                "origin": area,
                "content": content,
                "ans": ans,
                "analysis": analysis
            }
            new_test["test"].append(test_i)
        else:
            ans = ans.replace("√", "正确")
            test_i = {
                "tid": i + 1,
                "subject_id": test["subject_id"],
                "topic_id": test["topic_id"],
                "type": 2,
                "origin": area,
                "content": content,
                "ans": ans,
                "analysis": analysis
            }
            new_test["test"].append(test_i)

    output = json.dumps(new_test, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ':'))
    with open(os.path.join("datasets", "middle", "2022_junior_middle_classification_std.json"), "w", encoding='utf-8') as f:
        f.write(output)
