$(function(){
    var $combineOutputs = $('#combine_outputs');
    var endpoint = '/results/CombineOutputs/';
    var pollingTask;
    var requested = false;

    function check_output_status(){
        $.get(endpoint, function(data, textStatus, xhr){
            switch(xhr.status){
                case 200: {  // if file is ready
                    console.log(200);
                    $combineOutputs.find('button').removeClass('active');
                    //$combineOutputs.find('button').addClass('hidden');
                    stop_poll();
                    if (requested) {
                        location.reload();
                    }
                    return
                }
                case 202: {  // already started, but not done
                    console.log(202);
                    start_poll();
                    return
                }
                case 400:
                    console.log("There aren't results to compute on.");
                    $combineOutputs.find('button').addClass('hidden');
                    return;
                case 404: //results haven't been started computing yet
                    //display the button for user to press
                    console.log(404);
                    return
            }

        })
    }
    check_output_status(); // call immediately on page load

    function start_poll() {
        //replace with spinner
        //credit: http://jsfiddle.net/AndrewDryga/zcX4h/1/
        $combineOutputs.find('button').addClass('active');
        if(typeof pollingTask === 'undefined') {
            pollingTask = setInterval(check_output_status, 5000);
        }
    }

    function stop_poll() {
        clearInterval(pollingTask);
    }

    $combineOutputs.find('button').click(function(){
        requested = true;
        //start polling if it hasn't already started
        if(typeof pollingTask === 'undefined'){
            $.post(endpoint, {});  // post to endpoint
            start_poll()
        }
    })

});
