from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

class PageInfo:
    """分页信息"""
    def __init__(self, queryset, page=1, page_size=10):
        self.paginator = Paginator(queryset, page_size)
        
        try:
            self.page = self.paginator.page(page)
        except PageNotAnInteger:
            self.page = self.paginator.page(1)
        except EmptyPage:
            self.page = self.paginator.page(self.paginator.num_pages)
    
    def get_data(self):
        """获取分页数据"""
        return {
            'total': self.paginator.count,
            'page_size': self.paginator.per_page,
            'current_page': self.page.number,
            'total_pages': self.paginator.num_pages,
            'results': list(self.page.object_list),
            'has_next': self.page.has_next(),
            'has_previous': self.page.has_previous(),
        } 