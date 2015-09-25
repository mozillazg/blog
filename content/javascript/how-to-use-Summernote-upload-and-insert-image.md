title: 配置 Summernote 上传并插入本地图片
slug: how-to-use-Summernote-upload-and-insert-local-image
date: 2015-09-25
tags: Summernote

![Summernote-upload-and-insert-local-image-01.png](/static/images/javascript/Summernote-upload-and-insert-local-image-01.png)

本文将讲述如何在 summernote 中实现上传并插入本地图片的功能。


主要是通过设置 `onImageUpload` 事件回调函数来实现的：


      $('#editor').summernote({
        onImageUpload: function(files) {
          var $editor = $(this);
          // 构建一个 form 数据
          var data = new FormData()
          // 增加一个字段 fileup 值是待上传的文件的内容
          data.append('fileup', files[0])
          
          $.ajax({         // 上传文件到服务器端
            url: '/upload',
            method: 'POST',
            data: data,
            processData: false,      // 这两个比较关键，禁止处理 form 数据
            contentType: false,      // 
            success: function(data) {
                var imgURL = data.url;   // 获取服务端返回的图片地址
                // 插入图片
                $editor.summernote('insertImage', imgURL);
            };
          });
        }
      });


Demo: 

<a class="jsbin-embed" href="http://jsbin.com/taxire/embed">JS Bin on jsbin.com</a><script src="http://static.jsbin.com/js/embed.min.js?3.35.0"></script>


## 参考资料

* [Using amazon s3 storage with summernote #72](https://github.com/summernote/summernote/issues/72)