from collections import Counter
from conf import get_logger

logger = get_logger("face_groups")

class Face:
    def __init__(self, id, label, bounding_box):
        self.id = id
        self.label = label
        self.bounding_box = bounding_box

    def __repr__(self):
        return f'Face: ID: {self.id}, label: {self.label}, bounding_box: {self.bounding_box}'

class Group:
    def __init__(self):
        self.labels = Counter()
        self.bboxes = []
        self.main_bb = None

    def __repr__(self):
        return f'Main Box: {self.main_bb}, labels: {self.labels}'

    def add_face(self, face: Face):
        self.labels.update([face.label])
        self.bboxes.append(face.bounding_box)
        self.main_bb = face.bounding_box

    def get_best_label(self):
        """Choose one label from the set by frequency"""
        if len(self.labels):
            return self.labels.most_common(1)[0][0]
        else:
            return None

    def update_bb(self):
        pass

class FaceGrouping:
    threshold = None
    faces = None
    groups = None
    def __init__(self, threshold: float):
        self.threshold = threshold
        self.faces = []
        self.groups = []

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
        a1 = self.area(bb1)
        a2 = self.area(bb2)
        min_area = min(a1, a2)
        ov_area = self.overlapping_area(bb1, bb2)
        # print(f"Area 1: {a1}, Area 2: {a2}, Area Min: {min_area}, Overlapping Area: {ov_area}")
        return ov_area / min_area

    def equal_face_boxes(self, bb1, bb2, t: float = 0.5) -> bool:
        """Compares two bounding boxes and
        if the overlap score is higher
        than the threshold, returns True"""
        score = self.compare_face_boxes(bb1, bb2)
        return score > t

    # def add_face(self, face: Face):
    #     # face_id = face.id
    #     # face_bb = face.bounding_box
    #     self.faces.append(face)

    def merge_face(self, face: Face):
        face_bb = face.bounding_box
        face_label = face.label
        top_score = 0.0
        group_idx = None
        for i, group in enumerate(self.groups):
            group_bb = group.main_bb
            score = self.compare_face_boxes(face_bb, group_bb)
            if score > self.threshold and score > top_score:
                top_score =  score
                group_idx = i
        if group_idx is not None:
            self.groups[group_idx].add_face(face)
        else:
            new_group = Group()
            new_group.add_face(face)
            self.groups.append(new_group)

    def best_labels(self) -> set:
        labels = set()
        for group in self.groups:
            label = group.get_best_label()
            if label is not None:
                labels.add(label)
        return labels

    def group_faces(self):
        for face in self.faces:
            bb: list = face.bounding_box

if __name__ == '__main__':
    face_grouping = FaceGrouping(threshold=0.5)
    bb1 = [243, 156, 506, 468]
    bb2 = [257, 251, 427, 461]
    bb3 = [357, 451, 527, 691]
    # score = face_grouping.compare_face_boxes(bb1, bb3)
    # print(score)
    # c = face_grouping.equal_face_boxes(bb1, bb3)
    # print(c)
    face1 = Face(13, 'zhanibek', bb2)
    face2 = Face(13, 'adilkhan', bb1)
    face3 = Face(0, 'abil', bb3)
    # logger.info(face_grouping.groups)
    face_grouping.merge_face(face1)
    face_grouping.merge_face(face2)
    face_grouping.merge_face(face3)
    logger.info(face_grouping.groups)
    logger.info(face_grouping.best_labels())
    # for g in face_grouping.groups:
    #     logger.info(g.bboxes)
