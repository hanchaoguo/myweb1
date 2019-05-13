from django.forms import ModelForm
from .models import Cmdb, Task


class CmdbForm(ModelForm):
    class Meta:
        model = Cmdb
        fields = "__all__"


class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = "__all__"
