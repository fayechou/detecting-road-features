import numpy as np


class Line(object):
    """
    Represents a single lane edge line.
    """

    def __init__(self, x, y, h, w):
        """
        Initialises a line object by fitting a 2nd degree polynomial to provided line points.

        Parameters
        ----------
        x   : Array of x coordinates for pixels representing a line.
        y   : Array of y coordinates for pixels representing a line.
        h   : Image height in pixels.
        w   : Image width in pixels.
        """
        # polynomial coefficients for the most recent fit
        self.h = h
        self.w = w
        self.current_fit = self.fit(x, y)
        self.points = self.get_points()

    def get_points(self):
        """
        Generates points of the current best fit line.

        Returns
        -------
        Array with x and y coordinates of pixels representing
        current best approximation of a line.
        """
        y = np.linspace(0, self.h - 1, self.h)
        return np.stack((
            self.current_fit[0] * y ** 2 + self.current_fit[1] * y + self.current_fit[2],
            y
        )).astype(np.int).T

    def fit(self, x, y):
        """
        Fits a 2nd degree polynomial to provided points and returns its coefficients.

        Parameters
        ----------
        x   : Array of x coordinates for pixels representing a line.
        y   : Array of y coordinates for pixels representing a line.

        Returns
        -------
        2nd degree polynomial coefficients.
        """
        return np.polyfit(y, x, 2)

    def radius_of_curvature(self):
        """
        Calculates radius of curvature of the line in real world coordinate system (e.g. meters), assuming there are
        27 meters for 720 pixels for y axis and 3.7 meters for 700 pixels for x axis.

        Returns
        -------
        Estimated radius of curvature in meters.
        """
        # Define conversions in x and y from pixels space to meters
        ym_per_pix = 27 / 720  # meters per pixel in y dimension
        xm_per_pix = 3.7 / 700  # meters per pixel in x dimension
        # Fit new polynomials to x,y in world space
        y = self.points[:, 1]
        x = self.points[:, 0]
        fit_cr = np.polyfit(y * ym_per_pix, x * xm_per_pix, 2)
        return int(((1 + (2 * fit_cr[0] * 720 * ym_per_pix + fit_cr[1]) ** 2) ** 1.5) / np.absolute(2 * fit_cr[0]))

    def camera_distance(self):
        """
        Calculates distance to camera in real world coordinate system (e.g. meters), assuming there are 3.7 meters for
        700 pixels for x axis.

        Returns
        -------
        Estimated distance to camera in meters.
        """
        xm_per_pix = 3.7 / 700  # meters per pixel in x dimension
        x = self.points[np.max(self.points[:, 1])][0]
        return np.absolute((self.w // 2 - x) * xm_per_pix)