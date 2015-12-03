/**
 * Created on 12/3/2015 by Josiah for Issue # 668: https://github.com/NAVADMC/ADSM/issues/668
 */

$(function(){
    var $summaryCsv = $('#summary_csv');
    var endpoint = '/results/SummaryCSV/';
    var pollingTask;

    function check_summary_status(){
        $.get(endpoint).done(function(response){
            if (response.status == 'ready') {  // if file is ready
                $summaryCsv.find('button').addClass('hidden')
                $summaryCsv.find('.download-link').removeClass('hidden')
                stop_poll()
            } else if(response.status == 'computing') {  // already started, but not done
                start_poll()
            }
        })
    }
    check_summary_status(); // call immediately on page load

    function start_poll() {
        //replace with spinner
        //credit: http://jsfiddle.net/AndrewDryga/zcX4h/1/
        $summaryCsv.find('button').addClass('active');
        pollingTask = setInterval(check_summary_status, 5000);
    }

    function stop_poll() {
        clearInterval(pollingTask);
    };

    $summaryCsv.find('button').click(function(event){
        //start polling if it hasn't already started
        if(typeof pollingTask === 'undefined'){
            $.post(endpoint, {})  // post to endpoint
            start_poll()
        }
    })

})
