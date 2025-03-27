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