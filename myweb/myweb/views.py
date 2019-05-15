from django.views.generic import ListView
from django.http import JsonResponse, QueryDict
from django.db.models import Q
from pure_pagination.mixins import PaginationMixin
from .models import Cmdb, Task
from .forms import CmdbForm
import json


# from scripts.install import install
# from scripts import  Logger


# Create your views here.


class CmdbView(PaginationMixin, ListView):
    """
    cmdb列表
    """
    model = Cmdb
    template_name = 'cmdb/cmdb_list.html'
    context_object_name = 'cmdb_list'
    paginate_by = 2
    keyword = ''

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CmdbView, self).get_context_data(**kwargs)
        # print(context["paginator"])
        return context

    def get_queryset(self):
        queryset = super(CmdbView, self).get_queryset().order_by("-id")
        self.keyword = self.request.GET.get('keyword', '').strip()
        if self.keyword:
            queryset = queryset.filter(Q(Sn__icontains=self.keyword) |
                                       Q(Hostname__icontains=self.keyword) |
                                       Q(Ip__icontains=self.keyword))
        return queryset

    def post(self, request):
        form = CmdbForm(request.POST)
        if form.is_valid():
            form.save()
            res = {'code': 0, 'result': "添加资产成功"}
        else:
            res = {'code': 1, 'result': form.errors}
        return JsonResponse(res, safe=True)

    def delete(self, request, *args, **kwargs):
        webdata = QueryDict(request.body).dict()
        pk = webdata.get("id")
        try:
            self.model.objects.filter(id=pk).delete()
            res = {"code": 0, "result": "删除资产成功"}
        except:
            res = {"code": 1, "errmsg": "删除错误请联系管理员"}
        return JsonResponse(res, safe=True)

    def put(self, request, **kwargs):
        res = {'code': 0}
        webdata = QueryDict(request.body).dict()
        pk = webdata.pop('Id')
        try:
            self.model.objects.filter(id=pk).update(**webdata)
        except:
            res['code'] = 1
            res['error'] = "修改错误请联系管理员"
        return JsonResponse(res)


class Task(PaginationMixin, ListView):
    """
    task列表
    """
    model = Task
    template_name = 'task/task_list.html'
    context_object_name = 'task_list'
    paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(Task, self).get_context_data(**kwargs)
        return context

    def get_queryset(self):
        queryset = self.model.objects.all().order_by("-id")
        return queryset

    def create_task(self, data):
        """
        创建task
        :param data:{'operation_type': 'install', 'id': '4', 'raid': {'media_type': 'EMPTY', 'raid_level': 'RAID1'}, 'sn': '333', 'hostname': '333', 'OsVersion': '33', 'ethernet': {'inf0': {'Ip': '333', 'Netmask': '33', 'GW': '333', 'Mac': '333'}, 'ilo_info': {'ipaddr': '333', 'netmask': '333', 'gw': '333', 'mac_addr': '333'}, 'install_os': 'centos6.5', 'rootsize': '100G'}}
        :return: {'code': 0, 'result': {data:{id:1}}}
        """
        res = {'code': 1, 'result': ""}
        if not data:
            res['error'] = "参数错误"
            return res
        task_data = {}
        task_data["Cmdb_id"] = data.get("id", '')
        task_data["TaskID"] = data.get("sn", '')
        task_data["Taskname"] = data.get("operation_type", '')
        task_data["Taksstatus"] = 0
        try:
            obj = self.model.objects.create(**task_data)
            res['code'] = 0
            res["result"] = {"data": {"id": obj.id}}
            return res
        except Exception as e:
            res['error'] = e
            return res

    def update_task(self, data):
        """
        更新task状态
        :param data: {id:"1",Taksstatus:"xxxx"}
        :return: {'code': 0, 'result': "更新成功"}
        """
        res = {'code': 1, 'result': "", 'error': '参数错误'}
        if not data:
            return res
        id = data.get('id', "")
        if not id:
            return res
        Taksstatus = data.get("Taksstatus", "")
        try:
            self.model.objects.filter(id=id).update({"Taksstatus": Taksstatus})
            res['code'] = 0
            res["result"] = "更新状态成功"
            res.pop("error")
            return res
        except Exception as e:
            res["error"] = str(e)
            return res

        # logger = Logger.Logger().getlog()

    def delete(self, request, *args, **kwargs):
        webdata = QueryDict(request.body).dict()
        pk = webdata.get("id")
        try:
            self.model.objects.filter(id=pk).delete()
            res = {"code": 0, "result": "删除任务成功"}
        except:
            res = {"code": 1, "errmsg": "删除错误请联系管理员"}
        return JsonResponse(res, safe=True)


def AOC(request):
    if request.method == 'GET':
        # print (request)
        a = {'a': 1}
        print(a)
        # return restful.result(code=restful.Httpcode.paramserror,message="aa")
        return JsonResponse(a)

    if request.method == "POST":
        data = QueryDict(request.body).dict()['aa']
        data = json.loads(data)
        # task入库，返回id
        result = Task().create_task(data)
        if result.get("code", "") != 0:
            print("入库失败")
            return
        id = result["result"]["data"]["id"]
        print("id==>", id)
        # 更加id执行，然后更新任务状态，及创建任务详细信息

        r = data['operation_type']
        if r == "install":
            print("ok")
            # logger.info('接收安装参数，服务器开始安装')
            # result = install(data)

            # print ("-----------------------------------")
            # print (result)
            # logger.info(result)

        # print(type(data1))
        # d=re.sub("u'","\"",data)
        # d=re.sub("'","\"",d)
        # data1 = json.loads(d,encoding='utf-8')
        # t1 = aos.aos(data1)
        # print (t1)
        a = {"v": 1}
        return JsonResponse(a)
