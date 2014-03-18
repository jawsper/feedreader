/*
	File: main.js
	Copyright: 2013 Jasper Seidel
	License: MIT
*/

var base_path = '//' + document.location.host + '/feedreader/';

function api_request( path, args, callback )
{
    $.ajax({
		type: 'POST',
		url: get_api_url( path ),
		data: args,
		success: function( result )
		{
			callback( result );
		},
		error: function(xhr, textStatus, errorThrown)
		{
			show_result({
				caption: 'Error',
				message: errorThrown == 'FORBIDDEN' ? 'Your login has expired. Please refresh the page to re-login' : errorThrown,
				error: true,
			});
		}
	});
}

function get_url( path )
{
	//if( base_path.substr( -1 ) != '/' ) base_path += '/';
	//if( path.substr( 0, 1 ) == '/' ) path = path.substr( 1 );
	return base_path + path;
}
function get_api_url( path )
{
	return get_url( 'api/0' + path );
}

function add_new_feed( url )
{
	api_request( '/feed/add/', { url: url }, function( result )
	{
		if( result.success )
		{
			location.reload();
		}
	});
}

var outline_regex = /^outline-(\d+)$/

$(function()
{
	$('input:submit, button, a.button').button();
});

$(function()
{
	var csrftoken = $.cookie('csrftoken');
	function csrfSafeMethod(method) {
		// these HTTP methods do not require CSRF protection
		return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
	}
	$.ajaxSetup({
		crossDomain: false, // obviates need for sameOrigin test
		beforeSend: function(xhr, settings) {
			if (!csrfSafeMethod(settings.type)) {
				xhr.setRequestHeader("X-CSRFToken", csrftoken);
			}
		}
	});
});

function show_result( data )
{
	$('#result_text').text( data.message );
	if( data.caption ) $('#result_caption_text').text( data.caption );
	$('#result_caption').toggle( data.caption ? true : false );
	$('#result_container').toggleClass( 'ui-state-error', data.error ).toggleClass('ui-state-highlight', !data.error);
	$('#result_icon').toggleClass('ui-icon-alert', data.error).toggleClass('ui-icon-info', !data.error);
	$('#result').stop(true,true).fadeIn().delay(5000).fadeOut();
}

function get_unread_counts( outline_id )
{
	api_request( '/get_unread_count/', { 'outline_id': outline_id }, function( data )
	{
		document.title = data.total > 0 ? 'Feedreader (' + data.total + ')' : 'Feedreader';
		if( !data.counts ) return;
		$.each( data.counts, set_unread_count );
	});
}

function set_unread_count( outline_id, unread_count )
{
	$( '#outline-' + outline_id ).toggleClass( 'has-unread', unread_count > 0 );
	$( '#outline-unread-count-' + outline_id ).text( unread_count );
}

var options = 
{
	'showOnlyUnread': {
		'title': 'Show only unread posts',
		'type': 'boolean',
		'default': false,
		'callback': function()
		{
			$( '#outlines' ).toggleClass( 'show-only-unread', this['value'] );
		}
	}
};

function load_options()
{
	var opts = [];
	$.each( options, function( k ) { opts.push( k ) } );
	api_request( '/get_option/', { keys: opts }, function( result )
	{
		$.each( options, function( name, data )
		{
			if( typeof result.options[ name ] == 'undefined' ) // key not found
			{
				data['value'] = data['default'];
			}
			else
			{
				if( data['type'] == 'boolean' )
				{
					data['value'] = result.options[ name ] == 'true';
				}
				else
				{
					data['value'] = result.options[ name ];
				}
			}
			if( data['callback'] ) data['callback'].apply( data );
		});
	} )
}

function option_button_click( name )
{	
	if( options[ name ]['type'] == 'boolean' )
	{
		save_option( name, !options[ name ]['value'] );
	}
}

function save_option( name, value )
{
	var data = {};
	data[ name ] = value;
	api_request( '/set_option/', data, function( result )
	{
		if( result == 'OK' )
		{
			load_options();
		}
	});
}

function url_change( url )
{
	var m = url.match( /\/outline\/(\d+)\// );
	if( m )
	{
		set_outline( m[1] );
	}
}

function on_popstate(e)
{
	url_change( location.pathname );
}

$(function()
{
	// make sure to not propagate when clicked to prevent folders from opening/closing
	//$( '#outlines a' ).click( function(e) { e.stopPropagation(); } );
	
	$( '#outlines' )
		.on({ click: function( e )
			{
				history.pushState( null, null, this.href );
				url_change( this.href );
				e.preventDefault();
				e.stopPropagation();
			} }, 'a' )
		.on({
			click: function()
			{
				var outline = $( this ).parent();
				var outline_id = outline.attr( 'id' ).match( outline_regex )[1];
				outline.toggleClass( 'folder-closed' );
				set_outline_param( outline_id, 'folder_opened', outline.hasClass( 'folder-closed' ) ? 0 : 1, true );
			}
		}, '.folder > .outline-line' );
		
	// make a button for all options
	$.each( options, function( name, data )
	{
		var button = $( '<a>' ).text( data.title ).click( function() { option_button_click( name ); } ).button();
		$( '#navigation ul.options' ).append( $( '<li>' ).append( button ) );
	} );
	// load the options
	load_options();
	
	$( '#new-feed-popup' ).dialog({
		autoOpen: false,
		modal: true,
		buttons: {
			'Add feed': function()
			{
				add_new_feed( $( '#new-feed-url' ).val() );
			},
			'Cancel': function()
			{
				$( this ).dialog( 'close' );
			}
		},
		close: function()
		{
			$( '#new-feed-url' ).val( '' );
		}
	});
	
	$( '#button-new-feed' ).click( function() { $( '#new-feed-popup' ).dialog( 'open' ); } );
	// make the options and refresh button work
	$( '#button-options' ).click( function() { $( '#navigation .options' ).toggle(); } );
	$( '#button_refresh_page' ).click( function( e ) 
	{
		e.preventDefault();
		//get_unread_counts();
		load_navigation();
	});
	
	// trigger initial hash change, and set window.hashchange event
	//on_hash_change();
	//$( window ).on( 'hashchange', on_hash_change );
	
	// if is outline url, then set the outline
	
	
	//url_change( location.pathname );
	window.addEventListener( 'popstate', on_popstate );
	
	load_navigation();
});

function load_navigation()
{
	api_request( '/outlines/', { use_long_keys: 1 }, function( data )
	{
		render_navigation( data.outlines );
	});
}

function regexp_escape( input )
{
	return input.replace( /([\$\{\}])/g, '\\$1' );
}

function get_template( id )
{
	var re_template_keys = /\$\{(?:([a-z]+)\.)*([a-z_]+)\}/g;
	//var re_keyname = /^\$\{(?:([a-z]+)\.)*([a-z_]+)\}$/;
	
	var template = $( id ).text();
	
	var match = false;
	var keys = {};
	while( ( match = re_template_keys.exec( template, re_template_keys.lastIndex ) ) != null )
	{
		var key_name = match[0];
		keys[ key_name ] = match.splice( 1 );
	}
	
	/*var matched = template.match( re_template_keys );
	var keys = {};
	$.each( matched, function( k, v )
	{
		var split_key = v.match( re_keyname ); 
		if( !split_key )
		{
			console.debug( v );
		}
		else
		{
			var key_name = split_key[0];
			keys[ key_name ] = split_key.splice( 1 );
		}
	});*/
	
	return { str: template, keys: keys };
}

function apply_template( template, data_name, data )
{
	var str = template.str;
	$.each( data, function( k, v )
	{
		var name = data_name + '.' + k;
		var rx = RegExp( '\\$\\{' + name + '\\}', 'g' );
		str = str.replace( rx, v );
	});
	return str;
}

function make_outline( template, outline )
{
	var html = $( apply_template( template, 'outline', outline ) );
	html.addClass( outline.feed_id ? 'feed' : 'folder' );
	if( !outline.folder_opened )
	{
		html.addClass( 'folder-closed' );
	}
	html.toggleClass( 'has-unread', outline.unread_count > 0 );
	if( outline.feed_id )
	{
		$( '> .outline-line', html ).css( 'background-image', 'url(' + get_url( 'feed/' + outline.feed_id + '/favicon/' ) + ')' );
	}
	return html;
}

function render_navigation( navigation )
{
	var template = get_template( '#templateNavigationItem' );
	
	var main_ul = $( '#outlines' );
	main_ul.empty();
	$.each( navigation, function( k, outline )
	{
		var outline_html = make_outline( template, outline );
		
		if( outline.children && outline.children.length > 0 )
		{
			var children = $( '<ul>' );
			$.each( outline.children, function( k, child )
			{
				var child = make_outline( template, child );
				children.append( child );
			});
			outline_html.append( children );
		}
		main_ul.append( outline_html );
	});
}


String.prototype.format = function() {
  var args = arguments;
  return this.replace(/{(\d+)}/g, function(match, number) { 
    return typeof args[number] != 'undefined'
      ? args[number]
      : match
    ;
  });
};
