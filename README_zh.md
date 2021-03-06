# django-api-doc

一个基于django自动生成文档的项目

## 如何安装

可以使用pip安装

```
pip install django_api_doc
```

或者

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
    'django_api_doc',
)
```

设置 url

```
urlpatterns = [
    ...
    url(r'^api-docs/', include('django_api_doc.urls', namespace='api_docs')),
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

浏览器打开 `http://127.0.0.1:8000/api-docs/`就可以看到文档目录了, 例如：

![api_doc_image](https://raw.githubusercontent.com/fanhan/django-api-doc/master/test/api_doc_test.png)


#### 新增一些参数

```
API_DOC_IGNORE_NAMESPACES = []              # 列表里的namespaces将不会生成文档
API_DOC_TITLE = ''                          # 文档的标题
API_DOC_API_DOMAIN = 'http://api.com'       # API域名
API_DOC_SKIN = 'skin-blue'                  # skin-blue skin-black skin-purple skin-yellow skin-red skin-green 
```
