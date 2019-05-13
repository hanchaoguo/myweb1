from django.shortcuts import render
from django.views.generic import View, ListView
from django.http import JsonResponse, QueryDict
from .models import Cmdb
from .forms import CmdbForm
import json
import re



# Create your views here.


class CmdbView(ListView):
    """
    cmdb列表
    """
    model = Cmdb
    template_name = 'books/book_list.html'
    context_object_name = 'cmdb_list'
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CmdbView, self).get_context_data(**kwargs)
        return context

    def get_queryset(self):
        queryset = self.model.objects.all()
        return queryset

    def post(self, request):
        form = CmdbForm(request.POST)
        print (form)
        if form.is_valid():
            form.save()
            res = {'code': 0, 'result': "添加资产成功"}
        else:
            res = {'code': 0, 'result': form.errors}
        return JsonResponse(res, safe=True)

    def delete(self, request, *args, **kwargs):
        webdata = QueryDict(request.body).dict()
        pk = webdata.get("id")
        try:
            self.model.objects.filter(Sn=pk).delete()
            res = {"code": 0, "result": "删除资产成功"}
        except:
            res = {"code": 1, "errmsg": "删除错误请联系管理员"}
        return JsonResponse(res, safe=True)

    def put(self, request, **kwargs):
        res = {'code': 0}
        webdata = QueryDict(request.body).dict()
        pk = webdata.pop('Sn')
        print(webdata)
        try:
            self.model.objects.filter(Sn=pk).update(**webdata)
        except:
            res['code'] = 1
            res['error'] = "修改错误请联系管理员"
        return JsonResponse(res)


def AOC(request):
    if request.method=='GET':
         #print (request)
         a = {'a':1}
         print  (a)
         #return restful.result(code=restful.Httpcode.paramserror,message="aa")
         return JsonResponse(a)

    if request.method=="POST":
         data = (request.POST['data'])
         d=re.sub("u'","\"",data)
         d=re.sub("'","\"",d)
         data1 = json.loads(d,encoding='utf-8')



         a = {"v":1}
         return JsonResponse(a)



