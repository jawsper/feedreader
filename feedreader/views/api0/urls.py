from django.conf.urls import patterns, url

urlpatterns = patterns( 'feedreader.views.api0',
	url( r'^outlines/', 'outline.get_all_outlines' ),
	url( r'^get_options/$', 'get_options' ),
	url( r'^get_unread_count/$', 'get_unread' ),
	url( r'^get_option/$', 'get_option', name = 'get_option' ),
	url( r'^set_option/$', 'set_option', name = 'set_option' ),
	url( r'^outline/(?P<outline_id>\d+)/get_posts/$', 'outline.get_posts', name = 'get_posts' ),
	url( r'^outline/(?P<outline_id>\d+)/get_data/$', 'outline.get_outline_data', name = 'get_outline_data' ),
	url( r'^outline/(?P<outline_id>\d+)/set/$', 'outline.outline_set', name = 'outline_set' ),
	url( r'^outline/(?P<outline_id>\d+)/mark_as_read/', 'outline.outline_mark_as_read', name = 'outline_mark_as_read' ),
	url( r'^post/(?P<post_id>\d+)/action/(?P<action>[a-z_]+)/$', 'post.action' )
)
