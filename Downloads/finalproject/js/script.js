App = {};


App.yelp = {
    yelpAuth: { 
          consumerKey: "hmL-k5QDu0Lvc8bD6UyBjA", 
          consumerSecret: "MUvZc-hg9c5Q3HEhQ98CGEup32Q",
          accessToken: "ZLNpjCcyi8J7OLLcD1WhFXt73X9yTsRP",
          accessTokenSecret: "CY341ue4EpsUe1Y-bgL6No9j-es",
          serviceProvider: { 
            signatureMethod: "HMAC-SHA1"
          }
    },
    mapOptions: {
            zoom: 8,
            center: new google.maps.LatLng(42.3260624,-71.89384),
            mapTypeId: google.maps.MapTypeId.ROADMAP
    },    
    init: function() {
        mapOptions = App.yelp.mapOptions;
        // Defining objects
        var map = new google.maps.Map(document.getElementById('map-canvas'), App.yelp.mapOptions);
        var marker = new google.maps.Marker({position: mapOptions.center, map: map});
        App.yelp.map = map;
        App.yelp.marker = marker;

         google.maps.event.trigger(map, 'resize');
         map.panBy(-80, -120);

        // update Yelp Restaurants at the beginning.
        App.yelp.updateRestaurants(marker.getPosition().lat(), marker.getPosition().lng());

        // See if user allows you to access his/her location.
        if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(function(pos) {
                var me = new google.maps.LatLng(pos.coords.latitude, pos.coords.longitude);
                // Change map's center and update Restaurants.
                map.setCenter(me);
                marker.setPosition(me);
                App.yelp.updateRestaurants(marker.getPosition().lat(), marker.getPosition().lng());
            }, function(error) {
            });
        }

        // If user submits a search query find it using findLocation function, and update Restaurants.
        debugger;
        $('#searchRestaurants').submit(function(e) {
            App.yelp.findLocation($('#queryRestaurants').val());
            App.yelp.updateRestaurants(marker.getPosition().lat(), marker.getPosition().lng());
            e.preventDefault();
        });

        // If user clicked anywhere on the map, change the marker location and find restaurants nearby.
        google.maps.event.addListener(map, 'click', function(event) {
            marker.setPosition(event.latLng);
            App.yelp.updateRestaurants(marker.getPosition().lat(), marker.getPosition().lng());
        });

        $('.location').live('click', function(e) {
            App.yelp.findLocation($(this).html());
            e.preventDefault();
        });
    },
    // This function uses geocoder to find a location using an address, and puts the marker on the search result.
    findLocation: function(address) {
        // For search queries
        var geocoder = new google.maps.Geocoder ();

        geocoder.geocode ( { 'address': address}, function(results, status)  {
            if (status == google.maps.GeocoderStatus.OK)  {
                    App.yelp.map.setCenter(results [0].geometry.location);
                    App.yelp.marker.setPosition(results [0].geometry.location);
            } else {
                alert("Problem :D -> " + status);
            }
        }); 
    },    
    updateRestaurants: function(lat, lng) {
        var auth = App.yelp.yelpAuth;
        // Set parameters
        var terms = 'restaurants';
        var accessor = {
          consumerSecret: auth.consumerSecret,
          tokenSecret: auth.accessTokenSecret
        };
        parameters = [];
        parameters.push(['term', terms]);
        parameters.push(['ll', lat + ',' + lng]);
        parameters.push(['callback', 'cb']);
        parameters.push(['oauth_consumer_key', auth.consumerKey]);
        parameters.push(['oauth_consumer_secret', auth.consumerSecret]);
        parameters.push(['oauth_token', auth.accessToken]);
        parameters.push(['oauth_signature_method', 'HMAC-SHA1']);

        var message = { 
          'action': 'http://api.yelp.com/v2/search',
          'method': 'GET',
          'parameters': parameters 
        };

        OAuth.setTimestampAndNonce(message);
        OAuth.SignatureMethod.sign(message, accessor);
        var parameterMap = OAuth.getParameterMap(message.parameters);
        parameterMap.oauth_signature = OAuth.percentEncode(parameterMap.oauth_signature)
        console.log(parameterMap);
        $.ajax({
        'url': message.action,
        'data': parameterMap,
        'cache': true,
        'dataType': 'jsonp',
        'jsonpCallback': 'cb',
        'success': function(yelp_data, textStats, XMLHttpRequest) {
        var output = [];
        for (var i = 0; i < yelp_data.businesses.length; i++) {
            var li = '';
            var categoryStr = '';
            var business = yelp_data.businesses[i];
            var categories = business.categories;
            for (var j = 0; j < categories.length; j++) {
                categoryStr += '<b class="label-success label">' + categories[j][0] + '</b>';
                li = ['<li><div class="wrapper"><h3><a href="' + business.url + '" target="_blank">' + business.name + '</a></h3>',
                        '<span class="pull-right label label-danger">' + business.rating + '</span>',
                        '<span><a href="#" class="location">' +  business.location.display_address + '</a></span>',
                        '<span class="phone">Phone: ' + business.phone + '</span><hr />',
                        '<span class="categories">' + categoryStr + '</span>',
                        '</div></li>'].join('\n');
                output.push(li);
            }
        }
        $('.container_restaurants').html(output.join("\n"));
        }});
    }    
};


App.yummly = {
    credentials: {
      id: '5446fc71',
      key: '286bbfb9b2f35bc46676ab862d480890',
    },
    init: function() {
        $('#searchRecipe').submit(function(e) {
            App.yummly.searchRecipe($('#queryRecipe').val());
            e.preventDefault();
        }); 

        var query = 'soup';
        App.yummly.searchRecipe(query);

    },
    searchRecipe: function(query) {
    
        $.ajax({
        'url': 'http://api.yummly.com/v1/api/recipes?_app_id=' + App.yummly.credentials.id + '&_app_key=' + App.yummly.credentials.key + '&callback=test&q=' + query,
        'cache': true,
        'dataType': 'jsonp',
        'jsonpCallback': 'test',
        'success': function(data, textStats, XMLHttpRequest) {
           var output = [];
           for (var i = 0; i < data.matches.length; i++) {
            var li = '';
            var ingredientsStr = '';
            var recipe = data.matches[i];
            var ingredients = recipe.ingredients;
            for (var j = 0; j < ingredients.length; j++)
                ingredientsStr += '<b class="label-success label">' + ingredients[j] + '</b> ';
            li = ['<li><div class="wrapper">',
                    recipe.smallImageUrls && recipe.smallImageUrls.length ? '<span class="pull-left"><img src="' + recipe.smallImageUrls + '" /></span>' : '',
                    '<h3><a href="' + recipe.id + '" target="_blank">' + recipe.recipeName + '</a></h3>',
                    '<span class="pull-right label label-danger">' + recipe.rating + '</span>',
                    '<span class="time">Time: ' + recipe.totalTimeInSeconds + ' seconds</span><hr />',
                    '<span class="categories">' + ingredientsStr + '</span>',
                    '</div></li>'].join('\n');
            output.push(li);
           }
           $('.recipes').html(output.join("\n"));
           $('.recipes').show();
        }
        });    
}    


}


var funclicked = function() {
    $('.fun').toggle( "puff");
    $('.food').toggle( "puff");
	$('.relax').toggle( "puff");
	$('.study').toggle( "puff");
	$('.container_fun_subcats').show();
	$("#home1").show();
  }

var foodclicked = function() {    
	$('.food').toggle( "puff");
    $('.fun').toggle( "puff");
	$('.relax').toggle( "puff");
	$('.study').toggle( "puff");
	$('.container_food_subcats').show();
	$("#home1").show();
	$('.cooking').show();
	$('.Eating-Out').show();
}

var relaxclicked = function() {
    $('.relax').toggle( "puff");
    $('.food').toggle( "puff");
	$('.fun').toggle( "puff");
	$('.study').toggle( "puff");
	$('.container_relax_subcats').show();
	$("#home1").show();
}

var studyclicked = function() {
   	$('.study').toggle( "puff");
    $('.food').toggle( "puff");
	$('.relax').toggle( "puff");
	$('.fun').toggle( "puff");
	$('.container_study_subcats').show();
	$("#home1").show();
}

var Eatingclicked = function() {
     $('.container_restaurants').show();
     $('.cooking').toggle("puff");
     $("#map-canvas").show();
     $('.sidebar').show();
     $('.cooking').hide();
     $('.Eating-Out').toggle("puff");

    App.yelp.init();

}
var cookingclicked = function() {
     $('.recipes').show();
     $('.Cooking').toggle("puff");
     $('.searchRecipe').show();
     $('.sidebar1').show();
     $('.Eating-Out').hide();
     $('.main-header').show();

    App.yummly.init();
}










$(document).ready(function(){
		console.log('what what what what what')
		$('.cooking').hide();
		$('.Eating-Out').hide();
        $('.container_fun_subcats').hide();
    //    $('.recipes').hide();
        $('.searchRecipe').hide();
        $('.container_food_subcats').hide();
        $('.container_relax_subcats').hide();
        $('.container_study_subcats').hide();
        $('.container_restaurants').hide();
        $('.main-header').hide();
        $("#map-canvas").hide();
        $('.sidebar').hide()
        $('.Eating-Out').click(Eatingclicked);
	    $('.fun').click(funclicked);
		$('.food').click(foodclicked);
		$('.relax').click(relaxclicked);
		$('.study').click(studyclicked);
        $('.Cooking').click(cookingclicked);
        $("#home1").hide();
		$("#profile").hover(function() {
        $(this).stop().animate({ marginTop: "-10px" }, 200);
        $(this).parent().find("span").stop().animate({ marginTop: "18px", opacity: 0.25 }, 200);
    },function(){
        $(this).stop().animate({ marginTop: "0px" }, 300);
        $(this).parent().find("span").stop().animate({ marginTop: "1px", opacity: 1 }, 300);
    });
		$("#login").hover(function() {
        $(this).stop().animate({ marginTop: "-10px" }, 200);
        $(this).parent().find("span").stop().animate({ marginTop: "18px", opacity: 0.25 }, 200);
    },function(){
        $(this).stop().animate({ marginTop: "0px" }, 300);
        $(this).parent().find("span").stop().animate({ marginTop: "1px", opacity: 1 }, 300);
    });
		$("#home").hover(function() {
        $(this).stop().animate({ marginLeft: "-10px" }, 200);
        $(this).parent().find("span").stop().animate({ marginLeft: "18px", opacity: 0.25 }, 200);
    },function(){
        $(this).stop().animate({ marginLeft: "0px" }, 300);
        $(this).parent().find("span").stop().animate({ marginLeft: "1px", opacity: 1 }, 300);
    });
		$("#home1").hover(function() {
        $(this).stop().animate({ marginLeft: "-10px" }, 200);
        $(this).parent().find("span").stop().animate({ marginLeft: "18px", opacity: 0.25 }, 200);
    },function(){
        $(this).stop().animate({ marginLeft: "0px" }, 300);
        $(this).parent().find("span").stop().animate({ marginLeft: "1px", opacity: 1 }, 300);
    });

		
})

