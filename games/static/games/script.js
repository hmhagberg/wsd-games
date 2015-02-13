/*global $, jQuery */
"use strict";

$(document).ready(function() {

    // Showing tooltips without delay positions them wrong
    window.setTimeout(function(){
        $(".form-field").tooltip("show");
    }, 50);

    window.setTimeout(function(){
        $(".form-field").tooltip("hide");
    }, 3500);

    // Timeout for messages (e.g. login, logout...)
    window.setTimeout(function() {
        $(".alert").fadeTo(500, 0).slideUp(500, function(){
            $(this).remove();
            $("#messages-ul").addClass("hidden");
        });
    }, 5000);

    // Search (base_grid.html)
    // http://stackoverflow.com/questions/8746882/jquery-contains-selector-uppercase-and-lower-case-issue
    jQuery.expr[":"].contains = function(a, i, m) {
        return jQuery(a).text().toUpperCase().indexOf(m[3].toUpperCase()) >= 0;
    };
    $("#searchForm").submit(function(event) {
        var search = $("#search").val();
        $(".col-xs-12").each(function(){
           $(this).removeClass("hidden");
           $(this).not(":contains(" + search + ")").addClass("hidden");
        });
        event.preventDefault();
    });

    // Sort games (base_grid_gameCard.html)
    $("#sort-menu").find("a").click(function() {
        $("#sort").html($(this).text() + " <span class='caret'></span>");
        var sort = "";
        var compare = "";
        var count = 0;
        var count2 = 0;
        sort = $(this).text();
        var grid = $("#grid");
        var cardsCount = grid.children().length;
        if (sort === "Name") {
            for (var i = 0; i < cardsCount; i++) {
                compare = "";
                grid.children().each(function() {
                    if ($(this).find("h2").html() > compare && count >= i) {
                        compare = $(this).find("h2").html();
                        count2 = count;
                    }
                    count++;
                });
                grid.children("div:nth-child(" + (count2 + 1).toString() + ")").prependTo("#grid");
                count = 0;
                count2 = 0;
            }
        }
        else if (sort === "Price") {
            for (var j = 0; j < cardsCount; j++) {
                compare = "";
                grid.children().each(function() {
                    if (parseFloat($(this).find(".price").html().substring(7)) > compare && count >= j) {
                        compare = parseFloat($(this).find(".price").html().substring(7));
                        count2 = count;
                    }
                    count++;
                });
                grid.children("div:nth-child(" + (count2 + 1).toString() + ")").prependTo("#grid");
                count = 0;
                count2 = 0;
            }
        }
        else if (sort === "Developer") {
            for (var k = 0; k < cardsCount; k++) {
                compare = "";
                grid.children().each(function() {
                    if ($(this).find(".developer").html() > compare && count >= k) {
                        compare = $(this).find(".developer").html();
                        count2 = count;
                    }
                    count++;
                });
                grid.children("div:nth-child(" + (count2 + 1).toString() + ")").prependTo("#grid");
                count = 0;
                count2 = 0;
            }
        }
    });
});