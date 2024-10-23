from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, DestroyModelMixin


class UserFilterMixin:
    """
    用于将资源进行初步过滤，过滤得到当前用户的所属的资源,这里默认user的反向名字为user
    无需重写get_object的方法过滤，get_oobject是基于get_queryset进行的。
    在继承关系中MRO会将FOO(self, *args, **kwargs)和FOO() 当成一般的重写来决定优先级
    """
    # 自定义user的命名
    user_field_id = 'user_id'

    # 这里是拓展的
    # extended_user = None

    def get_queryset(self, *args, **kwargs):
        if not (queryset := kwargs.get("QuerySet", None)):
            queryset = super().get_queryset()
        user = self.request.user
        if not (user_filed_id := kwargs.get("user_field_id", None)):
            user_filed_id = self.user_field_id
        return queryset.filter(**{self.user_field_id: user.pk})
        #
        # if self.extended_user_field_name is None:
        #     user = user.getattr(self.user_field_name)
        #     return queryset.filter(**{self.user_field_name: user})
        # else:
        #     extended_user = user.getattr(self.extended_user)
        #     return queryset.filter(**{self.user_field_name: extended_user})

# 增加一个基于外键的检测过滤

class UserFilterListMixin(UserFilterMixin, ListModelMixin):
    pass


class UserFilterListRetrieveMixin(UserFilterMixin, ListModelMixin, RetrieveModelMixin):
    pass


class UserFilterListRetrieveDestroyMixin(UserFilterMixin, ListModelMixin, RetrieveModelMixin, DestroyModelMixin):
    pass


class UserFilterRetrieveMixin(UserFilterMixin, RetrieveModelMixin):
    pass
