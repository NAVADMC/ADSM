var results_status  = (function(pollTime){
    var pollInterval,
        last_progress = 1;
    var simulation_has_started = false;

    var update_results_status = function() {
        $.get('/results/simulation_status.json').done(function (status) {
            console.log('st', status.is_simulation_running)
            if(status.is_simulation_running) {
                simulation_has_started = true
            } else if( simulation_has_started ){ //not running but has started means it is now stopped 
                stop_poll()
                //return
            }
            if( simulation_has_started) {
                var simulation_complete = status.iterations_completed == status.iterations_total
                var simulation_progress = status.iterations_total === 0 ? 0 :
                        Math.max(status.iterations_completed / status.iterations_total,
                            0.5 / status.iterations_total)
                var status_text = status.iterations_started + " of " + status.iterations_total + " iterations in progress. " +
                        status.iterations_completed + " of " + status.iterations_total + " iterations completed.";

                if (simulation_complete) {
                    $('.simulation-progress').addClass('done');
                    status_text = "Simulation complete.  " + status.iterations_total + " iterations run.";
                    stop_poll();
                    if (last_progress < 1) {
                        window.location.reload();
                    }
                }
                $('.simulation-progress').width(simulation_progress * 100 + "%");
            } else {  //simulation hasn't started
                status_text = "Starting Simulation..."
            }            
            $('.simulation-status').text(status_text);

            last_progress = simulation_progress;
        });
    },

        start_poll = function() { pollInterval = setInterval(update_results_status, pollTime); update_results_status(); },
        stop_poll = function() {
            console.log("Stopping polling")
            clearInterval(pollInterval); 
        };


    return {
        start_poll: start_poll,
        stop_poll: stop_poll,
        get_last_progress: function() { return last_progress; }
    };
})(5000);

results_status.start_poll();
