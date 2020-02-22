# Import required libraries.

print("Loading the required Python modules for the ResNet152 model ...\n")

from objreg_utils import (
    img_url_to_json,
    plot_predictions,
    plot_single_prediction,
    get_model_api,
)
import glob
import json
import os
import mlhub


# Load model

predict_for = get_model_api()


# Get the images

folder = mlhub.utils.get_package_dir()
images = glob.glob(os.path.join("cache", "images", "*.jpg"))
images.sort()

print("\nThe ResNet152 model will be used for recognizing the images in\n'{}/cache/images/'".format(folder))
print("\nPlease close each image (Ctrl-w) to proceed through the demonstration.")

results = []


# Predict

for image in images:
    jsonimg = img_url_to_json(image, label=os.path.join(folder, image))
    json_lod = json.loads(jsonimg)
    output = predict_for(json_lod)

    # Plot the result

    plot_single_prediction(image, output)
    # print("\nPress Enter to continue on to the next image (Quit by Ctrl-d): ", end='')
    # try:
    #     answer = input()
    # except EOFError:
    #     print()
    #     sys.exit(0)

    results += [output, ]

# Plot the results together

plot_predictions(images, results)

print()
