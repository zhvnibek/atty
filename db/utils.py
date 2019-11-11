

# def overlapping_area(bb1: list, bb2: list) -> float:
#     """Compute the area of the overapping region if two rectangles"""
#     left = max(bb1[0], bb2[0])
#     right = min(bb1[2], bb2[2])
#     top = min(bb1[3], bb2[3])
#     bottom = max(bb1[1], bb2[1])
#     # print("left:{}, right:{}, top:{}, bottom:{}".format(left, right, top, bottom))
#     if left < right and bottom < top:
#         return (right - left) * (top - bottom)
#     return 0
#
# def area(bb: list) -> float:
#     """Compute rectangle's area"""
#     k, l, m, n = bb
#     return (m - k) * (n - l)
#
# def compare_face_boxes(bb1: list, bb2: list):
#     """Compute overlap score of two bounding boxes:
#     (area of overapping region) / (area of the less area)"""
#     a1 = area(bb1)
#     a2 = area(bb2)
#     min_area = min(a1, a2)
#     ov_area = overlapping_area(bb1, bb2)
#     # print(f"Area 1: {a1}, Area 2: {a2}, Area Min: {min_area}, Overlapping Area: {ov_area}")
#     return ov_area / min_area
#
# def equal_face_boxes(bb1, bb2, t: float = 0.5) -> bool:
#     """Compares two bounding boxes and
#     if the overlap score is higher
#     than the threshold, returns True"""
#     score = compare_face_boxes(bb1, bb2)
#     print(score)
#     return score > t

class Face:
    def __init__(self, id, label, bounding_box):
        self.id = id
        self.label = label
        self.bounding_box = bounding_box

    def __repr__(self):
        return f'Face: ID: {self.id}, label: {self.label}, bounding_box: {self.bounding_box}'

class FaceGrouping:
    faces = None

    def __init__(self):
        self.faces = []

    def __repr__(self):
        return 'FaceGrouping'

    def __len__(self):
        return len(self.faces)

    def __getitem__(self, key):
        return self.faces[key]

    def overlapping_area(self, bb1: list, bb2: list) -> float:
        """Compute the area of the overapping region if two rectangles"""
        left = max(bb1[0], bb2[0])
        right = min(bb1[2], bb2[2])
        top = min(bb1[3], bb2[3])
        bottom = max(bb1[1], bb2[1])
        # print("left:{}, right:{}, top:{}, bottom:{}".format(left, right, top, bottom))
        if left < right and bottom < top:
            return (right - left) * (top - bottom)
        return 0

    def area(self, bb: list) -> float:
        """Compute rectangle's area"""
        k, l, m, n = bb
        return (m - k) * (n - l)

    def compare_face_boxes(self, bb1: list, bb2: list):
        """Compute overlap score of two bounding boxes:
        (area of overapping region) / (area of the less area)"""
        a1 = area(bb1)
        a2 = area(bb2)
        min_area = min(a1, a2)
        ov_area = overlapping_area(bb1, bb2)
        # print(f"Area 1: {a1}, Area 2: {a2}, Area Min: {min_area}, Overlapping Area: {ov_area}")
        return ov_area / min_area

    def equal_face_boxes(self, bb1, bb2, t: float = 0.5) -> bool:
        """Compares two bounding boxes and
        if the overlap score is higher
        than the threshold, returns True"""
        score = compare_face_boxes(bb1, bb2)
        print(score)
        return score > t

    def add_face(self, face: Face):
        # face_id = face.id
        # face_bb = face.bounding_box
        self.faces.append(face)

    def group_faces(self):
        pass

if __name__ == '__main__':
    bb1 = [243, 156, 506, 468]
    bb2 = [257, 251, 427, 461]
    bb3 = [257, 251, 427, 491]
    # score = compare_face_boxes(bb1, bb2)
    # print(score)
    c = equal_face_boxes(bb1, bb3)
    print(c)
