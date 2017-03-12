from django.conf.urls import url
from .views import auth, options, outline, post


urlpatterns = [
    url(r'^auth/token/$', auth.token, name='auth_token'),
    url(r'^auth/verify/$', auth.verify, name='auth_verify'),

    url(r'^get_options/$', options.GetOptionsView.as_view(), name='get_options'),  # unused
    url(r'^get_option/$', options.GetOptionView.as_view(), name='get_option'),
    url(r'^set_option/$', options.SetOptionView.as_view(), name='set_option'),

    url(r'^feed/add/$', outline.AddFeedView.as_view(), name='feed_add'),
    url(r'^get_unread_count/$', outline.GetUnreadCountView.as_view(), name='get_unread'),
    url(r'^outlines/', outline.GetAllOutlinesView.as_view(), name='outline_get_all_outlines'),
    url(r'^outline/get_all_posts/$', outline.GetAllPostsView.as_view(), name='get_all_posts'),  # unused
    url(r'^outline/get_starred_posts/$', outline.GetStarredPostsView.as_view(), name='get_starred_posts'),  # unused
    url(r'^outline/get_posts/$', outline.GetPostsView.as_view(), name='get_posts'),
    url(r'^outline/get_data/$', outline.OutlineGetDataView.as_view(), name='get_outline_data'),  # unused
    url(r'^outline/set/$', outline.OutlineSetView.as_view(), name='outline_set'),
    url(r'^outline/mark_as_read/$', outline.OutlineMarkAsReadView.as_view(), name='outline_mark_read'),

    url(r'^post/action/$', post.PostActionView.as_view(), name='post_action')
]
