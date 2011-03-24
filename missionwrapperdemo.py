import Mission_Wrapper
missionfile = Mission_Wrapper.Wrapper()
missionfile.load_mission('mission1.txt')
missionfile.GetName()
#if you want to save a copy
#missionfile.SetName('Copy of ' + missionfile.GetName())
missionfile.save()
