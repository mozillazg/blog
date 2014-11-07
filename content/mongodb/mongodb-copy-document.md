Title: [mongodb]复制文档（document）
Date: 2014-10-27
Tags: 
Slug: mongodb-copy-document

可以通过下列命令复制文档

    > use db1
    > var docs=db.doc1.find();

    > use db2;
    > docs.forEach(function(doc){
        db.doc2.insert(doc); 
    } );

