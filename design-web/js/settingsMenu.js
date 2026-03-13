// Settings Menu Collapse/Expand Animation

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

    console.log("Expand");
    
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
});

