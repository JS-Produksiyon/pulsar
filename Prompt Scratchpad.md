# Prompt Scratchpad

Create another modal, again with the style in lines 453-498. Use Bootstrap 5.3 and jQuery when creating the code.

This one is to be called up by the inbound and outbound connections segments. The title needs to Nebula Firewall Connections :: Inbound or Nebula Firewall Connections :: Outbound depending on the .edit-connection item has data-connection-type="inbound" or data-connection-type="outbound" or the corresponding #btn-add-connection-in or #btn-add-connection-out

The modal needs to have four fields:

1. A number input called Port whose range runs from 0 to the maximum number of ports that an IP address has. There needs to be a note to set this field to 0 if any port is to be able to connect. For an example as to how to make this work see lines 118-120. When saved and set to 0, the content pasted into the table needs to be "Any".

2. A select field called Protocol with four options: Any, ICMP, TCP, and UDP.  The values need to be "any","icmp","tcp", and "udp" respectively. Only "Any" needs to have a translation data-i18n reference.

3. A text box called Host, which defaults to "any". If "Any" is entered, it needs to become lowercase upon updating. The field can only take alphanumeric characters and dashes.

4. A text box called Group, which has the same limitations as Host.

There needs to be a notice underneath Group that either Host or Group need to be filled in and if both are filled in the content in Host will be used. Use the same style of commenting as for the Port field

There needs to be three buttons just like in lines 531-544. Though the label on the Save button needs to be Save Connection and the label on the Delete button needs to be Delete Connection.

Use the logic for translation as found in the modal on lines 500-548. Also use the same logic in in settingsMenu.js to add and remove table rows as used for the Configure Static Host modal (see lines 221ff in settingsMenu.js).

However, if any field has the value of "any", it needs to be written as Any in the table row. If both Host and Group are left empty, assume "Any" in Host. If Host is empty and Group is filled in, Host needs to be set to "N/A". If Host is filled in Group needs to automatically be set as "N/A", even if there is information in 

Link this modal to the edit-connection buttons and have the backend code use the data-row-id in the button to determine which rows to act upon. Also link it to #settingsAddConnectionInBtn and settingsAddConnectionOutBtn respectively and set the fields as follows:

* Port: 0
* Protocol: Any
* Host: any
* Group: <empty>

When saving a new row, increment the highest number among the rows in the given table and assign it to the new row being added.
