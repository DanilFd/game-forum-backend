from math import ceil

from comments.models import NewsComment
from comments.serializers import ListNewsCommentSerializer, ListBlogCommentSerializer

page_size = 10


def paginate_comments(root_comments: list[NewsComment], page_number: int, context, is_news: bool):
    paginated_comments = dict(
        comments_count=0,
        results=[]
    )
    current_page_ = dict(
        count=0,
        number=1,
        comments=[]
    )
    comments_is_set = False

    def set_comments():
        if is_news:
            paginated_comments['results'] = ListNewsCommentSerializer(
                current_page_['comments'],
                many=True,
                context=context
            ).data
        else:
            paginated_comments['results'] = ListBlogCommentSerializer(
                current_page_['comments'],
                many=True,
                context=context
            ).data

    def get_page(comments: list[NewsComment]):
        nonlocal comments_is_set

        for comment in comments:
            paginated_comments['comments_count'] += 1
            current_page_['count'] += 1
            current_page_['comments'].append(comment)

            if current_page_['count'] == page_size:  # СОБРАЛИ СТРАНИЦУ
                if current_page_['number'] == page_number:  # та самая страница
                    comments_is_set = True
                    set_comments()

                current_page_['count'] = 0
                current_page_['comments'] = []
                current_page_['number'] += 1

            get_page(comment.children.all())

    get_page(root_comments)
    page_count = ceil(paginated_comments['comments_count'] / page_size)
    if not comments_is_set and page_number <= page_count:
        set_comments()

    return paginated_comments
