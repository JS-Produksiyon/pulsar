/**
 * Connection Animation Controller
 * Created: 2026-02-13
 * Last Updated: 2026-02-13
 * 
 * Manages connection, reconnection, and disconnection animations for the Pulsar UI.
 * Handles multi-phase connection animations controlled by the backend.
 */

/**
 * ConnectionAnimationClass - Controls the connection animation state machine
 * 
 * @class
 * @description Manages DOM animations and state transitions for Pulsar-Nebula connection UI
 * @param {Object} [config={}] - Configuration object to override default DOM selectors
 * @param {string} [config.connectButtonId='connect-connect'] - Connect button ID
 * @param {string} [config.cancelButtonId='connect-cancel'] - Cancel button ID
 * @param {string} [config.disconnectButtonId='connect-disconnect'] - Disconnect button ID
 * @param {string} [config.iconConnectedClass='icon-connected'] - Connected icon class
 * @param {string} [config.iconDefaultClass='connect-icon-img'] - Default icon class
 * @param {string} [config.pulsarConnectedIconId='icon-pulsar-connected'] - Pulsar connected icon ID
 * @param {string} [config.nebulaConnectedIconId='icon-nebula-connected'] - Nebula connected icon ID
 * @param {string} [config.pulsarNotConnectedIconId='icon-pulsar-not-connected'] - Pulsar icon container
 * @param {string} [config.nebulaNotConnectedIconId='icon-nebula-not-connected'] - Nebula icon container
 * @param {string} [config.pulsarProgressId='pulsar-to-nebula'] - Pulsar to Nebula progress bar ID
 * @param {string} [config.nebulaProgressId='nebula-to-pulsar'] - Nebula to Pulsar progress bar ID
 * @param {number} [config.fadeDuration=300] - Cross-fade animation duration in milliseconds
 */
class ConnectionAnimationClass {
  constructor(config = {}) {
    // Merge provided config with defaults
    this.config = {
      connectButtonId: 'connect-connect',
      cancelButtonId: 'connect-cancel',
      disconnectButtonId: 'connect-disconnect',
      iconConnectedClass: 'icon-connected',
      iconDefaultClass: 'connect-icon-img',
      pulsarConnectedIconId: 'icon-pulsar-connected',
      nebulaConnectedIconId: 'icon-nebula-connected',
      pulsarNotConnectedIconId: 'icon-pulsar-not-connected',
      nebulaNotConnectedIconId: 'icon-nebula-not-connected',
      pulsarProgressId: 'pulsar-to-nebula',
      nebulaProgressId: 'nebula-to-pulsar',
      fadeDuration: 300,
      ...config
    };

    // track the connection status of the animation class so reconnection
    // only is possible if we were once connected.
    this.connected = false;

    // Bind event handlers to maintain 'this' context
    this.handleConnectClick = this.handleConnectClick.bind(this);
    this.handleCancelClick = this.handleCancelClick.bind(this);
    this.handleDisconnectClick = this.handleDisconnectClick.bind(this);

    // Initialize event listeners
    this.initializeEventListeners();
  }

  /**
   * Initialize click event listeners on buttons
   * @private
   */
  initializeEventListeners() {
    $(`#${this.config.connectButtonId}`).on('click', this.handleConnectClick);
    $(`#${this.config.cancelButtonId}`).on('click', this.handleCancelClick);
    $(`#${this.config.disconnectButtonId}`).on('click', this.handleDisconnectClick);
  }

  /**
   * Handle connect button click - Phase 1 of connection animation
   * @private
   * @returns {boolean} True when animation is complete
   */
  handleConnectClick = () => {
    // Hide connect button and show cancel button
    $(`#${this.config.connectButtonId}`).hide();
    $(`#${this.config.cancelButtonId}`).show();

    // Cross-fade Pulsar icon to connected state
    $(`#${this.config.pulsarNotConnectedIconId}`).hide();
    $(`#${this.config.pulsarConnectedIconId}`).show();

    // Animate Pulsar-to-Nebula progress bar to 100%
    $(`#${this.config.pulsarProgressId} .progress-bar`)
      .animate({ width: '100%' }, this.config.fadeDuration);

    return true;
  };

  /**
   * Handle second phase of connection (called by backend)
   * Completes the connection animation sequence
   * @returns {boolean} True when animation is complete
   */
  startConnectionPhaseTwo() {
    // Cross-fade Nebula icon to connected state
    $(`#${this.config.nebulaNotConnectedIconId}`).hide();
    $(`#${this.config.nebulaConnectedIconId}`).show();

    // Animate Nebula-to-Pulsar progress bar to 0%
    $(`#${this.config.nebulaProgressId} .progress-bar`)
      .animate({ width: '0%' }, this.config.fadeDuration);

    // Hide cancel button and show disconnect button
    $(`#${this.config.cancelButtonId}`).hide();
    $(`#${this.config.disconnectButtonId}`).show();

    this.connected = true;

    return true;
  }

  /**
   * Start reconnection animation - Phase 1
   * Adds animated stripes to progress bars and sets Nebula-to-Pulsar to 100%
   * @returns {boolean} True when animation is complete
   */
  startReconnection() {
    // only trigger if we are connected
    if (!this.connected) { return false; }

    // Set Nebula-to-Pulsar progress bar to 100%
    $(`#${this.config.nebulaProgressId} .progress-bar`)
      .animate({ width: '100%' }, this.config.fadeDuration);

    // Add animated classes to both progress bars
    $(`#${this.config.pulsarProgressId} .progress-bar`)
      .addClass('progress-bar-striped progress-bar-animated');
    $(`#${this.config.nebulaProgressId} .progress-bar`)
      .addClass('progress-bar-striped progress-bar-animated');

    // switch to cancel button
    $(`#${this.config.cancelButtonId}`).show();
    $(`#${this.config.disconnectButtonId}`).hide();

    return true;
  }

  /**
   * Complete reconnection animation - Phase 2
   * Removes animated stripes and resets progress bars
   * @returns {boolean} True when animation is complete
   */
  completeReconnection(yes) {
    // only trigger if we're connected
    if (!this.connected) { return false; }

    // failure is not the default
    if (typeof yes != "boolean") { yes = true; }

    // Remove animated classes from both progress bars
    $(`#${this.config.pulsarProgressId} .progress-bar`)
      .removeClass('progress-bar-striped progress-bar-animated');
    $(`#${this.config.nebulaProgressId} .progress-bar`)
      .removeClass('progress-bar-striped progress-bar-animated');

    // Hide disconnect and/or cancel button and show connect button
    if (!yes) {
        // use the cancel command on the disconnection so it doesn't animate
        // the Nebula progress bar
        this.performDisconnectionAnimation(true);
    } else {
        // Set Nebula-to-Pulsar progress bar to 0%
        $(`#${this.config.nebulaProgressId} .progress-bar`)
            .animate({ width: '0%' }, this.config.fadeDuration);
        $(`#${this.config.cancelButtonId}`).hide();
        $(`#${this.config.disconnectButtonId}`).show();
    }  

    return true;
  }

  /**
   * Handle disconnect button click - Disconnection Protocol
   * @private
   * @returns {boolean} True when animation is complete
   */
  handleDisconnectClick = () => {
    // Remove animated classes from both progress bars
    $(`#${this.config.pulsarProgressId} .progress-bar`)
      .removeClass('progress-bar-striped progress-bar-animated');
    $(`#${this.config.nebulaProgressId} .progress-bar`)
      .removeClass('progress-bar-striped progress-bar-animated');

    this.performDisconnectionAnimation();
    return true;
  };

  /**
   * Handle cancel button click - Cancel Protocol
   * Sends cancel signal to backend and resets animation state
   * @private
   * @returns {boolean} True when animation is complete
   */
  handleCancelClick = () => {
    // Reset animation to original state
    this.performDisconnectionAnimation(true);

    // TODO: Send cancel signal to backend with False boolean
    // Example: this.sendCancelToBackend(false);

    return true;
  };

  /**
   * Perform the disconnection animation sequence
   * Used by both disconnect and cancel handlers
   * 
   * @param {boolean} cancel | (optional) Whether or not the cancel button has been clicked
   * @private
   */
  performDisconnectionAnimation(cancel) {
    // the default is that we are not canceling!
    if (typeof cancel != 'boolean') { cancel = false; }

    // connection is terminated
    this.connected = false;

    // Always reset Pulsar side progress bar
    $(`#${this.config.pulsarProgressId} .progress-bar`)
        .animate({ width: '0%' }, this.config.fadeDuration);
    // Reset the Nebula progress bar if we're not canceling, 
    // but under cancel only if the progress bar has been shrunk
    if (!cancel || (cancel && parseInt($(`#${this.config.pulsarProgressId} .progress-bar`).css("width")) < 150)){
        $(`#${this.config.nebulaProgressId} .progress-bar`)
            .animate({ width: '100%' }, this.config.fadeDuration);
    }

    setTimeout(() => {
        // Cross-fade Pulsar icon back to default
        $(`#${this.config.pulsarConnectedIconId}`).hide();
        $(`#${this.config.pulsarNotConnectedIconId}`).show();

        // Cross-fade Nebula icon back to default
        $(`#${this.config.nebulaConnectedIconId}`).hide();
        $(`#${this.config.nebulaNotConnectedIconId}`).show();

        // Hide disconnect and/or cancel button and show connect button
        $(`#${this.config.disconnectButtonId}`).hide();
        $(`#${this.config.cancelButtonId}`).hide();
        $(`#${this.config.connectButtonId}`).show();
    }, (this.config.fadeDuration*2));
  }

  /**
   * Clean up event listeners and reset state
   * Call this when destroying the object
   * @public
   */
  destroy() {
    $(`#${this.config.connectButtonId}`).off('click', this.handleConnectClick);
    $(`#${this.config.cancelButtonId}`).off('click', this.handleCancelClick);
    $(`#${this.config.disconnectButtonId}`).off('click', this.handleDisconnectClick);
  }
}
