import pandas as pd
from InfoStructure.Base import *
from typing import List, Dict, Union


def write_dataframe_to_excel(excel_path: Union[str, bytes, os.PathLike], dataframe: pd.DataFrame):
    with pd.ExcelWriter(excel_path) as writer:
        dataframe.to_excel(writer, index=False)
    return


class PatientClassEval(object):
    MRN: str
    Patient_RS_UID: str
    Patient_UID: int

    def set_patient_info(self, patient: PatientClass):
        self.MRN = patient.MRN
        self.Patient_RS_UID = patient.RS_UID
        self.Patient_UID = patient.Patient_UID


class CaseClassEval(PatientClassEval):
    Case_Name: str
    Case_UID: int

    def set_case_info(self, case: CaseClass):
        self.Case_Name = case.CaseName
        self.Case_UID = case.Case_UID


class ExamClassEval(CaseClassEval):
    Exam_Name: str
    Exam_UID: int

    def set_exam_info(self, exam: ExaminationClass):
        self.Exam_Name = exam.ExamName
        self.Exam_UID = exam.Exam_UID


class RegionOfInterestBaseEval(ExamClassEval):
    ROI_Name: str
    RS_Number: int
    Type: str
    Base_ROI_UID: int

    def set_roi_base_info(self, roi_base: RegionOfInterestBase):
        self.ROI_Name = roi_base.Name
        self.RS_Number = roi_base.RS_Number
        self.Type = roi_base.Type
        self.Base_ROI_UID = roi_base.Base_ROI_UID


class RegionOfInterestVolumeEval(RegionOfInterestBaseEval):
    Volume: float
    HU_Min: float
    HU_Max: float
    HU_Average: float
    Defined: bool
    ROI_UID: int

    def set_roi_info(self, roi: RegionOfInterest):
        self.ROI_Name = roi.Name
        self.Volume = roi.Volume
        self.HU_Min = roi.HU_Min
        self.HU_Max = roi.HU_Max
        self.HU_Average = roi.HU_Average
        self.ROI_UID = roi.ROI_UID


class PrescriptionROIEval(RegionOfInterestVolumeEval):
    Prescription_UID: int
    DoseAbsoluteVolume_cc: float
    DoseValue_cGy: float
    DoseVolume_percent: float
    RelativePrescriptionLevel: float
    PrescriptionType: str
    NumberOfFractions: int
    Dose_per_Fraction: float

    def set_rx_info(self, prescription: PrescriptionClass):
        self.Prescription_UID = prescription.Prescription_UID
        self.DoseAbsoluteVolume_cc = prescription.DoseAbsoluteVolume_cc
        self.DoseValue_cGy = prescription.DoseValue_cGy
        self.DoseVolume_percent = prescription.DoseVolume_percent
        self.RelativePrescriptionLevel = prescription.RelativePrescriptionLevel
        self.PrescriptionType = prescription.PrescriptionType
        self.NumberOfFractions = prescription.NumberOfFractions
        self.Dose_per_Fraction = prescription.Dose_per_Fraction
        self.set_roi_info(prescription.Referenced_ROI_Structure)


def return_dataframe_from_class_list(list_classes):
    return pd.DataFrame([vars(f) for f in list_classes])


class PandasEvaluation(object):
    Patient_DataBase: PatientDatabase

    def __init__(self, patient_database: PatientDatabase):
        self.Patient_DataBase = patient_database

    def return_all_info_from_roi_base(self, wanted_roi_base: RegionOfInterestBase) -> (PatientClass, CaseClass):
        for patient in self.Patient_DataBase.Patients.values():
            for case in patient.Cases.values():
                for roi_base in case.Base_ROIs.values():
                    if roi_base.Base_ROI_UID == wanted_roi_base.Base_ROI_UID:
                        return patient, case

    def return_all_info_from_poi_base(self, wanted_poi_base: PointOfInterestBase) -> (PatientClass, CaseClass):
        for patient in self.Patient_DataBase.Patients.values():
            for case in patient.Cases.values():
                for poi_base in case.Base_POIs.values():
                    if poi_base.Base_POI_UID == wanted_poi_base.Base_POI_UID:
                        return patient, case

    def return_all_info_from_roi(self, wanted_roi: RegionOfInterest) -> \
            (PatientClass, CaseClass, ExaminationClass, RegionOfInterestBase):
        for patient in self.Patient_DataBase.Patients.values():
            for case in patient.Cases.values():
                for exam in case.Examinations.values():
                    for roi in exam.ROIs.values():
                        if roi.ROI_UID == wanted_roi.ROI_UID:
                            return patient, case, exam, case.Base_ROIs[roi.Referenced_Base_ROI_UID]

    def return_all_info_from_poi(self, wanted_poi: PointOfInterest) -> \
            (PatientClass, CaseClass, ExaminationClass, PointOfInterestBase):
        for patient in self.Patient_DataBase.Patients.values():
            for case in patient.Cases.values():
                for exam in case.Examinations.values():
                    for poi in exam.POIs.values():
                        if poi.POI_UID == wanted_poi.POI_UID:
                            return patient, case, exam, case.Base_POIs[poi.Referenced_Base_POI_UID]

    def return_all_info_from_exam(self, wanted_exam: ExaminationClass) -> (PatientClass, CaseClass):
        for patient in self.Patient_DataBase.Patients.values():
            for case in patient.Cases.values():
                for exam in case.Examinations.values():
                    if exam.Exam_UID == wanted_exam.Exam_UID:
                        return patient, case

    def return_all_info_from_case(self, wanted_case: CaseClass) -> PatientClass:
        for patient in self.Patient_DataBase.Patients.values():
            for case in patient.Cases.values():
                if case.Case_UID == wanted_case.Case_UID:
                    return patient

    def return_above_info(self, object_of_interest):
        if type(object_of_interest) == RegionOfInterest:
            return self.return_all_info_from_roi(object_of_interest)
        elif type(object_of_interest) == PointOfInterest:
            return self.return_all_info_from_poi(object_of_interest)
        elif type(object_of_interest) == RegionOfInterestBase:
            return self.return_all_info_from_roi_base(object_of_interest)
        elif type(object_of_interest) == PointOfInterestBase:
            return self.return_all_info_from_poi_base(object_of_interest)
        elif type(object_of_interest) == ExaminationClass:
            return self.return_all_info_from_exam(object_of_interest)
        elif type(object_of_interest) == CaseClass:
            return self.return_all_info_from_case(object_of_interest)

    def return_list_of_eval_rois(self):
        eval_rois: List[RegionOfInterestVolumeEval]
        eval_rois = []
        for patient in self.Patient_DataBase.Patients.values():
            for case in patient.Cases.values():
                base_rois = case.Base_ROIs
                for exam in case.Examinations.values():
                    for roi in exam.ROIs.values():
                        base_roi = base_rois[roi.Referenced_Base_ROI_UID]
                        eval_roi = RegionOfInterestVolumeEval()
                        eval_roi.set_roi_info(roi)
                        eval_roi.set_roi_base_info(base_roi)
                        eval_roi.set_patient_info(patient)
                        eval_roi.set_case_info(case)
                        eval_roi.set_exam_info(exam)
                        eval_rois.append(eval_roi)
        return eval_rois

    def return_list_of_eval_prescriptions(self):
        eval_prescriptions: List[PrescriptionROIEval]
        rx: PrescriptionClass
        eval_prescriptions = []
        for patient in self.Patient_DataBase.Patients.values():
            for case in patient.Cases.values():
                base_rois = case.Base_ROIs
                for treatment_plan in case.TreatmentPlans.values():
                    exam = [i for i in case.Examinations.values() if i.Exam_UID == treatment_plan.Referenced_Exam_UID]
                    for beam_set in treatment_plan.BeamSets.values():
                        if beam_set.Primary_Prescription:
                            rx = beam_set.Primary_Prescription
                            if rx.PrescriptionType == 'DoseAtVolume':
                                structure_reference: RegionOfInterest
                                structure_reference = rx.Referenced_Structure
                                if structure_reference is None:
                                    continue
                                eval_rx = PrescriptionROIEval()
                                eval_rx.set_patient_info(patient)
                                eval_rx.set_case_info(case)
                                eval_rx.set_exam_info(exam[0])
                                eval_rx.set_rx_info(rx)
                                eval_rx.set_roi_base_info(base_rois[structure_reference.Referenced_Base_ROI_UID])
                                eval_prescriptions.append(eval_rx)
        return eval_prescriptions

    def return_dataframe_volume_rois(self):
        eval_rois = self.return_list_of_eval_rois()
        return return_dataframe_from_class_list(eval_rois)


if __name__ == '__main__':
    pass
