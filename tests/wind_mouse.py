import numpy as np
import matplotlib.pyplot as plt
from typing import List


# Reference
# https://github.com/BenLand100/Simpy/blob/ed224202764096681cdf5589df7470a7c9f34a6f/simpy/library/io.py#L41
def wind_mouse(
    start_x: float,
    start_y: float,
    dest_x: float,
    dest_y: float,
    G_0: float = 9,
    W_0: float = 3,
    M_0: float = 15,
    D_0: float = 12,
    move_mouse=lambda x, y: None,
):
    current_x: float = start_x
    current_y: float = start_y

    v_x: float = 0
    v_y: float = 0
    w_x: float = 0
    w_y: float = 0

    while (dist := np.hypot(dest_x - start_x, dest_y - start_y)) >= 1:
        w_mag = min(W_0, dist)

        if dist >= D_0:
            w_x = (w_x / np.sqrt(3)) + (2 * np.random.random() - 1) * (
                w_mag / np.sqrt(5)
            )
            w_y = (w_y / np.sqrt(3)) + (2 * np.random.random() - 1) * (
                w_mag / np.sqrt(5)
            )

        else:
            w_x /= np.sqrt(3)
            w_y /= np.sqrt(3)

            if M_0 < 3:
                M_0 = (np.random.random() * 3) + 3
            else:
                M_0 /= np.sqrt(5)

        v_x += w_x + (G_0 * (dest_x - start_x) / dist)
        v_y += w_y + (G_0 * (dest_y - start_y) / dist)

        v_mag = np.hypot(v_x, v_y)

        if v_mag > M_0:
            v_clip = (M_0 / 2) + (np.random.random() * M_0 / 2)
            v_x = (v_x / v_mag) * v_clip
            v_y = (v_y / v_mag) * v_clip

        start_x += v_x
        start_y += v_y

        move_x = int(np.round(start_x))
        move_y = int(np.round(start_y))

        if current_x != move_x or current_y != move_y:
            move_mouse(current_x := move_x, current_y := move_y)

        return current_x, current_y


if __name__ == "__main__":
    fig = plt.figure(figsize=[13, 13])

    plt.axis("off")
    for y in np.linspace(-200, 200, 25):
        points = np.array([])

        wind_mouse(
            start_x=0,
            start_y=y,
            dest_x=500,
            dest_y=y,
            move_mouse=lambda x, y: np.append(points, [x, y]),
        )

        points = np.asarray(points)
        plt.plot(*points.T)

        print(points)

    plt.xlim(-50, 550)
    plt.ylim(-250, 250)

    plt.show()
