Title: [django]添加额外的 form 错误信息
Date: 2013-02-27
Tags: django, form, python
Slug: django-add-extra-error-messages


通过两种方法给 Django 表单添加额外的错误信息。

第一种方法，使用 form 自定义校验（更详细的请查看 [django 官方文档](https://docs.djangoproject.com/en/dev/ref/forms/validation/)）：

定义 `clean` 方法：

    :::python
    class RegisterForm(forms.Form):
        # ...

        def clean(self):
            cleaned_data = super(RegisterForm, self).clean()
            email = cleaned_data.get('email', '')
            username = cleaned_data.get('username', '')

            re_username = r'^[a-zA-Z\d][-a-zA-Z\d]*$'

            if User.objects.filter(email=email).exists():
                msg = 'This email address already exists!'
                self._errors['email'] = self.error_class([msg])
                del cleaned_data['email']

            elif not re.match(re_username, username):
                msg = ('Username may only contain alphanumeric characters or'
                       'dashes and cannot begin with a dash')
                self._errors['username'] = self.error_class([msg])
                del cleaned_data['username']

            # ...

            return cleaned_data

定义 `clean_` 方法：

    :::python
    class SendForm(forms.Form):
        # ...

        def clean_recipient(self):
            data = self.cleaned_data['recipient']
            if not User.objects.filter(username=data).exists():
                raise forms.ValidationError("This user doesn't exists!")

            return data


    def send(request, template_name='message/send.html', extra_context=None):
        if request.method == 'POST':
            form = SendForm(request.POST)
            if form.is_valid():
                # ....
                recipient = form.cleaned_data['recipient']

                recipient = User.objects.get(username=recipient)
                # ...
                return HttpResponseRedirect(reverse_lazy('inbox'))
        else:
            form = SendForm()

        context = {
            'form': form,
        }
        if extra_context:
            context.update(extra_context)
        return render_to_response(template_name, context,
                                  context_instance=RequestContext(request))

第二种方法，更新 form.errors 字典：

    :::python
    from django.forms.util import ErrorList


    def send(request, template_name='message/send.html', extra_context=None):
        if request.method == 'POST':
            form = SendForm(request.POST)
            if form.is_valid():
                # ....
                recipient = form.cleaned_data['recipient']

                try:
                    recipient = User.objects.get(username=recipient)
                except ObjectDoesNotExist:
                    request.method = 'GET'
                    error_msg = ["This user doesn't exists!"]
                    form.errors['recipient'] = ErrorList(error_msg)
                    extra_context = {'form': form}
                    return send(request, template_name, extra_context)

                # ...
                return HttpResponseRedirect(reverse_lazy('inbox'))
        else:
            form = SendForm()

        context = {
            'form': form,
        }
        if extra_context:
            context.update(extra_context)
        return render_to_response(template_name, context,
                                  context_instance=RequestContext(request))

## 参考

* [Form and field validation | Django documentation | Django](https://docs.djangoproject.com/en/dev/ref/forms/validation/)
* [django/django/forms/forms.py at master · django/django · GitHub](https://github.com/django/django/blob/master/django/forms/forms.py)
* [django/django/forms/util.py at master · django/django · GitHub](https://github.com/django/django/blob/master/django/forms/util.py)
