import numpy as np
import torch

from models.experimental import attempt_load
from utils.augmentations import letterbox
from utils.general import check_img_size, non_max_suppression, scale_coords, xyxy2xywh
from utils.plots import Annotator, colors
from utils.torch_utils import select_device

class ai_core():
    def __init__(self):

        #torch.set_grad_enabled(False)

        self.model = None
        self.stride = 32
        self.names = ''
        self.device = ''
        self.half = False
        self.augment = False
        self.visualize = False
        self.conf_thres = 0.5
        self.iou_thres = 0.5
        self.classes = None
        self.agnostic_nms = False
        self.max_det = 1000
        self.line_thickness = 1
        self.hide_labels = False
        self.hide_conf = False


    def update_model(self, weights='', half=False):
        device = select_device(self.device)
        half &= device.type != 'cpu'
        model = torch.jit.load(weights) if 'torchscript' in weights else attempt_load(weights, map_location=device)
        stride = int(model.stride.max())
        names = model.module.names if hasattr(model, 'module') else model.names
        if half:
            model.half()

        self.model = model
        self.device = device
        self.half = half
        self.stride = stride
        self.names = names

    def detect(self, img0=None, imgsz=640, view_img=False):

        if img0 is None: return None, None, None

        model = self.model
        half = self.half
        device = self.device
        stride = self.stride
        augment = self.augment
        visualize = self.visualize
        conf_thres = self.conf_thres
        iou_thres = self.iou_thres
        classes = self.classes
        agnostic_nms = self.agnostic_nms
        max_det = self.max_det
        line_thickness = self.line_thickness
        names = self.names
        hide_labels = self.hide_labels
        hide_conf = self.hide_conf

        imgsz = check_img_size(imgsz, s=stride)
        img_t = letterbox(img0, [imgsz, imgsz], stride=stride, auto=True)[0]
        img_t = img_t.transpose((2, 0, 1))
        img_t = np.ascontiguousarray(img_t)

        imgsz = [imgsz, imgsz]

        model(torch.zeros(1, 3, *imgsz).to(device).type_as(next(model.parameters())))

        img_t = torch.from_numpy(img_t).to(device)
        img_t = img_t.half() if half else img_t.float()  # uint8 to fp16/32
        img_t = img_t / 255.0  # 0 - 255 to 0.0 - 1.0

        if len(img_t.shape) == 3:
            img_t = img_t[None]  # expand for batch dim

        pred = model(img_t, augment=augment, visualize=visualize)[0]
        pred = non_max_suppression(pred, conf_thres, iou_thres, classes, agnostic_nms, max_det=max_det)

        det = pred[0]
        im0 = img0.copy()
        gn = torch.tensor(im0.shape)[[1, 0, 1, 0]]
        annotator = Annotator(im0, line_width=line_thickness, example=str(names))

        xywh_list = []

        print(det)

        if len(det):
            det[:, :4] = scale_coords(img_t.shape[2:], det[:, :4], im0.shape).round()

            # Results
            for *xyxy, conf, cls in reversed(det):

                xywh = (xyxy2xywh(torch.tensor(xyxy).view(1, 4)) / gn).view(-1).tolist()
                if view_img:
                    c = int(cls)  # integer class
                    label = None if hide_labels else (names[c] if hide_conf else f'{names[c]} {conf:.2f}')
                    annotator.box_label(xyxy, label, color=colors(c, True))
                xywh.append(float(f'{conf:.2f}'))
                xywh_list.append(xywh)

        if view_img:
            im0 = annotator.result()

        return xywh_list, im0

        '''
        if img0 is None: return None, None, 0

        imgsz = check_img_size(imgsz, s=self.stride)
        img_t = letterbox(img0, [imgsz, imgsz], stride=self.stride, auto=True)[0]
        img_t = img_t.transpose((2, 0, 1))[::-1]
        img_t = np.ascontiguousarray(img_t)
        imgsz = [imgsz, imgsz]

        self.model(torch.zeros(1, 3, *imgsz).to(self.device).type_as(next(self.model.parameters())))

        img_t = torch.from_numpy(img_t).to(self.device)
        img_t = img_t.half() if self.half else img_t.float()
        img_t = img_t / 255.0
        if len(img_t.shape) == 3:
            img_t = img_t[None]
        pred = self.model(img_t, augment=False, visualize=False)[0]
        pred = non_max_suppression(pred, self.conf_thres, self.iou_thres, None, False, max_det=self.max_det)
        det = pred[0]
        gn = torch.tensor(img0.shape)[[1, 0, 1, 0]]
        annotator = Annotator(img0, line_width=1, example=str(self.names))
        xywh_list = []
        print(det)
        if len(det):
            det[:, :4] = scale_coords(img_t.shape[2:], det[:, :4], img0.shape).round()
            for *xyxy, conf, cls in reversed(det):
                xywh = (xyxy2xywh(torch.tensor(xyxy).view(1, 4)) / gn).view(-1).tolist()
                c = int(cls)
                label = f'{self.names[c]} {conf:.2f}'
                if view_img:
                    annotator.box_label(xyxy, label, color=colors(c, True))
                xywh.append(float(f'{conf:.2f}'))
                xywh.append(label)
                xywh_list.append(xywh)
        img_r = None
        if view_img:
            img_r = annotator.result()
        return xywh_list, img_r
        '''