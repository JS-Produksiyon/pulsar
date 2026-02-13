# Prompt to test building the connection animation with JS

When building code for me use the following standards:

1. Use camelCase variables.
2. Use Upper CamelCase for class names.
3. Use the whatever standard documentation method is preferred for the language you are working in (e.g. Docstrings and type hinting for Python or JSDoc for Javascript) and document everything except for the most obvious code. Add clear and concise comments to the generated code so it is easy to follow.
4. When creating full documents, designate the documents to be in utf-8 encoding. Follow whatever standard the target language prefers.
5. All documents need to have some sort of comment or docstring at the top with designates the date on which the document was created and a second line designating when the document was last updated. Use ISO-8601 for generating the date strings. Do not include the time, only the date.

## Connection animation

Build me a JavaScript class to control the connection, reconnection and disconnection animation of the icons at the center of the main screen. The most complex of these is the connection animation, as it will need to be controlled in phases as the back end goes through various steps in the connection process.

When building the class, set the various layers as defaults so I can call the class with myConnection = new ConnectionAnimationClass() or something like that and it will work. However, design it in such a way that, if I so wish, I can pass a JSON object designating different DOM IDs or CSS classes for the buttons, icons and layers, if so desired.

DOM manipulation will be done using jQuery.

Connection Protocol:

When the #connect-connect button is clicked, it is replaced with the #connect-cancel button, the image under .connect-icon.pulsar cross-fades to #icon-pulsar-connected , and set the #pulsar-to-nebula .progress-bar width to 100%. Return a boolean to note that the first step of the animation is complete.

The second step is triggered by the back end calling some sort of function attached to the class, in which first the icon under .connect-icon.nebula is cross-faded to #icon-nebula-connect. Then the width of the progress bar under #pulsar-to-nebula .progress-bar to 0% and replace the #connect-cancel button with #connect-disconnect. Return a boolean to note that the second step of the animation is complete.

Disconnection Protocol:

When the #connect-disconnect button is clicked, simultaneously set #pulsar-to-nebula .progress-bar to a width of 0% and #nebula-to-pulsar.progress-bar to 100%. Then cross fade #icon-pulsar-connected back to .connect-icon-image under .connect-icon.pulsar. Do the same with #icon-nebula-connected and .connect-icon-image under .connect-icon.nebula. Replace #connect-disconnect with #connect-connect. Return a boolean to note that the animation is complete.

Cancel Protocol:

When the cancel button is pressed, reset everything to the original state (see Disconnection Protocol) and send a False boolean to the back end to cancel the process.

## Reconnection animation

Add an animation option for reconnection which is triggered by calling a function connected to the class, where in step one .progress-bar-striped and .progress-bar-animated classes are added to #pulsar-to-nebula .progress-bar and #nebula-to-pulsar .progress-bar is set to a width of 100%. A boolean is returned to denote the step was taken.

Then add a second option in which will be triggered when reconnection is complete, where first #nebula-to-pulsar .progress-bar width is set to 0% and then the .progress-bar-stripted and .progress-bar-animated classes are removed from #pulsar-to-nebula .progress-bar.

