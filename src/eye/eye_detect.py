import cv2
import numpy as np

from src.type import Point, Mat
from src.color import bgr_black, bgr_white, bgr_blue


def get_eye_center(points: list[Point]) -> Point:
    n = len(points)
    if n == 0:
        raise ValueError("List has no item.")
    sum_point: Point = Point(0, 0)
    for p in points:
        sum_point += p
    return sum_point // n


# 目の輪郭を検知して円を描画する関数
def get_contouring(
    thresh, face_mid_y, frame=None, is_right: bool = False
) -> Point | None:
    cnts, _ = cv2.findContours(
        thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE
    )
    try:
        cnt = max(cnts, key=cv2.contourArea)
        moment = cv2.moments(cnt)
        cx = int(moment["m10"] / moment["m00"])
        cy = int(moment["m01"] / moment["m00"])
        if is_right:
            cx += face_mid_y
        if frame is not None:
            cv2.circle(frame, (cx, cy), 2, bgr_blue, 2)
        return Point(cx, cy)
    except ValueError:
        pass
    except ZeroDivisionError:
        pass


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
