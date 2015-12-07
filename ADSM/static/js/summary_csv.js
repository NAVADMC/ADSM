/**
 * Created on 12/3/2015 by Josiah for Issue # 668: https://github.com/NAVADMC/ADSM/issues/668
 */

$(function(){
    var $summaryCsv = $('#summary_csv');
    var endpoint = '/results/SummaryCSV/';
    var pollingTask;

    function check_summary_status(){
        $.get(endpoint).done(function(response){
            switch(response.status){
                case 200: {  // if file is ready
                    $summaryCsv.find('button').addClass('hidden')
                    $summaryCsv.find('.download-link').removeClass('hidden')
                    stop_poll()
                    return
                }
                case 202: {  // already started, but not done
                    start_poll()
                    return
                }
                case 400:
                    console.log("There aren't results to compute on.")
                    return
                case 404: //results haven't been started computing yet
                    //display the button for user to press
                    return
            }

        })
    }
    check_summary_status(); // call immediately on page load

    function start_poll() {
        //replace with spinner
        //credit: http://jsfiddle.net/AndrewDryga/zcX4h/1/
        $summaryCsv.find('button').addClass('active');
        if(typeof pollingTask === 'undefined') {
            pollingTask = setInterval(check_summary_status, 5000);
        }
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
