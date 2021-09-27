/*
	File: main.js
	Copyright: 2013 Jasper Seidel
	License: MIT
*/

var base_path = '//' + document.location.host + '/';


function api_request( path, args, callback )
{
	var fetch_args = {
		method: 'POST',
		headers: {
			'Accept': 'application/json',
			'Content-Type': 'application/json',
			'X-CSRFToken': Cookies.get('csrftoken')
		},
		credentials: 'include',
	};
	if(args) {
		fetch_args['body'] = JSON.stringify(args);
	};
	fetch(urls[path].url, fetch_args)
	.then(response => response.json())
	.catch(error => {
		show_result({
			caption: 'Error',
			message: error,
			success: false,
		});
	})
	.then(callback)
	.catch(console.log)
}

function get_url( path )
{
	//if( base_path.substr( -1 ) != '/' ) base_path += '/';
	//if( path.substr( 0, 1 ) == '/' ) path = path.substr( 1 );
	return base_path + path;
}

function get_media_url(path)
{
	return document.body.dataset.mediaUrl + path;
}

function add_new_feed( url )
{
	api_request( 'feed_add', { url: url }, function( result )
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

function show_result(data)
{
	$('#result_text').text( data.message );
	if(data.caption) $('#result_caption_text').text( data.caption);
	$('#result_caption').toggle(data.caption ? true : false);
	$('#result_container').toggleClass('ui-state-error', !data.success).toggleClass('ui-state-highlight', data.success);
	$('#result_icon').toggleClass('ui-icon-alert', !data.success).toggleClass('ui-icon-info', data.success);
	$('#result').stop(true, true).fadeIn().delay(5000).fadeOut();
}

var get_unread_counts = _.debounce(function( outline_id )
{
	api_request( 'get_unread', { 'outline_id': outline_id }, function( data )
	{
		document.title = data.total > 0 ? 'Feedreader (' + data.total + ')' : 'Feedreader';
		if( !data.counts ) return;
		$.each( data.counts, set_unread_count );
		set_outline_unread_count(data.counts[''+outline_id]);
	});
}, 500, { trailing: true });

function set_unread_count( outline_id, unread_count )
{
	var outline = $( '#outline-' + outline_id );
	outline.toggleClass( 'has-unread', unread_count > 0 );
	var outline_obj = outline.data('outline');
	if(outline_obj)
	{
		outline_obj.unread_count = unread_count;
		outline.data('outline', outline_obj);
	}
	$('> .outline-line > .outline-unread-count', outline).text(unread_count);
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
	api_request( 'get_option', { keys: opts }, function( result )
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
					data['value'] = result.options[ name ].toLowerCase() == 'true';
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
	api_request( 'set_option', data, function( result )
	{
		if(result.success)
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

	url_change(location.pathname)
});

function load_navigation()
{
	$('#button_refresh_page').button("option", "disabled", true);
	api_request('outline_get_all_outlines', {}, function(data) {
		render_navigation(data.outlines);
		$('#button_refresh_page').button("option", "disabled", false);
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
	var html = $(apply_template(template, 'outline', outline));
	html.data('outline', outline);
	html.addClass(outline.feed_id ? 'feed' : 'folder');
	if( !outline.folder_opened )
	{
		html.addClass( 'folder-closed' );
	}
	html.toggleClass( 'has-unread', outline.unread_count > 0 );
	if(outline.icon)
	{
		$('> .outline-line', html).css('background-image', `url(${get_media_url(outline.icon)})`);
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
		if(!outline) return;
		var outline_html = make_outline( template, outline );

		if( outline.children && outline.children.length > 0 )
		{
			var children = $( '<ul>' );
			$.each( outline.children, function( k, child )
			{
				if(!child) return;
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
