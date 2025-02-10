from django.contrib import admin
from django.db.models import F

from bboard.models import Rubric, Bb
from testapp.models import Machine, Spare


# @admin.display(description='Название и рубрика')
# def title_and_rubric(rec):
#     return f'{rec.title} ({rec.rubric.name})'

class PriceListFilter(admin.SimpleListFilter):
    title = 'Категория цен'
    parameter_name = 'price'

    def lookups(self, request, model_admin):
        return (
            ("low", "Низкая"),
            ("medium", "Средняя"),
            ("high", "Высокая"),
        )

    def queryset(self, request, queryset):
        if self.value() == 'low':
            return queryset.filter(price__lt=500)
        elif self.value() == 'medium':
            return queryset.filter(price__gte=500,
                                   price__lte=5000)
        elif self.value()  == 'high':
            return queryset.filter(price__gt=5000)

@admin.action(description='Уменьшить цену вдое')
def discount(modeladmin, request, queryset):
    f = F('price')
    for rec in queryset:
        # rec.price = f / 2
        rec.save()
    modeladmin.message_user(request, 'Действие выполнено!')

# class BbInLine(admin.TabularInline):
class BbInLine(admin.StackedInline):
    model = Bb
    extra = 1

    def get_extra(self, request, obj=None, **kwargs):
        if obj:
            return 3
        else:
            return 10


@admin.register(Rubric)
class RubricAdmin(admin.ModelAdmin):
    list_display = ("__str__", "order")
    search_fields = ('name',)
    # inlines = [BbInLine]
    inlines = (BbInLine,)

    def get_inlines(self, request, obj=None):
        if obj:
            return ()
        else:
            return (BbInLine)


# @admin.register(Bb, Rubric, Machine, Spare)
@admin.register(Bb)
class BbAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'price', 'published', 'rubric')
    # list_display = ("title_and_price", "content", "published", "rubric")
    # list_display = ("title_and_rubric", "content", 'price', 'published')

    @admin.display(description="Название и рубрика", ordering='title')
    def title_and_rubric(self, rec):
        return f"{rec.title} ({rec.rubric.name})"

    # title_and_rubric.short_description = 'Название и рубрика'
    # title_and_rubric.admin_order_field = 'title'

    # def get_list_display(self, request):
    #     ld = ['title', 'content', 'price']
    #     if request.user.is_superuser:
    #         ld += ['published', 'rubric']
    #     return ld

    # list_display_links = ('title', 'content')
    # list_display_links = None

    # def get_list_display_links(self, request, list_display):
    #     return list_display

    # list_editable = ('tiltle', 'content', 'price', 'rubric')
    # list_editable = ("content", "price", "rubric")

    # def get_queryset(self, request):
    #     qs = super().get_queryset(request)
    #     if request.user.is_superuser:
    #         return qs
    #     else:
    #         return qs.filter(is_hidden=False)

    search_fields = ('title', 'content')
    search_help_text = 'Поиск по названиям товаров и содержимому.'

    list_filter = (PriceListFilter,)

    autocomplete_fields = ('rubric',)

    #### Страницы добавления и правки ####
    # fields = ('title','price', 'content')
    # fields = (('title','price'), 'content')
    # fields = ('__str__', 'order')

    # def get_fields(self, request, obj=None):
    #     f = ['title', 'content', 'price']
    #     if not obj:
    #         f.append('rubric')
    #     return f

    # exclude = ('rubric', 'kind')
    # readonly_fields = ('published',)

    # fieldsets = (
    #     (None,
    #         {
    #             "fields": (("title", "rubric"), "content"),
    #             "classes": ("wide",),
    #         }),
    #     ("Дополнительные сведения", {
    #         'fields': ('price',),
    #         'description': 'Параметры необязательны для указания.'
    #     }),
    # )

    # def get_form(self, request, obj=None, **kwargs):
    #     if obj:
    #         return BbModelForm
    #     else:
    #         return BbAddModelForm

    # radio_fields = {'kind': admin.HORIZONTAL,
    #                 'rubric': admin.VERTICAL}

    actions = (discount,)


# admin.site.register(Rubric, RubricAdmin)
# admin.site.register(Bb, BbAdmin)
