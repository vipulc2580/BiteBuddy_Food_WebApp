let autocomplete;

function initAutoComplete(){
autocomplete = new google.maps.places.Autocomplete(
    document.getElementById('id_address'),
    {
        types: ['geocode', 'establishment'],
        //default in this app is "IN" - add your country code
        componentRestrictions: {'country': ['in']},
    });
    console.log('i m getting invoked');
// function to specify what should happen when the prediction is clicked
autocomplete.addListener('place_changed', onPlaceChanged);
}

function onPlaceChanged (){
    var place = autocomplete.getPlace();
    console.log('i m into this getting function');
    // User did not select the prediction. Reset the input field or alert()
    if (!place.geometry){
        console.log('id found');
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
                // console.log(response.status)
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
                    applyCartAmount(response['cart_amount']['subtotal'],response['cart_amount']['grand_total'],response['cart_amount']['taxes'])
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
                 applyCartAmount(response['cart_amount']['subtotal'],response['cart_amount']['grand_total'],response['cart_amount']['taxes']);
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
                    applyCartAmount(response['cart_amount']['subtotal'],response['cart_amount']['grand_total'],response['cart_amount']['taxes'])
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
    function applyCartAmount(subtotal,grand_total,taxes){
        if(window.location.pathname=='/cart/'){
            $('#subtotal').html(subtotal);
            $('#total').html(grand_total);
            // console.log('i m getting invoked')
                for (let taxType in taxes) {
                    let taxAmount = Object.values(taxes[taxType])[0];
                    // console.log(`Tax Type: ${taxType}, Tax Amount: ${taxAmount}`);
                //    console.log($('#tax-'+taxType).html())
                   $('#tax-'+taxType).html(taxAmount)
                //    console.log(taxAmount,$('#tax-'+taxType).html())
                }
        }
    }

    // add opening hours to vendor
    $('.add_opening_hours').on('click', function(e){
        e.preventDefault(); // Prevent form submission
        let url=$(this).attr('data-url');
        let day=document.getElementById('id_day').value;
        let from_hour=document.getElementById('id_from_hour').value;
        let to_hour=document.getElementById('id_to_hour').value;
        let is_closed=document.getElementById('id_is_closed').checked;
        let csrf_token=$('input[name=csrfmiddlewaretoken]').val()
        // console.log(day,from_hour,to_hour,is_closed,csrf_token,url)
        if(is_closed){
            is_closed='True'
            condition='day!=""'
        }
        else{
            is_closed='False'
            condition="day!='' && from_hour!='' && to_hour!=''"
        }
        if(eval(condition)){
            $.ajax({
                type:'POST',
                url:url,
                data:{
                    'day':day,
                    'from_hour':from_hour,
                    'to_hour':to_hour,
                    'is_closed':is_closed,
                    'csrfmiddlewaretoken':csrf_token
                },
                success: function(response){
                    if(response.status=='Success'){
                        if (response.is_closed === 'Closed') {
                            html = `<tr id="hour-${response.id}">
                                        <td><b>${response.day}</b></td>
                                        <td>Closed</td>
                                        <td><a href="#" class='remove_hour text-danger' data-url="/vendor/opening_hours/remove/${response.id}/">Remove</a></td>
                                    </tr>`;
                        } else {
                            html = `<tr id="hour-${response.id}">
                                        <td><b>${response.day}</b></td>
                                        <td>${response.from_hour} - ${response.to_hour}</td>
                                        <td><a href="#" class='remove_hour text-danger' data-url="/vendor/opening_hours/remove/${response.id}/">Remove</a></td>
                                    </tr>`;
                        }
        
                        $('.opening_hours tbody').append(html);
                        Swal.fire({
                            title: "Added!",
                            text: response.message,
                            icon: "success",
                            timer: 2000,
                            showConfirmButton: false,
                            toast: true,
                            position: "top-end"
                        });
                        document.getElementById('opening_hours').reset();
                    }else{
                        Swal.fire({
                            title:response.status,
                            text:response.message,
                            icon:'error',
                            confirmButtonText:true,
                        });
                        document.getElementById('opening_hours').reset();
                    }
                }
        })
        }
        else{
            Swal.fire({
                title: "Details Required!",
                text:"Please Fill Details",
                icon: "error",
                showConfirmButton: true
              });
        }
       
    });

    // remove opening hour 
    
    $(document).on('click', '.remove_hour', function(e) {
        e.preventDefault();
        let url = $(this).attr('data-url');
        let row = $(this).closest('tr');  // Get the closest table row
    
        Swal.fire({
            title: "Are you sure?",
            text: "You won't be able to revert this!",
            icon: "warning",
            showCancelButton: true,
            confirmButtonColor: "#d33",
            cancelButtonColor: "#3085d6",
            confirmButtonText: "Yes, delete it!"
        }).then((result) => {
            if (result.isConfirmed) {
                // User clicked "Yes", send AJAX request
                $.ajax({
                    type: 'GET',  // Ideally, DELETE method should be used
                    url: url,
                    success: function(response) {
                        if (response.status === 'Success') {
                            Swal.fire({
                                title: "Deleted!",
                                text: response.message,
                                icon: "success",
                                timer: 2000,
                                showConfirmButton: false,
                                toast: true,
                                position: "top-end"
                            });
                            row.remove();  // Remove the deleted row from the table
                        } else {
                            if (response.message === 'Login Required!') {
                                Swal.fire({
                                    title: "Login Required",
                                    text: response.message,
                                    icon: "warning",
                                    confirmButtonText: "Login",
                                    timer: 3000,
                                }).then((result) => {
                                    if (result.isConfirmed) {
                                        window.location.href = "/login";  // Redirect to login
                                    }
                                });
                            } else {
                                Swal.fire({
                                    title: "Error",
                                    text: response.message,
                                    icon: "error",
                                    timer: 2000,
                                    showConfirmButton: false,
                                    toast: true,
                                    position: "top-end"
                                });
                            }
                        }
                    },
                    error: function() {
                        Swal.fire({
                            title: "Error",
                            text: "Something went wrong! Please try again.",
                            icon: "error",
                            timer: 2000,
                            showConfirmButton: false,
                            toast: true,
                            position: "top-end"
                        });
                    }
                });
            }
        });
    });
    
    // place the cart item quantity on load
    $('.item_qty').each(function(){
        let the_id=$(this).attr('id')
        let quantity=$(this).attr('data-qty')
        // console.log(quantity,the_id)
        // get the previous quantity and then just append to it
        $('#'+the_id).html(quantity)
    });
    $(".reviews-sortby-active").on("click", function(e){
        e.preventDefault();  // Prevents page jump
        $(this).next(".delivery-dropdown").slideToggle();  // Toggle dropdown
    });
});


