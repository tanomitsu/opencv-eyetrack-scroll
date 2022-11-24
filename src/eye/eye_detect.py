# Third Party Library
import cv2
import numpy as np

# First Party Library
from src.color import bgr_black, bgr_blue, bgr_white
from src.type import Mat, Point


def get_eye_center(points: list[Point]) -> Point:
    n = len(points)
    if n == 0:
        raise ValueError("List has no item.")
    sum_point: Point = Point(0, 0)
    for p in points:
        sum_point += p
    return sum_point // n


def eval_contour(cnt, prev_point: Point = None) -> int:
    alpha = 0
    if prev_point is None:
        return cv2.contourArea(cnt)
    else:
        cnt_point = Point.from_contour(cnt)
        if cnt_point is None:
            raise ValueError("point is Null")
        print(
            f"dist: {Point.get_distance(Point.from_contour(cnt), prev_point)}"
        )
        print(f"area: {cv2.contourArea(cnt)}")
        return cv2.contourArea(cnt) - alpha * np.square(
            Point.get_distance(cnt_point, prev_point)
        )


# 目の輪郭を検知して円を描画する関数
def get_contouring(
    thresh, face_mid_y, frame=None, is_right: bool = False
) -> Point | None:
    index = int(is_right)
    cnts, _ = cv2.findContours(
        thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE
    )
    try:
        cnt = max(
            cnts,
            key=lambda cnt: eval_contour(
                cnt, get_contouring.prev_points[index]
            ),
        )
        c = Point.from_contour(cnt)
        if c is None:
            raise ValueError("point is Null.")
        if is_right:
            c.x += face_mid_y
        get_contouring.prev_points[index] = c
        if frame is not None:
            cv2.circle(frame, (c.x, c.y), 2, bgr_blue, 2)
        return Point(c.x, c.y)
    except ValueError:
        pass
    except ZeroDivisionError:
        pass


"""
    variable: prev_points
    index=0: left_eye
    index=1: right_eye
"""
get_contouring.prev_points: list[Point | None] = [None, None]


def extract_eyes(frame: Mat, lps: list[Point], rps: list[Point]) -> Mat:
    # make mask with eyes white and other black
    mask = np.zeros(frame.shape[:2], dtype=np.uint8)
    mask = make_hole_on_mask(mask, lps)
    mask = make_hole_on_mask(mask, rps)
    mask = cv2.dilate(mask, np.ones((9, 9), np.uint8), 5)

    # attach mask on frame
    masked_frame = cv2.bitwise_and(frame, frame, mask=mask)
    masked_area = (masked_frame == bgr_black).all(axis=2)
    masked_frame[masked_area] = bgr_white
    return masked_frame


def make_hole_on_mask(mask: Mat, points: list[Point]) -> Mat:
    points_list = [[p.x, p.y] for p in points]
    points_array = np.array(points_list, dtype=np.int32)
    mask = cv2.fillConvexPoly(mask, points_array, 255)
    return mask
