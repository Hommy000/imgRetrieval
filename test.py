import imagehash
import cv2
import numpy as np

def colorhash(image):
    """
    計算圖像的 colorhash 值。

    Args:
        image: 圖像。

    Returns:
        圖像的 colorhash 值。
    """

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    (h, s, v) = hsv.T

    # 將圖像分為 256 個小區域。
    rows, cols = h.shape[:2]
    size = 8
    xs = np.linspace(0, cols - 1, rows // size)
    ys = np.linspace(0, rows - 1, cols // size)

    # 計算每個小區域的平均色調和飽和度值。
    hash = np.zeros(64)
    for i in range(rows // size):
        for j in range(cols // size):
            x0, x1 = xs[i], xs[i + 1]
            y0, y1 = ys[j], ys[j + 1]

            h_avg = np.mean(h[y0:y1, x0:x1])
            s_avg = np.mean(s[y0:y1, x0:x1])

            hash[i * 32 + j * 8 + 0] = h_avg // 256
            hash[i * 32 + j * 8 + 1] = s_avg // 256

    return hash


if __name__ == "__main__":
    image = cv2.imread(".\sample\gura.png")
    hash = colorhash(image)
    print(hash)