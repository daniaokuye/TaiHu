from Img import cRaster
import numpy as np
import cv2
import matplotlib.pyplot as plt


class mabaodong(object):
    def __init__(self):
        super(mabaodong, self).__init__()

    def cnn(self, img, kernel=1):
        # convlution this img with a kernel size
        # img should be and only to be 2 dimensions
        ma = []
        for k in [3, 5]:
            conv_ft, x, y = self.prepare_kernel(k)
            out = list(map(self.prepare_img(img), zip(x, y)))
            out = np.vstack(out)
            conv_ft = conv_ft[:, np.newaxis, np.newaxis]
            ma.append((out, conv_ft))
        return ma

    def prepare_kernel(self, kernel_size):
        # arrange a list of kernel according to distance of point to center
        if kernel_size == 1:
            return [0]
        center = kernel_size // 2
        x = np.tile(np.arange(kernel_size), (kernel_size, 1)) - center
        y = np.tile(np.arange(kernel_size), (kernel_size, 1)).T - center
        xy = 1 / (x ** 2 + y ** 2 + 1e-15)
        xy[center, center] = 0
        xy /= np.sum(xy)
        return xy.reshape(-1), x.reshape(-1), y.reshape(-1)

    def prepare_img(self, img):
        # for map; move image
        def adjust_img(x):
            i, j = x
            out = self.move_img(img, i, j)
            return out[np.newaxis]

        return adjust_img

    def move_img(self, input, i, j):  # hor,vertical
        img = input.copy()
        print(':', i, j)
        h, w = img.shape
        if i != 0:
            h = np.zeros(h)
            u = [img, np.tile(h, (abs(i), 1)).T]
            img = np.column_stack(u[::int(np.sign(i + 0.5))])
            if i < 0:
                img = img[:, :i]
            else:
                img = img[:, i:]
        if j != 0:
            w = np.zeros(w)
            u = [img, np.tile(w, (abs(j), 1))]
            img = np.row_stack(u[::int(np.sign(j + 0.5))])
            if j < 0:
                img = img[:j, :]
            else:
                img = img[j:, :]
        return img


class ma_Unmixing(object):
    def __init__(self):
        super(ma_Unmixing, self).__init__()

    def pure_and_mix(self, img, threshold):
        # threshold to get pure water body
        # then dilation for mixed ones & outer is land endmembers
        # todo:threshold & < should be changed
        pure_water = (img > threshold).astype(np.uint8)
        kernel = np.ones((3, 3)).astype(np.uint8)
        out_dilation = cv2.dilate(pure_water, kernel)
        mixed = out_dilation - pure_water
        # land=0,mixed=1,pure water=2
        return mixed + pure_water * 2

    def check_case(self, ends, idx_origin):
        # 3*3 5*5 nearest to deteminate end members
        img, _ = ends
        img = img[:, idx_origin[0], idx_origin[1]]
        # deter = img.reshape(-1)
        # idx_origin = np.where(deter == 1)
        miniest_idx_origin = np.min(img, axis=0)
        idx = np.where(miniest_idx_origin != 0)
        y = [x[idx[0]] for x in idx_origin]
        return y

    # def deal_mixed(self, determination_endmembers):
    #     list(map(self.check_case, determination_endmembers))


def obtain_data(filename):
    a = cRaster()
    b = a.Iread(filename)
    img = b[0]
    img = img.astype(np.float32)
    return img


def unmix(img):
    unmixing = ma_Unmixing()
    mbd = mabaodong()
    img_endmembers = unmixing.pure_and_mix(img, 0)  # land=0,mixed=1,pure water=2
    out = np.zeros(img_endmembers.shape).astype(np.uint8)
    idx_origin = np.where(img_endmembers == 1)
    # determination_endmembers
    for ends in mbd.cnn(img_endmembers):
        idx = unmixing.check_case(ends, idx_origin)
        # 2 can be done by 5*5,otherwise 1 neighbour
        out[idx[0], idx[1]] += 1
    out2 = np.zeros(img_endmembers.shape).astype(np.uint8)
    out2[idx_origin[0], idx_origin[1]] = 1
    # 0: nothing; 1: 3*3; 2: neighbour; 3: 5*5
    return out + (img_endmembers == 1)


def get_ratio(LAU):
    Rou = [[np.max(x, axis=0), np.min(x, axis=0)] for x in LAU]  # pure land & pure water
    Rft = [np.sum(x, axis=0) for x in LAU]  # a mixed pixel
    ratio_l = []
    for Rou_i, Rft_i in zip(Rou, Rft):
        land, water = Rou_i
        tmp = (Rft_i - water) / (land - water)
        div = np.where((land - water) == 0)
        tmp[div[0], div[1]] = 0
        ratio_l.append(tmp)
        # ratio_w = 1 - ratio_l
    return ratio_l


if __name__ == "__main__":
    filename = "H:/work/modisNew/modis/AWEI_SH_129.tif"
    img = obtain_data(filename)
    mbd = mabaodong()
    LAU = mbd.cnn(img)  #
    LAU = [x * y for x, y in LAU]
    # out determine the endmembers
    out = unmix(img)
    ratio = get_ratio(LAU)
    ratio.append(ratio[0])
    res = np.zeros(img.shape)
    for key in [1, 2, 3]:
        res += ((out == key) * ratio[key - 1])
    print('o')
