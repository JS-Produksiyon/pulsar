/** 
 * Pulsar Frontend GUI Javascript 
 * 
 * @version 1.1
 * @author JMW
 * @description This script contains the frontend logic for the Pulsar GUI, handling user interactions, data fetching, and UI updates.
 * @license GNU General Public License v3.0
*/

$(document).ready(function() {

    if ($("#btn_exit_pulsar").length > 0) {
        $("#btn_exit_pulsar").on("click", function() {
            console.log("Exit Pulsar button clicked");
            window.pywebview.api.exitApp();
        });
    }

});