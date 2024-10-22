# from abc import ABCMeta
#
# from django.http import Http404
#
#
# class ExtendedUserMixin:
#     __metaclass__ = ABCMeta
#
#     # 提供一个自定义的参数，可以选择性的覆盖lookup_field
#     def get_object(self):
#         try:
#             return self.get_queryset().get(**{self.lookup_field: self.kwargs[self.lookup_field]})
#         except self.get_queryset().model.DoesNotExist:
#             raise self.get_exception()
#
#     def get_object(self):
#         """
#         Returns the object the view is displaying.
#
#         You may want to override this if you need to provide non-standard
#         queryset lookups.  Eg if objects are referenced using multiple
#         keyword arguments in the url conf.
#         """
#         queryset = self.filter_queryset(self.get_queryset())
#         #
#         lookup_url_kwarg = self.lookup_field
#         obj = queryset.filter(**{self.lookup_field: self.kwargs[lookup_url_kwarg]}).first()
#         if obj is None:
#             return Http404
#
#         filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
#         obj = get_object_or_404(queryset, **filter_kwargs)
#         return obj