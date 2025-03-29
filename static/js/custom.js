let autocomplete;

function initAutoComplete(){
autocomplete = new google.maps.places.Autocomplete(
    document.getElementById('id_address'),
    {
        types: ['geocode', 'establishment'],
        //default in this app is "IN" - add your country code
        componentRestrictions: {'country': ['in']},
    })
// function to specify what should happen when the prediction is clicked
autocomplete.addListener('place_changed', onPlaceChanged);
}

function onPlaceChanged (){
    var place = autocomplete.getPlace();

    // User did not select the prediction. Reset the input field or alert()
    if (!place.geometry){
        document.getElementById('id_address').placeholder = "Start typing...";
    }
    else{
        // console.log('place name=>', place.name)
    }
    // get the address components and assign them to the fields
    // console.log(place);
    var geocoder = new google.maps.Geocoder();
    var addressInput = document.getElementById('id_address');
    
    if (!addressInput) {
        console.error("Element with ID 'id_address' not found.");
    } else {
        var address = addressInput.value.trim();
    
        if (!address) {
            console.error("Address field is empty");
        } else {
            geocoder.geocode({ 'address': address }, function (results, status) {
                console.log('results=>', results);
                console.log('status=>', status);
    
                if (status === "OK") {
                    var latitude = results[0].geometry.location.lat();
                    var longitude = results[0].geometry.location.lng();
                    $('#id_latitude').val(latitude)
                    $('#id_longtitude').val(longitude)
                    $('#id_address').val(address)
                } else {
                    console.error("Geocoding failed: " + status);
                }
            });
            
            // let's loop through address components and assign other address data
            console.log(place.address_components)
            for(let i=0;i<place.address_components.length;i++){
                for(let j=0;j<place.address_components[i].types.length;j++){
                    if(place.address_components[i].types[j]=='country'){
                        $('#id_country').val(place.address_components[i].long_name)
                    }
                    if(place.address_components[i].types[j]=='administrative_area_level_1'){
                        $('#id_state').val(place.address_components[i].long_name)
                    }
                    if(place.address_components[i].types[j]=="locality"){
                        $('#id_city').val(place.address_components[i].long_name)
                    }
                    if(place.address_components[i].types[j]=="postal_code"){
                        $('#id_pincode').val(place.address_components[i].long_name)
                    }
                    else{
                        $('#id_pincode').val('')
                    }
                }
            }
        }
    }
}

$(document).ready(function(){
    $('.add_to_cart').on('click',function(e){
        e.preventDefault();
        let food_id=$(this).attr('data-id');
        let url=$(this).attr('data-url');
        $.ajax({
            type:'GET',
            url:url,
            success: function(response){
                // console.log(response)
                if(response.status=='login_required'){
                    // console.log('login_required');
                    Swal.fire({
                        title: "Login Required",
                        text: response['message'],
                        icon: "warning",
                        confirmButtonText: "Login",
                        timer:3000,
                      }).then((result) => {
                        if (result.isConfirmed) {
                          window.location.href = "/login";  // Change to your login URL
                        }
                      });
                      
                }
                else if(response.status=='Failed'){
                    Swal.fire({
                        title: "Failed!",
                        text:response['message'],
                        icon: "error",
                        timer: 3000,
                        showConfirmButton: true 
                      });
                }
                else{
                cart_counter = response?.cart_counter?.cart_count || "0";
                $('#cart_counter').html(cart_counter); 
                
                // Safely access quantity, fallback to "0" if undefined or null
                    let qty = response?.qty ?? "0"; 
                    $('#qty-' + food_id).html(qty);
                    applyCartAmount(response['cart_amount']['subtotal'],response['cart_amount']['grand_total'],response['cart_amount']['tax'])
                }

            }
        });
    });

    // decrease cart
    $('.decrease_cart').on('click',function(e){
        e.preventDefault();
        let food_id=$(this).attr('data-id');
        let url=$(this).attr('data-url');
        let id=$(this).attr('data-cart-id');
                    // console.log(id);
        // console.log(food_id,url);
        $.ajax({
            type:'GET',
            url:url,
            success: function(response){
                //   console.log(response)
                if(response.status=='login_required'){
                    // console.log('login_required');
                    Swal.fire({
                        title: "Login Required",
                        text: response['message'],
                        icon: "warning",
                        confirmButtonText: "Login",
                        timer:3000,
                      }).then((result) => {
                        if (result.isConfirmed) {
                          window.location.href = "/login";  // Change to your login URL
                        }
                      });
                      
                }
                else if(response.status=='Failed'){
                    Swal.fire({
                        title: "Failed!",
                        text:response['message'],
                        icon: "error",
                        timer: 3000,
                        showConfirmButton: true
                      });
                }
                else{
                cart_counter = response?.cart_counter?.cart_count || "0";
                $('#cart_counter').html(cart_counter); 
                
                // Safely access quantity, fallback to "0" if undefined or null
                let qty = response?.qty ?? "0"; 
                $('#qty-' + food_id).html(qty);
                
                 if(window.location.pathname=='/cart/' && qty==0){
                    
                    delete_cart_element(id,response);
                    check_empty_cart();
                 }
                 applyCartAmount(response['cart_amount']['subtotal'],response['cart_amount']['grand_total'],response['cart_amount']['tax']);
                }
  
            }
        });
    });

    // delete cart item 
    $('.delete_cart').on('click',function(e){
        e.preventDefault();
        let item_id=$(this).attr('data-id');
        let url=$(this).attr('data-url');
        // console.log(food_id,url);
        $.ajax({
            type:'GET',
            url:url,
            success: function(response){
                // console.log(response);
                if(response.status=='login_required'){
                    // console.log('login_required');
                    Swal.fire({
                        title: "Login Required",
                        text: response['message'],
                        icon: "warning",
                        confirmButtonText: "Login",
                        timer:3000,
                      }).then((result) => {
                        if (result.isConfirmed) {
                          window.location.href = "/login";  // Change to your login URL
                        }
                      });
                      
                }
                else if(response.status=='Failed'){
                    if(response.message=='Cart Item does not exist in Cart'){
                        delete_cart_element(item_id,response)
                    }
                    else{
                    Swal.fire({
                        title: "Failed!",
                        text:response['message'],
                        icon: "error",
                        timer: 3000,
                        showConfirmButton: true 
                      });
                    }
                }
                else{
                    delete_cart_element(item_id,response)
                    applyCartAmount(response['cart_amount']['subtotal'],response['cart_amount']['grand_total'],response['cart_amount']['tax'])
                }
                check_empty_cart();

            }
        });
    });
    
    function check_empty_cart(){
        if ($("#menu-item-list-6272 ul li").length === 0) {
            // console.log('i m here');
            $("#empty-cart").show();  // Show empty cart message
        }
    }
    // remove cart item
    function delete_cart_element(id,response){
        cart_counter = response?.cart_counter?.cart_count || "0";
        $('#cart_counter').html(cart_counter); 
        $('#cart-item-'+id).remove();
        Swal.fire({
            title: "Item Deleted",
            text: response['message'],
            icon: "success",
            timer: 2000,
            showConfirmButton: false,
            toast: true,
            position: "top-end"
        });
    }

    //apply Cart Amounts
    function applyCartAmount(subtotal,grand_total,tax){
        if(window.location.pathname=='/cart/'){
            $('#subtotal').html(subtotal);
            $('#total').html(grand_total);
            // $('#tax').html(tax);
        }
    }

    // place the cart item quantity on load
    $('.item_qty').each(function(){
        let the_id=$(this).attr('id')
        let quantity=$(this).attr('data-qty')
        // console.log(quantity,the_id)
        // get the previous quantity and then just append to it
        $('#'+the_id).html(quantity)
    });
});


