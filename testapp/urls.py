from django.urls import path

from testapp.views import AdvUse, Spare, Machine, SMS

app_name = "testapp"

# vals = {'mode': 'index'}

urlpatterns = [
    path("add/", AdvUse.as_view(), name="add"),
    # path("<int:rubric_id>/", by_rubric, vals, name="by_rubric"),
    path("<int:rubric_id>/", by_rubric, name="by_rubric"),
    path("", index, name="index"),
]
