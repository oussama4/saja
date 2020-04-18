// Google Maps

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}



function remove(e){
	var xhr = new XMLHttpRequest();
	var id = e.getAttribute('data-id');
	xhr.onload = function (){
	if(xhr.status >= 200 && xhr.status < 300){
		var response = JSON.parse(xhr.responseText);
		if(response.delete){
			var listItems = document.querySelector('#listItems');
			var badge = document.querySelector('#badge');
			var cart = document.querySelector('#cart');
			listItems.removeChild(document.querySelector(`li[data-id="${id}"]`));
			if(cart)
				cart.removeChild(document.querySelector(`div[data-id="${id}"]`));
			
			document.querySelector('#totalPrice').innerHTML = response.total.toString();
			badge.innerHTML = parseInt(badge.innerHTML) - response.quantity;
			var totalCart = document.querySelector('#totalCart')
                        if (totalCart)  totalCart.innerHTML = response.total;

			var discount = document.querySelector("#discount")
			if(discount) discount.innerHTML = response.discount;
			var totalDiscount = document.querySelector('#totalDiscount')
                        if (totalDiscount) totalDiscount.innerHTML = response.totalDiscount;

		}
	}else{
		console.log('the request failed!');
		}
	}

	//xhr.open('GET', '/remove_from_cart/'+id,true);
	//xhr.send();
	var csrftoken = getCookie('csrftoken');
        xhr.open("POST", '/remove_from_cart/', true);
        xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded; charset=UTF-8");
        xhr.setRequestHeader('X-CSRFToken', csrftoken);
        xhr.send("id="+id);

	
};

function remove_item(e){
	var xhr = new XMLHttpRequest();
	var id  = e.getAttribute('data-id');
	xhr.onload = function(){
		if(xhr.status >= 200 && xhr.status <= 300){
			var response = JSON.parse(xhr.responseText);
			var badge = document.querySelector('#badge');
			badge.innerHTML = parseInt(badge.innerHTML) - 1;
			document.querySelector('#totalPrice').innerHTML = response.total;
			document.querySelector('#totalCart').innerHTML = response.total;
			if(response.delete){
				var listItems = document.querySelector('#listItems');
                        	
                        	var cart = document.querySelector('#cart');
                        	listItems.removeChild(document.querySelector(`li[data-id="${id}"]`));
                        	if(cart)
                                	cart.removeChild(document.querySelector(`div[data-id="${id}"]`));
                        	
			}else if(!response.delete){
				document.querySelector(`input[data-id="${id}"]`).value=response.quantity;
				document.querySelector(`span[data-id="${id}"]`).innerHTML=response.quantity;
				document.querySelector(`.totalItem[data-id="${id}"]`).innerHTML = response.totalItem;
				document.querySelector("#discount").innerHTML = response.discount 
                            	document.querySelector('#totalDiscount').innerHTML = response.totalDiscount;
			}



		}
	}
	//xhr.open('GET','/remove_item/'+id,true);
	//xhr.send()
	var csrftoken = getCookie('csrftoken');
        xhr.open("POST", '/remove_item/', true);
        xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded; charset=UTF-8");
        xhr.setRequestHeader('X-CSRFToken', csrftoken);
        xhr.send("id="+id);


}

 function initMap() {
  var elements = document.querySelectorAll('.js-map');
  Array.prototype.forEach.call(elements, function(el) {
    var lat = +el.dataset.latitude,
        lng = +el.dataset.longitude,
        zoom = +el.dataset.zoom;
    if ((lat !== '') && (lng !== '') && (zoom > 0)) {
      var map = new google.maps.Map(el, {
        zoom: zoom,
        center: { lat: lat, lng: lng },
        disableDefaultUI: true
      });
     var marker = new google.maps.Marker({
        map: map,
        animation: google.maps.Animation.DROP,
        position: { lat: lat, lng: lng }
      });
    }
  });
}

(function(){
	var addItem = document.querySelectorAll('.add_to_cart');
	addItem.forEach(el=>{
		el.addEventListener('click', (e)=>{
			e.preventDefault()
			var id = el.getAttribute('data-id')
			var xhr = new XMLHttpRequest();
			xhr.onload = function () {
				if (xhr.status >= 200 && xhr.status < 300){
					var response = JSON.parse(xhr.responseText);
					var badge = document.querySelector('#badge');
					var listItems = document.querySelector('#listItems');	

					badge.innerHTML = parseInt(badge.innerHTML) + 1 
					if(response.existe){
						document.querySelector(`span[data-id="${id}"]`).innerHTML=response.product[1];
						var input = document.querySelector(`input[data-id="${id}"]`);
						if (input) input.value=response.product[1];

						var totalItem = document.querySelector(`.totalItem[data-id="${id}"]`);
						if (totalItem)  totalItem.innerHTML = response.totalItem;

						var totalCart = document.querySelector('#totalCart')
						if (totalCart)  totalCart.innerHTML = response.total;

						var discount =  document.querySelector("#discount")
						if (discount)  discount.innerHTML = response.discount;
						var totalDiscount = document.querySelector('#totalDiscount')
                        			if (totalDiscount)  totalDiscount.innerHTML = response.totalDiscount; 
					}
					if(!response.existe){
					var htmlItem =`
					<li data-id="${id}" class="item uk-visible-toggle">
                			<article >
                  			<div  class="uk-grid-small" uk-grid>

						<div class="uk-width-1-4">
						   <div class="tm-ratio tm-ratio-4-3">
                        		     	     <a class="tm-media-box" href="#">
                          				<figure class="tm-media-box-wrap">
                            			  	  <img src="${response.product[1]}" alt="${response.product[0]}">
                          				</figure>                       
                        		     	    </a>   
                      				   </div>   
                    				</div>     
                   
                   				<div class="uk-width-expand">   
                      				 <a class="uk-link-heading uk-text-small" href="">${response.product[0]}</a>
                      				 <div class="uk-margin-xsmall uk-grid-small uk-flex-middle" uk-grid>
                        			 <div class="uk-text-bolder uk-text-small">${response.product[2]}</div>
                        			 	<div class="uk-text-meta uk-text-xsmall">
								<span><span data-id="${id}" class='total'>${response.product[3]}</span>×${response.product[2]}</span>
							</div>
                      				 </div>   
                    				</div>     
                                
                    				<div>      
                      				  <button data-id = "${id}" onclick="remove(this)" class="delete_from_cart uk-icon-link uk-text-danger uk-invisible-hover" uk-icon="icon: close; ratio: .75"
						   uk-tooltip="{% trans 'supprimer' %}">
						  </button>
                    				</div> 
					     </div>
					   </article>
					</li>`;
						
					listItems.innerHTML+=htmlItem;
					}
					document.querySelector('#totalPrice').innerHTML = response.total;
					
				}else {
					console.log('The request failed!');
				}
			}
			//xhr.open('GET', '/add_to_cart/'+id,true);
			//xhr.send();
			var csrftoken = getCookie('csrftoken');
			xhr.open("POST", '/add_to_cart/', true);
			xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded; charset=UTF-8");
			xhr.setRequestHeader('X-CSRFToken', csrftoken);
			xhr.send("id="+id);
		})
	})
})();

//      var map;
//      function initMap() {
//        map = new google.maps.Map(document.getElementById('js-map'), {
//          center: {lat: -34.397, lng: 150.644}
//          zoom: 8
//        });
//      }
// Change view

(function (){ 
var mq = window.matchMedia('all and (max-width: 700px)');

if(mq.matches) {

	var upper = document.querySelectorAll('.upper');
	var tog = document.querySelectorAll('.uk-transition-tog');
	tog.forEach(el=>{
		el.classList.remove('uk-transition-tog');
	});
	upper.forEach(el=>{
		el.parentNode.removeChild(el);
	})

}
}
)();
function toggle (e){
	var upper= document.querySelectorAll('.upper');
	var tog = document.querySelectorAll('.uk-transition-tog');
	var flip = document.querySelectorAll('.flip');
	if(e.id=="id"){
		upper.forEach(el => {
			el.style.display='block';
		});
		flip.forEach(el=>{
			el.classList.add('uk-transition-flip');
		});
	}else{
		flip.forEach(el => {
		el.classList.remove('uk-transition-flip');
		});
		upper.forEach(el=>{
			el.style.display='none';
		});
	}
}

(function() {
  var container = document.getElementById('products');

  if(container) {
    var grid = container.querySelector('.js-products-grid'),
        viewClass = 'tm-products-',
        optionSwitch = Array.prototype.slice.call(container.querySelectorAll('.js-change-view a'));

    function init() {
      optionSwitch.forEach(function(el, i) {
        el.addEventListener('click', function(ev) {
          ev.preventDefault();
          _switch(this);
        }, false );
      });
    }

    function _switch(opt) {
      optionSwitch.forEach(function(el) {
        grid.classList.remove(viewClass + el.getAttribute('data-view'));
      });
      grid.classList.add(viewClass + opt.getAttribute('data-view'));
    }

    init();
  }
})();

// Increment

function increment(incrementor, target) {
  var value = parseInt(document.getElementById(target).value, 10);
  value = isNaN(value) ? 0 : value;
  if(incrementor < 0) {
    if(value > 1) {
      value+=incrementor;
    }
  } else {
    value+=incrementor;
  }
  document.getElementById(target).value = value;
}

// Scroll to description

(function() {
//  UIkit.scroll('.js-scroll-to-description', {
//    duration: 300,
//    offset: 58
//  });
})();

// Update sticky tabs

(function() {
//  UIkit.util.on('.js-product-switcher', 'show', function() {
//    UIkit.update();
//  });
})();

// Add to cart

(function() {
  var addToCartButtons = document.querySelectorAll('.js-add-to-cart');

  Array.prototype.forEach.call(addToCartButtons, function(el) {
    el.onclick = function() {
      UIkit.offcanvas('#cart-offcanvas').show();
    };
  });
})();

// Action buttons

(function() {
  var addToButtons = document.querySelectorAll('.js-add-to');

  Array.prototype.forEach.call(addToButtons, function(el) {
    var link;
    var message = '<span class="uk-margin-small-right" uk-icon=\'check\'></span>Added to '  ;
    var links = {
      favorites: '<a href="/favorites">favorites</a>',
      compare: '<a href="/compare">compare</a>',
    };
    if(el.classList.contains('js-add-to-favorites')) {
      link = links.favorites;
    };
    if(el.classList.contains('js-add-to-compare')) {
      link = links.compare;
    }
    el.onclick = function() {
      if(!this.classList.contains('js-added-to')) {
        UIkit.notification({
          message: message + link,
          pos: 'bottom-right'
        });
      }
      this.classList.toggle('tm-action-button-active');
      this.classList.toggle('js-added-to');
    };
  });
})();


