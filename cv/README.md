# ILMoS Computer Vision Component

CV component is utilized to see whether seats are occupied or not. The changes are reflected onto the server and on all clients.

<p align="center">
  <img src="https://media.giphy.com/media/8NEOz5DPOduuZ0nJqG/giphy.gif" width="720" height="405"/>
</p>

- The *real-time* stream is captured by an IP camera and flooded through the RTSP protocol over TCP.
- Every second a frame is grabbed from the stream and divided into crops.
- Each crop is fed through a ResNet18 that is trained on our private dataset.
- If moving average of decisions made by the model exceeds a noise margin, status are updated.

Weights can be downloaded [here](https://drive.google.com/file/d/1uP5jWd_Rum3bsp9R23c_rYxOsElAMKRY/view?usp=sharing).
