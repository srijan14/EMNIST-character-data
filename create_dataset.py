from scipy.io import loadmat
import os
import uuid
import sys
import logging
logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
rootLogger = logging.getLogger()

fileHandler = logging.FileHandler("{0}/{1}.log".format("./logs", "default"))
fileHandler.setFormatter(logFormatter)
rootLogger.addHandler(fileHandler)

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
rootLogger.addHandler(consoleHandler)

rootLogger.setLevel(logging.DEBUG)

def imsave(fname, arr, vmin=None, vmax=None, cmap=None, format=None, origin=None):
    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    from matplotlib.figure import Figure
    fig = Figure(figsize=arr.shape[::-1], dpi=1, frameon=False)
    canvas = FigureCanvas(fig)
    fig.figimage(arr, cmap=cmap, vmin=vmin, vmax=vmax, origin=origin)
    fig.savefig(fname, dpi=1, format=format)


def make_dir(path):
    try:
        os.makedirs(path)
    except OSError as e:
        pass
    return


def create_structure(type):
    if os.path.exists(os.path.join(os.getcwd(),"./data")) and os.path.exists(
            os.path.join(os.getcwd(),"./data",type)) and os.path.exists(
        os.path.join(os.getcwd(),"./data",type,"train")) and os.path.exists(
        os.path.join(os.getcwd(),"./data",type,"test")):
        return

    make_dir(os.path.join(os.getcwd(),"./data"))
    make_dir(os.path.join(os.getcwd(),"./data",type))
    make_dir(os.path.join(os.getcwd(),"./data",type,"train"))
    make_dir(os.path.join(os.getcwd(),"./data",type,"test"))
    return


def create_data(data_path,type,split):
    data = loadmat(os.path.abspath(os.path.join(os.getcwd(),data_path)))

    # Loading Training Data
    X_train = data["dataset"][0][0][0][0][0][0]
    y_train = data["dataset"][0][0][0][0][0][1]

    ##Loading Testing Data
    X_test = data["dataset"][0][0][1][0][0][0]
    y_test = data["dataset"][0][0][1][0][0][1]

    nb_classes = 62

    X_train = X_train.astype('float32')
    X_test = X_test.astype('float32')
    X_train /= 255
    X_test /= 255

    X_train = X_train.reshape(X_train.shape[0], 28, 28)
    X_test = X_test.reshape(X_test.shape[0], 28, 28)

    print('EMNIST data loaded: train:', len(X_train), 'test:', len(X_test))
    print('X_train:', X_train.shape)
    print('y_train:', y_train.shape)

    if split is "train":
        X = X_train
        y = y_train
    elif split is "test":
        X = X_test
        y = y_test

    count = 0
    for index,image in enumerate(X):
        try:
            label = str(y[index][0])
            out_path = os.path.abspath(os.path.join(os.getcwd(),"./data",
                                                    type,split,label))
            if not os.path.exists(out_path):
                os.makedirs(out_path)
            filename = str(uuid.uuid4()) + ".png"
            out_file_path = os.path.abspath(os.path.join(os.getcwd(),
                                                         "./data", type,split,label,filename))
            imsave(out_file_path,image,cmap="gray")
            rootLogger.info("Saved {} for {}, belonging to class {}".format(
                filename,split,label))
        except Exception as e:
            rootLogger.error("Unable to save {} file {} with label {}".
                               format(split,filename,label))
            count = count + 1
    rootLogger.info("Number of files not saved  for {} : {}".format(split,count))


if __name__ == "__main__":
    if len(sys.argv) > 3 or len(sys.argv) < 3:
        rootLogger.error("Wrong parameters passed\nexample run command :  python "
              "create_dataset.py eminst_data_path type i.e.\npython "
              "create_dataset.py ./eminst_mat/byclass/emnist-byclass.mat byclass")
        exit()

    data_path=sys.argv[1]
    by_type = sys.argv[2]
    create_structure(by_type)
    # create_data(data_path,by_type,"train")
    create_data(data_path, by_type, "test")