#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import numpy as np


class ConnComps():

    def __init__(self, num=-1):
        pass

    def run(self, img):
        label = np.int32(img.copy())
        ncomp = 1
        while True:
            pt = self.__find_seed(label)
            if not pt:
                break
            cv2.floodFill(label, None, pt, ncomp)
            ncomp += 1
        return label

    def __find_seed(self, img):
        tmp = np.where(img == 255)
        pt = ()
        if tmp[0].any() and tmp[1].any():
            pt = (tmp[1][0], tmp[0][0])
        return pt


class MyComp():

    def __init__(self, label, idx, pts):
        self._label = label
        self._idx = idx
        self._nelem = pts.shape[0]
        self._cent = np.mean(pts, axis=0)
        self._box = self.__get_box(pts)

    def __get_box(self, pts):
        t1 = np.sort(pts[:, 0])
        t2 = np.sort(pts[:, 1])
        return [np.array([t1[0], t2[0]]), np.array([t1[-1], t2[-1]])]

    @property
    def idx(self):
        return self._idx

    @property
    def cent(self):
        return self._cent

    @property
    def pts(self):
        return self._pts

    @property
    def box(self):
        return self._box

    @property
    def nelem(self):
        return self._nelem


class MyBlobDetector():

    def __init__(self, num_comp, min_elem):
        self._nc = num_comp
        self._me = min_elem
        self._cc = ConnComps()

    def run(self, img):
        cc = self._cc.run(img)
        mycomps = []

        for label in np.unique(cc)[1:]:
            nelem = len(cc[cc == label])
            if nelem > self._me:
                idx = cc == label
                (y, x) = np.where(cc == label)
                pts = np.array([x, y]).T
                mycomps.append(MyComp(label, idx, pts))

        comps = self.__get_biggest(mycomps)
        return comps

    def __get_biggest(self, comps):
        nelem = np.array([x.nelem for x in comps])
        idx = np.argsort(-nelem)[0:self._nc]
        comps = [comps[i] for i in idx.tolist()]
        return comps
