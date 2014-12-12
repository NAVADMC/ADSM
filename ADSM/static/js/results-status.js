var results_status  = (function(pollTime){
    var pollInterval,
        last_progress = 1;

    var update_results_status = function() {
        $.get('/results/simulation_status.json').done(function (status) {
            var simulation_complete = status.iterations_completed == status.iterations_total,
                simulation_progress = status.iterations_total === 0 ? 0 :
                                        Math.max(status.iterations_completed / status.iterations_total,
                                               0.5 / status.iterations_total),
                status_text = status.iterations_started + " of " + status.iterations_total + " iterations in progress. " +
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
            $('.simulation-status').text(status_text);

            last_progress = simulation_progress;
        });
    },

        start_poll = function() { pollInterval = setInterval(update_results_status, pollTime); update_results_status(); },
        stop_poll = function() { clearInterval(pollInterval); };


    return {
        start_poll: start_poll,
        stop_poll: start_poll
    };
})(5000);

results_status.start_poll();
