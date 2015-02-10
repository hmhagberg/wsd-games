$(document).ready(function() {

    // Showing tooltips without delay positions them wrong
    window.setTimeout(function(){
        $('.form-field').tooltip('show');
    }, 50);

    window.setTimeout(function(){
        $('.form-field').tooltip('hide');
    }, 3500);
});