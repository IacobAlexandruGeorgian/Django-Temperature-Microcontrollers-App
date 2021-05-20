$(document).ready(function(){

    $(".datetimeinput").datepicker({changeYear: true, changeMonth: true, dateFormat: 'yy-mm-dd'});

    function removeData(chart) {
    chart.data.datasets.pop();
    chart.update();
}

});