import numpy as np


def subselect_2d(arr, x, y, w, h, exclude_center=False):
    """
    subselects a rectangle (2w+1, 2h+1) centered at (x, y) with bounds checking
    Args:
        arr:
        x:
        y:
        w:
        h:

    Returns: subselected list of lists

    """
    x_lower = max(x - w, 0)
    x_upper = min(x + w + 1, len(arr))
    y_lower = max(y - h, 0)
    y_upper = min(y + h + 1, len(arr[0]))
    return [[arr[i][j] for i in range(x_lower, x_upper) if not (exclude_center and i == x and j == y)]
            for j in range(y_lower, y_upper)]


def subselect_3d(arr, x, y, z, w, h, d, exclude_center=False):
    """
    subselects a rectangle (2w+1, 2h+1, 2d+1) centered at (x, y,z) with bounds checking
    Args:

    Returns: subselected list of lists
    """
    x_lower = max(x - w, 0)
    x_upper = min(x + w + 1, len(arr))
    y_lower = max(y - h, 0)
    y_upper = min(y + h + 1, len(arr[0]))
    z_lower = max(z - d, 0)
    z_upper = min(z + d + 1, len(arr[0][0]))
    return [[[arr[i][j][k] for i in range(x_lower, x_upper) if not (exclude_center and i == x and j == y and k == z)]
             for j in range(y_lower, y_upper)]
            for k in range(z_lower, z_upper)]


def subselect_4d(arr, center, widths, exclude_center=False):
    """
    subselects a rectangle (2w+1, 2h+1, 2d+1) centered at center with bounds checking
    Args:

    Returns: subselected list of lists
    """
    lower = [max(center[i] - widths[i], 0) for i in range(len(widths))]
    upper = [min(center[i] + widths[i] + 1, np.array(arr).shape[i]) for i in range(len(widths))]

    val = [[[[arr[i][j][k][l] for i in range(lower[0], upper[0]) if
              not (exclude_center and i == center[0] and j == center[1] and k == center[2])]
             for j in range(lower[1], upper[1])]
            for k in range(lower[2], upper[2])]
           for l in range(lower[3], upper[3])]

    return [[[[arr[i][j][k][l] for i in range(lower[0], upper[0]) if
               not (exclude_center and i == center[0] and j == center[1] and k == center[2] and l == center[3])]
              for j in range(lower[1], upper[1])]
             for k in range(lower[2], upper[2])]
            for l in range(lower[3], upper[3])]
