from elasticsearch_dsl import Search, connections


connections.create_connection(hosts=['localhost'], timeout=20)


def search(pattern):
    """
    从ES中搜索博客文章的标题和内容
    """
    s = Search(index='blog').highlight_options(type='plain', pre_tags=['<em style="color:red">'], post_tags=['</em>']).\
        highlight('title', 'content').query('multi_match', query=pattern, fields=['title', 'content'])
    response = s.execute()
    return response
