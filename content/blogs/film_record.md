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

If you are using windows and not have access to Pro version Cubase like me, you can follow my path to use the loopback plugin to output the processed sound to OBS as input. without that plugin, the input from your audio interface will likely be clean tone from you device (e.g. guitar) with no effects and you probably won't hear the tracks from Cubase.

{{ youtube(id="IlelvEbFE3s", height="400", width="800") }}

Watch this detailed tutorial to understand how to configure the settings: [DAW Cubase to OBS using loopback plugin.](https://www.youtube.com/watch?v=IlelvEbFE3s)

#### Step 2: Prepare OBS for Video, Screen, and Audio Capture
Install OBS if it's not already set up.
1. For camera, add a new source by clicking the + under the 'Sources' window. Select Video Capture Device and configure it to capture video from your camera.
2. For display, choose Display Capture, select the monitor displaying Cubase, and confirm. Make sure to capture the entire screen to show all aspects of your production environment.
3. For audio, instead of using Audio Output Capture, choose **Audio Input Capture** to ensure it uses the loopback feed. Select your loopback device as the source. This setup ensures that OBS captures the mixed audio outputting from Cubase, including all effects and tracks.

#### Step 3: Syncing Audio and Video
To sync your audio with your video in OBS, fine-tune the delay:

Right-click on the audio source in the 'Sources' list and select Advanced Audio Properties.
Here, you can set the sync offset for your audio source. Adjust this until your audio aligns perfectly with the video, testing with a clap or a metronome.

#### Step 4: Recording Your Session
Hit the ‘Start Recording’ button in OBS to start screensharing.
Then perform your session in Cubase while OBS captures the screen and camera.


### Tips for Optimal Recording
Ensure good lighting and proper camera placement for the best video quality.
Wear headphones to avoid feedback or echo in the audio.
Conduct a test run before the actual recording to fix any sync issues between audio and video.


### Conclusion
With Cubase for audio and OBS for video, this setup can help you to capture your music production sessions and I hope this helps you :)





### Reference
[How to RECORD AUDIO with CUBASE and OBS](https://www.youtube.com/watch?v=X1Bduqqnr9g) \
[How to FILM & RECORD any DAW! (SCREEN AND CAMERA AT ONCE)](https://www.youtube.com/watch?v=Q3s-appprns) \
[DAW Cubase to OBS using loopback plugin.](https://www.youtube.com/watch?v=IlelvEbFE3s)