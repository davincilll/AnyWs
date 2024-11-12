import os

import django
from openai import OpenAI

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
django.setup()
from card_module.serializers.WordCardModelSerializer import WordCardModelSerializer
from drf_jsonschema_serializer import to_jsonschema

client = OpenAI(
    base_url="https://api.fast-tunnel.one/v1",
    api_key="sk-75POYYxLq5ToYuEFA0365423557c49D4A0A5A97b764392C0"
)


def remove_length_constraints(schema):
    """递归地移除 maxLength 和 minLength 字段"""
    # 检查 schema 是否是有效的对象
    if isinstance(schema, dict):
        schema["additionalProperties"] = False
        if "properties" in schema:

            for key, value in schema["properties"].items():
                # 移除 maxLength 和 minLength
                value.pop('maxLength', None)
                value.pop('minLength', None)

                # 递归处理嵌套对象
                remove_length_constraints(value)

        # 处理 items 字段，用于数组类型
        if "items" in schema:
            remove_length_constraints(schema["items"])


json_schema = to_jsonschema(WordCardModelSerializer())
# json_schema["additionalProperties"] = False
remove_length_constraints(json_schema)
schema_wrapper = {
    "type": "json_schema",
    "json_schema": {
        "name": "word_card"
        # "strict": True
    }
}
schema_wrapper["json_schema"]["schema"] = json_schema
completion = client.beta.chat.completions.parse(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "制作单词记忆卡片，按照指定json结构提供内容，翻译部分要求使用中文提供,sceneExampleSentence使用英文给出"},
        {
            "role": "user",
            "content": "completion"
        }
    ],
    response_format=schema_wrapper
)
result = completion.choices[0].message.content
print(result)
