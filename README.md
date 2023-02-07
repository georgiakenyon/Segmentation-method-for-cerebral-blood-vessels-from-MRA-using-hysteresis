# Segmentation-method-for-cerebral-blood-vessels-from-MRA-using-hysteresis
Segmentation method for cerebral blood vessels from MRA using hysteresis


![brain](https://user-images.githubusercontent.com/78221858/217150728-2a36cda1-9f18-434b-b411-0947c7d37cd9.png)


Segmentation of cerebral blood vessels from Magnetic Resonance Imaging (MRI) is an open problem that could be solved with deep learning (DL). However, annotated data for training is often scarce. Due to the absence of open-source tools, we aim to develop a classical segmentation method that generates vessel ground truth from Magnetic Resonance Angiography for DL training of segmentation across a variety of modalities. The method combines size-specific Hessian filters, hysteresis thresholding and connected component correction. The optimal choice of processing steps was evaluated with a blinded scoring by a clinician using 24 3D images. The results show that all method steps are necessary to produce the highest (14.2/15) vessel segmentation quality score. Omitting the connected component correction caused the largest quality loss. The method, which is available on request, can be used to train DL models for vessel segmentation. 

![pipeline](https://user-images.githubusercontent.com/78221858/217150857-59b8f0f5-93c8-41eb-905d-f3788ec083de.png)
