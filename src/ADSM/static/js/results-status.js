var results_status  = (function(pollTime){
    var pollInterval,
        last_progress = 1;

    var update_results_status = function() {
        $.get('/results/simulation_status.json').done(function (context) {
            if( !context.simulation_has_started) { //simulation hasn't started
                $('.simulation-status').text("Starting Simulation...")
                return
            }
            if( context.simulation_has_started && !context.is_simulation_running ){ //not running but has started means it is now stopped 
                //stop_poll()
                console.log("Stopping Poll", context.simulation_has_started, context.is_simulation_running)
                //return
            }
            if( context.simulation_has_started) {
                var simulation_complete = context.iterations_completed == context.iterations_total
                var simulation_progress = context.iterations_total === 0 ? 0 :
                        Math.max(context.iterations_completed / context.iterations_total,
                            0.5 / context.iterations_total)
                var status_text = context.iterations_started + " of " + context.iterations_total + " iterations in progress. " +
                        context.iterations_completed + " of " + context.iterations_total + " iterations completed.";

                if (simulation_complete) {
                    $('.simulation-progress').addClass('done');
                    status_text = "Simulation complete.  " + context.iterations_total + " iterations run.";
                    stop_poll();
                    if (last_progress < 1) {
                        window.location.reload();
                    }
                }
                $('.simulation-progress').width(simulation_progress * 100 + "%");
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
