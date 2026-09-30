// Settings Menu Collapse/Expand Animation
/*
  Last Updated: 2026-04-25
*/

$(document).ready(function() {
  const COLLAPSE_WIDTH = 65; // px
  const EXPAND_WIDTH = 346;
  const ANIMATION_DURATION = 300; // ms

  // Collapse menu
  $(document).on('click', '[data-pulsar-link="collapseMenu"]', function(e) {
    e.preventDefault(); 
    
    const $menuExpanded = $('#settings-menu-expanded');
    const $menuCollapsed = $('#settings-menu-collapsed');
    
    if (!$menuExpanded.length || !$menuCollapsed.length) return;

    // Animate to collapse width
    $menuExpanded.animate({ width: COLLAPSE_WIDTH }, ANIMATION_DURATION, function() {
      // Hide expanded, show collapsed
      $menuExpanded.addClass('d-none');
      $menuCollapsed.removeClass('d-none');
      $(".settings-height-right").addClass("expanded");
    });
    
  });

  // Expand menu
  $(document).on('click', '[data-pulsar-link="expandMenu"]', function(e) {
    e.preventDefault();
    
    const $menuExpanded = $('#settings-menu-expanded');
    const $menuCollapsed = $('#settings-menu-collapsed');
    
    if (!$menuExpanded.length || !$menuCollapsed.length) return;

    $(".settings-height-right").removeClass("expanded");

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
    // hide all instances of the settings sections, but only if not collapsing...
    if ($(this).data("pulsar-link") != "collapseMenu" && $(this).data("pulsar-link") != "expandMenu") {
      $(".settings-config-panel").hide();
    }
    // display the correct settings sections
    if ($(this).data("pulsar-link") == "generalSettings") {
      $("#settings-general").show();
    }
    if ($(this).data("pulsar-link") == "connectionProfiles") {
      if ($("#switchMultipleConnections").is(":checked")) {
        $("#settings-multiple-connections").show();
        $("#deleteConnectionButton").removeClass("pulsar-d-none");
      } else {
        $("#deleteConnectionButton").addClass("pulsar-d-none");
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

  // ====================================================================
  // CONFIGURE STATIC HOSTS MODAL HANDLERS
  // ====================================================================

  // Bootstrap modal instances for static host dialogs
  let staticHostModalInstance = null;
  let deleteStaticHostModalInstance = null;

  // Track which row is being edited (null = adding new)
  let editingStaticHostRowId = null;

  // Initialize static host modal
  const staticHostModalEl = document.getElementById('configureStaticHostModal');
  if (staticHostModalEl) {
    staticHostModalInstance = new bootstrap.Modal(staticHostModalEl, {
      backdrop: 'static',
      keyboard: false
    });
  }

  // Initialize delete confirmation modal
  const deleteStaticHostModalEl = document.getElementById('deleteStaticHostModal');
  if (deleteStaticHostModalEl) {
    deleteStaticHostModalInstance = new bootstrap.Modal(deleteStaticHostModalEl, {
      backdrop: 'static',
      keyboard: false
    });
  }

  // Open modal to EDIT an existing static host row
  $(document).on('click', '.edit-static-host', function(e) {
    e.preventDefault();

    const rowId = $(this).data('row-id');
    const $row = $('#nodeStaticHostsTable tbody tr[data-row-id="' + rowId + '"]');
    if (!$row.length) return;

    // Store row ID so save/delete know which row to target
    editingStaticHostRowId = rowId;

    // Read values from the table row columns
    const internalIP = $row.find('td:eq(1)').text().trim();
    const externalIP = $row.find('td:eq(2)').text().trim();
    const isLighthouse = $row.find('td:eq(0) .fa-lighthouse').length > 0;

    // Populate modal fields
    $('#staticHostInternalIP').val(internalIP);
    $('#staticHostExternalIP').val(externalIP);
    $('#switchStaticHostLighthouse').prop('checked', isLighthouse);

    // Show delete button when editing an existing host
    $('#modalStaticHostDelete').show();

    if (staticHostModalInstance) {
      staticHostModalInstance.show();
    }
  });

  // Open modal to ADD a new static host (empty fields)
  $(document).on('click', '#btn-add-static-host', function(e) {
    e.preventDefault();

    // No row being edited
    editingStaticHostRowId = null;

    // Clear all fields
    $('#staticHostInternalIP').val('');
    $('#staticHostExternalIP').val('');
    $('#switchStaticHostLighthouse').prop('checked', false);

    // Hide delete button when adding a new host
    $('#modalStaticHostDelete').hide();

    if (staticHostModalInstance) {
      staticHostModalInstance.show();
    }
  });

  // SAVE static host (update existing row or append new row)
  $(document).on('click', '#modalStaticHostSave', function(e) {
    e.preventDefault();

    const internalIP = $('#staticHostInternalIP').val().trim();
    const externalIP = $('#staticHostExternalIP').val().trim();
    const isLighthouse = $('#switchStaticHostLighthouse').is(':checked');

    // Require both fields
    if (!internalIP || !externalIP) {
      alert('Please fill in both IP fields.');
      return;
    }

    // Check for duplicate Internal IP (skip the row being edited)
    let duplicateFound = false;
    $('#nodeStaticHostsTable tbody tr').each(function() {
      const rowId = $(this).data('row-id');
      if (editingStaticHostRowId && rowId == editingStaticHostRowId) return; // skip self
      if ($(this).find('td:eq(1)').text().trim() === internalIP) {
        duplicateFound = true;
        return false; // break
      }
    });
    if (duplicateFound) {
      alert('A static host with Internal IP "' + internalIP + '" already exists.');
      return;
    }

    // Lighthouse icon HTML (empty string when not a lighthouse)
    const lighthouseHtml = isLighthouse
      ? '<i class="fa-regular fa-lighthouse"></i>'
      : '';

    if (editingStaticHostRowId) {
      // --- Update existing row ---
      const $row = $('#nodeStaticHostsTable tbody tr[data-row-id="' + editingStaticHostRowId + '"]');
      $row.find('td:eq(0)').html(lighthouseHtml);
      $row.find('td:eq(1)').text(internalIP);
      $row.find('td:eq(2)').text(externalIP);
    } else {
      // --- Add new row ---
      // Determine next row ID (highest existing + 1)
      let maxId = 0;
      $('#nodeStaticHostsTable tbody tr').each(function() {
        const id = parseInt($(this).data('row-id'), 10);
        if (id > maxId) maxId = id;
      });
      const newId = maxId + 1;

      // Build row HTML matching existing table structure
      const newRow =
        '<tr class="align-middle" data-row-id="' + newId + '">' +
          '<td class="text-center">' + lighthouseHtml + '</td>' +
          '<td>' + $('<span>').text(internalIP).html() + '</td>' +
          '<td>' + $('<span>').text(externalIP).html() + '</td>' +
          '<td class="text-end">' +
            '<button class="btn btn-sm btn-primary edit-static-host" data-row-id="' + newId + '" data-i18n-title="settingsEditStaticHostBtn" title="Edit Static Host">' +
              '<i class="fa-regular fa-pencil"></i>' +
            '</button>' +
          '</td>' +
        '</tr>';

      $('#nodeStaticHostsTable tbody').append(newRow);
    }

    // Close modal
    if (staticHostModalInstance) {
      staticHostModalInstance.hide();
    }
  });

  // DELETE button — open confirmation modal
  $(document).on('click', '#modalStaticHostDelete', function(e) {
    e.preventDefault();
    if (deleteStaticHostModalInstance) {
      deleteStaticHostModalInstance.show();
    }
  });

  // CONFIRM DELETE — remove the row and close both modals
  $(document).on('click', '#modalStaticHostConfirmDelete', function(e) {
    e.preventDefault();

    if (editingStaticHostRowId) {
      $('#nodeStaticHostsTable tbody tr[data-row-id="' + editingStaticHostRowId + '"]').remove();
      editingStaticHostRowId = null;
    }

    // Close confirmation modal, then close the host modal
    if (deleteStaticHostModalInstance) {
      deleteStaticHostModalInstance.hide();
    }
    if (staticHostModalInstance) {
      staticHostModalInstance.hide();
    }
  });

  // ====================================================================
  // CONFIGURE HOST MODAL HANDLERS
  // ====================================================================

  // Bootstrap modal instances for host dialogs
  let hostModalInstance = null;
  let deleteHostModalInstance = null;

  // Track which row is being edited (null = adding new)
  let editingHostRowId = null;

  // Initialize host modal
  const hostModalEl = document.getElementById('configureHostModal');
  if (hostModalEl) {
    hostModalInstance = new bootstrap.Modal(hostModalEl, {
      backdrop: 'static',
      keyboard: false
    });
  }

  // Initialize delete confirmation modal
  const deleteHostModalEl = document.getElementById('deleteHostModal');
  if (deleteHostModalEl) {
    deleteHostModalInstance = new bootstrap.Modal(deleteHostModalEl, {
      backdrop: 'static',
      keyboard: false
    });
  }

  // Open modal to EDIT an existing host row
  $(document).on('click', '.edit-hosts', function(e) {
    e.preventDefault();

    const rowId = $(this).data('row-id');
    const $row = $('#hostsTable tbody tr[data-row-id="' + rowId + '"]');
    if (!$row.length) return;

    // Store row ID so save/delete know which row to target
    editingHostRowId = rowId;

    // Read values from the table row columns
    const hostName = $row.find('td:eq(0)').text().trim();
    const hostIP = $row.find('td:eq(1)').text().trim();

    // Populate modal fields
    $('#hostName').val(hostName);
    $('#hostIPAddress').val(hostIP);

    // Show delete button when editing an existing host
    $('#modalHostDelete').show();

    if (hostModalInstance) {
      hostModalInstance.show();
    }
  });

  // Open modal to ADD a new host (empty fields)
  $(document).on('click', '#btn-add-host', function(e) {
    e.preventDefault();

    // No row being edited
    editingHostRowId = null;

    // Clear all fields
    $('#hostName').val('');
    $('#hostIPAddress').val('');

    // Hide delete button when adding a new host
    $('#modalHostDelete').hide();

    if (hostModalInstance) {
      hostModalInstance.show();
    }
  });

  // SAVE host (update existing row or append new row)
  $(document).on('click', '#modalHostSave', function(e) {
    e.preventDefault();

    const hostName = $('#hostName').val().trim();
    const hostIP = $('#hostIPAddress').val().trim();

    // Require both fields
    if (!hostName || !hostIP) {
      alert('Both Host Name and Host IP Address are required.');
      return;
    }

    // Validate Host Name (domain name syntax)
    const domainRegex = /^[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$/;
    if (!domainRegex.test(hostName)) {
      alert('Host Name must conform to correct domain name syntax.');
      return;
    }

    // Validate Host IP Address (IPv4 or IPv6)
    const ipv4Regex = /^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/;
    const ipv6Regex = /^(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))$/;
    if (!ipv4Regex.test(hostIP) && !ipv6Regex.test(hostIP)) {
      alert('Host IP Address must be a valid IPv4 or IPv6 address.');
      return;
    }

    // Check for duplicate Host Name (skip the row being edited)
    let duplicateFound = false;
    $('#hostsTable tbody tr').each(function() {
      if ($(this).data('row-id') === editingHostRowId) return; // Skip the row being edited
      const existingHostName = $(this).find('td:eq(0)').text().trim();
      if (existingHostName === hostName) {
        duplicateFound = true;
        return false;
      }
    });
    if (duplicateFound) {
      alert('A host with this name already exists.');
      return;
    }

    if (editingHostRowId) {
      // Update existing row
      const $row = $('#hostsTable tbody tr[data-row-id="' + editingHostRowId + '"]');
      $row.find('td:eq(0)').text(hostName);
      $row.find('td:eq(1)').text(hostIP);
    } else {
      // Add new row
      const newRowId = Date.now(); // Simple unique ID
      const newRow = `
        <tr data-row-id="${newRowId}">
          <td>${hostName}</td>
          <td>${hostIP}</td>
          <td>
            <button class="btn btn-sm btn-primary edit-hosts" data-row-id="${newRowId}" data-i18n-title="settingsEditHostRecord" title="Edit Host Record">
              <i class="fa-regular fa-pencil"></i>
            </button>
          </td>
        </tr>
      `;
      $('#hostsTable tbody').append(newRow);
    }

    // Close modal
    if (hostModalInstance) {
      hostModalInstance.hide();
    }
  });

  // DELETE button — open confirmation modal
  $(document).on('click', '#modalHostDelete', function(e) {
    e.preventDefault();
    if (deleteHostModalInstance) {
      deleteHostModalInstance.show();
    }
  });

  // CONFIRM DELETE — remove the row and close both modals
  $(document).on('click', '#modalHostConfirmDelete', function(e) {
    e.preventDefault();

    if (editingHostRowId) {
      $('#hostsTable tbody tr[data-row-id="' + editingHostRowId + '"]').remove();
    }

    // Close confirmation modal, then close the host modal
    if (deleteHostModalInstance) {
      deleteHostModalInstance.hide();
    }
    if (hostModalInstance) {
      hostModalInstance.hide();
    }
  });

  // ====================================================================
  // CONFIGURE FIREWALL CONNECTION MODAL HANDLERS
  // ====================================================================

  // Bootstrap modal instances for firewall connection dialogs
  let connectionModalInstance = null;
  let deleteConnectionModalInstance = null;

  // Track which row and table are being edited (null = adding new)
  let editingConnectionRowId = null;
  let editingConnectionType = null; // 'inbound' or 'outbound'

  // Direction labels for the modal title
  const connectionDirectionLabels = {
    'inbound': 'Inbound',
    'outbound': 'Outbound'
  };

  // Initialize connection modal
  const connectionModalEl = document.getElementById('configureConnectionModal');
  if (connectionModalEl) {
    connectionModalInstance = new bootstrap.Modal(connectionModalEl, {
      backdrop: 'static',
      keyboard: false
    });
  }

  // Initialize delete connection confirmation modal
  const deleteConnectionModalEl = document.getElementById('deleteConnectionModal');
  if (deleteConnectionModalEl) {
    deleteConnectionModalInstance = new bootstrap.Modal(deleteConnectionModalEl, {
      backdrop: 'static',
      keyboard: false
    });
  }

  /**
   * Returns the jQuery table selector based on connection type.
   */
  function getConnectionTable(type) {
    return type === 'inbound'
      ? '#nodeInboundConnectionTable'
      : '#nodeOutboundConnectionTable';
  }

  /**
   * Strips non-alphanumeric/dash characters from a value.
   */
  function sanitizeAlphanumDash(val) {
    return val.replace(/[^a-zA-Z0-9\-]/g, '');
  }

  /**
   * Capitalises "any" to "Any" for table display, passes others through.
   */
  function displayValue(val) {
    return val.toLowerCase() === 'any' ? 'Any' : val;
  }

  // Restrict Host and Group fields to alphanumeric + dash on input
  $(document).on('input', '#connectionHost, #connectionGroup', function() {
    $(this).val(sanitizeAlphanumDash($(this).val()));
  });

  // Open modal to EDIT an existing firewall connection row
  $(document).on('click', '.edit-connection', function(e) {
    e.preventDefault();

    const rowId = $(this).data('row-id');
    const connType = $(this).data('connection-type');
    const tableSelector = getConnectionTable(connType);
    const $row = $(tableSelector + ' tbody tr[data-row-id="' + rowId + '"]');
    if (!$row.length) return;

    // Store editing context
    editingConnectionRowId = rowId;
    editingConnectionType = connType;

    // Set modal title direction label
    $('#connectionDirectionLabel').text(connectionDirectionLabels[connType] || connType);

    // Read values from row: Port, Protocol, Host, Group
    const portText = $row.find('td:eq(0)').text().trim();
    const protoText = $row.find('td:eq(1)').text().trim();
    const hostText = $row.find('td:eq(2)').text().trim();
    const groupText = $row.find('td:eq(3)').text().trim();

    // Populate fields ("Any" → 0 for port, lowercase for selects/text)
    $('#connectionPort').val(portText === 'Any' ? 0 : parseInt(portText, 10));
    $('#connectionProtocol').val(protoText.toLowerCase());
    $('#connectionHost').val(hostText === 'N/A' ? '' : hostText.toLowerCase());
    $('#connectionGroup').val(groupText === 'N/A' ? '' : groupText.toLowerCase());

    // Show delete button when editing
    $('#modalConnectionDelete').show();

    if (connectionModalInstance) {
      connectionModalInstance.show();
    }
  });

  // Open modal to ADD a new OUTBOUND connection
  $(document).on('click', '#btn-add-connection-out', function(e) {
    e.preventDefault();

    editingConnectionRowId = null;
    editingConnectionType = 'outbound';

    // Set title direction
    $('#connectionDirectionLabel').text(connectionDirectionLabels['outbound']);

    // Default field values
    $('#connectionPort').val(0);
    $('#connectionProtocol').val('any');
    $('#connectionHost').val('any');
    $('#connectionGroup').val('');

    // Hide delete button for new entries
    $('#modalConnectionDelete').hide();

    if (connectionModalInstance) {
      connectionModalInstance.show();
    }
  });

  // Open modal to ADD a new INBOUND connection
  $(document).on('click', '#btn-add-connection-in', function(e) {
    e.preventDefault();

    editingConnectionRowId = null;
    editingConnectionType = 'inbound';

    // Set title direction
    $('#connectionDirectionLabel').text(connectionDirectionLabels['inbound']);

    // Default field values
    $('#connectionPort').val(0);
    $('#connectionProtocol').val('any');
    $('#connectionHost').val('any');
    $('#connectionGroup').val('');

    // Hide delete button for new entries
    $('#modalConnectionDelete').hide();

    if (connectionModalInstance) {
      connectionModalInstance.show();
    }
  });

  // SAVE firewall connection (update existing row or append new row)
  $(document).on('click', '#modalConnectionSave', function(e) {
    e.preventDefault();

    let port = parseInt($('#connectionPort').val(), 10);
    const protocol = $('#connectionProtocol').val();
    let host = sanitizeAlphanumDash($('#connectionHost').val().trim());
    let group = sanitizeAlphanumDash($('#connectionGroup').val().trim());

    // Clamp port to valid range
    if (isNaN(port) || port < 0) port = 0;
    if (port > 65535) port = 65535;

    // Normalize "any" to lowercase for comparison
    if (host.toLowerCase() === 'any') host = 'any';
    if (group.toLowerCase() === 'any') group = 'any';

    // If both Host and Group are empty, default Host to "any"
    if (!host && !group) {
      host = 'any';
    }

    // If Host is filled, Group becomes N/A
    // If Host is empty but Group is filled, Host becomes N/A
    let displayHost, displayGroup;
    if (host) {
      displayHost = displayValue(host);
      displayGroup = 'N/A';
    } else {
      displayHost = 'N/A';
      displayGroup = displayValue(group);
    }

    // Port display: 0 → "Any", otherwise the number
    const displayPort = (port === 0) ? 'Any' : port;

    // Protocol display: capitalise "any" → "Any", uppercase others
    const protoMap = { 'any': 'Any', 'icmp': 'ICMP', 'tcp': 'TCP', 'udp': 'UDP' };
    const displayProto = protoMap[protocol] || protocol;

    const tableSelector = getConnectionTable(editingConnectionType);
    const connTypeAttr = editingConnectionType;
    const editBtnTitle = connTypeAttr === 'inbound' ? 'Edit Inbound Connection' : 'Edit Outbound Connection';
    const editBtnI18n = connTypeAttr === 'inbound' ? 'settingsEditInboundBtn' : 'settingsEditOutboundBtn';

    if (editingConnectionRowId) {
      // --- Update existing row ---
      const $row = $(tableSelector + ' tbody tr[data-row-id="' + editingConnectionRowId + '"]');
      $row.find('td:eq(0)').text(displayPort);
      $row.find('td:eq(1)').text(displayProto);
      $row.find('td:eq(2)').text(displayHost);
      $row.find('td:eq(3)').text(displayGroup);
    } else {
      // --- Add new row ---
      // Determine next row ID from the target table
      let maxId = 0;
      $(tableSelector + ' tbody tr').each(function() {
        const id = parseInt($(this).data('row-id'), 10);
        if (id > maxId) maxId = id;
      });
      const newId = maxId + 1;

      // Build row HTML matching existing table structure
      const newRow =
        '<tr data-row-id="' + newId + '">' +
          '<td>' + $('<span>').text(displayPort).html() + '</td>' +
          '<td>' + $('<span>').text(displayProto).html() + '</td>' +
          '<td>' + $('<span>').text(displayHost).html() + '</td>' +
          '<td>' + $('<span>').text(displayGroup).html() + '</td>' +
          '<td class="text-end">' +
            '<button class="btn btn-sm btn-primary edit-connection" data-connection-type="' + connTypeAttr + '" data-row-id="' + newId + '" data-i18n-title="' + editBtnI18n + '" title="' + editBtnTitle + '">' +
              '<i class="fa-regular fa-pencil"></i>' +
            '</button>' +
          '</td>' +
        '</tr>';

      $(tableSelector + ' tbody').append(newRow);
    }

    // Close modal
    if (connectionModalInstance) {
      connectionModalInstance.hide();
    }
  });

  // DELETE button — open confirmation modal
  $(document).on('click', '#modalConnectionDelete', function(e) {
    e.preventDefault();
    if (deleteConnectionModalInstance) {
      deleteConnectionModalInstance.show();
    }
  });

  // CONFIRM DELETE — remove the row and close both modals
  $(document).on('click', '#modalConnectionConfirmDelete', function(e) {
    e.preventDefault();

    if (editingConnectionRowId && editingConnectionType) {
      const tableSelector = getConnectionTable(editingConnectionType);
      $(tableSelector + ' tbody tr[data-row-id="' + editingConnectionRowId + '"]').remove();
      editingConnectionRowId = null;
    }

    // Close confirmation modal, then the connection modal
    if (deleteConnectionModalInstance) {
      deleteConnectionModalInstance.hide();
    }
    if (connectionModalInstance) {
      connectionModalInstance.hide();
    }
  });

  // Open dialog to edit config file directly
  $("#connectionEditConfigFile").click(function (instance){
    // code to get raw .yaml from backend goes here

    // open the modal
    $("#modalEditConfigFile").modal("show");
    // focus on the edit field as soon as the modal opens
    $("#modalEditConfigFileText").trigger("focus");
  });


  // Keep Alive button functions
  if ($("#switchProfileKeepAlive").length > 0) {
    $("#switchProfileKeepAlive").click(function (instance) {
      let pingSwitch = $("#switchProfileNoPing");
      
      if ($(this).is(":checked")) {
        pingSwitch.prop("checked", false);
        pingSwitch.prop("disabled", true);
      } else {
        pingSwitch.prop("disabled", false);
      }
    });
  }

});


