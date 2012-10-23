
// -------------------------------------------------------------------------------
// fonctions javascript
// -------------------------------------------------------------------------------

(function(){
    if (!console ) {
	var names = ["log", "debug", "info", "warn", "error", "assert", "dir", "dirxml", "group", "groupEnd", "time", "timeEnd", "count", "trace", "profile", "profileEnd"];
	
	window.console = {};
	for (var i = 0; i < names.length; i++) {
	    window.console[names[i]] = function(){};
	}
    }
})();


// gestion des chronos et compte a rebourg

var temps_passe=0;


var current_location=new Array();
var previous_location=new Array();
var last_url_called=0;
var last_time_called=getCurrentTime() ;
var last_table="#none";
var redirect_url='xxx';
var old_message=0;

var is_graphics_shown=0;

var previous_response= new Array();
var previous_time= new Array();

var isAutomaticReload = false;

var update_max = 20;
var update_frequency = 5;
var currently_loading=0;

var url_visited = new Array();
var url_to_visit = new Array();
var loading = new Array();

// -------------------------------------------------------------------------------
// fonctions gestion timer
// -------------------------------------------------------------------------------
// 

function getCurrentTime() {
	return  Math.round(+new Date()/1000);
}

function secondsToTime(secs)
{
    var hours = Math.floor(secs / (60 * 60));
   
    var divisor_for_minutes = secs % (60 * 60);
    var minutes = Math.floor(divisor_for_minutes / 60);
 
    var divisor_for_seconds = divisor_for_minutes % 60;
    var seconds = Math.ceil(divisor_for_seconds);
   
    s = "";

    if (hours>0) { 
	s = s + hours + " h ";
	if (minutes<10) {
	    s = s + "0";
	}
    }
    if ((hours>0) ||  (minutes>0)) { 
	s = s + minutes + " m ";
	if (seconds<10) { s = s + "0";}
    }
    s = s + seconds + " s ";

    return s;
}

function update_clock() {
    passe=$('div#temps_qui_passe');
    delta=getCurrentTime() - last_time_called;
    temps_passe=parseInt(delta);    
    s= 'il y a '+ secondsToTime(temps_passe) +'.' ;

    passe.replaceWith("<div id='temps_qui_passe' style='float: left; text-align: left;' >" + s +
		      "<a href='#' onClick='reload()' id='reload' >" +
		      "<img  src='IMAGES/reload.jpg' title='mise a jour \n maintenant' height='16' width='16' /></a>"+
		      "</div>");
    if (delta>update_max) {
	reload();
	return;
    }
}

function update_view() {
    setTimeout('update_view()',update_frequency*1000);
    update_clock();
}

function affiche_message(message) {
    if ($('#message').length) {
	if (!old_message) {
	    old_message = $('#message').html();
	}
	else {
	    message = $('#message').html() + "<BR>" + message;
	}
	//alert("saved in old_message : "+old_message);
	$('#message').replaceWith("<div id='message' style='color:red'><B>"+message+"</B></div>");		
	setTimeout('delete_message()',5*1000);
    }
    else {
	console.log("should affiche_message but length of message is zero!!!!");
    }
}

function delete_message() {
    // alert("read from old_message : "+old_message);
    //message = $('#sous-titre').val();
    if (old_message) {
	$('#message').replaceWith("<div id='message'>"+old_message+"</div>");
    }
    old_message = 0;
}

function affiche_popup(titre,content) {
    var $dialog = $('<div id="popup"></div>')
	.html(content)
	.dialog({
		autoOpen: false,
		title: titre,
		width: 500,
		height: 300,
	    });
    $dialog.dialog('open');
}

// -------------------------------------------------------------------------------
// fonctions Navigation
// -------------------------------------------------------------------------------
// 


function reload(id) {
    if (last_url_called) {
	//console.log("reload avec last_url_called="+last_url_called);
	load2Id('corps',last_url_called,1);
    }
}


function ssh_kill(id) {
    load2Id('corps',"ssh_kill",1);
}


// -------------------------------------------------------------------------------
// fonctions ajax
// -------------------------------------------------------------------------------

function affiche(reponse) {
    //alert('dans affiche blocs :'+reponse);
    //    last_table="#none";
   redirect_url = 0;
   blocs = reponse.split("---NEWBLOC---");
   bloc=blocs.shift();
   while (blocs.length>1) {
       bloc=blocs.shift();
       a=bloc.split('---CONTENT---')
       id=a[0];
       content=a[1];
       //console.log("id="+id+"\ncontent="+content);
       cible=$("div#"+id);
       switch(id) {
       case 'redirect':
	   url = content;
	   load2Id('corps',url,1,'You are connected');
	   return 1
	   //alert("recu table:"+last_table);
	   break;
       case 'table':
	   last_table = '#'+content;
	   //alert("recu table:"+last_table);
	   break;
       case 'commande':
	   if (content=="nothing") {
	       //alert("stop displaying here");
	       return 1;
	   }
	   break;
       case 'message' :
	   //alert("message :"+content);
	      affiche_message(content);
	      break;
       case 'titre_popup' :
	   titre_popup = content;
	   break;
       case 'popup':
       case 'popup_noline':
	   dialogbox = affiche_popup(titre_popup,content,redirect_url);
	   //alert("popup :"+content);
	   if ($("#connexionForm").length) { 
	       login_form();
	   }
	   return 1;
       default :
	   if (cible=='titre') { titre=content;}
	   if (cible!=null) {
	       //console.log("cible("+cible+")=///"+content+"////");
	       cible.replaceWith("<div id="+id+">"+content+"</div>");
	       if ($("#connexionForm").length) { 
		   login_form();
	       }
	   }
       }
   }
   return 0;
}


function load2Id(id,url_add,force,message) { // (2)
  
    console.log("load2Id avec id="+id+" et url_add="+url_add);
    

    force= force || 0;

    l=previous_response[url_add];
    lp=l+"###";
    i=lp.indexOf("undefined###");
    j=(url_add+"####").indexOf("&force=1");
    if (j>=0) { 
	url_add=url_add.replace("&force=1",""); 
	//alert("j : "+j+"url_add sans force:"+url_add);
	force = 1;
    }

    if (i!=0 && j<0 && force==0) {
        //$(id).html = l;
	affiche(l);
	last_time_called = previous_time[url_add];
	last_url_called = url_add;
	complete_view();
	return;
	//alert("delta="+delta+"  temps_passe="+temps_passe);
    }


    if (currently_loading) return;

    already_loading = loading[url_add]+"###";
    if (already_loading.indexOf("undefined###") !=0) {
	//console.log("already loading load2Id avec url_add"+url_add);
	return;
    }

    if (message!=undefined) {
	affiche_message(message);
    }
    
    loading[url_add]=1;
    currently_loading=1;
    $('#loading').replaceWith("<div  id='loading'> <img src='IMAGES/ajax-loader.gif'></div>");
    $.ajax({
	    type: "GET",
		url: url_add,
		cache: force==0,
		dataType: "text",
		success:
	    function(response){
		//console.log( "data received" +response);
		previous_response[url_add] = previous_response[url_add] || "null";
		if (!(previous_response[url_add]==response)){
		    //console.log("modif");
		    previous_response[url_add]=response;
		    previous_time[url_add]=getCurrentTime();
		    last_time_called = previous_time[url_add];
		    // console.log("la "+url_add)
		    temps_passe=0;
		}
		else {
		    //console.log("no modif");
		    if (force>0) {
			previous_time[url_add]=getCurrentTime();
			last_time_called = previous_time[url_add];
		    }
		}

		previous_location[id]=$("div#"+id).html();
		if (last_url_called)
		    url_visited.push(last_url_called);
	        url_to_visit = new Array();
		last_url_called=url_add;
		// console.log("url_visited="+url_visited.join('<<::>>')+
		// 	    "  url_to_visit="+url_to_visit.join('<<::>>')+ 
		// 	    " last_url_called="+last_url_called);
		affiche_nok=affiche(response);
		delete     loading[url_add];
		currently_loading=0;
	    },
		error:
	    function (request, textStatus, errorThrown) {
		// typically only one of textStatus or errorThrown 
		// will have info
		this; // the options for this ajax request
		alert(request.responseText);
		delete     loading[url_add];
		currently_loading=0;
	    },
		complete:
	    function(){
		if (!affiche_nok) {
		    complete_view();
		}
		$('div#loading').replaceWith(
					     "<div id='loading' style='float: right; text-align: left;'>"+
					     "<div style='float: left; text-align: left;' id='temps_qui_passe'> </div>"+
					     "<div style='float: left; text-align: left;' id='switch'> </div></div>"
				 );
		delete     loading[url_add];
		currently_loading=0;
		update_clock();
	    }
	});


}


//--------------------------------------------------------------------------------
// completion de la page web 
//--------------------------------------------------------------------------------

function complete_view() {
    //alert("in complete_view for last_table:"+last_table);
    if ($(last_table).length) {
	//alert('ici :'+$("#datablexxxx").length);
	//tablesort("table:last");
	if ($(last_table).length) {
	    //alert("exists!!!");
	    $(last_table).dataTable( {
		    "aaSorting": [[ 2, "desc" ]],
			"aLengthMenu": [ 10, 25, 50, 100, 200, 500 ],
			"iDisplayLength": 10,
			"bJQueryUI": true,
			"sPaginationType": "full_numbers",
			"bAutoWidth": false,
			"bStateSave": true,
			"bSortClasses": false
			} );
	    
	    //fnFilterGlobal(last_table,"",0);
	}

	$(last_table).bind('mousewheel', function(event, delta, deltaX, deltaY) {
		if (delta<0) {
		    $(last_table).dataTable().fnPageChange( 'next' );
		}
		else if (delta>0) {
		    $(last_table).dataTable().fnPageChange( 'previous' );
		}
		add_context_menus();
	    });


	context = $(last_table).attr("context");
	//alert("context="+context);
	add_context_menus();




    }

    

    $('#jsddm > li').bind('mouseover', jsddm_open);
    $('#jsddm > li').bind('mouseout',  jsddm_timer);
    document.onclick = jsddm_close;

    update_clock();

}

function add_context_menus() {
    if ($(last_table).length) {
	//alert('ici :'+$(last_table).length);
	$(document).bind('keydown', 's', function () {
		$(last_table+" INPUT").focus(); 
		return false;});
	// menu deroulant

	context = $(last_table).attr("context");
	if ($("div#myMenu_"+context)) {
	    // Show menu when #myDiv is clicked
	    $(last_table+" TR").contextMenu({
		    menu: 'myMenu_'+context
			},
		function(action, el, pos) {
		    //console.log(el.parent().parent());
		    var div1 = document.getElementById("myMenu_"+context);
		    var clef = parseInt(div1.getAttribute("clef"));
		    var element = el.children()[clef].innerHTML; 
		    //alert("clef = "+clef+"\nelement="+element);
		    //alert("try reading clef from"+"div#myMenu_"+context+":"+clef);
		    //alert('Action: ' + action + '\n\n' +
		    //	  'clef:   ' + clef + '\n' + 
		    //	  'Element ID: ' + element + '\n\n' + 
		    //	  'X: ' + pos.x + '  Y: ' + pos.y + ' (relative to element)\n\n' + 
		    //	  'X: ' + pos.docX + '  Y: ' + pos.docY+ ' (relative to document)'
		    //	  );
		    if ($("#current_dir").length) {
			//alert("current_dir="+$("#current_dir").val());
			command = "do/"+$("#access").val()+"/"+$("#machine").val()
			    +"/"+action+"/"+$("#current_dir").val()+element.substring(2);
		    }
		    else {
			command = "do/"+$("#access").val()+"/"+$("#machine").val()
			    +"/"+action+"/"+element.substring(1);
		    }
		    //xxxxalert("command = "+command);
		    load2Id("corps",command,force=1);
		});
	}
    }
}


function login_form() {
    // login form
    //alert('applying login_form');
    $("#connexionForm").submit( function() {							 
	    params = "username="+$("#id_username").val()+
		"&password="+$("#id_password").val()+
		"&next_url="+$("#next_url").val()+
		"&key="+$("#key").val()+"&access="+$("#access").val()+
		"&machine="+$("#target_machine").val();
	    //alert('ici params='+params);
	    $.ajax({
		    type: "POST",
			url: "authent",
			data: params,
			success: function(msg){
			//alert(msg);
			affiche(msg);
		    }
		});
	    return false;
	});
}

function fnFilterGlobal(tablename,data,column){
    //alert('in filterglobal '+tablename+' '+data);
    $(tablename).dataTable().fnFilter(data,null, null, null);
    add_context_menus();
}



function start() {//111
    load2Id("cartouche","cartouche");
    update_view();
    url_visited = new Array();
    $('#jsddm > li').bind('mouseover', jsddm_open);
    $('#jsddm > li').bind('mouseout',  jsddm_timer);
    document.onclick = jsddm_close;
}


// barre de  menu déroulant

var jsddm_timeout         = 9000;
var jsddm_closetimer		= 0;
var ddmenuitem      = 0;

function jsddm_open()
{	jsddm_canceltimer();
	jsddm_close();
	ddmenuitem = $(this).find('ul').eq(0).css('visibility', 'visible');}

function jsddm_close()
{	if(ddmenuitem) ddmenuitem.css('visibility', 'hidden');}

function jsddm_timer()
{	jsddm_closetimer = window.setTimeout(jsddm_close, jsddm_timeout);}

function jsddm_canceltimer()
{	if(jsddm_closetimer)
	{	window.clearTimeout(jsddm_closetimer);
		jsddm_closetimer = null;}}



$(document).ready(function startup() {

	// ecran d'aide
	$.fx.speeds._default = 1000;
	$( "#dialog" ).dialog({
		autoOpen: false,
		    show: "explode",
		    hide: "explode"
		});

	//$(document).attr("title", "new title value");

	$(document).bind('keydown', 'v', function () {
		//alert('v key pressed');
		toggle_graphics(); 
		return false;});
	$(document).bind('keydown', 'g', function () {
		//alert('g key pressed');
		show_graphics(); 
		return false;});
	$(document).bind('keydown', 't', function () {
		//alert('g key pressed');
		show_corps(); 
		return false;});

	$(document).bind('keydown', 'u', function () {
		reload(); 
		return false;});




	// ------------------------------------------------------------
	// raccourcis clavier pour se deplacer rapidement dans la table
	// des jobs
	// ------------------------------------------------------------

	$(document).bind('keydown', 'backspace', function () {
		fnFilterGlobal(last_table,"",0); 
		return false;
	    }
	    );
	$(document).bind('keydown', 'pageup', function () {
		$(last_table).dataTable().fnPageChange( 'previous' );
		return false;
	    }
	    );
	$(document).bind('keydown', 'pagedown', function () {
		$(last_table).dataTable().fnPageChange( 'next' );
		return false;
	    }
	    );
	$(document).bind('keydown', 'home', function () {
		$(last_table).dataTable().fnPageChange( 'first' );
		return false;
	    }
	    );
	$(document).bind('keydown', 'end', function () {
		$(last_table).dataTable().fnPageChange( 'last' );
		return false;
	    }
	    );



	// ------------------------------------------------------------
	// raccourcis clavier filtrant les jobs par etat
	// ------------------------------------------------------------

	$(document).bind('keydown', 'r', function () {
		fnFilterGlobal(last_table,"RUNNING",0); 
		return false;
	    }
	    );
	$(document).bind('keydown', 'w', function () {
		fnFilterGlobal(last_table,"WAITING",0); 
		return false;
	    }
	    );
	$(document).bind('keydown', 'q', function () {
		fnFilterGlobal(last_table,"QUEUED",0); 
		return false;
	    }
	    );
	$(document).bind('keydown', 'p', function () {
		fnFilterGlobal(last_table,"PENDING",0); 
		return false;
	    }
	    );
	$(document).bind('keydown', 'i', function () {
		fnFilterGlobal(last_table,"IDLE",0); 
		return false;
	    }
	    );


	// ------------------------------------------------------------
	// raccourcis clavier listant les jobs
	// ------------------------------------------------------------

	$(document).bind('keydown', '0', function () {
		reload(); 
		return false;});


	$(document).bind('keydown', '7', function () {
		affiche_message('test_message');
		return false;
	    }
	    );


	$(document).bind('keydown', '8', function () {
		load2Id('corps','/do/ssh/server/ls?_=1344534652658');
		return false;
	    }
	    );

	$(document).bind('keydown', 'f1', function () {
		affiche_popup('Aide de VISHNU Portal','More very soon!');
		return false;
	    }
	    );

	$(document).bind('keydown', '1', function () {
		$("#jobs_machine_1").click();
		return false;
	    }
	    );
	$(document).bind('keydown', '2', function () {
		$("#jobs_machine_2").click();
		return false;
	    }
	    );
	$(document).bind('keydown', '3', function () {
		$("#jobs_machine_3").click();
		return false;
	    }
	    );
	$(document).bind('keydown', '4', function () {
		$("#jobs_machine_4").click();
		return false;
	    }
	    );

	$(document).bind('keydown', '5', function () {
		$("#jobs_machine_5").click();
		return false;
	    }
	    );

	$(document).bind('keydown', '6', function () {
		$("#jobs_machine_6").click();
		return false;
	    }
	    );

	$(document).bind('keydown', '7', function () {
		$("#jobs_machine_7").click();
		return false;
	    }
	    );

	$(document).bind('keydown', '8', function () {
		$("#jobs_machine_8").click();
		return false;
	    }
	    );

	$(document).bind('keydown', '9', function () {
		$("#jobs_machine_9").click();
		return false;
	    }
	    );
	$(document).bind('keydown', 'ctrl+1', function () {
		$("#ls_1").click();
		return false;
	    }
	    );
	$(document).bind('keydown', 'ctrl+2', function () {
		$("#ls_2").click();
		return false;
	    }
	    );
	$(document).bind('keydown', 'ctrl+3', function () {
		$("#ls_3").click();
		return false;
	    }
	    );
	$(document).bind('keydown', 'ctrl+4', function () {
		$("#ls_4").click();
		return false;
	    }
	    );

	$(document).bind('keydown', 'ctrl+5', function () {
		$("#ls_5").click();
		return false;
	    }
	    );

	$(document).bind('keydown', 'ctrl+6', function () {
		$("#ls_6").click();
		return false;
	    }
	    );

	$(document).bind('keydown', 'ctrl+7', function () {
		$("#ls_7").click();
		return false;
	    }
	    );

	$(document).bind('keydown', 'ctrl+8', function () {
		$("#ls_8").click();
		return false;
	    }
	    );

	$(document).bind('keydown', 'ctrl+9', function () {
		$("#ls_9").click();
		return false;
	    }
	    );

	$(document).bind('keydown', 'alt+left', function () {
		if (url_visited.length>2) {
		    url = url_visited.pop();
		    url_to_visit.unshift(url);
		    // console.log("url_visited="+url_visited.join('<<::>>')+
		    // 		"  url_to_visit="+url_to_visit.join('<<::>>')+
		    // 		" last_url_called="+last_url_called);
		    // console.log("back to "+url);
		    load2Id('corps',url);
		    add_context_menus();
		    return false;
		}
	    }
	    );

	$(document).bind('keydown', 'alt+right', function () {
		if (url_to_visit.length>1) {
		    url = url_to_visit.shift()
		    url_visited.push(last_url_called);
		    url_visited.push(url);
		    // console.log("url_visited="+url_visited.join('<<::>>')+
		    // 		"  url_to_visit="+url_to_visit.join('<<::>>')+
		    // 		" last_url_called="+last_url_called);
		    // console.log("forward to "+last_url_called);
		    load2Id('corps',url);
		    add_context_menus();
		    return false;
		}
	    }
	    );

    
	// ------------------------------------------------------------
	// compatibility checking for csrf post django
	// ------------------------------------------------------------

       $(document).ajaxSend(function(event, xhr, settings) {
           function getCookie(name) {
               var cookieValue = null;
               if (document.cookie && document.cookie != '') {
                   var cookies = document.cookie.split(';');
                   for (var i = 0; i < cookies.length; i++) {
                       var cookie = jQuery.trim(cookies[i]);
                       // Does this cookie string begin with the name we want?
                       if (cookie.substring(0, name.length + 1) == (name + '=')) {
                           cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                           break;
                       }
                   }
               }
               return cookieValue;
           }
           function sameOrigin(url) {
               // url could be relative or scheme relative or absolute
               var host = document.location.host; // host + port
               var protocol = document.location.protocol;
               var sr_origin = '//' + host;
               var origin = protocol + sr_origin;
               // Allow absolute or scheme relative URLs to same origin
               return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
                   (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
                   // or any other URL that isn't scheme relative or absolute i.e relative.
                   !(/^(\/\/|http:|https:).*/.test(url));
           }
           function safeMethod(method) {
               return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
           }

           if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
               xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
           }
       });

	start();
    }
)


