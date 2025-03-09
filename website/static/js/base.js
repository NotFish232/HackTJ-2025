$(function() {
    let p = window.location.pathname;

    let selected_class = "text-theme-medium font-semibold scale-20";

    $("#btn_1").removeClass(selected_class);
    $("#btn_2").removeClass(selected_class);
    $("#btn_3").removeClass(selected_class);

    if (p === "/") {
        $("#btn_1").addClass(selected_class);
    } else if (p === "/protein_search") {
        $("#btn_2").addClass(selected_class);
    } else if (p === "/visualizer") {
        $("#btn_3").addClass(selected_class);
    }
});