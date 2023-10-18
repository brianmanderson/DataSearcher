from InfoStructure.Base import *


def return_list_volume_rois(patient_database: PatientDatabase) -> List[RegionOfInterest]:
    roi_list = []
    for patient in patient_database.Patients.values():
        for case in patient.Cases.values():
            for exam in case.Examinations.values():
                for roi in exam.ROIs.values():
                    roi_list.append(roi)
    return roi_list


def return_list_dose_rois(patient_database: PatientDatabase) -> List[RegionOfInterestDose]:
    roi_list = []
    for patient in patient_database.Patients.values():
        for case in patient.Cases.values():
            for treatment_plan in case.TreatmentPlans.values():
                for optimization in treatment_plan.Optimizations.values():
                    for roi in optimization.DoseROIs.values():
                        roi_list.append(roi)
    return roi_list


def return_list_rois_by_name(rois: List[RegionOfInterest] or List[RegionOfInterestDose],
                             name: str) -> List[RegionOfInterest] or List[RegionOfInterestDose]:
    roi_list = []
    for roi in rois:
        if roi.Name.lower().find(name) != -1:
            roi_list.append(roi)
    return roi_list


class ROIDataClass(object):
    ROI_Volume_List: List[RegionOfInterest]
    ROI_Dose_List: List[RegionOfInterestDose]
    Patient_DataBase: PatientDatabase

    def __init__(self, patient_database: PatientDatabase):
        self.Patient_DataBase = patient_database

    def return_unique_roi_names(self):
        unique_names = []
        for roi in self.ROI_Volume_List:
            if roi.Name not in unique_names:
                unique_names.append(roi.Name)
        return unique_names

    def compile_roi_volumes(self):
        self.ROI_Volume_List = return_list_volume_rois(self.Patient_DataBase)

    def compile_roi_doses(self):
        self.ROI_Dose_List = return_list_dose_rois(self.Patient_DataBase)

    def find_volume_rois_by_name(self, name):
        return return_list_rois_by_name(self.ROI_Volume_List, name)

    def find_dose_rois_by_name(self, name):
        return return_list_rois_by_name(self.ROI_Dose_List, name)


if __name__ == '__main__':
    pass
