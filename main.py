from tkinter import *
from tkinter import ttk, colorchooser
from neuralNetwork import NeuralNetwork

WIDTH, HEIGHT = 800, 600

class GUI:
    def __init__(self):
        self.root = Tk()
        self.root.title("Neural network")

        self.brushWidth = 10
        self.currentColor = "#000000"

        self.points = []
        self.savedPoints = []
        self.maxPoints = 15
        self.query = False
        self.nn = None
        self.un = set()

        self.oldX = None
        self.oldY = None

        self.pointsNumber = 15
        self.learningRate = 0.15
        self.errorTollerance = 10
        self.hiddenNodes = 100
        self.epochs = 100

        self.canvas = Canvas(self.root, width = WIDTH - 10, height = HEIGHT - 10, bg = "white")
        self.canvas.pack()
        self.canvas.bind("<B1-Motion>", self.Paint)
        self.canvas.bind("<ButtonRelease-1>", self.Release)

        self.buttonFrame = Frame(self.root, borderwidth = 10)
        self.parFrame = Frame(self.root, borderwidth = 10)
        self.buttonFrame.pack(fill = X)
        self.parFrame.pack(fill = X)

        self.buttonFrame.columnconfigure(0, weight = 2)
        self.buttonFrame.columnconfigure(1, weight = 2)
        self.buttonFrame.columnconfigure(2, weight = 2)
        self.buttonFrame.columnconfigure(3, weight = 1)

        self.parFrame.columnconfigure(0, weight = 1)
        self.parFrame.columnconfigure(1, weight = 1)
        self.parFrame.columnconfigure(2, weight = 1)
        self.parFrame.columnconfigure(3, weight = 1)
        self.parFrame.columnconfigure(4, weight = 1)
        self.parFrame.columnconfigure(5, weight = 1)

        self.clearButton = Button(self.buttonFrame, text = "Clear", command = self.Clear)
        self.clearButton.grid(row = 0, column = 0, sticky = W + E)

        self.saveButton = Button(self.buttonFrame, text = "Save", command = self.Save)
        self.saveButton.grid(row = 0, column = 1, sticky = W + E)

        self.learnButton = Button(self.buttonFrame, width = 2, text = "Train", command = self.Train)
        self.learnButton.grid(row = 0, column = 2, sticky = W + E)

        self.savedLabel = Label(self.buttonFrame, text = "0")
        self.savedLabel.grid(row = 0, column = 3, sticky = W + E)

        self.pointsLabel = Label(self.parFrame, text = "Points: ")
        self.pointsLabel.grid(row = 0, column = 0, sticky = W)

        self.pointsText = Text(self.parFrame, height = 1, width = 10)
        self.pointsText.grid(row = 0, column = 1, sticky = W)

        self.hiddenLabel = Label(self.parFrame, text = "Hidden layer neurons: ")
        self.hiddenLabel.grid(row = 0, column = 2, sticky = W)

        self.hiddenText = Text(self.parFrame, height = 1, width = 10)
        self.hiddenText.grid(row = 0, column = 3, sticky = W)

        self.learningLabel = Label(self.parFrame, text = "Learning rate: ")
        self.learningLabel.grid(row = 1, column = 0, sticky = W)

        self.learningText = Text(self.parFrame, height = 1, width = 10)
        self.learningText.grid(row = 1, column = 1, sticky = W)

        self.epochLabel = Label(self.parFrame, text = "Epochs: ")
        self.epochLabel.grid(row = 1, column = 2, sticky = W)

        self.epochText = Text(self.parFrame, height = 1, width = 10)
        self.epochText.grid(row = 1, column = 3, sticky = W)

        self.referenceLabel = Label(self.parFrame, text = "Label: ")
        self.referenceLabel.grid(row = 0, column = 4, sticky = W)

        self.referenceText = Text(self.parFrame, height = 1, width = 10)
        self.referenceText.grid(row = 0, column = 5, sticky = W)

        self.guessLabel = Label(self.parFrame, text = "NN guess: ")
        self.guessLabel.grid(row = 1, column = 4, sticky = W)

        self.guessText = Text(self.parFrame, height = 1, width = 10)
        self.guessText.grid(row = 1, column = 5, sticky = W)


        self.root.mainloop();

    def Paint(self, event):
        if self.oldX and self.oldY:
            self.points.append([event.x, event.y])
            self.canvas.create_line(self.oldX ,self.oldY, event.x, event.y, width=self.brushWidth, fill=self.currentColor, capstyle=ROUND, smooth=True)

        self.oldX = event.x
        self.oldY = event.y

    def Release(self, event):
        i = 1
        self.maxPoints = 15
        loop = True

        if (self.pointsText.get("1.0", "end-1c").isdigit()):
            self.maxPoints = int(self.pointsText.get("1.0", "end-1c"))

        # VECTORIZATION
        while (loop):
            while (True):
                self.points[i] = [(self.points[i][0] + self.points[i + 1][0]) / 2, (self.points[i][1] + self.points[i + 1][1]) / 2]
                del self.points[i + 1]
                i = i + 1

                if (len(self.points) <= self.maxPoints):
                    loop = False
                    break

                if (i > len(self.points) - 2):
                    break
            i = 1

        # DRAWING POINTS
        for point in self.points:
            self.canvas.create_oval(point[0] - (self.brushWidth / 2), point[1] - (self.brushWidth / 2), point[0] + (self.brushWidth / 2), point[1] + (self.brushWidth / 2), fill = "red")

        self.oldX = None
        self.oldY = None   

        print("NUMBER OF POINTS AFTER: ", len(self.points))

        # IF TRAINED THEN WE QUERY POINTS
        if (self.query and len(self.points) == self.maxPoints):

            # SQUISH POINTS BETWEEN 0 AND 1
            self.points = self.Normalize(self.points)

            # PREPARE INPUTS
            inputs = []
            for p in self.points:
                inputs.append(p[0])
                inputs.append(p[1]) 

            # GET OUTPUTS
            outputs = self.nn.Query(inputs)
            print("NN OUTPUTS: ")
            print(outputs)

            # CLEAN OUTPUTS
            outputs = list(outputs)

            unCast = list(self.un)

            pattern = unCast[outputs.index(max(outputs))]
            per = max(outputs)
            
            self.guessText.delete("1.0", "end-1c")
            self.guessText.insert("end-1c", str(pattern) + " : " + str(round(per[0] * 100, 1)) + "%")
   

    def Clear(self):
        self.canvas.delete("all")
        self.points.clear()

    def Save(self):
        self.points = self.Normalize(self.points)
        if (len(self.points) != 0):
            self.points.append(self.referenceText.get("1.0", "end-1c"))
            
            self.savedPoints.append([])
            for p in self.points:
                self.savedPoints[len(self.savedPoints) - 1].append(p)

        self.savedLabel['text'] = len(self.savedPoints)

    def Train(self):
        inputNodes = self.maxPoints * 2

        if (self.hiddenText.get("1.0", "end-1c").isdigit()):
            self.hiddenNodes = int(self.hiddenText.get("1.0", "end-1c"))

        self.un = set()

        # WE PREPARE OUTPUT LABELS IN SET (UNIQUE)
        for p in self.savedPoints:
            self.un.add(p[len(p) - 1])

        print("SET: ")
        print(self.un)

        outputNodes = len(self.un)

        # LENGTHS
        print("INPUTS: ", inputNodes)
        print("HIDDEN: ", self.hiddenNodes)
        print("OUTPUTS: ", outputNodes)

        if (self.learningText.get("1.0", "end-1c").isdigit()):
            self.learningRate = int(self.learningText.get("1.0", "end-1c"))

        # WE CREATE NN
        self.nn = NeuralNetwork(inputNodes, self.hiddenNodes, outputNodes, self.learningRate)

        if (self.epochText.get("1.0", "end-1c").isdigit()):
            self.epochs = int(self.epochText.get("1.0", "end-1c"))

        # WE TRAIN NETWORK
        for i in range(0, self.epochs):
            for s in self.savedPoints:
                inputs = []
                outputs = list(self.un)
                for i in range(0, len(s) - 1):
                    inputs.append(s[i][0])
                    inputs.append(s[i][1]) 

                for i in range(0, len(outputs)):
                    if (outputs[i] == s[len(s) - 1]):
                        outputs[i] = 1
                    else:
                        outputs[i] = 0

                print("INPUTS: ")
                print(inputs)
                print("OUTPUTS: ")
                print(outputs)
                self.nn.Train(inputs, outputs)

        self.query = True

        pass

    def Normalize(self, points):
        minx = 9999
        miny = 9999
        maxp = 0

        # WE FIND MIN POINT AND MAX X/Y
        for p in points:
            minx = min(minx, p[0])
            miny = min(miny, p[1])
            maxp = max(max(p[0], p[1]), maxp)

        # WE SUBTRACT MIN POINT AND DIVIDE BY MAX X/Y
        for p in points:
            p[0] = (p[0] - minx) / maxp
            p[1] = (p[1] - miny) / maxp

        return points

if __name__ == '__main__':
    GUI()
