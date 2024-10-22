from app.common.decorator.ViewSetDecorator import params_check
from app.common.mixins.CustomCreateModelMixin import CustomCreateModelMixin


class CheckAndTransmitUserParamCreateModelMixin(CustomCreateModelMixin):
    @params_check(['user'])
    def create(self, request, *args, **kwargs):
        kwargs['user'] = request.user.openid
        return super().create(request, *args, **kwargs)
