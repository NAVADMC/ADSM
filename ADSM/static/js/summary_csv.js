/**
 * Created on 12/3/2015 by Josiah for Issue # 668: https://github.com/NAVADMC/ADSM/issues/668
 */

$(function(){
    var $summaryCsv = $('#summary_csv');
    var endpoint = '/results/SummaryCSV/';
    var pollingTask;
    var requested = false;

    function check_summary_status(){
        $.get(endpoint, function(data, textStatus, xhr){
            switch(xhr.status){
                case 200: {  // if file is ready
                    $summaryCsv.find('button').removeClass('active')
                    $summaryCsv.find('button').addClass('hidden')
                    $summaryCsv.find('.summary-download').removeClass('hidden')
                    stop_poll()
                    if (requested) {
                        location.reload();
                    }
                    return
                }
                case 202: {  // already started, but not done
                    start_poll()
                    return
                }
                case 400:
                    console.log("There aren't results to compute on.")
                    $summaryCsv.find('button').addClass('hidden')
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
        requested = true;
        //start polling if it hasn't already started
        if(typeof pollingTask === 'undefined'){
            $.post(endpoint, {})  // post to endpoint
            start_poll()
        }
    })

})
