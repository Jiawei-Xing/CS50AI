At first, I tried the codes from the lecture video: 1 convolutional and pooling layer, 32 3x3 filters for convolution, 2x2 for pooling, 128 hidden layers, and dropout with 0.5 rate. However, the result was not good, with loss 3.5049 and accuracy 0.0562.

(1) I tried more convolutional and pooling layers. After changing from 1 to 3 layers, I got a better result, with loss 1.9904 and accuracy 0.3834. It took more time to run. 

(2) I tried more and larger filters for convolutional layers. After changing 32 layers to 100 layers, the result was not impoved largely, with loss 3.4922 and accuracy 0.0566. After changing 3x3 filters to 10x10 filters, the result was not impoved largely, with loss 3.5051 and accuracy 0.0566. It took more time to run. 

(3) I tried larger pool sizes for pooling layers. After changing 2x2 pools to 10x10 pools, the result was impoved, with loss 1.4537 and accuracy 0.5142. It ran faster. 

(4) I tried more hidden layers. After changing 128 to 300 hidden layers, the result was improved, with loss 2.1089 and accuracy 0.3902. It was slower.

(5) Finally, I tried higher rates for dropout. After changing 0.5 to 0.8, the result was not changed largely, with loss 3.4997 and 0.0571. Runtime did not change largely. 

In summary, more convolutional and pooling layers, larger pool sizes, and more hidden layers did help improve the model. Therefore, I used 2 convolutional and pooling layers, 3x3 pools, and 1000 hidden layers, and managed to get a better result, with loss 0.4019 and accuracy 0.9033. 