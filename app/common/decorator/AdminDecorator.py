from django.conf import settings
from django.contrib.admin import ModelAdmin
from django.contrib.admin import TabularInline
from django.contrib.admin.sites import AdminSite, site as default_site
from django.db.models import Field
from django.db.models.fields.related import ManyToManyField

from app.common.exceptionbox.errors import InternalServerError


def custom_admin_decorator(register_model=None, site=None, has_delete_action=True, auto_actions=True,
                           auto_list_display_and_filter=True, has_add_permission=True, auto_select_related=True,
                           auto_inline=True, auto_editable=True, auto_readonly=True):
    """
    自定义装饰器，用于增强 admin 中 model 注册的一些操作
    """

    def _model_admin_wrapper(admin_class):
        # 处理删除操作的逻辑
        if not has_delete_action:
            _override_get_actions(admin_class)

        # 自动添加 actions
        if auto_actions:
            _add_actions(admin_class, register_model)

        # 自动添加 list_display 和 list_filter
        if auto_list_display_and_filter:
            _add_list_display_and_filter(admin_class, register_model)

        # 处理添加权限
        if not has_add_permission:
            admin_class.has_add_permission = lambda self, request, obj=None: False

        # 注册模型
        if register_model:
            _register_model(admin_class, register_model, site)

        # 处理 select_related
        if auto_select_related:
            _handle_select_related(admin_class, register_model)

        # 处理 inline
        if auto_inline:
            _handle_inline(admin_class, register_model)

        # 处理可编辑字段
        if auto_editable:
            _handle_editable(admin_class, register_model)

        # 处理只读字段
        if auto_readonly:
            _handle_readonly(admin_class, register_model)

        return admin_class

    return _model_admin_wrapper


def _override_get_actions(admin_class):
    original_get_actions = admin_class.get_actions

    def get_actions_without_delete_selected(self, request):
        actions = original_get_actions(self, request)
        actions.pop('delete_selected', None)
        return actions

    debug_mode = settings.DEBUG
    if not debug_mode:
        admin_class.get_actions = get_actions_without_delete_selected


def _add_actions(admin_class, register_model):
    original_actions = list(getattr(admin_class, 'actions', []))

    for attr_name in dir(register_model):
        attr = getattr(register_model, attr_name)
        if _is_action(attr):
            original_actions.append(attr_name)

    for attr_name in dir(admin_class):
        if attr_name != "action_checkbox":
            attr = getattr(admin_class, attr_name)
            if _is_action(attr):
                original_actions.append(attr_name)

    admin_class.actions = original_actions


def _is_action(attr):
    return hasattr(attr, 'short_description') and hasattr(attr, 'allowed_permissions')


def _add_list_display_and_filter(admin_class, register_model):
    original_list_display = list(getattr(admin_class, 'list_display', []))
    original_list_filter = list(getattr(admin_class, 'list_filter', []))

    if adminMeta := getattr(register_model, 'AdminMeta', None):
        if filter_fields := getattr(adminMeta, 'filter_fields', None):
            original_list_filter.extend(filter_fields)

    field_names = [field.attname for field in register_model._meta.fields]
    non_field_attrs = set(dir(register_model)) - set(field_names)

    for attr_name in field_names:
        attr = getattr(register_model, attr_name, None)
        if _should_add_list_display(attr):
            original_list_display.append(attr_name)
        if _should_add_list_filter(attr):
            original_list_filter.append(attr_name)

    for attr_name in non_field_attrs:
        attr = getattr(register_model, attr_name, None)
        if _should_add_list_display(attr):
            original_list_display.append(attr_name)
        if _should_add_list_filter(attr):
            original_list_filter.append(attr_name)

    admin_class.list_display = sorted(original_list_display)
    admin_class.list_filter = original_list_filter


def _should_add_list_display(attr):
    return isinstance(attr, Field) and not isinstance(attr, ManyToManyField) or \
        (hasattr(attr, 'short_description') and not hasattr(attr, 'allowed_permissions'))


def _should_add_list_filter(attr):
    return hasattr(attr, 'choices') and getattr(attr, 'choices', None)


def _register_model(admin_class, register_model, site):
    admin_site = site or default_site
    if not isinstance(admin_site, AdminSite):
        raise ValueError("site must subclass AdminSite")
    if not issubclass(admin_class, ModelAdmin):
        raise ValueError("Wrapped class must subclass ModelAdmin.")
    admin_site.register(register_model, admin_class=admin_class)


def _handle_select_related(admin_class, register_model):
    if adminMeta := getattr(register_model, 'AdminMeta', None):
        if hasattr(adminMeta, 'select_related_fields'):
            select_related_fields = adminMeta.select_related_fields

            def get_queryset(self, request):
                qs = super().get_queryset(request)
                return qs.select_related(*select_related_fields)

            admin_class.get_queryset = get_queryset


def _handle_inline(admin_class, register_model):
    def tabularInlineClassFactory(config: dict):
        if config.get('extra') is None:
            config['extra'] = 0
        if config.get('model') is None:
            raise InternalServerError("model is required")
        return type(f"{config['model'].__name__}TabularInline", (TabularInline,), config)

    if adminMeta := getattr(register_model, 'AdminMeta', None):
        if tabularInlineConfig := getattr(adminMeta, 'tabularInlineConfig', None):
            original_inlines = list(getattr(admin_class, 'inlines', []))
            for value in tabularInlineConfig.values():
                original_inlines.append(tabularInlineClassFactory(value))
            admin_class.inlines = original_inlines


def _handle_editable(admin_class, register_model):
    if adminMeta := getattr(register_model, 'AdminMeta', None):
        if list_editable_fields := getattr(adminMeta, 'list_editable_fields', None):
            original_list_editable = list(getattr(admin_class, 'list_editable', []))
            for value in list_editable_fields:
                if value not in original_list_editable:
                    original_list_editable.append(value)
            admin_class.list_editable = original_list_editable


def _handle_readonly(admin_class, register_model):
    if adminMeta := getattr(register_model, 'AdminMeta', None):
        if readonly_fields := getattr(adminMeta, 'readonly_fields', None):
            original_readonly_fields = list(getattr(admin_class, 'readonly_fields', []))
            for value in readonly_fields:
                if value not in original_readonly_fields:
                    original_readonly_fields.append(value)
            admin_class.readonly_fields = original_readonly_fields
