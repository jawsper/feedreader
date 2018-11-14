from django.urls import path
from .views import auth, options, outline, post


urlpatterns = [
    path('auth/token/', auth.token, name='auth_token'),
    path('auth/verify/', auth.verify, name='auth_verify'),

    path('get_options/', options.GetOptionsView.as_view(), name='get_options'),  # unused
    path('get_option/', options.GetOptionView.as_view(), name='get_option'),
    path('set_option/', options.SetOptionView.as_view(), name='set_option'),

    path('feed/add/', outline.AddFeedView.as_view(), name='feed_add'),
    path('get_unread_count/', outline.GetUnreadCountView.as_view(), name='get_unread'),
    path('outlines/', outline.GetAllOutlinesView.as_view(), name='outline_get_all_outlines'),
    path('outline/get_all_posts/', outline.GetAllPostsView.as_view(), name='get_all_posts'),  # unused
    path('outline/get_starred_posts/', outline.GetStarredPostsView.as_view(), name='get_starred_posts'),  # unused
    path('outline/get_posts/', outline.GetPostsView.as_view(), name='get_posts'),
    path('outline/get_data/', outline.OutlineGetDataView.as_view(), name='get_outline_data'),  # unused
    path('outline/set/', outline.OutlineSetView.as_view(), name='outline_set'),
    path('outline/mark_as_read/', outline.OutlineMarkAsReadView.as_view(), name='outline_mark_read'),

    path('post/action/', post.PostActionView.as_view(), name='post_action')
]
