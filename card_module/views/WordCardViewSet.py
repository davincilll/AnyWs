from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from app.common.decorator.ViewSetDecorator import router_register, params_check
from app.common.mixins.CustomCreateModelMixin import CustomCreateModelMixin
from app.common.mixins.PartialUpdateModelMixin import PartialUpdateModelMixin
from app.common.mixins.UserFilterMixin import UserFilterListRetrieveDestroyMixin
from app.routers import card_module_router
from card_module.models.WordCard import WordCard, RootExplain, UsefulPhraseUsingThisVocabulary
from card_module.serializers.WordCardModelSerializer import WordCardModelSerializer, \
    RootExplainModelSerializer, UsefulPhraseUsingThisVocabularyModelSerializer


@router_register(card_module_router)
class WordCardViewSet(GenericViewSet, PartialUpdateModelMixin, ListModelMixin, RetrieveModelMixin, DestroyModelMixin,
                      CustomCreateModelMixin):
    """
    list: 需要jwt，获取所有的用户的WordCard资源对象
    create: 需要jwt，创建用户的WordCard资源对象
    partial_update: 需要jwt，部分更新用户的WordCard资源对象
    destroy: 需要jwt，删除用户的WordCard资源对象
    """
    queryset = WordCard.objects.all()
    serializer_class = WordCardModelSerializer
    authentication_classes = [JWTAuthentication, ]

    # permission_classes = [IsAuthenticated]

    # @params_check(not_allowed_params=["user"])
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    # @params_check(not_allowed_params=['user'])
    def create(self, request, *args, **kwargs):
        kwargs['user_id'] = request.user.pk
        return super().create(request, *args, **kwargs)


@router_register(card_module_router)
class UsefulPhraseUsingThisVocabularyViewSet(UserFilterListRetrieveDestroyMixin, GenericViewSet,
                                             PartialUpdateModelMixin,
                                             CustomCreateModelMixin):
    """
    list: 获取所有的UsefulPhraseUsingThisVocabulary资源对象,需要添加过滤参数word_card_id
    create: 创建UsefulPhraseUsingThisVocabulary资源对象，需要传入word_card_id参数
    partial_update: 部分更新UsefulPhraseUsingThisVocabulary资源对象
    destroy: 删除UsefulPhraseUsingThisVocabulary资源对象
    """
    queryset = UsefulPhraseUsingThisVocabulary.objects.all()
    serializer_class = UsefulPhraseUsingThisVocabularyModelSerializer
    authentication_classes = [JWTAuthentication, ]
    permission_classes = [IsAuthenticated]

    @params_check(required_params=['word_card_id'])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @params_check(not_allowed_params=['user'])
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @params_check(not_allowed_params=['user'])
    def create(self, request, *args, **kwargs):
        kwargs['user'] = request.user
        return super().create(request, *args, **kwargs)


@router_register(card_module_router)
class RootExplainViewSet(UserFilterListRetrieveDestroyMixin, GenericViewSet, PartialUpdateModelMixin,
                         CustomCreateModelMixin):
    """
    list: 获取所有的RootExplain资源对象,需要添加过滤参数word_card_id
    create: 创建RootExplain资源对象，需要传入word_card_id参数
    partial_update: 部分更新RootExplain资源对象
    destroy: 删除RootExplain资源对象
    """
    queryset = RootExplain.objects.all()
    serializer_class = RootExplainModelSerializer
    authentication_classes = [JWTAuthentication, ]
    permission_classes = [IsAuthenticated]

    @params_check(required_params=['word_card_id'])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @params_check(not_allowed_params=['user'])
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @params_check(not_allowed_params=['user'])
    def create(self, request, *args, **kwargs):
        kwargs['user'] = request.user
        return super().create(request, *args, **kwargs)
