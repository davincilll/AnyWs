from rest_framework.decorators import api_view

from app.common.decorator.ViewSetDecorator import func_params_check
from app.common.exceptionbox.success_response import SuccessResponse
from card_module.serializers.WordCardModelSerializer import WordCardSchema
from translation_module.utils.chatgpt_helper import get_system_role_content, get_schema_from_serializer, \
    structured_parse_by_gpt


# Create your views here.


@api_view(['POST'])
@func_params_check(required_params=['content'])
def translate(request):
    content = request.data['content']
    question_domain = "计算机科学"
    system_role_content = get_system_role_content(question_domain)
    json_schema = get_schema_from_serializer(WordCardSchema(), "word_card")
    result = structured_parse_by_gpt(json_schema, system_role_content, content)
    return SuccessResponse(data=result)
