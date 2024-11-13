from drf_jsonschema_serializer import to_jsonschema
from openai import OpenAI

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
# django.setup()

client = OpenAI(
    base_url="https://api.fast-tunnel.one/v1",
    api_key="sk-75POYYxLq5ToYuEFA0365423557c49D4A0A5A97b764392C0",
    timeout=60
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


def get_schema_from_serializer(serializer, topic):
    """
    从序列化器中获取 JSON Schema
    """
    json_schema = to_jsonschema(serializer)
    remove_length_constraints(json_schema)
    schema_wrapper = {
        "type": "json_schema",
        "json_schema": {
            "name": f"{topic}",
            "schema": json_schema
            # "strict": True
        }
    }
    return schema_wrapper


def get_system_role_content(question_domain):
    system_role_content = f"""
                 按照指定json结构对提供的内容进行解析制作单词记忆卡片，对于提供的json中的content字段严格使用提供的指定内容:
                 1. 翻译部分要求使用中文提供,scene_example_sentence使用英文给出;
                 2. 你在翻译的过程中应该注意到用户是从事{question_domain}领域相关联性的工作;
                """
    return system_role_content


def structured_parse_by_gpt(json_schema, system_role_content, user_role_content):
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {"role": "system",
             "content": system_role_content},
            {
                "role": "user",
                "content": user_role_content
            }
        ],
        response_format=json_schema
    )
    result = completion.choices[0].message.content
    return result
