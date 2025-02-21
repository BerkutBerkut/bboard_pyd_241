from django.urls import path, include
from django.views.generic.dates import WeekArchiveView, DayArchiveView
from django.views.generic.edit import CreateView

from rest_framework.routers import DefaultRouter

from bboard.models import Bb
from bboard.views import (index, by_rubric, 
                          BbCreateView,
                          add_and_save, bb_detail, 
                          BbRubricBbsView,
                          BbDetailView, BbEditView,
                          BbDeleteView, BbIndexView,
                          BbRedirectView, edit, 
                          rubrics, bbs)
# from bboard.views import add_icecream
from bboard.views import  manage_icecreams, success_view
# from bboard.views import create_icecream
from bboard.views import icecream_list, search
from bboard.views import user_info
from bboard.views import (
    return_string,
    return_html,
    return_json,
    show_request_parameters,
    log_request_data,
    my_login,
    my_logout,
    all_users_group_view,
    api_rubrics,
    api_rubric_detail,
    APIRubrics,
    APIRubricDetail,
    APIRubricViewSet,
    api_bbs,
    api_bb_detail,
    APIBbs,
    APIBbDetail,
    APIBbViewSet,
)
from django.views.decorators.cache import cache_page


app_name = 'bboard'

router = DefaultRouter()
router.register('rubrics', APIRubricViewSet)
router.register("bbs", APIBbViewSet)

urlpatterns = [
    # path("api/rubrics/<int:pk>/", api_rubric_detail),
    # path("api/rubrics/", api_rubrics),
    # path("api/bbs/<int:pk>/", api_bb_detail),
    # path("api/bbs/", api_bbs),
    # path("api/rubrics/<int:pk>/", APIRubrics.as_view()),
    # path("api/rubrics/", APIRubrics.as_view()),
    # path("api/bbs/<int:pk>/", APIBbs.as_view()),
    # path("api/bbs/", APIBbs.as_view()),
    # path("api/rubrics/<int:pk>/", APIRubricDetail.as_view()),
    # path("api/rubrics/", APIRubrics.as_view()),
    path("api/", include(router.urls)),
    # path("api/bbs/<int:pk>/", APIBbDetail.as_view()),
    # path("api/bbs/", APIBbs.as_view()),
    path("", my_login, name="home"),  # Перенаправление на авторизацию
    path("login/", my_login, name="login"),  # URL для входа
    path("logout/", my_logout, name="logout"),  # URL для выхода
    # path('<int:year>/week/<int:week>/',fe
    #      WeekArchiveView.as_view(model=Bb, date_field='published',
    #                              context_object_name='bbs')),
    # path('<int:year>/<int:month>/<int:day>/',
    #      DayArchiveView.as_view(model=Bb, date_field='published',
    #                             month_format='%m',
    #                             context_object_name='bbs')),
    path(
        "<int:year>/<int:month>/<int:day>/",
        BbRedirectView.as_view(),
        name="old_archive",
    ),
    path("rubrics/", rubrics, name="rubrics"),
    path("bbs/<int:rubric_id>/", bbs, name="bbs"),
    path("add/", BbCreateView.as_view(), name="add"),
    path("edit/<int:pk>/", BbEditView.as_view(), name="edit"),
    # path('edit/<int:pk>/', edit, name='edit'),
    path("delete/<int:pk>/", BbDeleteView.as_view(), name="delete"),
    path(
        "<int:rubric_id>/",
        BbRubricBbsView.as_view(),
        # cache_page(60 * 5)(BbRubricBbsView.as_view()),
        # cache_page(30)(BbRubricBbsView.as_view()),
        name="by_rubric",
    ),
    path("detail/<int:pk>/", BbDetailView.as_view(), name="detail"),
    # path("create_icecream/", create_icecream, name="create_icecreame"),
    path("manage_icecreams/", manage_icecreams, name="manage_icecreams"),
    path("success/", success_view, name="success"),
    # path('add_icecream/', add_icecream, name='add_icecream'),
    path("icecream_list/", icecream_list, name="icecream_list"),
    path("user_info/<int:user_id>/", user_info, name="user_info"),
    path("search/", search, name="search"),
    path("index", index, name="index"),  # Главная страница
    # path('', BbIndexView.as_view(), name='index'),
    path(
        "show_request_parameters/",
        show_request_parameters,
        name="show_request_parameters",
    ),
    path(
        "log_request_data/",
        log_request_data,
        name="log_request_data",
    ),
    path("return_string/", return_string, name="return_string"),
    path("return_html/", return_html, name="return_html"),
    path("return_json/", return_json, name="return_json"),
    path("context_user_groups/", all_users_group_view, name="context_user_groups"),
]
