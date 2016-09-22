# django-api-doc

一个基于django自动生成文档的项目, 目前基本功能有,但是前端比较丑

## 如何安装

因为项目暂时不够满意,所以暂时没有使用pip安装

```
git clone git@github.com:fanhan/django-api-doc.git

cd django-api-doc/

python setup.py install

```

## 怎么使用

将`django_api_doc` 添加到settings中

```
INSTALLED_APPS = (
    ...
    'django-api-doc',
)
```

设置 url

```
urlpatterns = [
    ...
    url(r'^api-docs/', include('django-api-doc.urls', namespace='api_docs')),
]
```

在你的url.py里,需要把name,namespace写上

```
urlpatterns = [
    ...
    url(r'^common/', include('apps.test.urls', namespace='test')),
]
```
在apps/test/urls.py里

```
urlpatterns = [
    ...
    url(r'^$', views.TestIndex.as_view(), name='test_index'),
]
```


在view.py里用markdown语法写注释

```python

class TestIndexView(View):
    """
    test
    """
    
    def get(self, request):
        """
        test index
        
        #### 请求参数
        
        字段 | 类型 | 必须 | 说明
        ---- | ---- | ---- | ----
        无 | 无 | 无 | 无
        
        #### 返回值
            {
                "text": "test",
            }
        
        """
        pass
```



## 目前存在哪些问题

1. 分析urlpatterns代码比较混乱
2. 日志文档前端样式需要调整
3. url_pattern或者reverse得到url的方法不够好

