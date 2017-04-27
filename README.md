# django-api-doc

API docs for django

## Installation

Install using `pip`

```
pip install django_api_doc
```

or

```
git clone git@github.com:fanhan/django-api-doc.git

cd django-api-doc/

python setup.py install

```

## Example

Add `django_api_doc` to your INSTALLED_APPS setting.

```
INSTALLED_APPS = (
    ...
    'django_api_doc',
)
```

Now edit the your_project/urls.py module in your project:

```
urlpatterns = [
    ...
    url(r'^api-docs/', include('django_api_doc.urls', namespace='api_docs')),
]
```

In your project `urls.py`, you need set `name` or `namespace`

```
urlpatterns = [
    ...
    url(r'^common/', include('apps.test.urls', namespace='test')),
]
```

In `your_apps/urls.py`, you can set urlpatterns like this...

```
urlpatterns = [
    ...
    url(r'^$', views.TestIndex.as_view(), name='test_index'),
]
```


In `view.py`, please use the `markdown` to write comments

```python

class TestIndexView(View):
    """
    test
    """
    
    def get(self, request):
        """
        test index
        
        #### Param
        
        params | category | must | description
        ---- | ---- | ---- | ----
        null | null | null | null
        
        #### Return
            {
                "text": "test",
            }
        
        """
        pass
```

then, open the url `http://127.0.0.1:8000/api-docs/`, you can see like this
![api_doc_image](https://raw.githubusercontent.com/fanhan/django-api-doc/master/test/api_doc_test.png)

## Add some parameters

```
API_DOC_IGNORE_NAMESPACES = []          # ignore your_project/urls.py namespaces
API_DOC_TITLE = ''                      # doc html title
API_DOC_API_DOMAIN = 'http://api.com'   # api domain
API_DOC_SKIN = 'skin-blue'              # skin-blue skin-black skin-purple skin-yellow skin-red skin-green 
```
