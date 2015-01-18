/*
	File: outline.js
	Copyright: 2013 Jasper Seidel
	License: MIT
*/

/* globals */
var g_outline_id = null;
var g_outline_data = null;
var g_current_post = null;
var g_limit = 10;

/* directly after load init everything */

$(function()
{
	$('body').keypress(function(e)
	{
		switch(String.fromCharCode(e.which))
		{
			case 'r':
				$('#button_refresh').click();
				break;
			case 'j':
				move_post(+1);
				break;
			case 'k':
				move_post(-1);
				break;
			case 'f':
				$('body').toggleClass('fullscreen');
				if($('body').hasClass('fullscreen')) $('#content').focus();
				break;
			case 'm':
				if(g_current_post != null)
				{
					var cb = g_current_post.find('.footer .action.read');
					cb.prop('checked', !cb.prop('checked'));
					set_post_read_state(post_get_id(g_current_post), cb.is(':checked') ? 1 : 0);
				}
				break;
			case 's':
				if(g_current_post != null)
				{
					var cb = g_current_post.find('.footer .action.starred');
					cb.prop('checked', !cb.prop('checked'));
					set_post_starred_state(post_get_id(g_current_post), cb.is(':checked') ? 1 : 0);
				}
				break;
			case 'v':
				if(g_current_post != null)
				{
					window.open(g_current_post.find('.link a').attr('href'), '_blank');
				}
				break;
			default: return true; // don't care
		}
		//e.preventDefault();
	});
	$( '#button_refresh' ).click( function() { load_outline( g_outline_id, true ); } );
	$( '#button_mark_all_as_read' ).click( function() { mark_all_as_read( g_outline_id ); } );
	$( '#button_show_only_new' ).click( function() { set_outline_param( g_outline_id, 'show_only_new' ); } );
	$( '#button_sort_order' ).click( function() { set_outline_param( g_outline_id, 'sort_order' ); } );
	$('#button_toggle_fullscreen').click(function(){
		$('body').toggleClass('fullscreen');
		if($('body').hasClass('fullscreen'))
			$('#content').focus();
	});
	$('#button_prev_post').click(function(){ move_post(-1) });
	$('#button_next_post').click(function(){ move_post(+1) });
	$( '#load_more_posts a' ).click( function() { load_more_posts( g_outline_id, null, null ); } );
});

/* outline functions */

function set_outline( a_outline_id )
{
	g_outline_id = a_outline_id;
	load_outline( g_outline_id, false );
}

function set_outline_param( a_outline_id, key, value, no_load )
{
	if( !a_outline_id ) return;
	data = { outline: a_outline_id, 'action': key };
	if( value ) data['value'] = value;
	
	api_request( 'outline_set', data, function( data )
	{
		if( !data.error )
		{
			if( !no_load ) load_outline( a_outline_id, true );
		}
	});
}


function set_outline_data( a_outline_id, data )
{
	g_outline_data = data;
	$( '#outline_title > a' ).text( data.title ).attr( 'href', data.htmlUrl );
	update_outline_unread_count();
	$( '#button_sort_order' ).button( 'option', 'label', data.sort_order == 'ASC' ? 'Oldest first' : 'Newest first' );
	
	get_unread_counts( a_outline_id );
}

function set_outline_unread_count(count)
{
	g_outline_data.unread_count = count;
	update_outline_unread_count();
}
function update_outline_unread_count()
{
	$('#button_show_only_new').button('option', 'label', g_outline_data.show_only_new ? g_outline_data.unread_count + ' new item' + ( g_outline_data.unread_count != 1 ? 's' : '' ) : 'All items' );
}

function get_outline_data( a_outline_id )
{
	if( !a_outline_id ) return;
	api_request( 'get_outline_data', { outline: a_outline_id }, function( data )
	{
		if( !data.error )
		{
			set_outline_data( a_outline_id, data );
		}
	});
}

function count_visible_unread_posts()
{
	// get all unchecked posts and skip those
	// or just all posts
	var count = $(g_outline_data.show_only_new ? '#posts .post .action.read:not(:checked)' : '#posts .post').length;
	return count;
}

function load_outline( a_outline_id, forced_refresh )
{
	if( !a_outline_id ) return;

	$('#load_more_posts').hide();
	$('#no_more_posts').hide();

	api_request( 'get_posts', { limit: g_limit, outline: a_outline_id, forced_refresh: forced_refresh }, function( data )
	{
		if( !data.error )
		{
			if( g_outline_id != a_outline_id ) return; // attempt to prevent slow loads from overwriting the current outline
			set_outline_data( a_outline_id, data );
			
			$( '#content' ).scrollTop( 0 );
			$( '#posts' ).empty();
			g_current_post = null;
			if( data.posts.length > 0 )
			{
				$.each( data.posts, function( k, post )
				{
					$( '#posts' ).append( post_build_html( post, data.is_feed ) );
					post_attach_handlers( post.id );
				});
				$('#no_more_posts').hide();
			}
			else
			{
				$('#no_more_posts').show();
			}
			$('#load_more_posts').show();
		}
	});
}


function mark_all_as_read( a_outline_id )
{
	if( !a_outline_id ) return;
	api_request( 'outline_mark_read', { outline: a_outline_id }, function( data )
	{
		if( !data.error ) load_outline( a_outline_id, true );
	});
}

function load_more_posts( a_outline_id, on_success, on_failure )
{
	if( !a_outline_id ) return;

	$('#load_more_posts').hide();
	$('#no_more_posts').hide();

	skip = count_visible_unread_posts();

	api_request( 'get_posts', { outline: a_outline_id, skip: skip, limit: g_limit }, function( data )
	{
		if( !data.error )
		{
			if( data.posts.length > 0 )
			{
				$.each( data.posts, function( k, post )
				{
					$( '#posts' ).append( post_build_html( post, data.is_feed ) );
					post_attach_handlers( post.id );
				});
				$('#no_more_posts').hide();
				if( on_success ) on_success();
			}
			else
			{
				$('#no_more_posts').show();
				if( on_failure ) on_failure();
			}
			$('#load_more_posts').show();
		}
	});
}

/* post functions */

function post_get_id( post )
{
	return post && post.attr('id').replace( /[^\d]/g, '' );
}
function id_get_post( post_id )
{
	return $('#post_' + post_id );
}

function set_post_read_state( post_id, state )
{
	set_post_attr_state( post_id, 'read', state );
	if( !state )
	{
		var post = id_get_post( post_id );
		post.data( 'do-not-auto-mark-read', true );
	}
	// only visually update the unread count.
	// TODO: every now and then actually do API hit...?
	// Maybe better on a timer...
	g_outline_data.unread_count += state ? -1 : 1;
	update_outline_unread_count();
}
function set_post_starred_state( post_id, state )
{
	set_post_attr_state( post_id, 'starred', state );
}
function set_post_attr_state( post_id, attr, state )
{
	api_request( 'post_action', { post: post_id, action: attr, state: state }, function( data )
	{
		show_result( data );
	});
}

function select_post_by_id( post_id )
{
	select_post( id_get_post( post_id ) );
}

function select_post( post )
{	
	if( g_current_post != null && post.length > 0 && g_current_post.attr( 'id' ) == post.attr( 'id' ) ) return;
	
	if( g_current_post != null ) g_current_post.removeClass( 'current' );
	if( post.length == 0 )
	{
		g_current_post = null;
		return;
	}
	g_current_post = post;
	g_current_post.addClass( 'current' );
	
	post[0].scrollIntoView( true );
	
	if( !post.data( 'do-not-auto-mark-read' ) && !post.find( '.footer .action.read' ).attr( 'checked' ) )
	{
		post.find( '.footer .action.read' ).attr( 'checked', true );
		set_post_read_state( post_get_id( post ), 1 );
	}
}

function post_attach_handlers( post_id )
{
	id_get_post( post_id ).click( function()
	{
		select_post_by_id( post_id );
	} )
	.find( '.footer .action.starred' ).click(function()
	{
		set_post_starred_state( post_id, $(this).is(':checked') ? 1 : 0 );
	}).end()
	.find( '.footer .action.read' ).click(function()
	{
		set_post_read_state( post_id, $(this).is(':checked') ? 1 : 0 );
	}).end()
	.find('.body .content a').attr('target', '_blank');
}

function post_build_html( post, is_feed )
{
	var postTemplate = $( "#postTemplate" ).html();
	var template = postTemplate.format( 
		post.id,
		post.link,
		post.title,
		post.pubDate,
		( is_feed ? '' : 'from ' + post.feedTitle + ' ' ) + ( post.author ? 'by <span class="authorName">{0}</span>'.format( post.author ) : '' ),
		post.content,
		post.starred ? ' checked="checked"' : '',
		post.read ? ' checked="checked"' : ''
	);
	return template;
}

function move_post( direction )
{
	if( direction > 0 )
	{
		if( g_current_post == null )
		{
			select_post( $('#posts .post').first() );
		}
		else
		{
			var next_post = g_current_post.next( '.post' );
			if( next_post.length > 0 )
			{
				select_post( next_post );
				if( g_current_post.next( '.post' ).length == 0 )
				{
					load_more_posts( g_outline_id, null, null );
				}
			}
			else
			{
				load_more_posts( g_outline_id, function(){ move_post(+1) }, null );
			}
		}
	}
	else
	{
		if( g_current_post == null ) return; // can't do anything
		select_post( g_current_post.prev( '.post' ) );
	}
}

