==================
Object Recognition
==================

This package, based on the `deep learning kubernetes tutorial
<https://blogs.technet.microsoft.com/machinelearning/2018/04/19/deploying-deep-learning-models-on-kubernetes-with-gpus/>`__
by Mathew Salvaris and Fidan Boylu Uz of Microsoft, demonstrates a
pre-trained `ResNet152
<https://www.tensorflow.org/hub/modules/google/imagenet/resnet_v1_152/classification/1>`__
model to identify the main object of a photo. Sample images are
provided within the package and the demonstration applies the
pre-built model to each image. This pre-built model has been trained
to recognise `1000 different kinds of classes/objects
<http://data.dmlc.ml/mxnet/models/imagenet/synset.txt>`__.  These
include goldfish, great white shark, tiger shark, sports car, etc.

Visit the github repository for the sample code.
https://Github.com/mlhubber/objects

-----
Usage
-----

* To install and run the pre-built model::

  $ pip install mlhub
  $ ml install object-recognition
  $ ml configure object-recognition
  $ ml demo object-recognition

* To classify:

  - An image from a local file::

      $ ml score object-recognition ~/.mlhub/object-recognition/images/lynx.jpg

  - Images in a folder::

      $ ml score object-recognition ~/.mlhub/object-recognition/images/

  - An image from the web (See https://en.wikipedia.org/wiki/Aciagrion_occidentale) ::

      $ ml score object-recognition https://upload.wikimedia.org/wikipedia/commons/thumb/6/6d/Aciagrion_occidentale-Kadavoor-2017-05-08-002.jpg/440px-Aciagrion_occidentale-Kadavoor-2017-05-08-002.jpg

  - Interatively without repeatedly reloading the model::

      $ ml score object-recognition

* To visualise the network graph of the model::

    $ ml display object-recognition

  The default browser will be opened to display the graph rendered by
  `TensorBoard <https://www.tensorflow.org/guide/graph_viz>`__.
  Please refresh the browser if it cannot connect to
  http://localhost:6006, because starting TensorBoard may take time.

* To print a textual summary of the model::

    $ ml print object-recognition            # Show only a short summary of the model
    $ ml print object-recognition --verbose  # Show a long list of layers of the model
    $ ml print object-recognition -n 10      # Show only the first or last 10 layers
