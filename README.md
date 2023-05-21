# python-neural-network-from-scratch
Simple neural network that can recognize handwritten doodles.
The versions in the requirements file are the ones I used, but you can use the latest versions.

### Training

When you first run the script, you need to train the network. Set the parameters you want or use the ones below. Draw the sample, give it label in the "Label" textbox and click the "Save button" to save the training sample. Draw at least 5 samples for each label.

UI explanation:
- "Clear" button clears the canvas
- "Save" button saves drawn data sample
- "Train" button trains the network (use when you are done with creating training samples)
- in "Label" textbox set the name of the data sample that is drawn on the canvas

I found out that these parameters are working great:
- Points: 20
- Learning rate: 0.1
- Hidden layer neurons: 100
- Epochs: 100

![image](https://github.com/Timbelion/python-neural-network-from-scratch/assets/76007113/8e8296ed-4915-46e4-80d0-e93e0f308b02)

### Query

After you've finished drawing samples and clicked the "Train" button, wait until the network is trained (check the console) and you can start testing it! 
Start drawing your doodles on the canvas and network will write its prediction in the "NN guess" label.

![image](https://github.com/Timbelion/python-neural-network-from-scratch/assets/76007113/4362088f-7b6a-4b7f-ad5a-fc31f66605cb)





