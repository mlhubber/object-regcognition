#!/bin/sh

model="$(python -c "from mlhub import utils; print(utils.get_package_name())")"

checkpoint_url='http://download.tensorflow.org/models/resnet_v1_152_2016_08_28.tar.gz'
checkpoint_tar="$(basename ${checkpoint_url})"
checkpoint_file='resnet_v1_152.ckpt'

label_url='http://data.dmlc.ml/mxnet/models/imagenet/synset.txt'
label_file="$(basename ${label_url})"

img_name=(\
  'lynx.jpg' \
  'sportscar.jpg' \
  'ship.jpg' \
  'croc.jpg' \
  'tarsier.jpg' \
  'robin.jpg' \
)

img_url=(\
  'https://upload.wikimedia.org/wikipedia/commons/thumb/6/68/Lynx_lynx_poing.jpg/220px-Lynx_lynx_poing.jpg' \
  'https://upload.wikimedia.org/wikipedia/commons/3/3a/Roadster_2.5_windmills_trimmed.jpg' \
  'http://www.worldshipsociety.org/wp-content/themes/construct/lib/scripts/timthumb/thumb.php?src=http://www.worldshipsociety.org/wp-content/uploads/2013/04/stock-photo-5495905-cruise-ship.jpg&w=570&h=370&zc=1&q=100' \
  'http://yourshot.nationalgeographic.com/u/ss/fQYSUbVfts-T7pS2VP2wnKyN8wxywmXtY0-FwsgxpiZv_E9ZfPsNV5B0ER8-bOdruvNfMD5EbP4SznWz4PYn/' \
  'https://cdn.arstechnica.net/wp-content/uploads/2012/04/bohol_tarsier_wiki-4f88309-intro.jpg' \
  'http://i.telegraph.co.uk/multimedia/archive/03233/BIRDS-ROBIN_3233998b.jpg' \
)

######################################################################
# Setup

# Call mlhub.utils.create_package_cache_dir to get the package-specific cache dir.
# Then link it into ./cache

cache_dir="$(python -c "from mlhub import utils; print(utils.create_package_cache_dir())")"
ln -s ${cache_dir} cache
cache_dir="cache"

# Change dir to ./cache to make following work inside ./cache

cd ${cache_dir}

######################################################################
# Dependencies

echo "Install dependencies required by '${model}' ..."
sudo apt-get install python3-pil
pip3 install ipython
pip3 install matplotlib
pip3 install tensorflow
pip3 install keras

######################################################################
# Resouces

dr="resources"
if [[ ! -d ${dr} ]]; then
  echo "Obtain ${dr} ..."
  mkdir ${dr}
fi

pushd ${dr} 1>/dev/null

if [[ ! -f "${checkpoint_file}" ]]; then
  echo "Download the model checkpoint ..."

  # --quiet makes wget won't show all verbose detail about downloading
  # --show-progress makes wget only show the progress of downloading
  # 2>&1 makes all the messages from wget show up, since those messages are directed to stderr,
  #      which won't be shown if this script is invoked by subprocess.Popen(..., stderr=PIPE)
  wget --quiet --show-progress ${checkpoint_url} 2>&1
  tar xvf ${checkpoint_tar} 1>/dev/null
  rm ${checkpoint_tar}
fi

if [[ ! -f "${label_file}" ]]; then
  echo "Download the synset for the model to translate model output to a specific label ..."
  wget --quiet --show-progress ${label_url} 2>&1
fi

popd 1>/dev/null


######################################################################
# Images

dr="images"
if [[ ! -d ${dr} ]]; then
  echo "Obtain ${dr} ..."
  mkdir ${dr}
fi

pushd ${dr} 1>/dev/null

for ((i=0; i<${#img_name[*]}; i++))
do
  img=${img_name[${i}]}
  if [[ ! -f ${img} ]]; then
    echo "... ${img}"
    wget  --quiet --show-progress -O ${img} ${img_url[${i}]} 2>&1
  fi
done

popd 1>/dev/null
