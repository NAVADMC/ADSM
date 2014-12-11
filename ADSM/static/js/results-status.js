var results_status  = (function(pollTime){
    var pollInterval;

    var update_results_status = function() {
        $.get('/results/simulation_status.json').done(function (status) {
            var simulation_complete = status.iterations_completed == status.iterations_total,
                simulation_progress = status.iterations_total === 0 ? 0 :
                                        Math.max(status.iterations_completed / status.iterations_total,
                                               0.5 / status.iterations_total),
                status_text = status.iterations_started + " of " + status.iterations_total + " iterations in progress. " +
                                status.iterations_completed + " of " + status.iterations_total + " iterations completed.";

            if (simulation_complete) {
                $('.simulation-progress').addClass('progress-bar-success');
                status_text = "Simulation complete.  " + status.iterations_total + " iterations run.";
                stop_poll();
            }
            
            $('.simulation-progress').width(simulation_progress * 100 + "%");
            $('.simulation-status').text(status_text);

        });
    },

        start_poll = function() { update_results_status(); setInterval(update_results_status, pollTime); },
        stop_poll = function() { clearInterval(pollInterval); };


    return {
        start_poll: start_poll,
        stop_poll: start_poll
    };
})(5000);

results_status.start_poll();
