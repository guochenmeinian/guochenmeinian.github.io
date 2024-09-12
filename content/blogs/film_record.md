+++
title = "film & record at once"
date = 2024-04-30
[taxonomies]
tags = ['music']
+++

👋 Hello

As a musician or producer, effectively showcasing your work is essential, and what better way to do this than by filming and recording your sessions. This guide will walk through the process of using Cubase and OBS (Open Broadcaster Software) to capture the screen, camera, and audio tracks simultaneously. For those who are not into music production, learning how to use these tools can enhance your editing skills for other projects, such as streaming and vlogging. So, feel free to stick around to learn how these powerful tools can benefit a wide range of creative endeavors :)

### Setting Up Cubase with OBS
#### Step 1: Configure Audio in Cubase

If you are using windows and not have access to Pro version Cubase like me, you can follow my path to ReaPlugs and add ReaStream Plugin to output the processed sound to OBS as input. Without that plugin, your audio interface will likely not be able to receive the input audio or just simply receive the clean tone from you device (e.g. guitar) with no effects and you probably won't hear the tracks from Cubase.

Here’s how:

1. Download ReaPlugs: Go to Google and search for ReaPlugs. Click on the link to download the bundle from the Reaper website. (Link: ReaPlugs Bundle).
2. Install the bundle like any other plugin and restart Cubase.

{{ youtube(id="IlelvEbFE3s", height="400", width="800") }}

Watch this detailed tutorial to understand how to configure the settings: [Cubase How to Stream/Record Audio Output to OBS](https://www.youtube.com/watch?v=Y3nfyrzPPfc).

#### Step 2: Add ReaStream Plugin to Cubase
1. Open Cubase, go to the Mixer, and select the Stereo Out channel (your master output).
2. Add the ReaStream Standalone plugin to the Stereo Out channel.
3. In the ReaStream plugin interface:
   - Change the mode from Receive Audio to Send Audio.
   - Set the Send mode to Local Broadcast from the dropdown menu.

At this point, Cubase is ready to send its audio output to OBS.

#### Step 3: Configure OBS for Audio, Video, and Screen Capture
Install OBS if it's not already set up.
1. **Camera:** Add a new source by clicking the + under the 'Sources' window. Select Video Capture Device and configure it to capture video from your camera.
2. **Display:** Choose Display Capture, select the monitor displaying Cubase, and confirm. Make sure to capture the entire screen to show all aspects of your production environment.
3. **Audio:** Instead of Audio Output Capture, add an Audio Input Capture.
   - Name it appropriately (e.g., “Cubase Audio”).
   - Mute your microphone input, as the default audio input may capture your voice.

#### Step 4: Set Up VST Plugin in OBS to Capture Cubase Audio
1. In OBS, click the cogwheel next to your **Audio Input Capture** and select Filters.
2. Add a new **VST2 Plugin** by clicking the "+" under the Filters section.
3. Select **ReaStream Standalone** from the dropdown as the plugin.
4. You don't need to modify anything else within the plugin; it's already set to receive the audio from Cubase.

#### Step 5: Recording Your Session
Hit Start Recording in OBS to begin your session recording while Cubase handles the audio and OBS captures the screen and camera.


### Tips for Optimal Recording
- Ensure good lighting and proper camera placement for the best video quality.
- Wear headphones to avoid feedback or echo in the audio.
- Conduct a test run before the actual recording to fix any sync issues between audio and video.


### Conclusion
With Cubase for audio and OBS for video, this setup can help you to capture your music production sessions and I hope this helps you :)





### Reference
[Cubase How to Stream/Record Audio Output to OBS](https://www.youtube.com/watch?v=Y3nfyrzPPfc)
[How to RECORD AUDIO with CUBASE and OBS](https://www.youtube.com/watch?v=X1Bduqqnr9g) \
[How to FILM & RECORD any DAW! (SCREEN AND CAMERA AT ONCE)](https://www.youtube.com/watch?v=Q3s-appprns) \
[DAW Cubase to OBS using loopback plugin.](https://www.youtube.com/watch?v=IlelvEbFE3s)