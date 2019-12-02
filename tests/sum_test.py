import sys
sys.path.append("C:\\Users\\wmakinen\\Documents\\Summer 2019\\QC Automation\\SSXLQC")
from ssxlqc.sum.rfsum import RFSummary
from ssxlqc.sum.tracksum import TrackSummary
from ssxlqc.sum.conveyersum import ConveyerSummary


rf_sum = RFSummary("C:\\Users\\wmakinen\\Documents\\Summer 2019\\QC Automation\\SSXLQC\\ssxlqc\\data\\rf")
rf_sum.summarize()
# print(rf_sum.parse_filename("iBot107_20190107_092051.csv"))

# track_sum = TrackSummary("C:\\Users\\wmakinen\\Documents\\Summer 2019\\QC Automation\\SSXLQC\\ssxlqc\\data\\track")
# track_sum.summarize()

# conveyer_sum = ConveyerSummary("C:\\Users\\wmakinen\\Documents\\Summer 2019\\QC Automation\\SSXLQC\\ssxlqc\\data\\conveyer")
# conveyer_sum.summarize()