# DataSearcher

Query helpers for the patient database built by the companion **InfoStructure** package (a separate, currently private repo that structures RayStation treatment-planning data into a `PatientDatabase` of patients, cases, examinations, ROIs/POIs, treatment plans, and prescriptions). DataSearcher walks that hierarchy so you can pull out ROIs and prescriptions across all patients without writing the nested loops yourself.

Small utility library, not actively maintained (last updated 2023).

## Components

- **`ROITools.py`** — flattens a `PatientDatabase` into lists of ROIs:
  - `return_list_volume_rois` / `return_list_dose_rois` collect every exam ROI or optimization dose-ROI across all patients.
  - `return_list_rois_by_name` filters ROIs by name substring (matched against the lowercased ROI name, so pass a lowercase query).
  - `ROIDataClass` wraps these plus `return_unique_roi_names` for surveying naming across the database.
- **`PandasTools.py`** — turns the hierarchy into flat tables:
  - `PandasEvaluation` builds "eval" records that combine patient, case, exam, ROI (volume, HU stats), and prescription attributes (dose, fractions) into one row each, and can look an object's parent patient/case/exam back up from any ROI, POI, exam, or case.
  - `return_dataframe_from_class_list` / `return_dataframe_volume_rois` convert those records to pandas DataFrames; `write_dataframe_to_excel` exports to Excel.

## Requirements

- Python 3 with `pandas`
- The `InfoStructure` package importable on your path (`from InfoStructure.Base import *`)

## Usage

There is no CLI or entry point; import the modules and pass in a loaded `PatientDatabase`:

```python
from DataSearcher.PandasTools import PandasEvaluation

evaluator = PandasEvaluation(patient_database)
df = evaluator.return_dataframe_volume_rois()
```
