/*
	File: outline.js
	Copyright: 2013 Jasper Seidel
	Licence: MIT
*/

/* globals */
var outline_id = null;
var current_post = null;

/* directly after load init everything */

$(function()
{
	$('body').keypress(function( e )
	{
		switch( e.which )
		{
			case 'r'.charCodeAt(0):
				$( '#button_refresh' ).click();
				break;
			case 'j'.charCodeAt(0):
				move_post( +1 );
				break;
			case 'k'.charCodeAt(0):
				move_post( -1 );
				break;
			case 'f'.charCodeAt(0):
				$('body').toggleClass( 'fullscreen' );
				if( $( 'body' ).hasClass( 'fullscreen' ) ) $( '#content' ).focus();
				break;
			case 'm'.charCodeAt(0):
				if( current_post != null )
				{
					var cb = current_post.find( '.footer .action.read' );
					cb.prop( 'checked', !cb.prop('checked' ) );
					mark_post_read_state( post_get_id( current_post ), cb.is(':checked') ? 1 : 0 );
				}
				break;
			case 's'.charCodeAt(0):
				if( current_post != null )
				{
					var cb = current_post.find( '.footer .action.starred' );
					cb.prop( 'checked', !cb.prop('checked' ) );
					//mark_post_starred_state( post_get_id( current_post ), cb.is(':checked') ? 1 : 0 );
				}
				break;
			case 'v'.charCodeAt(0):
				if( current_post != null )
				{
					window.open( current_post.find( '.link a' ).attr( 'href' ), '_blank' );
				}
				break;
			default: return true; // don't care
		}
		//e.preventDefault();
	});
	$( '#content' ).scroll( function()
	{
		$( '#scroll_pos' ).text( $( '#content' ).scrollTop() );
	});
	$( '#button_refresh' ).click( function() { load_outline( outline_id, true ); } );
	$( '#button_mark_all_as_read' ).click( function() { mark_all_as_read( outline_id ); } );
	$( '#button_show_only_new' ).click( function() { set_outline_param( outline_id, 'show_only_new' ); } );
	$( '#button_sort_order' ).click( function() { set_outline_param( outline_id, 'sort_order' ); } );
});

/* outline functions */

function set_outline( new_outline_id )
{
	outline_id = new_outline_id;
	load_outline( outline_id, false );
}

function set_outline_param( outline_id, key, value, no_load )
{
	if( !outline_id ) return;
	data = { 'action': key };
	if( value ) data['value'] = value;
	
	$.post( get_api_url( '/outline/' + outline_id + '/set/' ), data, function( result )
	{
		if( result == 'OK' )
		{
			if( !no_load ) load_outline( outline_id, true );
		}
	});
}


function set_outline_data( outline_id, data )
{
	$( '#outline_title > a' ).text( data.title ).attr( 'href', data.htmlUrl );
	$( '#button_show_only_new' ).button( 'option', 'label', data.show_only_new ? data.unread_count + ' new item' + ( data.unread_count != 1 ? 's' : '' ) : 'All items' );
	$( '#button_sort_order' ).button( 'option', 'label', data.sort_order == 'ASC' ? 'Oldest first' : 'Newest first' );
	
	get_unread_counts( outline_id );
}

function get_outline_data( outline_id )
{
	if( !outline_id ) return;
	api_request( '/outline/' + outline_id + '/get_data/', {}, function( data )
	{
		set_outline_data( outline_id, data );
	});
}

function load_outline( outline_id, forced_refresh )
{
	if( !outline_id ) return;
	api_request( '/outline/' + outline_id + '/get_posts/', { forced_refresh: forced_refresh }, function( data )
	{
		set_outline_data( outline_id, data );
		
		$( '#content' ).scrollTop( 0 );
		$( '#posts' ).empty();
		current_post = null;
		$.each( data.posts, function( k, post )
		{
			$( '#posts' ).append( post_build_html( post, data.is_feed ) );
			post_attach_handlers( post.id );
		});
	});
}


function mark_all_as_read( outline_id )
{
	if( !outline_id ) return;
	api_request( '/outline/' + outline_id + '/mark_as_read/', {}, function( data )
	{
		if( data.success ) load_outline( outline_id, true );
	});
}

function load_more_posts( outline_id, skip, on_complete )
{
	if( !outline_id ) return;
	api_request( '/outline/' + outline_id + '/get_posts/', { skip: skip }, function( data )
	{
		$.each( data.posts, function( k, post )
		{
			$( '#posts' ).append( post_build_html( post, data.is_feed ) );
			post_attach_handlers( post.id );
		});
		if( on_complete ) on_complete();
	});
}

/* post functions */

function post_get_id( post ) { return post && post.attr('id').replace( /[^\d]/g, '' ); }
function id_get_post( post_id ) { return $('#post_' + post_id ); }

function mark_post_read_state( post_id, state )
{
	set_post_attr_state( post_id, 'read', state );
	if( !state )
	{
		var post = id_get_post( post_id );
		post.data( 'do-not-auto-mark-read', true );
	}
}
function set_post_starred_state( post_id, state )
{
	set_post_attr_state( post_id, 'starred', state );
}
function set_post_attr_state( post_id, attr, state )
{
	api_request( '/post/' + post_id + '/action/' + attr + '/', { state: state }, function( data )
	{
		show_result( data );
		get_outline_data( outline_id );
	});
}

function select_post_by_id( post_id )
{
	select_post( id_get_post( post_id ) );
}

function select_post( post )
{	
	if( current_post != null && post.length > 0 && current_post.attr( 'id' ) == post.attr( 'id' ) ) return;
	
	if( current_post != null ) current_post.removeClass( 'current' );
	if( post.length == 0 )
	{
		current_post = null;
		return;
	}
	current_post = post;
	current_post.addClass( 'current' );
	
	post[0].scrollIntoView( true );
	
	if( !post.data( 'do-not-auto-mark-read' ) && !post.find( '.footer .action.read' ).attr( 'checked' ) )
	{
		post.find( '.footer .action.read' ).attr( 'checked', true );
		mark_post_read_state( post_get_id( post ), 1 );
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
		mark_post_read_state( post_id, $(this).is(':checked') ? 1 : 0 );
	});
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
		if( current_post == null )
		{
			select_post( $('#posts .post').first() );
		}
		else
		{
			var next_post = current_post.next( '.post' );
			if( next_post.length > 0 ) select_post( next_post );
			
			if( current_post.next( '.post' ).length == 0 )
			{
				//load_more_posts( outline_id, $('#posts .post').length );
			}
		}
	}
	else
	{
		if( current_post == null ) return; // can't do anything
		select_post( current_post.prev( '.post' ) );
	}
}

