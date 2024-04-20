Windows PowerShell

install package
```bash
npm i y-websocket
```

```bash
$env:PORT=8888 
$env:HOST='localhost' 
$env:YPERSISTENCE ='./data'
```

```bash
npx y-websocket
```


**Documentation**

AI model market research 
Multi-modal model 
- Chatgpt-4 (qualitatively way better)
- Claude 
- Gemini pro
- Qianwen 

Given the same set of images input with manual annotations. 
Ask the model to judge the difference between the two images and highlight the difference.

Initial sketch for the interview room UI
![sketch](https://raw.githubusercontent.com/AllenAnZifeng/MockAI_Backend/master/images/sketch.jpg)

Initial system design for the backend workflow
![first design](https://raw.githubusercontent.com/AllenAnZifeng/MockAI_Backend/master/images/first-design.jpg)

Next.js SSR did not work well with Tldraw image export. Change to using Selenium to run the browser to visit an internal site to get the image.
The second design outlines the new workflow.

![second design](https://raw.githubusercontent.com/AllenAnZifeng/MockAI_Backend/master/images/second-design.jpg)

Deployment Details
- used tailscale to construct a private network to allow homeserver to be exposed
- nginx on public Linode used reverse proxy

![deployment-detail](https://raw.githubusercontent.com/AllenAnZifeng/MockAI_Backend/master/images/deployment-detail.jpg)



