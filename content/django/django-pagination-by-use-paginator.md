Title: [django]使用 Paginator 实现分页功能
Date: 2013-01-26
Tags: python, django
Slug: django-pagination-by-use-paginator


在 django 中使用 Paginator 可以很方便的实现分页功能，下面就通过一个具体的例子来讲讲如何使用 Paginator。

## 在 view 中使用 Paginator

    :::python
    from django.core.paginator import Paginator
    from django.core.paginator import EmptyPage
    from django.core.paginator import PageNotAnInteger
    from hello.models import Topic


    def index(request):
        limit = 3  # 每页显示的记录数
        topics = Topic.objects.all()
        paginator = Paginator(topics, limit)  # 实例化一个分页对象

        page = request.GET.get('page')  # 获取页码
        try:
            topics = paginator.page(page)  # 获取某页对应的记录
        except PageNotAnInteger:  # 如果页码不是个整数
            topics = paginator.page(1)  # 取第一页的记录
        except EmptyPage:  # 如果页码太大，没有相应的记录
            topics = paginator.page(paginator.num_pages)  # 取最后一页的记录

        return render_to_response('index.html', {'topics': topics})

## 模板中的相关操作

    :::html+django
    {% for topic in topics.object_list %}
      <p>{{ topic.title }}</p>
    {% endfor %}

    <!-- 第一种分页显示方式 -->
    <p>
      {# topics.paginator.page_range 这个函数返回包含一个所有页码数的 range 对象 #}
      {# 即 range(1, topics.paginator.num_pages + 1) #}
      {% for page_number in topics.paginator.page_range %}
        {% ifequal page_number  topics.number %}
          {{ page_number }}
        {% else %}
          <a href="?page={{ page_number }}">{{ page_number }}</a>
        {% endifequal %}
      {% endfor %}
    </p>


    <!-- 另一种分页显示方式 -->
    <p>
    {% if topics.has_previous %}
      <a href="?page={{ topics.previous_page_number }}">Previous</a>
      {% endif %}
      {# topics.paginator.number_pages 返回总页数 #}
      Page {{ topics.number }} of {{ topics.paginator.num_pages }}.
    {% if topics.has_next %}
      <a href="?page={{ topics.next_page_number }}">Next</a>
    {% endif %}
    </p>

效果：

![django-pagination](/static/images/2013-1-26-django-pagination.png)

基于 django 1.4.3 的示例项目：[仓库](https://github.com/mozillazg/django-simple-projects/tree/master/projects/pagination) && [下载](/static/downloads/pagination.tar.gz) 。


## 参考

* [Pagination - Django Documentation](https://docs.djangoproject.com/en/1.4/topics/pagination)
