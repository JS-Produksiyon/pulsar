// Settings Menu Collapse/Expand Animation
/*
  Last Updated: 2026-04-01
*/

$(document).ready(function() {
  const COLLAPSE_WIDTH = 65; // px
  const EXPAND_WIDTH = 346;
  const ANIMATION_DURATION = 300; // ms

  // Collapse menu
  $(document).on('click', '[data-pulsar-link="collapseMenu"]', function(e) {
    e.preventDefault();
    console.log("Collapse")
    
    const $menuExpanded = $('#settings-menu-expanded');
    const $menuCollapsed = $('#settings-menu-collapsed');
    
    if (!$menuExpanded.length || !$menuCollapsed.length) return;

    // Animate to collapse width
    $menuExpanded.animate({ width: COLLAPSE_WIDTH }, ANIMATION_DURATION, function() {
      // Hide expanded, show collapsed
      $menuExpanded.addClass('d-none');
      $menuCollapsed.removeClass('d-none');
    });
  });

  // Expand menu
  $(document).on('click', '[data-pulsar-link="expandMenu"]', function(e) {
    e.preventDefault();
    
    const $menuExpanded = $('#settings-menu-expanded');
    const $menuCollapsed = $('#settings-menu-collapsed');
    
    if (!$menuExpanded.length || !$menuCollapsed.length) return;

    // Show expanded menu
    $menuExpanded.removeClass('d-none');
    $menuCollapsed.addClass('d-none');

    // Calculate target width: min of max-width or col-2 approximation
    // Bootstrap col-2 = 16.666% of container
    const $container = $('#settings');
    const containerWidth = $container.width();
    const col2Width = containerWidth * (3 / 12); // col-2 = 2/12 of container
    const targetWidth = Math.min(EXPAND_WIDTH, col2Width); // Adjust 250 to your preferred max-width

    // Set initial width and animate to expanded width
    $menuExpanded.css({ width: COLLAPSE_WIDTH });
    $menuExpanded.animate({ width: targetWidth }, ANIMATION_DURATION);
  });

  // Handle Nebula Binaries radio button state
  function updateNebulaBinariesState() {
    const $filePathBox = $('#nebulaBinariesFilePathBox');
    const $filePathBrowse = $('#nebulaBinariesFilePathBrowse');
    const isSysPathChecked = $('#nebulaBinariesSysPath').is(':checked');

    // Disable file path elements if system path is selected
    $filePathBox.prop('disabled', isSysPathChecked);
    $filePathBrowse.prop('disabled', isSysPathChecked);

    if (!isSysPathChecked) {
      $filePathBox.focus();
    }

  }

  // Initialize on page load
  updateNebulaBinariesState();

  // Update when radio buttons change
  $(document).on('change', 'input[name="nebulaBinaries"]', function() {
    updateNebulaBinariesState();
  });

  // Show or hide settings sections
  $(".settings-link").click(function (instance) {
    // hide all instances of the settings sections
    $(".settings-config-panel").hide();

    // display the correct settings sections
    if ($(this).data("pulsar-link") == "generalSettings") {
      $("#settings-general").show();
    }
    if ($(this).data("pulsar-link") == "connectionProfiles") {
      if ($("#switchMultipleConnections").is(":checked")) {
        $("#settings-multiple-connections").show();
      } else {
        $("#settings-connection-edit").show();
      }
    }
  });

  // Show single connection screen on edit
  $(".connection-edit").click(function (instance) {
    // hide all instances of the settings sections
    $(".settings-config-panel").hide();

    // code to load single connection data goes here
    $("#connectionProfileId").text($(this).data("connection-id"));

    // show single connection
    $("#settings-connection-edit").show();;

  })

  // ====================================================================
  // EDIT CERTIFICATE MODAL HANDLERS
  // ====================================================================
  
  // Reference to the Bootstrap modal instance
  let editCertificateModalInstance = null;
  
  // Certificate type mapping for display labels
  // This cannot stay like this when we go into localization. I'll leave it for now.
  const certificateTypeLabels = {
    'root': 'Nebula Network Root Certificate',
    'private': 'Node Private Certificate',
    'key': 'Node Private Key'
  };

  // Initialize the modal instance
  const modalElement = document.getElementById('editCertificateModal');
  if (modalElement) {
    editCertificateModalInstance = new bootstrap.Modal(modalElement, {
      backdrop: 'static',
      keyboard: false
    });
  }

  // Open certificate edit modal when edit buttons are clicked
  $(document).on('click', '#settings-connection-root-cert-edit, #settings-connection-private-cert-edit, #settings-connection-private-key-edit', function(e) {
    e.preventDefault();
    
    // Determine which certificate type is being edited based on button ID
    const buttonId = $(this).attr('id');
    let certType = '';
    
    if (buttonId === 'settings-connection-root-cert-edit') {
      certType = 'root';
    } else if (buttonId === 'settings-connection-private-cert-edit') {
      certType = 'private';
    } else if (buttonId === 'settings-connection-private-key-edit') {
      certType = 'key';
    }
    
    // Set the certificate type in the modal title
    $('#certificateTypeLabel').text(certificateTypeLabels[certType] || 'Certificate');
    
    // Store the certificate type for use in save handler
    $('#editCertificateModal').data('currentCertType', certType);
    
    // Clear the form fields
    $('#certificateTextArea').val('');
    $('#certificateFilePath').val('');
    
    // Show the modal
    if (editCertificateModalInstance) {
      editCertificateModalInstance.show();
    }
  });

  // Handle save certificate button click
  $(document).on('click', '#modalCertificateSave', function(e) {
    e.preventDefault();
    
    // Get the current certificate type
    const certType = $('#editCertificateModal').data('currentCertType');
    
    // Get the certificate data (either from text area or file path)
    const certificateText = $('#certificateTextArea').val().trim();
    const certificateFile = $('#certificateFilePath').val().trim();
    
    // Validate that at least one field is filled
    if (!certificateText && !certificateFile) {
      alert('Please enter certificate text or select a certificate file.');
      return;
    }
    
    // TODO: Add backend call here to import/save the certificate
    // Example structure:
    // $.ajax({
    //   url: '/api/certificate/import',
    //   type: 'POST',
    //   data: {
    //     type: certType,
    //     text: certificateText,
    //     file: certificateFile
    //   },
    //   success: function(response) {
    //     // Handle successful save
    //     editCertificateModalInstance.hide();
    //   },
    //   error: function(error) {
    //     // Handle error
    //     console.error('Certificate save error:', error);
    //   }
    // });
    
    console.log('Saving certificate of type:', certType);
    console.log('Certificate text provided:', !!certificateText);
    console.log('Certificate file path:', certificateFile);
  });

  // Handle file browse button click for certificate file selection
  $(document).on('click', '#certificateFileBrowse', function(e) {
    e.preventDefault();
    
    // TODO: Implement file browser dialog
    // This will depend on your desktop application framework
    // For web-based apps, you might use a file input instead
    console.log('Certificate file browser clicked');
  });

});


