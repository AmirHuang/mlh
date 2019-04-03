from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import serializers, status

from news.models import NewsModel, CategoryModel, CommentModel
from news.serializers import NewsSerializer, CategorySerializer, NewsDeatilSerializer, CommentSerializer, \
    FollowerNewsSerializer, UserInfoSerializer
from users.models import User


class IndexPage(ListAPIView):
    serializer_class = NewsSerializer

    def get_queryset(self, pk):
        if pk:
            return CategoryModel.objects.get(id=pk).news.order_by('update_time')
        return NewsModel.objects.filter(is_delete=False).order_by('-click')[:30]

    def get(self, request, pk=None):
        """获取新闻数据"""
        queryset = self.filter_queryset(self.get_queryset(pk))  # 查询出来的所有的新闻
        try:
            user = request.user
            user = User.objects.get(id=user.id)
            # 遍历这个新闻,看这个新闻被用户关注了没有,如果没关注,follow为False,否则为true
        except Exception as f:
            page = self.paginate_queryset(queryset)
            serializer = self.get_serializer(page, many=True)
            results = serializer.data
            for news in results:
                news['follow'] = False
                del news['followed_user']
            return self.get_paginated_response(results)
        else:
            user_data = UserInfoSerializer(user).data
            page = self.paginate_queryset(queryset)
            serializer = self.get_serializer(page, many=True)
            results = serializer.data
            for news in results:
                if user_data in news['followed_user']:
                    news['follow'] = True
                    del news['followed_user']
                else:
                    news['follow'] = False
                    del news['followed_user']
            return self.get_paginated_response(results)


class GetCategory(ListAPIView):
    pagination_class = None
    serializer_class = CategorySerializer
    queryset = CategoryModel.objects.all()


class GetNews(ListAPIView):
    serializer_class = NewsSerializer

    # 排序
    def get(self, request, pk=None):
        user = request.user
        self.queryset = CategoryModel.objects.get(id=pk).news.order_by('-update_time')
        return super().get(request)


class NewsAPIView(RetrieveAPIView):
    """单个新闻详情 """
    serializer_class = NewsDeatilSerializer

    queryset = NewsModel.objects.filter(is_delete=False)


class FollowedNewsAPIView(CreateAPIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        user = request.user
        self.permission_classes = [IsAuthenticated]
        if data['action'] == 'follow':
            news_id = data['news_id']
            try:
                news = user.like_news.get(id=news_id)
            except NewsModel.DoesNotExist:
                serializer = FollowerNewsSerializer(data={'like_news': news_id})
                serializer.is_valid(raise_exception=True)
                f = serializer.data
                news = NewsModel.objects.get(id=data['news_id'])
                user.like_news.add(news)
                data = {
                    'news_id': news_id,
                    'follow': True
                }
                return Response(data=data)
            raise serializers.ValidationError({'message': '已经关注过了'})
        elif data['action'] == 'remove':
            news_id = data['news_id']
            try:
                user.like_news.get(id=news_id)
            except NewsModel.DoesNotExist:
                return Response(data={"message": '没有关注过此新闻'}, status=status.HTTP_400_BAD_REQUEST)
            news = NewsModel.objects.get(id=data['news_id'])
            user.like_news.remove(news)
            data = {
                'news_id': news_id,
                'follow': False
            }
            return Response(data=data)
        else:
            raise serializers.ValidationError({"message": '请求参数错误'})


class CommentView(ListAPIView, CreateAPIView):
    serializer_class = CommentSerializer
    pagination_class = None

    def get(self, request, pk):
        # 查询这条新闻的所有评论
        self.queryset = NewsModel.objects.get(id=pk).comment.all().order_by('-create_time')
        return super().get(request)

    def get_permissions(self):
        m = self.request.method
        if m == 'POST':
            self.permission_classes = [IsAuthenticated]

        return super().get_permissions()
