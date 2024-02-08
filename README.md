# python-neural-network-from-scratch
Simple neural network written from scratch that can recognize handwritten doodles.

# Requirements

Module  | Version
------------- | -------------
tkintertable  | 1.3.2
numpy  | 1.21.0
matplotlib  | 3.4.3

# Instructions

When you first run the script *main.py*, you need to train the network. Set the parameters you want or use the ones below. Draw the sample, give it label in the "Label" textbox and click the "Save button" to save the training sample. Draw at least 5 samples for each label.

UI explanation:
- "Clear" button clears the canvas
- "Save" button saves drawn data sample
- "Train" button trains the network (use when you are done with creating training samples)
- in "Label" textbox set the name of the data sample that is drawn on the canvas

I found that these parameters work great:
- Points: 20
- Learning rate: 0.1
- Hidden layer neurons: 100
- Epochs: 100

After you've finished drawing samples and clicked the "Train" button, wait until the network is trained (check the console) and you can start testing it! 
Start drawing your doodles on the canvas and network will write its prediction in the "NN guess" label.
