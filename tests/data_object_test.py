import sys
sys.path.append("C:\\Users\\wmakinen\\Documents\\Summer 2019\\QC Automation\\SSXLQC")
from ssxlqc.unpack.rfdata import RFData
from ssxlqc.unpack.trackdata import TrackData
from ssxlqc.unpack.conveyerdata import ConveyerData

conveyer_sum = ConveyerSummary("C:\\Users\\wmakinen\\Documents\\Summer 2019\\QC Automation\\SSXLQC\\ssxlqc\\data\\conveyer")


# test_data = RFData("C:\\Users\\wmakinen\\Documents\\Summer 2019\\QC Automation\\SSXLQC\\ssxlqc\\data\\trrf\\iBot107_20190304_082902.csv") 
test_data = TrackData("C:\\Users\\wmakinen\\Documents\\Summer 2019\\QC Automation\\SSXLQC\\ssxlqc\\data\\track\\131_new_ibot.txt") 
# test_data = ConveyerData("C:\\Users\\wmakinen\\Documents\\Summer 2019\\QC Automation\\SSXLQC\\ssxlqc\\data\\conveyer\\conveyer_iBot128_20190709_135530.txt") 
test_data.unpack()

# test_data.write_formatted_data()
test_data.write_trial_summary()
# print(test_data.get_summary())
# print(test_data.get_file_length())
