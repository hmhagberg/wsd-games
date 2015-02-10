$(document).ready(function() {

    // Showing tooltips without delay positions them wrong
    window.setTimeout(function(){
        $('.form-field').tooltip('show');
    }, 50);

    window.setTimeout(function(){
        $('.form-field').tooltip('hide');
    }, 3500);

    // Search (base_grid.html)
    // http://stackoverflow.com/questions/8746882/jquery-contains-selector-uppercase-and-lower-case-issue
    jQuery.expr[':'].contains = function(a, i, m) {
        return jQuery(a).text().toUpperCase().indexOf(m[3].toUpperCase()) >= 0;
    };
    $("#searchForm").submit(function(event) {
        var search = $("#search").val();
        $(".col-xs-12").each(function(){
           $(this).removeClass("hidden");
           $(this).not(':contains(' + search + ')').addClass("hidden");
        });
        event.preventDefault();
    });
});