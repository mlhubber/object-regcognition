Object Recognition
==================

This [MLHub](https://mlhub.ai) package, based on a [deep learning
kubernetes
tutorial](https://github.com/Microsoft/AKSDeploymentTutorialAML) by
Yan Zhang, Mathew Salvaris, and Fidan Boylu Uz of Microsoft,
demonstrates the pre-built
[ResNet152](https://tfhub.dev/google/imagenet/resnet_v1_152/classification/1)
model using the open source TensorFlow and available from [tfhub](https://tfhub.dev)
to identify the main object of a photo. Sample images are provided
within the package and the demonstration applies the pre-built model
to each image. This pre-built model has been trained to recognise
[1000 different kinds of
classes/objects](http://mlhub.ai/cache/data.dmlc.ml/mxnet/models/imagenet/synset.txt).
These include goldfish, great white shark, tiger shark, sports car,
etc.

Visit the github repository for the examples and code:
<https://github.com/mlhubber/objects>

## Quick Start Command Line Examples

```console
ml demo objects
ml gui objects
ml identify objects https://g3n1u5.com/mlhub/ryleybench.png
ml identify objects https://g3n1u5.com/mlhub/slide.png
ml identify objects https://g3n1u5.com/mlhub/parkedcars.png
ml identify objects https://g3n1u5.com/mlhub/pond.png
```

Usage
-----

- To install mlhub 

        $ pip3 install mlhub

- To install and run the pre-built model:

        $ ml install   objects
        $ ml readme    objects
        $ ml configure objects
        $ ml demo      objects
        $ ml identify  objects

Examples
--------

- To identify the object in an image from a local file:

		$ ml identify objects ~/.mlhub/objects/images/lynx.jpg

- To identify the object in images in a folder:

        $ ml identify objects ~/.mlhub/objects/images/

- To identify the object in an image from the web (e.g.
        <https://en.wikipedia.org/wiki/Aciagrion_occidentale>) :

        $ ml identify objects https://upload.wikimedia.org/wikipedia/commons/thumb/6/6d/Aciagrion_occidentale-Kadavoor-2017-05-08-002.jpg/440px-Aciagrion_occidentale-Kadavoor-2017-05-08-002.jpg

- To interactively provide images without repeatedly reloading the model:

        $ ml identify objects
